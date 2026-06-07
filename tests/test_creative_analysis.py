"""
test_creative_analysis.py -- tests for decide() from creative_analysis.py.

Scenario table: HARD_KILL, SOFT_KILL, REFRESH_CREATIVE,
SCALE, WAIT, KEEP, WATCH. All data is ready-made dicts, no API.
"""

import pytest
from creative_analysis import decide


def _row(
    spend=0.0, conversions=0, cpa=None, ctr=1.5,
    frequency=1.0, impressions=5000,
):
    """Helper: build a stats row with sensible defaults."""
    return {
        "spend": spend,
        "conversions": conversions,
        "cpa": cpa,
        "ctr": ctr,
        "frequency": frequency,
        "impressions": impressions,
    }


class TestDecide:
    """Tests for the decide() function."""

    # --- HARD_KILL ---

    def test_hard_kill_zero_conv_high_spend(self):
        """0 conversions, spent >= 3x CPA, enough impressions -> HARD_KILL."""
        row = _row(spend=30.0, conversions=0, cpa=None, impressions=5000)
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "HARD_KILL"

    def test_hard_kill_exactly_3x(self):
        """Exactly 3x CPA -> HARD_KILL (boundary)."""
        row = _row(spend=30.0, conversions=0, impressions=1500)
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "HARD_KILL"

    def test_hard_kill_needs_volume(self):
        """0 conv, 3x CPA, but few impressions -> NOT HARD_KILL (no has_volume)."""
        row = _row(spend=30.0, conversions=0, impressions=500)
        result = decide(row, target_cpa=10.0)
        # has_volume = spend >= target_cpa AND impressions >= 1000
        # spend 30 >= 10 -> True, impressions 500 < 1000 -> False
        # has_volume = False -> won't fall into HARD_KILL
        assert result["action"] != "HARD_KILL"

    # --- SOFT_KILL ---

    def test_soft_kill_zero_conv_2x_cpa(self):
        """0 conversions, spent >= 2x CPA (but < 3x) -> SOFT_KILL."""
        row = _row(spend=25.0, conversions=0, impressions=2000)
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "SOFT_KILL"

    def test_soft_kill_exactly_2x(self):
        """Exactly 2x CPA -> SOFT_KILL."""
        row = _row(spend=20.0, conversions=0, impressions=3000)
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "SOFT_KILL"

    # --- WAIT ---

    def test_wait_little_data(self):
        """Few conversions and little spend -> WAIT."""
        row = _row(spend=15.0, conversions=2, cpa=7.5, impressions=2000)
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "WAIT"

    def test_wait_zero_conv_low_spend(self):
        """0 conversions, little spend (< 2x CPA, no volume) -> WAIT."""
        row = _row(spend=5.0, conversions=0, impressions=500)
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "WAIT"

    # --- REFRESH_CREATIVE ---

    def test_refresh_creative_high_freq_low_ctr(self):
        """High frequency (>=3) + low CTR (<0.7%) -> REFRESH_CREATIVE."""
        # Must not fall into KILL/WAIT earlier -> plenty of conversions and spend
        row = _row(
            spend=600.0, conversions=55, cpa=10.9,
            ctr=0.5, frequency=3.5, impressions=30000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "REFRESH_CREATIVE"

    def test_no_refresh_normal_freq(self):
        """frequency < 3 -> NOT REFRESH_CREATIVE."""
        row = _row(
            spend=600.0, conversions=55, cpa=10.9,
            ctr=0.5, frequency=2.5, impressions=30000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] != "REFRESH_CREATIVE"

    def test_no_refresh_normal_ctr(self):
        """CTR >= 0.7 -> NOT REFRESH_CREATIVE (even at high frequency)."""
        row = _row(
            spend=600.0, conversions=55, cpa=10.9,
            ctr=1.2, frequency=4.0, impressions=30000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] != "REFRESH_CREATIVE"

    # --- SCALE ---

    def test_scale_good_cpa_enough_conversions(self):
        """CPA <= target and >= 50 conversions -> SCALE."""
        row = _row(
            spend=400.0, conversions=55, cpa=7.27,
            ctr=1.8, frequency=1.5, impressions=25000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "SCALE"

    def test_scale_boundary_50_conversions(self):
        """Exactly 50 conversions, CPA = target -> SCALE."""
        row = _row(
            spend=500.0, conversions=50, cpa=10.0,
            ctr=1.5, frequency=1.2, impressions=20000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "SCALE"

    def test_no_scale_49_conversions(self):
        """49 conversions -> NOT SCALE (too little data to scale confidently)."""
        row = _row(
            spend=490.0, conversions=49, cpa=10.0,
            ctr=1.5, frequency=1.2, impressions=20000,
        )
        result = decide(row, target_cpa=10.0)
        # 49 conv, 490 spend -> spend < max(500, 100) = 500 -> WAIT
        assert result["action"] != "SCALE"

    def test_no_scale_cpa_above_target(self):
        """CPA above target -> NOT SCALE."""
        row = _row(
            spend=600.0, conversions=50, cpa=12.0,
            ctr=1.5, frequency=1.2, impressions=20000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] != "SCALE"

    # --- WATCH ---

    def test_watch_high_cpa(self):
        """CPA > 1.5x target, conversions >= 5 -> WATCH."""
        row = _row(
            spend=800.0, conversions=50, cpa=16.0,
            ctr=1.5, frequency=1.2, impressions=20000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "WATCH"

    # --- KEEP ---

    def test_keep_normal(self):
        """All metrics within norm, but CPA slightly above target -> KEEP."""
        row = _row(
            spend=600.0, conversions=50, cpa=12.0,
            ctr=1.5, frequency=1.2, impressions=20000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "KEEP"

    def test_keep_cpa_slightly_above_but_not_15x(self):
        """CPA > target, but <= 1.5x target -> KEEP."""
        row = _row(
            spend=700.0, conversions=50, cpa=14.0,
            ctr=1.5, frequency=1.2, impressions=20000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "KEEP"

    # --- Response structure ---

    def test_result_has_action_and_reason(self):
        """The result contains action and reason."""
        row = _row(spend=10.0, conversions=1, cpa=10.0)
        result = decide(row, target_cpa=10.0)
        assert "action" in result
        assert "reason" in result
        assert isinstance(result["reason"], str)
        assert len(result["reason"]) > 0

    # --- Rule priority ---

    def test_hard_kill_before_refresh(self):
        """HARD_KILL takes priority over REFRESH_CREATIVE (checks branch order)."""
        # Matches both: 0 conv + 3xCPA + high freq + low CTR
        row = _row(
            spend=30.0, conversions=0, cpa=None,
            ctr=0.3, frequency=4.0, impressions=5000,
        )
        result = decide(row, target_cpa=10.0)
        assert result["action"] == "HARD_KILL"
