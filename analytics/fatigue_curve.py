"""
fatigue_curve.py — creative fatigue detector by day.

Implements rule 4.10 / 3.9 as code: fatigue = rising frequency + falling CTR +
rising CPM over time. Hard to catch by eye, easy to catch from a daily series.

Pulls stats with a daily breakdown (time_increment=1) and, for each ad, looks at
the trend over the recent days. Outputs the ads that are "burning out."

Run:
    export META_ACCESS_TOKEN="EAAB..."
    python fatigue_curve.py --account act_123 --days 14
"""

import argparse
import sys
from collections import defaultdict
from typing import List, Dict, Any

from meta_client import MetaClient


def _trend(values: List[float]) -> float:
    """
    Simple trend sign: compare the mean of the first and second halves of the series.
    Returns the relative change (e.g. +0.4 = grew by 40%).
    No numpy — to avoid pulling in dependencies.
    """
    values = [v for v in values if v is not None]
    if len(values) < 4:
        return 0.0
    mid = len(values) // 2
    first = sum(values[:mid]) / mid
    second = sum(values[mid:]) / (len(values) - mid)
    if first == 0:
        return 0.0
    return (second - first) / first


def detect_fatigue(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Group daily rows by ad_id and evaluate trends.
    Fatigue when BOTH hold: frequency rising, CTR falling.
    """
    by_ad: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_ad[r["ad_id"]].append(r)

    out = []
    for ad_id, days in by_ad.items():
        days.sort(key=lambda d: d["date_start"])
        if len(days) < 4:
            continue  # series too short

        ctr_trend = _trend([d["ctr"] for d in days])
        freq_trend = _trend([d["frequency"] for d in days])
        cpm_trend = _trend([d["cpm"] for d in days])

        # Fatigue: CTR fell ≥15% AND frequency rose ≥15%
        fatigued = ctr_trend <= -0.15 and freq_trend >= 0.15
        # Early signal: one of them moved hard + CPM is rising
        warning = (ctr_trend <= -0.25 or freq_trend >= 0.30) and cpm_trend >= 0.10

        if fatigued or warning:
            out.append({
                "ad_id": ad_id,
                "ad_name": days[-1].get("ad_name", ""),
                "days_tracked": len(days),
                "ctr_trend_pct": round(ctr_trend * 100, 1),
                "freq_trend_pct": round(freq_trend * 100, 1),
                "cpm_trend_pct": round(cpm_trend * 100, 1),
                "current_frequency": round(days[-1]["frequency"], 2),
                "status": "FATIGUED" if fatigued else "WARNING",
                "action": "Refresh the creative (not the budget) — rule 4.10",
            })

    out.sort(key=lambda r: (r["status"] != "FATIGUED", r["ctr_trend_pct"]))
    return out


def print_report(rows: List[Dict[str, Any]]) -> None:
    if not rows:
        print("\nNo creative fatigue detected. 👍")
        return
    print(f"\n{'STATUS':<10} {'NAME':<30} {'CTR↓':>7} {'FREQ↑':>7} {'CPM↑':>7} {'FREQ now':>9}")
    print("-" * 78)
    for r in rows:
        print(f"{r['status']:<10} {r['ad_name'][:28]:<30} "
              f"{r['ctr_trend_pct']:>6}% {r['freq_trend_pct']:>6}% "
              f"{r['cpm_trend_pct']:>6}% {r['current_frequency']:>9}")
    print("\nTakeaway: these ads are burning out — refresh the creative, leave the budget alone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meta Ads creative fatigue detector")
    parser.add_argument("--account", help="Ad account ID act_XXXX")
    parser.add_argument("--csv", help="CSV with a daily breakdown (date_start column)")
    parser.add_argument("--days", type=int, default=14)
    args = parser.parse_args()

    if args.csv:
        data = MetaClient.from_csv(args.csv)
    elif args.account:
        # time_increment=1 — critical: gives the daily breakdown
        data = MetaClient().get_insights(args.account, level="ad",
                                         days=args.days, time_increment=1)
    else:
        print("Need either --account or --csv")
        sys.exit(1)

    print_report(detect_fatigue(data))
