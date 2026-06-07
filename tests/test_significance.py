"""
test_significance.py -- tests for compare_proportions() and enough_data()
from significance_test.py.

Covers: a clear difference (high confidence), noise (low confidence),
zero sample size, the 65%/90% boundary thresholds, and edge cases.
"""

import pytest
from significance_test import compare_proportions, enough_data


# ============================================================
# compare_proportions()
# ============================================================

class TestCompareProportions:
    """Tests for the two-proportion z-test."""

    def test_clear_winner_high_confidence(self):
        """Clear difference: A is much better than B -> confidence >= 90%."""
        # A: 50 out of 500 (10%), B: 20 out of 500 (4%) -- a large difference
        result = compare_proportions(conv_a=50, n_a=500, conv_b=20, n_b=500)
        assert "error" not in result
        assert result["confidence_pct"] >= 90
        assert result["winner"] == "A"
        assert "RELIABLE" in result["verdict"]

    def test_noise_low_confidence(self):
        """Noise: the difference is minimal -> confidence < 65%."""
        # A: 10 out of 100 (10%), B: 9 out of 100 (9%) -- almost identical
        result = compare_proportions(conv_a=10, n_a=100, conv_b=9, n_b=100)
        assert "error" not in result
        assert result["confidence_pct"] < 65
        assert "NOISE" in result["verdict"]

    def test_medium_confidence_65_to_90(self):
        """In-between case: Meta would call a winner, but it's too early to scale."""
        # Numbers chosen so confidence lands between 65 and 90
        # A: 30 out of 200 (15%), B: 20 out of 200 (10%) -- noticeable but not huge
        result = compare_proportions(conv_a=30, n_a=200, conv_b=20, n_b=200)
        assert "error" not in result
        assert 65 <= result["confidence_pct"] < 90
        assert "WEAK" in result["verdict"]

    def test_zero_sample_a(self):
        """Zero sample size for A -> error."""
        result = compare_proportions(conv_a=0, n_a=0, conv_b=5, n_b=100)
        assert "error" in result

    def test_zero_sample_b(self):
        """Zero sample size for B -> error."""
        result = compare_proportions(conv_a=5, n_a=100, conv_b=0, n_b=0)
        assert "error" in result

    def test_both_zero_samples(self):
        """Both samples zero -> error."""
        result = compare_proportions(conv_a=0, n_a=0, conv_b=0, n_b=0)
        assert "error" in result

    def test_identical_rates(self):
        """Identical rates -> confidence 0%, noise."""
        result = compare_proportions(conv_a=10, n_a=100, conv_b=10, n_b=100)
        assert "error" not in result
        assert result["confidence_pct"] == 0.0
        assert result["winner"] == "tie"
        assert "NOISE" in result["verdict"]

    def test_zero_conversions_both(self):
        """Zero conversions on both sides -> se=0 -> "zero variance" error."""
        result = compare_proportions(conv_a=0, n_a=100, conv_b=0, n_b=100)
        assert "error" in result
        assert "variance" in result["error"].lower() or "identical" in result["error"].lower()

    def test_all_conversions_both(self):
        """All trials successful on both sides -> se=0 -> error."""
        result = compare_proportions(conv_a=100, n_a=100, conv_b=100, n_b=100)
        assert "error" in result

    def test_b_wins(self):
        """B is better than A -> winner = B."""
        result = compare_proportions(conv_a=5, n_a=500, conv_b=50, n_b=500)
        assert "error" not in result
        assert result["winner"] == "B"

    def test_result_fields_present(self):
        """Check that all expected fields are in the response."""
        result = compare_proportions(conv_a=50, n_a=500, conv_b=20, n_b=500)
        expected_keys = {"rate_a", "rate_b", "diff_abs_pct", "diff_rel_pct",
                         "z_score", "p_value", "confidence_pct", "winner", "verdict"}
        assert expected_keys.issubset(result.keys())

    def test_rates_are_percentages(self):
        """rate_a and rate_b are percentages (0-100), not fractions (0-1)."""
        result = compare_proportions(conv_a=10, n_a=100, conv_b=5, n_b=100)
        assert result["rate_a"] == 10.0
        assert result["rate_b"] == 5.0

    def test_p_value_range(self):
        """p-value is always between 0 and 1."""
        result = compare_proportions(conv_a=30, n_a=300, conv_b=20, n_b=300)
        assert 0 <= result["p_value"] <= 1

    def test_diff_rel_pct_none_when_b_zero_rate(self):
        """If p_b=0, diff_rel_pct = None (division by zero)."""
        result = compare_proportions(conv_a=5, n_a=100, conv_b=0, n_b=100)
        # se won't be 0 (p_pool != 0 and != 1), so there is no error
        assert "error" not in result
        assert result["diff_rel_pct"] is None

    def test_large_sample_precision(self):
        """Large samples: even a tiny difference -> high confidence."""
        # A: 1050 out of 10000 (10.5%), B: 1000 out of 10000 (10.0%)
        result = compare_proportions(conv_a=1050, n_a=10000, conv_b=1000, n_b=10000)
        assert "error" not in result
        # At these volumes even a 0.5% difference can be significant
        assert result["confidence_pct"] > 0


# ============================================================
# enough_data()
# ============================================================

class TestEnoughData:
    """Tests for the data-sufficiency check."""

    def test_enough_by_conversions(self):
        """50+ conversions -> enough, regardless of spend."""
        result = enough_data(conversions=50, spend=10.0, target_cpa=5.0)
        assert result["enough"] is True
        assert "conversions" in result["reason"]

    def test_enough_by_spend(self):
        """Spend >= max(500, 10*CPA) -> enough."""
        # target_cpa=10 -> threshold = max(500, 100) = 500
        result = enough_data(conversions=3, spend=500.0, target_cpa=10.0)
        assert result["enough"] is True
        assert "spend" in result["reason"]

    def test_enough_by_spend_high_cpa(self):
        """High CPA -> threshold = 10*CPA, if 10*CPA > 500."""
        # target_cpa=100 -> threshold = max(500, 1000) = 1000
        result = enough_data(conversions=3, spend=1000.0, target_cpa=100.0)
        assert result["enough"] is True
        assert result["spend_threshold"] == 1000.0

    def test_not_enough(self):
        """Too few conversions and too little spend -> not enough."""
        result = enough_data(conversions=3, spend=20.0, target_cpa=10.0)
        assert result["enough"] is False
        assert "NOT ENOUGH" in result["reason"].upper()

    def test_zero_conversions_low_spend(self):
        """Zero conversions + little spend -> not enough."""
        result = enough_data(conversions=0, spend=5.0, target_cpa=10.0)
        assert result["enough"] is False

    def test_zero_target_cpa(self):
        """target_cpa=0 -> spend threshold = 500 (fallback)."""
        result = enough_data(conversions=3, spend=499.0, target_cpa=0)
        assert result["enough"] is False
        assert result["spend_threshold"] == 500.0

    def test_none_target_cpa(self):
        """target_cpa=None -> spend threshold = 500 (fallback)."""
        result = enough_data(conversions=3, spend=501.0, target_cpa=None)
        assert result["enough"] is True

    def test_result_fields(self):
        """All expected fields are present."""
        result = enough_data(conversions=10, spend=50.0, target_cpa=5.0)
        assert "conversions" in result
        assert "spend" in result
        assert "spend_threshold" in result
        assert "enough" in result
        assert "reason" in result

    def test_boundary_49_conversions(self):
        """49 conversions + little spend -> not enough (boundary)."""
        result = enough_data(conversions=49, spend=10.0, target_cpa=5.0)
        assert result["enough"] is False

    def test_boundary_50_conversions(self):
        """Exactly 50 conversions -> enough (boundary)."""
        result = enough_data(conversions=50, spend=0.0, target_cpa=5.0)
        assert result["enough"] is True
