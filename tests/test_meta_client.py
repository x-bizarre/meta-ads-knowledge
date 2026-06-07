"""
test_meta_client.py -- tests for the pure functions in meta_client.py:
_normalize(), _extract_action(), _date_params().

Does NOT hit the network -- tests only parsing and data transformation.
"""

import json
import datetime
import pytest
from unittest.mock import patch

from meta_client import _normalize, _extract_action, _date_params, _ACTION_ALIASES


# ============================================================
# _extract_action()
# ============================================================

class TestExtractAction:
    """Tests for extracting a specific action_type from the actions field."""

    def test_exact_match_purchase(self):
        """Exact match on 'purchase'."""
        actions = [
            {"action_type": "link_click", "value": "100"},
            {"action_type": "purchase", "value": "12"},
        ]
        assert _extract_action(actions, "purchase") == 12.0

    def test_alias_offsite_conversion(self):
        """Short 'purchase' finds 'offsite_conversion.fb_pixel_purchase'."""
        actions = [
            {"action_type": "link_click", "value": "50"},
            {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "7"},
        ]
        assert _extract_action(actions, "purchase") == 7.0

    def test_alias_omni_purchase(self):
        """Short 'purchase' finds 'omni_purchase'."""
        actions = [
            {"action_type": "omni_purchase", "value": "15"},
        ]
        assert _extract_action(actions, "purchase") == 15.0

    def test_full_action_type_direct(self):
        """A full action_type with no alias -> exact match."""
        actions = [
            {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "9"},
        ]
        assert _extract_action(actions, "offsite_conversion.fb_pixel_purchase") == 9.0

    def test_lead_alias(self):
        """Alias for lead."""
        actions = [
            {"action_type": "offsite_conversion.fb_pixel_lead", "value": "20"},
        ]
        assert _extract_action(actions, "lead") == 20.0

    def test_add_to_cart_alias(self):
        """Alias for add_to_cart."""
        actions = [
            {"action_type": "offsite_conversion.fb_pixel_add_to_cart", "value": "33"},
        ]
        assert _extract_action(actions, "add_to_cart") == 33.0

    def test_no_match(self):
        """No match -> 0.0."""
        actions = [
            {"action_type": "link_click", "value": "100"},
        ]
        assert _extract_action(actions, "purchase") == 0.0

    def test_empty_actions(self):
        """Empty list -> 0.0."""
        assert _extract_action([], "purchase") == 0.0

    def test_none_actions(self):
        """None -> 0.0."""
        assert _extract_action(None, "purchase") == 0.0

    def test_actions_as_json_string(self):
        """actions as a JSON string (from CSV) -> parsed and works."""
        actions_str = json.dumps([
            {"action_type": "purchase", "value": "5"},
        ])
        assert _extract_action(actions_str, "purchase") == 5.0

    def test_invalid_json_string(self):
        """Invalid JSON -> 0.0."""
        assert _extract_action("not json at all", "purchase") == 0.0

    def test_value_not_numeric(self):
        """value not a number -> 0.0 (doesn't crash)."""
        actions = [
            {"action_type": "purchase", "value": "abc"},
        ]
        assert _extract_action(actions, "purchase") == 0.0

    def test_missing_value_field(self):
        """No value field -> 0.0."""
        actions = [
            {"action_type": "purchase"},
        ]
        assert _extract_action(actions, "purchase") == 0.0

    def test_first_matching_wins(self):
        """If there are several matches -- the first one is taken."""
        actions = [
            {"action_type": "purchase", "value": "10"},
            {"action_type": "omni_purchase", "value": "20"},
        ]
        # 'purchase' matches exactly first
        assert _extract_action(actions, "purchase") == 10.0

    def test_unknown_action_type(self):
        """An unknown action_type with no aliases -> exact match."""
        actions = [
            {"action_type": "custom_event_xyz", "value": "42"},
        ]
        assert _extract_action(actions, "custom_event_xyz") == 42.0
        assert _extract_action(actions, "something_else") == 0.0


# ============================================================
# _date_params()
# ============================================================

class TestDateParams:
    """Tests for building the date parameters for the Insights API."""

    def test_standard_7_days(self):
        """7 days -> date_preset=last_7d."""
        result = _date_params(7)
        assert result == {"date_preset": "last_7d"}

    def test_standard_14_days(self):
        """14 days -> date_preset=last_14d."""
        result = _date_params(14)
        assert result == {"date_preset": "last_14d"}

    def test_standard_28_days(self):
        """28 days -> date_preset=last_28d."""
        result = _date_params(28)
        assert result == {"date_preset": "last_28d"}

    def test_standard_30_days(self):
        """30 days -> date_preset=last_30d."""
        result = _date_params(30)
        assert result == {"date_preset": "last_30d"}

    def test_standard_90_days(self):
        """90 days -> date_preset=last_90d."""
        result = _date_params(90)
        assert result == {"date_preset": "last_90d"}

    def test_standard_3_days(self):
        """3 days -> date_preset=last_3d."""
        result = _date_params(3)
        assert result == {"date_preset": "last_3d"}

    def test_nonstandard_10_days(self):
        """10 days (non-standard) -> time_range with explicit dates."""
        result = _date_params(10)
        assert "time_range" in result
        assert "date_preset" not in result
        # Parse time_range and check the format
        tr = json.loads(result["time_range"])
        assert "since" in tr
        assert "until" in tr
        # Check that the dates are valid ISO strings
        since = datetime.date.fromisoformat(tr["since"])
        until = datetime.date.fromisoformat(tr["until"])
        assert (until - since).days == 10

    def test_nonstandard_45_days(self):
        """45 days -> time_range."""
        result = _date_params(45)
        assert "time_range" in result
        tr = json.loads(result["time_range"])
        since = datetime.date.fromisoformat(tr["since"])
        until = datetime.date.fromisoformat(tr["until"])
        assert (until - since).days == 45

    def test_nonstandard_1_day(self):
        """1 day -> time_range (no last_1d preset)."""
        result = _date_params(1)
        assert "time_range" in result

    def test_all_valid_presets_covered(self):
        """All 6 standard presets return a date_preset."""
        for days in [3, 7, 14, 28, 30, 90]:
            result = _date_params(days)
            assert "date_preset" in result, f"days={days} should give a date_preset"


# ============================================================
# _normalize()
# ============================================================

class TestNormalize:
    """Tests for normalizing a row from the Meta API / CSV."""

    def test_basic_normalization(self):
        """Basic normalization: numbers as float, conversions extracted."""
        row = {
            "ad_id": "123",
            "ad_name": "Test Ad",
            "adset_id": "456",
            "adset_name": "Test Adset",
            "campaign_id": "789",
            "campaign_name": "Test Campaign",
            "impressions": "10000",
            "reach": "8000",
            "frequency": "1.25",
            "clicks": "200",
            "ctr": "2.0",
            "cpc": "0.50",
            "cpm": "10.0",
            "spend": "100.0",
            "actions": [{"action_type": "purchase", "value": "10"}],
            "action_values": [{"action_type": "purchase", "value": "500.0"}],
            "date_start": "2026-06-01",
            "date_stop": "2026-06-07",
        }
        result = _normalize(row)
        assert result["ad_id"] == "123"
        assert result["impressions"] == 10000.0
        assert result["spend"] == 100.0
        assert result["conversions"] == 10.0
        assert result["conversion_value"] == 500.0
        assert result["cpa"] == 10.0  # 100 / 10
        assert result["roas"] == 5.0  # 500 / 100

    def test_zero_conversions_cpa_none(self):
        """0 conversions -> CPA = None."""
        row = {
            "spend": "50",
            "actions": [],
        }
        result = _normalize(row)
        assert result["conversions"] == 0.0
        assert result["cpa"] is None

    def test_zero_spend_roas_none(self):
        """0 spend -> ROAS = None."""
        row = {
            "spend": "0",
            "actions": [{"action_type": "purchase", "value": "5"}],
            "action_values": [{"action_type": "purchase", "value": "250"}],
        }
        result = _normalize(row)
        assert result["roas"] is None

    def test_missing_fields(self):
        """Missing fields -> default values (0.0 / '')."""
        row = {}
        result = _normalize(row)
        assert result["impressions"] == 0.0
        assert result["spend"] == 0.0
        assert result["conversions"] == 0.0
        assert result["ad_id"] == ""
        assert result["ad_name"] == ""
        assert result["cpa"] is None
        assert result["roas"] is None

    def test_string_numbers(self):
        """Numbers as strings (typical for CSV) -> float."""
        row = {"impressions": "1500", "spend": "25.50", "ctr": "1.75"}
        result = _normalize(row)
        assert result["impressions"] == 1500.0
        assert result["spend"] == 25.5
        assert result["ctr"] == 1.75

    def test_none_values(self):
        """None values -> 0.0 (doesn't crash)."""
        row = {"impressions": None, "spend": None, "ctr": None}
        result = _normalize(row)
        assert result["impressions"] == 0.0
        assert result["spend"] == 0.0

    def test_invalid_string_values(self):
        """Non-numeric strings -> 0.0."""
        row = {"impressions": "N/A", "spend": "error"}
        result = _normalize(row)
        assert result["impressions"] == 0.0
        assert result["spend"] == 0.0

    def test_conversion_event_env(self):
        """CONVERSION_EVENT from the environment changes which conversions are counted."""
        row = {
            "spend": "100",
            "actions": [
                {"action_type": "lead", "value": "20"},
                {"action_type": "purchase", "value": "5"},
            ],
        }
        with patch.dict("os.environ", {"CONVERSION_EVENT": "lead"}):
            result = _normalize(row)
            assert result["conversions"] == 20.0

    def test_all_output_fields_present(self):
        """Check the completeness of the output fields."""
        row = {"spend": "10"}
        result = _normalize(row)
        expected_keys = {
            "ad_id", "ad_name", "adset_id", "adset_name",
            "campaign_id", "campaign_name",
            "impressions", "reach", "frequency", "clicks",
            "ctr", "cpc", "cpm", "spend",
            "conversions", "conversion_value",
            "cpa", "roas",
            "date_start", "date_stop",
        }
        assert expected_keys == set(result.keys())

    def test_actions_as_json_string_in_normalize(self):
        """actions as a JSON string (from CSV) -> parsed correctly."""
        actions_json = json.dumps([
            {"action_type": "purchase", "value": "8"},
        ])
        row = {"spend": "80", "actions": actions_json}
        result = _normalize(row)
        assert result["conversions"] == 8.0
        assert result["cpa"] == 10.0  # 80 / 8

    def test_offsite_conversion_alias_in_normalize(self):
        """offsite_conversion.fb_pixel_purchase is found via the 'purchase' alias."""
        row = {
            "spend": "100",
            "actions": [
                {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "10"},
            ],
            "action_values": [
                {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "500"},
            ],
        }
        # By default CONVERSION_EVENT=purchase, so the alias should pick it up
        result = _normalize(row)
        assert result["conversions"] == 10.0
        assert result["conversion_value"] == 500.0
