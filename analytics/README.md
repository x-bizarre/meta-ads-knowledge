# Meta Ads post-hoc analytics — scripts

Python scripts for precise analysis of ad results. They do what you can't reliably
do "by eye": compute statistical significance, catch creative fatigue from the daily
time series, and apply the kill/scale thresholds from the knowledge base automatically.

They work **on top of** the knowledge base: thresholds come from `../knowledge/04_optimization.md`,
and the geo adjustment comes from `../knowledge/06_geo_currency.md`.

---

## Installation

```bash
pip install -r requirements.txt
export META_ACCESS_TOKEN="EAAB..."     # the same long-lived token used by the MCP server
export CONVERSION_EVENT="purchase"      # which event counts as a conversion (default: purchase)
```

The token is read **only from the environment variable** — it is not in the code and never should be.

All scripts can also run **offline from CSV** (an export from Ads Manager) — for cases when
you don't have a token or need privacy. Use the `--csv export.csv` flag.

---

## Scripts

### `meta_client.py` — the API client
Pulls stats (`get_insights`), normalizes them, extracts real conversions from the
`actions` field, and honestly computes CPA and ROAS (instead of relying on Meta's modeled numbers).
On its own it analyzes nothing — it's the "data pipe" for everything else.

```bash
python meta_client.py act_XXXXXXXX        # sanity check: fetches rows and prints the first one
```

### `creative_analysis.py` — what to do with each ad
Applies the thresholds from file 04 and returns a decision for each creative/ad set:
`HARD_KILL / SOFT_KILL / REFRESH_CREATIVE / SCALE / WATCH / WAIT / KEEP`.

```bash
python creative_analysis.py --account act_XXX --target-cpa 8 --level ad --out report.csv
```

⚠️ `--target-cpa` is **required** — the script won't guess the threshold for you (the rule in file 06:
compute it from your own geo, not from US medians).

### `significance_test.py` — is it safe to draw a conclusion yet
Two-proportion z-test. It tells you straight: is the difference between variants significant,
or just noise. Implements rule 4.5 (65% = weak, 90% = reliable).

```bash
python significance_test.py --a 12 380 --b 7 410
# A: 12 conversions out of 380 clicks, B: 7 out of 410
```

Works without the API — you can punch in the numbers straight from Ads Manager.

### `fatigue_curve.py` — who's burning out
Takes the daily breakdown and catches fatigue: CTR dropping + frequency rising + CPM rising.
What's invisible at a single point in time becomes obvious on the trend.

```bash
python fatigue_curve.py --account act_XXX --days 14
```

---

## A typical workflow

```
1. creative_analysis.py   → see what to kill and what to scale
2. fatigue_curve.py       → separately check whether your top ads are burning out
3. significance_test.py   → before swapping the winner, confirm the difference isn't noise
4. Actions — via Meta MCP (update_adset / update_ad / update_campaign)
```

The scripts only **analyze and advise**. The actual ad changes are made by the MCP server
(Meta MCP) — by design: a human reviews the output and approves it.

---

## What the scripts DELIBERATELY don't do

- **They don't change ads.** Read and analysis only. Changes go through MCP, with human approval.
- **They don't guess target CPA.** You always pass the threshold yourself (the geo adjustment).
- **They don't blindly trust modeled numbers.** CPA/ROAS are computed from raw conversions; on expensive
  decisions, still cross-check against your till/CRM (rule 5.5).
- **They don't pull in scipy/pandas.** Just requests — so it deploys in a single `pip install` without pain.
