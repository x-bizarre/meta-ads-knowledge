"""
significance_test.py — statistical significance check between two variants.

Implements rule 4.5 from the knowledge base: "Meta declaring a winner at 65%
confidence ≠ statistically reliable." This script honestly computes whether you
can already draw a conclusion.

Two tests are used:
  1. Two-proportion z-test — for rate metrics (CTR, conversion rate).
  2. A simple sample-sufficiency check — whether there is enough data at all.

No API required: you can call it by hand with numbers from Ads Manager.

Example (compare the conversion rate of two creatives):
    python significance_test.py --a 12 380 --b 7 410
    # A: 12 conversions out of 380 clicks, B: 7 out of 410

Or via import:
    from significance_test import compare_proportions
    result = compare_proportions(conv_a=12, n_a=380, conv_b=7, n_b=410)
"""

import argparse
import math
from typing import Dict, Any


def _normal_cdf(z: float) -> float:
    """Standard normal CDF via erf (no scipy needed)."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def compare_proportions(conv_a: int, n_a: int, conv_b: int, n_b: int) -> Dict[str, Any]:
    """
    Two-proportion z-test. Compares two rates (e.g. conversion rate).

    conv_a/n_a — successes and trials for variant A (conversions and clicks)
    conv_b/n_b — same for B

    Returns: rate A, rate B, the difference, p-value, confidence and a verdict.
    """
    if n_a == 0 or n_b == 0:
        return {"error": "Zero sample size — nothing to compare."}

    p_a = conv_a / n_a
    p_b = conv_b / n_b
    # Pooled proportion for the z-test
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))

    if se == 0:
        return {"error": "Zero variance — the variants are identical or there is no data."}

    z = (p_a - p_b) / se
    # Two-sided p-value
    p_value = 2 * (1 - _normal_cdf(abs(z)))
    confidence = (1 - p_value) * 100

    # Thresholds from the knowledge base (rule 4.5):
    #   ≥65% — Meta would call a winner (a low bar)
    #   ≥90% — reliable enough for expensive decisions / scaling
    if confidence >= 90:
        verdict = "RELIABLE: you can scale the winner"
    elif confidence >= 65:
        verdict = "WEAK: Meta would call a winner, but wait longer before expensive decisions"
    else:
        verdict = "NOISE: the difference is not significant, keep testing"

    winner = "A" if p_a > p_b else ("B" if p_b > p_a else "tie")

    return {
        "rate_a": round(p_a * 100, 3),
        "rate_b": round(p_b * 100, 3),
        "diff_abs_pct": round((p_a - p_b) * 100, 3),
        "diff_rel_pct": round((p_a - p_b) / p_b * 100, 1) if p_b else None,
        "z_score": round(z, 3),
        "p_value": round(p_value, 4),
        "confidence_pct": round(confidence, 1),
        "winner": winner,
        "verdict": verdict,
    }


def enough_data(conversions: int, spend: float, target_cpa: float) -> Dict[str, Any]:
    """
    Whether there is enough data to draw any conclusion about a variant.
    Threshold from rule 4.5: ≥50 conversions OR ~$500 of spend (or ~10× CPA) per ad set.
    """
    spend_threshold = max(500, target_cpa * 10) if target_cpa else 500
    ok_by_conversions = conversions >= 50
    ok_by_spend = spend >= spend_threshold

    return {
        "conversions": conversions,
        "spend": spend,
        "spend_threshold": round(spend_threshold, 2),
        "enough": ok_by_conversions or ok_by_spend,
        "reason": (
            "enough conversions (≥50)" if ok_by_conversions
            else f"enough spend (≥${spend_threshold:.0f})" if ok_by_spend
            else "NOT ENOUGH DATA — any conclusion would be noise, keep collecting"
        ),
    }


def _print(result: Dict[str, Any]) -> None:
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    print("\n=== Variant comparison ===")
    print(f"  Variant A: {result['rate_a']}%")
    print(f"  Variant B: {result['rate_b']}%")
    print(f"  Difference: {result['diff_abs_pct']}% (rel. {result['diff_rel_pct']}%)")
    print(f"  Confidence: {result['confidence_pct']}%   (p-value {result['p_value']})")
    print(f"  Winner: {result['winner']}")
    print(f"\n  >>> {result['verdict']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A/B statistical significance for Meta Ads")
    parser.add_argument("--a", nargs=2, type=int, metavar=("CONV", "N"),
                        help="Variant A: conversions and trials (clicks/impressions)")
    parser.add_argument("--b", nargs=2, type=int, metavar=("CONV", "N"),
                        help="Variant B: conversions and trials")
    args = parser.parse_args()

    if args.a and args.b:
        res = compare_proportions(args.a[0], args.a[1], args.b[0], args.b[1])
        _print(res)
    else:
        parser.print_help()
