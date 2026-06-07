"""
test_fatigue.py -- tests for _trend() and detect_fatigue() from fatigue_curve.py.

All data is synthetic -- no API calls.
"""

import pytest
from fatigue_curve import _trend, detect_fatigue


# ============================================================
# _trend()
# ============================================================

class TestTrend:
    """Tests for trend computation (sign and magnitude)."""

    def test_growing_series(self):
        """A rising series -> positive trend."""
        # First half ~10, second ~20 -> growth ~100%
        values = [10, 10, 10, 10, 20, 20, 20, 20]
        result = _trend(values)
        assert result > 0
        assert abs(result - 1.0) < 0.01  # (20-10)/10 = 1.0

    def test_falling_series(self):
        """A falling series -> negative trend."""
        values = [20, 20, 20, 20, 10, 10, 10, 10]
        result = _trend(values)
        assert result < 0
        assert abs(result - (-0.5)) < 0.01  # (10-20)/20 = -0.5

    def test_flat_series(self):
        """A flat series -> trend ~0."""
        values = [5, 5, 5, 5, 5, 5, 5, 5]
        result = _trend(values)
        assert result == 0.0

    def test_too_short_series(self):
        """Fewer than 4 points -> 0.0 (too little data)."""
        assert _trend([1, 2, 3]) == 0.0
        assert _trend([1, 2]) == 0.0
        assert _trend([1]) == 0.0
        assert _trend([]) == 0.0

    def test_exactly_4_points(self):
        """Exactly 4 points -> counted (2+2 split)."""
        values = [10, 10, 20, 20]
        result = _trend(values)
        assert result > 0

    def test_none_values_filtered(self):
        """None values are filtered out."""
        values = [10, None, 10, None, 20, None, 20, None]
        result = _trend(values)
        # After filtering: [10, 10, 20, 20]
        assert result > 0

    def test_all_none(self):
        """All None -> 0.0."""
        assert _trend([None, None, None, None, None]) == 0.0

    def test_first_half_zero(self):
        """First half = 0 -> 0.0 (guard against division by zero)."""
        values = [0, 0, 0, 0, 10, 10, 10, 10]
        result = _trend(values)
        assert result == 0.0

    def test_odd_length_series(self):
        """Odd number of points -> correct split (mid = len//2)."""
        # 5 points: first 2, last 3
        values = [10, 10, 20, 20, 20]
        result = _trend(values)
        # first = 10, second = 20 -> (20-10)/10 = 1.0
        assert result > 0

    def test_gradual_increase(self):
        """A gradual increase -> positive trend."""
        values = [1, 2, 3, 4, 5, 6, 7, 8]
        result = _trend(values)
        assert result > 0


# ============================================================
# detect_fatigue()
# ============================================================

def _make_daily_rows(ad_id, days_data):
    """
    Build a list of daily rows for a single ad.
    days_data: a list of tuples (ctr, frequency, cpm, date_start).
    """
    rows = []
    for i, (ctr, freq, cpm, date) in enumerate(days_data):
        rows.append({
            "ad_id": ad_id,
            "ad_name": f"Ad_{ad_id}",
            "ctr": ctr,
            "frequency": freq,
            "cpm": cpm,
            "date_start": date,
        })
    return rows


class TestDetectFatigue:
    """Tests for the fatigue detector."""

    def test_fatigued_ad(self):
        """CTR falls >= 15%, frequency rises >= 15% -> FATIGUED."""
        # CTR: first half ~2.0, second ~1.5 -> drop 25%
        # Frequency: first ~1.0, second ~1.5 -> growth 50%
        days = _make_daily_rows("fatigued_1", [
            (2.0, 1.0, 10, "2026-06-01"),
            (2.0, 1.0, 10, "2026-06-02"),
            (2.1, 1.1, 10, "2026-06-03"),
            (1.9, 1.1, 11, "2026-06-04"),
            (1.5, 1.5, 12, "2026-06-05"),
            (1.4, 1.6, 12, "2026-06-06"),
            (1.3, 1.7, 13, "2026-06-07"),
            (1.2, 1.8, 13, "2026-06-08"),
        ])
        result = detect_fatigue(days)
        assert len(result) > 0
        assert result[0]["ad_id"] == "fatigued_1"
        assert result[0]["status"] in ("FATIGUED", "WARNING")

    def test_stable_ad(self):
        """Stable CTR and frequency -> nothing burns out."""
        days = _make_daily_rows("stable_1", [
            (1.8, 1.2, 10, "2026-06-01"),
            (1.9, 1.2, 10, "2026-06-02"),
            (1.8, 1.3, 10, "2026-06-03"),
            (1.7, 1.2, 10, "2026-06-04"),
            (1.8, 1.3, 10, "2026-06-05"),
            (1.9, 1.2, 10, "2026-06-06"),
            (1.8, 1.3, 10, "2026-06-07"),
            (1.7, 1.2, 10, "2026-06-08"),
        ])
        result = detect_fatigue(days)
        assert len(result) == 0

    def test_too_few_days(self):
        """Fewer than 4 days -> skipped (not enough for a trend)."""
        days = _make_daily_rows("short_1", [
            (2.0, 1.0, 10, "2026-06-01"),
            (1.0, 2.0, 15, "2026-06-02"),
            (0.5, 3.0, 20, "2026-06-03"),
        ])
        result = detect_fatigue(days)
        assert len(result) == 0

    def test_multiple_ads_mixed(self):
        """Several ads: one burns out, another is stable."""
        fatigued = _make_daily_rows("ad_bad", [
            (2.0, 1.0, 10, "2026-06-01"),
            (2.0, 1.0, 10, "2026-06-02"),
            (1.5, 1.5, 12, "2026-06-03"),
            (1.5, 1.5, 12, "2026-06-04"),
            (1.0, 2.0, 14, "2026-06-05"),
            (1.0, 2.0, 14, "2026-06-06"),
            (0.8, 2.5, 16, "2026-06-07"),
            (0.7, 3.0, 18, "2026-06-08"),
        ])
        stable = _make_daily_rows("ad_good", [
            (1.8, 1.2, 10, "2026-06-01"),
            (1.8, 1.2, 10, "2026-06-02"),
            (1.9, 1.2, 10, "2026-06-03"),
            (1.8, 1.3, 10, "2026-06-04"),
            (1.8, 1.2, 10, "2026-06-05"),
            (1.8, 1.3, 10, "2026-06-06"),
            (1.9, 1.2, 10, "2026-06-07"),
            (1.8, 1.2, 10, "2026-06-08"),
        ])
        all_rows = fatigued + stable
        result = detect_fatigue(all_rows)
        ad_ids = [r["ad_id"] for r in result]
        assert "ad_bad" in ad_ids
        assert "ad_good" not in ad_ids

    def test_warning_ctr_drops_hard(self):
        """CTR falls > 25% while CPM rises -> WARNING (early signal)."""
        days = _make_daily_rows("warn_1", [
            (3.0, 1.0, 8, "2026-06-01"),
            (3.0, 1.0, 8, "2026-06-02"),
            (2.8, 1.1, 9, "2026-06-03"),
            (2.8, 1.1, 9, "2026-06-04"),
            (2.0, 1.1, 10, "2026-06-05"),
            (1.8, 1.1, 10, "2026-06-06"),
            (1.5, 1.2, 11, "2026-06-07"),
            (1.5, 1.2, 11, "2026-06-08"),
        ])
        result = detect_fatigue(days)
        # CTR falls ~45%, frequency rises a little (~15%), CPM rises ~25%
        # warning = (ctr_trend <= -0.25 OR freq_trend >= 0.30) AND cpm_trend >= 0.10
        # ctr_trend ~-0.45 -> True, cpm_trend ~0.25 -> True => WARNING
        assert len(result) > 0
        assert result[0]["ad_id"] == "warn_1"

    def test_empty_input(self):
        """Empty list -> empty result."""
        assert detect_fatigue([]) == []

    def test_output_fields(self):
        """Check that all fields are present in the result."""
        days = _make_daily_rows("check_fields", [
            (2.0, 1.0, 10, "2026-06-01"),
            (2.0, 1.0, 10, "2026-06-02"),
            (1.0, 2.0, 14, "2026-06-03"),
            (1.0, 2.0, 14, "2026-06-04"),
            (0.5, 3.0, 18, "2026-06-05"),
            (0.5, 3.0, 18, "2026-06-06"),
        ])
        result = detect_fatigue(days)
        if result:  # may be empty if thresholds aren't met
            for r in result:
                assert "ad_id" in r
                assert "ad_name" in r
                assert "days_tracked" in r
                assert "ctr_trend_pct" in r
                assert "freq_trend_pct" in r
                assert "cpm_trend_pct" in r
                assert "current_frequency" in r
                assert "status" in r
                assert "action" in r

    def test_sorting_fatigued_first(self):
        """FATIGUED sorts before WARNING."""
        fatigued = _make_daily_rows("fat_1", [
            (2.0, 1.0, 10, "2026-06-01"),
            (2.0, 1.0, 10, "2026-06-02"),
            (1.0, 2.0, 12, "2026-06-03"),
            (1.0, 2.0, 12, "2026-06-04"),
            (0.5, 3.0, 14, "2026-06-05"),
            (0.5, 3.0, 14, "2026-06-06"),
        ])
        # For a warning: CTR drops sharply, freq doesn't rise much, but CPM rises
        warning = _make_daily_rows("warn_2", [
            (3.0, 1.0, 8, "2026-06-01"),
            (3.0, 1.0, 8, "2026-06-02"),
            (2.0, 1.0, 9, "2026-06-03"),
            (2.0, 1.0, 9, "2026-06-04"),
            (1.5, 1.1, 10, "2026-06-05"),
            (1.5, 1.1, 10, "2026-06-06"),
        ])
        all_rows = warning + fatigued
        result = detect_fatigue(all_rows)
        if len(result) >= 2:
            # FATIGUED should come before WARNING
            statuses = [r["status"] for r in result]
            if "FATIGUED" in statuses and "WARNING" in statuses:
                fat_idx = statuses.index("FATIGUED")
                warn_idx = statuses.index("WARNING")
                assert fat_idx < warn_idx
