# 01 — Campaign structure (Meta Ads, B2C + traffic, 2025-2026)

> Terminology updated to match the current Ads Manager:
> CBO → **Advantage campaign budget**; ASC / Advantage+ Shopping → **Advantage+ Sales Campaign**.

---

## CBO vs ABO (budget at the campaign level vs at the ad set level)

### Rule 1.1: Core mechanics
- **Gist:** CBO (Advantage campaign budget) is a budget set at the CAMPAIGN level, with the algorithm splitting it across ad sets on its own. ABO is a budget set manually on EACH ad set, and each one spends exactly that amount.
- **Reliability:** [OFFICIAL META]
- **Source:** https://www.facebook.com/business/help/153514848493595

### Rule 1.2: ABO for testing, CBO for scaling
- **Gist:** ABO forces an even split → great for a controlled test of audiences/creatives. CBO is better for scaling proven winners.
- **Reliability:** [AGENCY CONSENSUS]

### Rule 1.3: The risk of CBO on small budgets
- **Gist:** On a small daily budget, CBO starves the slow ad sets — it quickly dumps the money into one ad set while the others never exit learning. On small budgets, ABO gives you control.
- **Reliability:** [AGENCY CONSENSUS]

### Rule 1.4: Don't pick one forever
- **Gist:** On small budgets — ABO (control). On large budgets with a proven winner — CBO (scale). A Lebesgue measurement showed ABO at 94% vs CBO at 81% ROAS on prospecting — but this is [DISPUTED], a single source; treat it as a case study.
- **Reliability:** [DISPUTED]

---

## Advantage+ Sales Campaign (formerly ASC)

### Rule 1.5: What it is and who it's for
- **Gist:** A fully AI-driven campaign: Meta optimizes creatives, targeting, placements, and budget itself. It merges prospecting and retargeting. The primary B2C use case is e-commerce / direct sales with a pixel and a conversion history.
- **Meta's efficiency claim:** ~**17% lower cost per conversion** vs manual (this is Meta's own marketing figure; the real-world effect varies — do NOT cite it as a guarantee). ⚠️ An older version of the knowledge base quoted "-9%" — that number is fabricated, Meta has never published it.
- **Reliability:** [OFFICIAL META] for the mechanics; the savings figure is Meta self-promotion.
- **Source:** https://www.facebook.com/business/ads/meta-advantage-plus/sales-campaigns

### Rule 1.6: Controls are limited
- **Gist:** The only hard constraints you can set are: minimum age, gender, geo, languages, and excluded custom audiences. Interests / lookalike / custom audiences act as "hints," and the algorithm may go beyond them.
- **Reliability:** [OFFICIAL META]

### Rule 1.7: Budget and monitoring for Advantage+ Sales
- **Gist:** You need a budget for ~50 conversions/week and about a month to stabilize. Load a diverse set of creatives from the start (begin with 10-20 strong ones). Don't watch ROAS alone (it credits itself with warm buyers you'd have gotten anyway) — track CPM, frequency, and CPA.
- **Reliability:** [AGENCY CONSENSUS]

---

## How many campaigns / ad sets / ads

### Rule 1.8: How many ad sets per campaign
- **Gist:** There's no hard limit. Consensus: **3-5** well-funded ad sets per campaign. Enough for comparison without spreading the budget too thin.
- **Reliability:** [AGENCY CONSENSUS]

### Rule 1.9: How many creatives per ad set (ALIGNED with file 03)
- **Gist:** Meta best practice is **10-20 creatives per AD SET** with 1-3 ad sets. A realistic agency starting point for a new account / small budget is **3-6** strong creatives, adding more as budget grows.
- ⚠️ This is per AD SET, not per campaign. The old "max 6 ads per ad set" was a recommendation, not a limit, and it has loosened with Advantage+.
- **Reliability:** [OFFICIAL META] (10-20) + [AGENCY CONSENSUS] (3-6 to start)

### Rule 1.10: The consolidation trend (the big shift)
- **Gist:** Fewer campaigns/ad sets with broader audiences work BETTER than many narrow ones. This is the first item in Meta's official "Performance 5" framework (Account Simplification). The goal is for each ad set to reach ~50 conversions/week.
- **Reliability:** [OFFICIAL META]
- **Source:** Meta Blueprint Performance 5

---

## Budgets and the Learning Phase

### Rule 1.11: 50 events per week — the threshold to exit learning
- **Gist:** An ad set needs ~**50 optimization events per WEEK** (per AD SET, not per campaign) to exit the learning phase. Until then, results are unstable. This is a benchmark for the minimum signal, not a magic threshold.
- ⚠️ If you physically can't hit that many conversions — see `05_pixel_and_coldstart.md`, the event ladder.
- **Reliability:** [OFFICIAL META]
- **Source:** https://www.facebook.com/business/help/112167992830700

### Rule 1.12: Two DIFFERENT budget formulas (don't confuse them)
- **Weekly minimum to exit learning:** `target CPA × 50 events`. Example: CPA $30 → $1,500/week (~$214/day).
- **Daily headroom for stable optimization (a separate recommendation):** `~10× target CPA/day`. Example: CPA $30 → ~$300/day.
- ⚠️ These are TWO different things, not two versions of one rule. The first is the minimum needed to learn at all. The second is comfortable headroom.
- **Reliability:** [AGENCY CONSENSUS], derived from the official 50/week rule.

### Rule 1.13: What RESETS the learning phase
- **Resets it:** changing budget/bid by **>~20%**, swapping the creative, changing the audience, changing the optimization event, changing the bid strategy.
- **Does NOT reset it:** renaming, a minor text edit, a budget change of **<20%**.
- ⚠️ This rule ties directly into scaling (see file 04): raising the budget >20% at once = a reset. That's why aggressive scaling is done by duplicating the ad set rather than ramping it up.
- **Reliability:** [OFFICIAL META] (the fact of the reset) + [AGENCY CONSENSUS] (the 20% threshold)

---

## Funnel structure

### Rule 1.14: A separate retargeting layer is no longer mandatory
- **Gist:** With broad targeting (Advantage+ Audience), remarketing happens "on its own" — the algorithm first works the pixel/history, then expands. A dedicated retargeting ad set is often unnecessary. BUT there's a camp that keeps 10-20% of budget on explicit retargeting — it depends on the size of your warm base.
- **Reliability:** [AGENCY CONSENSUS], see the open question.

### Rule 1.15: A reference point for the budget split
- **Gist:** ~**70-80%** on broad/Advantage+ prospecting, ~**10-20%** on retargeting, ~**5-10%** on interest/lookalike tests. A reference point, not a law.
- **Reliability:** [AGENCY CONSENSUS]

---

## Common structural mistakes

### Rule 1.16: Audience overlap (self-cannibalization)
- **Gist:** Overlapping audiences compete in the auction → CPM rises, optimization slows. Check with the Audience Overlap tool (works for audiences of 10k+).
- **Threshold (ALIGNED with file 02):** target overlap **<15-20%**; act when **>25-30%**.
- **Reliability:** [OFFICIAL META] (the tool) + [AGENCY CONSENSUS] (the thresholds)

### Rule 1.17: Budget fragmentation
- **Gist:** Many underfunded ad sets → none of them reaches 50 conv/week → the algorithm starves for signals. The fix is structural: consolidate.
- **Reliability:** [AGENCY CONSENSUS]

---

## CONTRADICTIONS AND OPEN QUESTIONS

1. **CBO vs ABO on prospecting.** "CBO for scaling" (the majority view) vs the Lebesgue measurement (ABO had higher ROAS). It depends on budget: small → ABO, large → CBO.
2. **Whether you need a separate retargeting layer.** "Not needed with broad" vs "keep 10-20%." Depends on the size of your warm base.

## OUTDATED — DO NOT APPLY

- Splitting the account into many narrow interest-based ad sets (contradicts Performance 5).
- The hard "6 ads per ad set" limit (it was a recommendation and has loosened).
- A mandatory multi-stage TOF/MOF/BOF funnel as separate campaigns (overkill for B2C).
- Narrow interest targeting as the foundation (interests are now hints — see file 02).
- "-9% cost per conversion for Advantage+ Sales" — a fabricated number, Meta has never published it.
