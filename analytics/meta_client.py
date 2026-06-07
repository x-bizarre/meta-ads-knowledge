"""
meta_client.py — a thin client for the Meta Marketing API for post-hoc analytics.

Why a separate module: the other scripts (creative_analysis, fatigue_curve,
significance_test) shouldn't know HOW the data is fetched — they just receive a
list of stats rows. The source is swappable: a live API or a CSV export.

The token is read from the META_ACCESS_TOKEN environment variable. It's the same
long-lived token the MCP server uses. NEVER hardcode the token in the code.

Usage:
    export META_ACCESS_TOKEN="EAAB..."
    from meta_client import MetaClient
    client = MetaClient()
    rows = client.get_insights(account_id="act_123", level="ad", days=30)
"""

import os
import json
import time
import csv
import datetime
from typing import List, Dict, Any, Optional

import requests

# The API version can be overridden via the META_API_VERSION environment variable.
# Meta updates the API roughly every 3 months; old versions are deprecated after 2 years.
API_VERSION = os.environ.get("META_API_VERSION", "v21.0")
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Fields pulled by default. They are enough for all the analytics scripts.
DEFAULT_FIELDS = [
    "ad_id", "ad_name",
    "adset_id", "adset_name",
    "campaign_id", "campaign_name",
    "impressions", "reach", "frequency",
    "clicks", "ctr", "cpc", "cpm", "spend",
    "actions", "action_values",        # conversions and their value (purchases, etc.)
    "date_start", "date_stop",
]


class MetaClient:
    """A minimal client: only what's needed for post-hoc analytics (read-only)."""

    def __init__(self, access_token: Optional[str] = None):
        # Token from the environment, unless passed explicitly
        self.token = access_token or os.environ.get("META_ACCESS_TOKEN")
        if not self.token:
            raise RuntimeError(
                "No token. Set the META_ACCESS_TOKEN environment variable "
                "(the same long-lived token the MCP server uses)."
            )

    def _request(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """A single Graph API request with basic rate-limit handling."""
        params = dict(params)
        params["access_token"] = self.token
        url = f"{BASE_URL}/{path}"

        for attempt in range(4):
            resp = requests.get(url, params=params, timeout=60)
            if resp.status_code == 200:
                return resp.json()
            # Rate limit exceeded — Meta likes codes 4 / 17 / 80004 / 613
            if resp.status_code in (429, 500, 503):
                wait = 2 ** attempt * 5  # 5, 10, 20, 40 sec
                print(f"  Rate limit / temporary error, waiting {wait}s...")
                time.sleep(wait)
                continue
            # Any other error — show the body and fail
            raise RuntimeError(f"Meta API error {resp.status_code}: {resp.text}")
        raise RuntimeError("Could not fetch data after several attempts (rate limit).")

    def get_insights(
        self,
        account_id: str,
        level: str = "ad",
        days: int = 30,
        breakdown: Optional[str] = None,
        time_increment: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch stats. Returns a flat list of rows (dict).

        level         — "ad" / "adset" / "campaign" / "account"
        days          — over how many of the most recent days
        breakdown     — e.g. "age", "gender", "publisher_platform" (optional)
        time_increment — 1 = split by day (needed for fatigue curves)
        """
        if not account_id.startswith("act_"):
            account_id = f"act_{account_id}"

        params: Dict[str, Any] = {
            "level": level,
            "fields": ",".join(DEFAULT_FIELDS),
            "limit": 500,
        }
        # Add date_preset or time_range depending on the number of days
        params.update(_date_params(days))
        if breakdown:
            params["breakdowns"] = breakdown
        if time_increment:
            params["time_increment"] = time_increment

        rows: List[Dict[str, Any]] = []
        data = self._request(f"{account_id}/insights", params)
        rows.extend(data.get("data", []))

        # Pagination: we prefer paging.next (the full URL from Meta), but if it's
        # missing we use cursors.after. Guarded against KeyError via .get().
        while True:
            paging = data.get("paging", {})
            next_url = paging.get("next")
            if not next_url:
                break
            after = paging.get("cursors", {}).get("after")
            if not after:
                break
            params["after"] = after
            data = self._request(f"{account_id}/insights", params)
            rows.extend(data.get("data", []))

        return [_normalize(r) for r in rows]

    @staticmethod
    def from_csv(path: str) -> List[Dict[str, Any]]:
        """
        An alternative to the API: load an export from Ads Manager (CSV).
        Useful when you have no token or want to work offline.
        The CSV columns should be named like the API fields (or close to it).
        """
        with open(path, newline="", encoding="utf-8") as f:
            return [_normalize(row) for row in csv.DictReader(f)]


# Only these `days` values are supported by Meta as a date_preset.
# For the rest — we use time_range with explicit dates (from/to).
_VALID_PRESETS = {
    3: "last_3d", 7: "last_7d", 14: "last_14d",
    28: "last_28d", 30: "last_30d", 90: "last_90d",
}


def _date_params(days: int) -> Dict[str, Any]:
    """
    Return the date parameters for an Insights API request.

    For standard day counts (3,7,14,28,30,90) — returns a date_preset.
    For non-standard ones (10, 45, etc.) — returns a time_range with explicit
    dates, because the Meta API accepts ONLY fixed date_presets.
    """
    preset = _VALID_PRESETS.get(days)
    if preset:
        return {"date_preset": preset}

    # Non-standard number of days → compute an explicit range
    today = datetime.date.today()
    since = today - datetime.timedelta(days=days)
    return {
        "time_range": json.dumps({
            "since": since.isoformat(),
            "until": today.isoformat(),
        })
    }


# Mapping of short conversion names to full Meta API action_types.
# The format can differ across API versions. If you set CONVERSION_EVENT, you can
# pass a full action_type (e.g. "offsite_conversion.fb_pixel_purchase"); in that
# case the mapping isn't used and an exact match is done.
_ACTION_ALIASES = {
    "purchase": [
        "purchase",
        "offsite_conversion.fb_pixel_purchase",
        "omni_purchase",
        "onsite_web_purchase",
    ],
    "lead": [
        "lead",
        "offsite_conversion.fb_pixel_lead",
        "onsite_web_lead",
    ],
    "add_to_cart": [
        "add_to_cart",
        "offsite_conversion.fb_pixel_add_to_cart",
        "omni_add_to_cart",
    ],
    "complete_registration": [
        "complete_registration",
        "offsite_conversion.fb_pixel_complete_registration",
    ],
    "initiate_checkout": [
        "initiate_checkout",
        "offsite_conversion.fb_pixel_initiate_checkout",
        "omni_initiate_checkout",
    ],
}


def _extract_action(actions: Any, action_type: str) -> float:
    """
    Pull the count of a specific action (e.g. 'purchase') out of the actions field.
    Meta returns actions as a list of dicts [{action_type, value}, ...].

    Lookup: first an exact match on action_type, then on aliases (short name →
    full Meta API forms). This is needed because the action_type format has
    changed across API versions (v18+ may return "purchase", earlier ones —
    "offsite_conversion.fb_pixel_purchase", etc.).
    """
    if not actions:
        return 0.0
    if isinstance(actions, str):
        try:
            actions = json.loads(actions)
        except (ValueError, TypeError):
            return 0.0

    # Build the set of acceptable action_types to look for
    targets = {action_type}
    # If a short name was passed — add all known full forms
    if action_type in _ACTION_ALIASES:
        targets.update(_ACTION_ALIASES[action_type])

    for a in actions:
        if a.get("action_type") in targets:
            try:
                return float(a.get("value", 0))
            except (ValueError, TypeError):
                return 0.0
    return 0.0


def _normalize(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a row into a convenient shape: numbers as float, conversions surfaced.
    Which event counts as a "conversion" is configured via CONVERSION_EVENT.
    """
    conversion_event = os.environ.get("CONVERSION_EVENT", "purchase")

    def num(key: str) -> float:
        try:
            return float(row.get(key, 0) or 0)
        except (ValueError, TypeError):
            return 0.0

    conversions = _extract_action(row.get("actions"), conversion_event)
    conv_value = _extract_action(row.get("action_values"), conversion_event)
    spend = num("spend")

    return {
        "ad_id": row.get("ad_id", ""),
        "ad_name": row.get("ad_name", ""),
        "adset_id": row.get("adset_id", ""),
        "adset_name": row.get("adset_name", ""),
        "campaign_id": row.get("campaign_id", ""),
        "campaign_name": row.get("campaign_name", ""),
        "impressions": num("impressions"),
        "reach": num("reach"),
        "frequency": num("frequency"),
        "clicks": num("clicks"),
        "ctr": num("ctr"),
        "cpc": num("cpc"),
        "cpm": num("cpm"),
        "spend": spend,
        "conversions": conversions,
        "conversion_value": conv_value,
        # Derived metrics, computed honestly (not modeled)
        "cpa": (spend / conversions) if conversions else None,
        "roas": (conv_value / spend) if spend else None,
        "date_start": row.get("date_start", ""),
        "date_stop": row.get("date_stop", ""),
    }


if __name__ == "__main__":
    # Quick check: python meta_client.py act_XXXX
    import sys
    if len(sys.argv) < 2:
        print("Usage: python meta_client.py act_XXXXXXXX")
        sys.exit(1)
    c = MetaClient()
    data = c.get_insights(sys.argv[1], level="ad", days=30)
    print(f"Rows fetched: {len(data)}")
    if data:
        print(json.dumps(data[0], indent=2, ensure_ascii=False))
