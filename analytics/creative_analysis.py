"""
creative_analysis.py — breaks down results by creative/ad set and outputs decisions.

Covers Step 6 of the playbook (optimization) as code rather than "by eye."
For each object it applies thresholds from the knowledge base (file 04) and
outputs a recommendation: WAIT / HARD_KILL / SOFT_KILL / SCALE / REFRESH_CREATIVE / KEEP.

IMPORTANT (rule from file 06): all thresholds are computed from YOUR target_cpa,
not from US medians. target_cpa is passed as an argument — without it the script
does not guess.

Run:
    export META_ACCESS_TOKEN="EAAB..."
    python creative_analysis.py --account act_123 --target-cpa 8 --level ad

Or from CSV (offline):
    python creative_analysis.py --csv export.csv --target-cpa 8
"""

import argparse
import csv
import sys
from typing import List, Dict, Any

from meta_client import MetaClient


def decide(row: Dict[str, Any], target_cpa: float) -> Dict[str, Any]:
    """
    Apply the kill/scale thresholds from file 04 to a single stats row.
    Returns a decision and a human-readable reason.
    """
    spend = row["spend"]
    conv = row["conversions"]
    cpa = row["cpa"]
    ctr = row["ctr"]
    freq = row["frequency"]
    impressions = row["impressions"]

    # "Meaningful volume" — so we don't kill on 3 clicks (rule 4.4).
    # Rough benchmark: at least 1× target_cpa spent AND ≥1000 impressions.
    has_volume = spend >= target_cpa and impressions >= 1000

    # --- KILL on spend (rule 4.4) ---
    if conv == 0 and spend >= 3 * target_cpa and has_volume:
        return _d("HARD_KILL", f"Spent {spend:.0f} (≥3× CPA {target_cpa}) with 0 conversions and {impressions:.0f} impressions")
    if conv == 0 and spend >= 2 * target_cpa and has_volume:
        return _d("SOFT_KILL", f"Spent {spend:.0f} (≥2× CPA) with 0 conversions — don't turn off before 72h after calibration")

    # --- Not enough data → wait (rule 4.3) ---
    if conv < 50 and spend < max(500, target_cpa * 10) and not (conv == 0 and has_volume):
        return _d("WAIT", f"Too little data ({int(conv)} conv, {spend:.0f} spend) — don't draw conclusions from noise")

    # --- Creative fatigue (rule 4.10): high frequency + low CTR ---
    if freq >= 3.0 and ctr and ctr < 0.7:
        return _d("REFRESH_CREATIVE", f"Frequency {freq:.1f} + CTR {ctr:.2f}% — fatigue, change the CREATIVE (not the budget)")

    # --- Winner → scale (rule 4.6) ---
    if cpa is not None and cpa <= target_cpa and conv >= 50:
        return _d("SCALE", f"CPA {cpa:.2f} ≤ target {target_cpa} at {int(conv)} conv — scale +10-20% / 3-5 days OR duplicate the ad set")

    # --- CPA above target, but there are conversions → keep watching ---
    if cpa is not None and cpa > 1.5 * target_cpa and conv >= 5:
        return _d("WATCH", f"CPA {cpa:.2f} above 1.5× target — watch, candidate for turning off")

    return _d("KEEP", f"Within norm (CPA {cpa if cpa is None else round(cpa,2)}, {int(conv)} conv)")


def _d(action: str, reason: str) -> Dict[str, Any]:
    return {"action": action, "reason": reason}


def analyze(rows: List[Dict[str, Any]], target_cpa: float) -> List[Dict[str, Any]]:
    """Run every row through decide() and sort by action priority."""
    priority = {
        "HARD_KILL": 0, "SOFT_KILL": 1, "REFRESH_CREATIVE": 2,
        "WATCH": 3, "SCALE": 4, "WAIT": 5, "KEEP": 6,
    }
    out = []
    for row in rows:
        d = decide(row, target_cpa)
        out.append({**row, **d})
    out.sort(key=lambda r: priority.get(r["action"], 9))
    return out


def print_report(rows: List[Dict[str, Any]]) -> None:
    print(f"\n{'ACTION':<16} {'NAME':<32} {'SPEND':>8} {'CONV':>5} {'CPA':>7} {'CTR':>6} {'FREQ':>5}")
    print("-" * 90)
    for r in rows:
        name = (r.get("ad_name") or r.get("adset_name") or r.get("campaign_name") or "")[:30]
        cpa = "-" if r["cpa"] is None else f"{r['cpa']:.2f}"
        ctr = "-" if not r["ctr"] else f"{r['ctr']:.2f}"
        print(f"{r['action']:<16} {name:<32} {r['spend']:>8.0f} {int(r['conversions']):>5} {cpa:>7} {ctr:>6} {r['frequency']:>5.1f}")
    print("\nReasons:")
    for r in rows:
        if r["action"] not in ("KEEP",):
            name = (r.get("ad_name") or r.get("adset_name") or "")[:30]
            print(f"  [{r['action']}] {name}: {r['reason']}")


def save_csv(rows: List[Dict[str, Any]], path: str) -> None:
    if not rows:
        return
    keys = ["action", "reason", "ad_name", "adset_name", "campaign_name",
            "spend", "conversions", "cpa", "roas", "ctr", "frequency", "impressions"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meta Ads creative/ad set analysis with recommendations")
    parser.add_argument("--account", help="Ad account ID act_XXXX (if from API)")
    parser.add_argument("--csv", help="Path to a CSV export (if offline)")
    parser.add_argument("--target-cpa", type=float, required=True,
                        help="YOUR target CPA in the account currency (required, not guessed)")
    parser.add_argument("--level", default="ad", choices=["ad", "adset", "campaign"])
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--out", help="Where to save the CSV report")
    args = parser.parse_args()

    if args.csv:
        data = MetaClient.from_csv(args.csv)
    elif args.account:
        data = MetaClient().get_insights(args.account, level=args.level, days=args.days)
    else:
        print("Need either --account or --csv")
        sys.exit(1)

    result = analyze(data, args.target_cpa)
    print_report(result)
    if args.out:
        save_csv(result, args.out)
