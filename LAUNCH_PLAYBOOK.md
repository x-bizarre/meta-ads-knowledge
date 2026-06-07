# Step-by-step playbook for launching a B2C campaign in Meta Ads

> The main working document. The agent treats it as a checklist when launching from scratch.
> Each step links to the details in `knowledge/`. Numeric thresholds must be recalculated for your geo (file 06).

---

## STEP 0 — Measurement (BEFORE launch — nothing works without it)
→ details: `knowledge/05_pixel_and_coldstart.md`

- [ ] Pixel + Conversions API installed, events arriving (Events Manager)
- [ ] Deduplication set up (event_id)
- [ ] Domain verified, AEM — 8 events prioritized (Purchase at the top)
- [ ] Checked: is the product a special category (credit/housing/employment → targeting restrictions)?
- [ ] Geo, ad account currency, payment method and tax verified (file 06)

**If measurement isn't set up — do not launch. This is item #0, not a "later."**

---

## STEP 0.5 — Comms strategy (product, offer, voice, taboos)
→ template: `templates/COMMS_STRATEGY_TEMPLATE.md`

- [ ] Comms strategy filled in: product in one sentence, ICP, offer (Hormozi-style), tone of voice
- [ ] Communication TABOOS spelled out (what we never say) — the agent must not break them
- [ ] Target CPA stated in the ad account's currency — every threshold is derived from it (not the US median!)

**Without a comms strategy, copy is written blind. Fill it in BEFORE creatives (step 4).**

---

## STEP 1 — Objective and optimization event
→ details: `knowledge/05` (event ladder)

- Campaign objective: for sales — Sales/Conversions (NOT Traffic/Awareness "for the sake of sales").
- Pick an optimization event you can hit at **≥50/week per ad set**.
- If purchases are <50/week → move down the event ladder: Purchase → Initiate Checkout → Add to Cart →
  View Content. Optimize for the highest frequent event, and move up to Purchase once volume grows.

---

## STEP 2 — Structure
→ details: `knowledge/01_structure.md`

- **Budget:** small budget / new account → **ABO** (control). Large budget + a proven
  winner → **CBO** (scale).
- **Ad sets per campaign:** 3-5, each adequately funded (don't split into starved ones).
- **Budget split:** ~70-80% broad/Advantage+ prospecting, 10-20% retargeting, 5-10% tests.
- **Minimum budget:** `target CPA × 50 / 7` per day, so it can learn (file 05, rule 5.4).
  One funded ad set beats five starved ones.
- Consider an **Advantage+ Sales Campaign** for e-commerce with a conversion history (file 01, 1.5).

---

## STEP 3 — Audiences
→ details: `knowledge/02_audiences.md`

- **Default: broad + Advantage+ Audiences.** Narrow interest targeting as your foundation is outdated.
- Interests/lookalike — treat them as HINTS, not hard rules (and the priority of those hints is unreliable).
- **Lookalike:** start at 2-3% for conversions, 5% for awareness; source ≥1000-5000 (buyers are best).
- **Retargeting:** windows tied to the purchase cycle (hot 3-7 days, reactivation 30-90).
- **Check overlap** between ad sets: target <15-20%, act when >25-30%.
- ⚠️ For small geos, "1M+" reach may be unreachable — compensate with a more frequent event (file 06).

---

## STEP 4 — Creatives
→ details: `knowledge/03_creatives.md` + `knowledge/07_creative_pipeline_and_existing_posts.md`

> Two flows (details in file 07):
> - **A — new creative:** generate/file → `upload_ad_image` → `create_ad_creative` → `create_ad`.
> - **B — existing post:** `create_ad_creative(object_story_id="{page_id}_{post_id}")` → `create_ad`.
>   Promotes a live IG/FB post while keeping its likes/comments (social proof).


- **How many:** start with **3-6 strong** creatives per ad set (new account), top up to 10-20 as
  budget allows. Don't dump 20 weak ones — it dilutes learning.
- **Format:** vertical 9:16 is the main one (Reels/Stories/feed). Video — reach; static with a clear
  offer — direct response; carousel — storytelling/collections.
- **Hook in the first 3 seconds.** Captions are mandatory.
- **UGC style** usually beats studio for B2C (except premium/luxury).
- **Copy:** the key message and offer in the first ~125 characters of the primary text (before "See More"). Keep the headline short.
- **Offer:** specifics + benefit + honest urgency + risk reversal. Check it against the
  anti-pattern table (file 03).
- **Advantage+ Creative:** turn it on selectively and A/B test it, NOT "everything at once" (it breaks copy/visuals).

---

## STEP 5 — Launch and the learning phase
→ details: `knowledge/04_optimization.md`

- After launch — **don't touch it for the first 3-7 days** / while in learning. You can watch, but not change.
- Don't set a cost cap at launch (it strangles delivery). Use Highest volume (lowest cost).
- The only exception for early intervention is extreme overspend (see STEP 6, hard kill).

---

## STEP 6 — Optimization (after exiting learning)
→ details: `knowledge/04_optimization.md` (threshold table)

**Kill:**
- HARD KILL: ≥3× target CPA at 0 conversions **AND** a meaningful volume of impressions (not on 3 clicks).
- SOFT KILL: ≥2× CPA at 0 conversions, no sooner than 72h.
- ⚠️ Low CTR at a normal CPA is NOT a reason to kill. CTR = a yellow flag to "refresh the creative."

**Scale:**
- Conservatively (default): +10-20% every 3-5 days (keep it <20% so you don't reset learning).
- Aggressively: only by **DUPLICATING** the ad set (not raising the budget!), on a fat winner.

**Before any "winner/loser" verdict:** ≥50 conversions or ~$500 per ad set.

**Creative fatigue:** falling CTR + rising frequency → swap the creative (not the budget). Refresh
every 7-14 days at high spend.

**Don't reset learning:** budget/bid edits <20%; don't change the event/targeting/main
creative without good reason. Make changes no more than once every 24-48h; the optimal cycle is 7-14 days.

---

## STEP 7 — Reality check
→ details: `knowledge/05`, rule 5.5

- Ads Manager numbers are modeled (partly extrapolated) and diverge from GA4/your till.
- For high-stakes decisions, reconcile against real sales (CRM/till), not Ads Manager alone.

---

## Discipline (what really separates a good media buyer from the rest)
1. Don't draw conclusions from noise (let it exit learning).
2. Don't poke the campaign every day.
3. Cut on money, not on cosmetic metrics.
4. Scale smoothly or by duplicating — don't break learning.
5. All numeric thresholds come from your own geo/baseline, not US medians.
