# 05 — Pixel / CAPI + cold start (STEP #0 of any B2C launch)

> This topic was missing from the first pass — the critic caught a critical gap. Without
> measurement set up correctly, the entire conversion optimization (files 01-04) physically cannot work.

---

## Why this is step #0

After iOS 14.5 (App Tracking Transparency), the browser pixel loses a significant share of
events — users opt out of tracking. If all you have is the pixel and no Conversions API,
Meta "doesn't see" most of the conversions → it can't train the algorithm → all
optimization toward sales runs blind. That's why measurement is set up BEFORE launch.

---

### Rule 5.1: What to set up BEFORE the first launch
1. **Meta Pixel** — browser-side tracking on the site/landing page.
2. **Conversions API (CAPI)** — server-side tracking that passes events around browser blocks.
3. **Deduplication** — so that a single event arriving from both the pixel and CAPI isn't counted twice (event_id).
4. **Domain verification** — verify the domain in Business Manager.
5. **Aggregated Event Measurement (AEM)** — set up and prioritize up to **8 events** per domain (Meta caps this after iOS 14.5). Your most valuable event (Purchase) goes on top.
- **Reliability:** [OFFICIAL META]

### Rule 5.2: The optimization event ladder (the FIX for the "<50 conversions/week" problem)
If you physically get fewer than 50 sales a week (new product, small budget, expensive item),
you can't optimize for Purchase right away — the ad set will be stuck in learning limited forever.
Step down the funnel toward a MORE FREQUENT event, then climb back up:

```
Purchase (rare)
  ↑ once you build volume — climb back up
Initiate Checkout
  ↑
Add to Cart
  ↑
View Content / Landing Page View (frequent)  ← start here if conversions are scarce
```

- **Logic:** optimize for the higher, more frequent event while signal accumulates; once purchases
  reach ≥50/week — switch to Purchase. Switching the event = a learning reset, do it deliberately.
- **Reliability:** [AGENCY CONSENSUS]

### Rule 5.3: Cold start of a new account (account warm-up)
- **The first 1-2 weeks CPA is inflated** — Meta has no conversion history for your pixel, the algorithm is learning. This is normal, not a reason to panic and restart everything.
- **Do NOT set a cost cap / bid cap at the start** — it will choke delivery (see file 04, rule 4.12). Begin on highest volume (lowest cost).
- **Do NOT touch the campaign in the first days** — let the algorithm gather signal.
- **Which event to start with** — the one that will reach ≥50/week (see ladder 5.2).
- **Reliability:** [AGENCY CONSENSUS]

### Rule 5.4: Minimum viable starting budget
- **Formula:** for one ad set to exit learning within a week, you need `target CPA × 50 / 7` per day
  on the event you're optimizing for.
- **Example:** if you optimize for Add to Cart with a "CPA" of $5 → you need ~$36/day just to
  learn. For Purchase with a CPA of $40 → ~$286/day. This is exactly why the event ladder exists — it lowers the
  required starting budget.
- ⚠️ Launching an underfunded campaign = it will never learn and will burn money for nothing.
  One funded ad set beats five starving ones.
- **Reliability:** [AGENCY CONSENSUS]

### Rule 5.5: Attribution and number discrepancies
- **Default attribution window after iOS:** 7-day click + 1-day view.
- **Ads Manager shows modeled conversions** — part of the data is MODELED (estimated
  statistically) rather than counted directly. That's why Ads Manager numbers diverge from
  GA4 / Shopify / actual sales.
- ⚠️ When making a kill/scale decision, remember: Ads Manager numbers are approximate. Reconcile them with actual
  sales (POS/CRM), especially on expensive products.
- **Reliability:** [OFFICIAL META]

### Rule 5.6: Special Ad Categories
- For some B2C verticals (credit/finance, housing, employment; indirectly — certain health/age-related
  products) Meta RESTRICTS targeting: it bans targeting by age, gender, ZIP, and narrows
  detailed targeting.
- ⚠️ If the product falls into a special category — the entire audience strategy from file 02 changes.
  Check this BEFORE launch, otherwise the campaign gets rejected or its reach gets cut.
- **Reliability:** [OFFICIAL META]

---

## "Cleared for launch" checklist
- [ ] Pixel + CAPI installed, events arriving (check in Events Manager)
- [ ] Deduplication works (no double counting)
- [ ] Domain verified, AEM configured (8 events prioritized)
- [ ] Optimization event chosen that will reach ≥50/week (ladder 5.2)
- [ ] Budget ≥ minimum viable (5.4)
- [ ] No cost cap set (cold start)
- [ ] Checked whether the product is a special category (5.6)
- [ ] Geo/currency/taxes checked (file 06)
