# 06 — Geo / currency / taxes (adjustment for non-US markets)

> The whole knowledge base is built on US/global benchmarks. For other markets the numbers
> are different, and there are payment/tax nuances. This file corrects the rest.

---

## The main adjustment: US benchmarks are INFLATED for non-US geo

All the CPM/CPC/CPA numbers in file 04 (`~$13.48 CPM`, `~$38 CPA`, etc.) are US/global medians.

- **For non-US markets (CIS, LATAM, Southeast Asia, emerging markets) the real CPM
  is FAR lower** — often 3-10× cheaper than the US.
- **Direct consequence:** all the kill thresholds from file 04 ("3× target CPA at 0 conversions") must be calculated
  from YOUR real target CPA for your geo, not from US medians. Otherwise the agent will cut
  too early or too late.
- **Rule:** US benchmarks are only a thinking framework ("what to compare against"), NOT
  absolute thresholds. Absolute thresholds = your own historical baseline for the specific
  geo and product.

---

## Audience size for small markets

- File 02 says "reach from 1M for conversions." For small countries that may be unattainable.
- **What to do:** for small geos a smaller reach is acceptable; compensate with a more frequent optimization
  event (the ladder from file 05) and broader targeting with no narrowing.

---

## Ad account currency

- ⚠️ **The account currency is set at creation and changes ONLY by recreating the account.** Choose
  it deliberately from the start.
- It affects: how spend is calculated, the currency you're charged in, how the numbers reconcile with accounting.

---

## Payments and sanctions/regional specifics

> If you operate from a country with restrictions on international payments, attaching a card/account
> to Meta can be non-trivial. General principles:

- **Where you can run and pay for an ad account** — check against the specific card/account.
  Cards from some countries may not go through for Meta Ads payments — check in advance.
- **Account jurisdiction** — it makes sense to tie it to the country whose account/card pays.
- **Advertising tax / VAT** — depends on the country of the ad account. For non-business accounts in
  a number of countries Meta adds a local tax on top. Factor it into the real CPA calculation (tax = +X%
  on every charge).
- ⚠️ This is NOT legal advice — before launching from a new card/jurisdiction, check against the
  current Meta rules for the specific country.

---

## How this file interacts with the others

| File | What file 06 corrects |
|---|---|
| 02 (audiences) | "reach from 1M" — for small geos may be unattainable |
| 04 (optimization) | all CPM/CPC/CPA benchmarks — US-inflated, calculate from your own geo |
| 05 (cold start) | minimum budget — in local currency, accounting for local CPM |

**Takeaway for the agent:** before applying any numeric threshold from files 01-05 — ask/clarify
the geo and currency of the specific launch, and recalculate thresholds from the real target CPA, not from US medians.
