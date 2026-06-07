# 04 — Post-launch optimization (Meta Ads, B2C + traffic, 2025-2026)

> Benchmarks are a REFERENCE POINT. They depend heavily on niche/geo/season. For non-US geos, US
> figures are inflated by multiples — see file 06. Always compare against your own historical baseline.

---

### Rule 4.1: Learning phase = ~50 events over 7 days per ad set
- **Gist:** After launch or a major edit, an ad set is in the learning phase — the algorithm is unstable. "Exit" happens once it has accumulated ~50 conversions and you haven't made any major edits. Per AD SET, not per campaign.
- ⚠️ If you physically can't hit 50/week — do NOT wait forever; step down the event ladder (see file 05).
- **Reliability:** [OFFICIAL META]

### Rule 4.2: "Learning Limited" — a structural problem, not "wait it out"
- **Gist:** The status = a forecast that the ad set won't reach 50/week. It's fixed by changing the structure: raise the budget, broaden the audience, merge ad sets, choose a more frequent optimization event.
- **Reliability:** [OFFICIAL META]

### Rule 4.3: Don't draw conclusions from noise (WINDOW HIERARCHY — aligned)
- **Gist:** While an ad set is in learning, CPA/ROAS are distorted. The hierarchy:
  1. **Don't touch (just watch):** the first 3-7 days / while in learning. The only exception is extreme overspend (see 4.4, hard kill).
  2. **Evaluate the bundle:** after exiting learning OR 5-7 days.
  3. **Change anything:** no more than once every 24-48h; the optimal edit cycle is once every 7-14 days.
- **Reliability:** [AGENCY CONSENSUS]

### Rule 4.4: When to KILL — thresholds (CORRECTED by the critic)
- **HARD KILL (can be early), but ONLY with sufficient impression volume:** spent ≥**3× target CPA with 0 conversions** AND accumulated a meaningful number of clicks/impressions (not 3-4 clicks). Without volume, this is noise, not a reason to kill.
- **SOFT KILL (after calibration):** ≥2× target CPA with 0 conv, OR 1.5× CPA with 1 conv — but no sooner than **72 hours** and preferably after exiting learning.
- ⚠️ **CTR < 0.5% is NOT a reason to kill on its own.** A low CTR with a normal CPA = the ad set is converting the people who clicked. A CTR drop = a yellow flag to "review the creative," not a command to kill. The real kill criterion is MONEY (CPA/spend), not clickability.
- **Reliability:** [AGENCY CONSENSUS] — the 2×/3× multipliers are practice, not a Meta standard.

### Rule 4.5: Statistical significance
- **A/B tests [OFFICIAL META]:** minimum ~100 events before evaluating; confidence ≥65% = winner (a low bar!), ≥90% for lift/holdout. Duration 2 weeks, max 30 days.
- **For scaling decisions [AGENCY CONSENSUS]:** ≥50 conversions OR ~$500 spend per ad set; for a reliable read on a variant — ~100 conversions per variation.
- ⚠️ "Meta declared a winner at 65%" ≠ "statistically reliable." For expensive decisions, wait for more.
- **Reliability:** [OFFICIAL META] + [AGENCY CONSENSUS]

### Rule 4.6: Scaling — the CONSERVATIVE camp (the default)
- **Gist:** Raise the budget gradually so you don't knock the ad set out of learning.
- **Threshold:** **+10-20% every 3-5 days** (industry standard). Stay under 20% at a time so you don't reset learning (see file 01, Rule 1.13).
- **Reliability:** [AGENCY CONSENSUS]

### Rule 4.7: Scaling — the AGGRESSIVE camp (CORRECTED by the critic)
- ⚠️ **IMPORTANT:** raising a working ad set's budget directly by +30-50% **resets the learning phase** (the reset threshold is ~20%). This is NOT a safe approach.
- **The safe way to scale aggressively:** **DUPLICATE** the ad set (the new ad set takes on the risk of fresh learning; you leave the proven winner untouched). On the duplicate you can set a larger budget right away.
- Only on a "fat" winner (≫50 conv/week), with close monitoring and a readiness to roll back.
- **Reliability:** [DISPUTED] — dangerous on a thin signal.

### Rule 4.8: Horizontal vs Vertical scaling
- **Vertical:** you grow the budget of the same winner (+20%/~3 days). Fast, but you risk hitting the audience ceiling.
- **Horizontal:** you duplicate the bundle onto new audiences/creatives, changing one variable at a time. Safer for small budgets. With excessive fragmentation it dilutes the signal.
- **Often:** go horizontal first (find the audiences that work), then vertical (pour budget into the best).
- **Reliability:** [AGENCY CONSENSUS]

### Rule 4.9: What counts as a "major" edit (resets learning)
- **Resets it:** changing the optimization event, a substantial targeting change, a budget/bid shift of **>~20%**, replacing the main creative.
- **Does NOT reset it:** minor text edits, modest budget adjustments (<20%).
- **Reliability:** [OFFICIAL META] + [AGENCY CONSENSUS] (20%)

### Rule 4.10: Creative fatigue → refresh the creative
- **Gist:** A falling CTR / a jump in CPC-CPM alongside rising frequency = fatigue. Fix it by swapping the creative, not the budget.
- **Frequency:** Meta — brand lift plateaus after ≈2, BUT that's not a ceiling (there are working accounts with frequency 10-16, depending on audience size and purchase cycle). Decide on CTR/CPC/CPA.
- **Refresh:** in high-spend accounts (>$100/day), fatigue sets in within 4-7 days; refresh the creative every 7-14 days or when metrics drop.
- **Reliability:** [OFFICIAL META] (plateau ≈2) + [AGENCY CONSENSUS] (cycles)

### Rule 4.11: B2C benchmarks (a REFERENCE POINT, not a norm — CORRECTED by the critic)
- ⚠️ These are US/global medians. **For non-US geos the real figures are lower by multiples** — see file 06. Apply only with an adjustment for your niche/geo/year.
- **CPM:** ~$13.48 — this is the **global average across ALL industries 2025** (WordStream/Triple Whale), NOT B2C-specific.
- **CTR:** global average ~0.90-2.2% (depends heavily on niche); lead gen ~2.5%.
- **CPA:** median ~$38 (all industries, US).
- ⚠️ Don't believe the false precision of "$38.17" / "1.71%" — those are medians from specific reports of a specific year, not an absolute.
- **Reliability:** [AGENCY CONSENSUS] — aggregated data.

### Rule 4.12: Cost cap — NOT at the start (CORRECTED by the critic)
- ⚠️ A cost cap set close to target CPA (e.g., 1.2×) on a new account with no conversion history **chokes delivery** — Meta can't find conversions in the narrow window and simply doesn't spend.
- **The right way:** at cold start — highest volume (lowest cost) with NO cap. Introduce a cost cap only AFTER exiting learning and reaching a stable CPA, as a late-stage optimization. Then ~1.2× target CPA is a reasonable reference point.
- **Reliability:** [AGENCY CONSENSUS]

---

## DECISION THRESHOLDS (quick table)

| Decision | Trigger | When | Reliability |
|---|---|---|---|
| WAIT (don't touch) | In learning OR <50 conv/7d OR <3-5 days | Metrics are noisy | [OFFICIAL+CONSENSUS] |
| HARD KILL | ≥3× CPA with 0 conv **AND** meaningful impression volume | Even early, but not on 3 clicks | [AGENCY CONSENSUS] |
| SOFT KILL | ≥2× CPA with 0 conv; no sooner than 72h | After calibration | [AGENCY CONSENSUS] |
| Don't kill on CTR | low CTR with a normal CPA = keep it | — | [corrected] |
| Scale conservatively | winner is stable → +10-20% / 3-5 days | The baseline mode | [AGENCY CONSENSUS] |
| Scale aggressively | DUPLICATE the ad set (don't ramp it up!) when ≫50 conv/week | Only on a fat signal | [DISPUTED] |
| Data threshold for a verdict | A/B ≥100 events ≥65%; scale ≥50 conv / $500 | Before "winner/loser" | [OFFICIAL+CONSENSUS] |
| Refresh the creative | falling CTR + rising frequency | On fatigue | [AGENCY CONSENSUS] |
| Don't reset learning | budget/bid edits <20%; don't change the event/targeting/creative | When making tweaks | [OFFICIAL+CONSENSUS] |

---

## CONTRADICTIONS AND OPEN QUESTIONS

- **Scaling (the main one):** conservative (+10-20%/3-5 days directly) vs aggressive (+30-50% ONLY via a duplicate). The default is conservative. Raising directly by >20% resets learning.
- **Frequency ceiling:** Meta ≈2 plateau vs practice 10-16. There's no universal number.
- **A/B confidence:** Meta's "winner" at 65% is a low bar; for expensive decisions, wait for more.
- **The rumor "10 conv/3 days instead of 50/7"** — [UNVERIFIED], do NOT use it as a setting. The official reference point is 50/week.

## OUTDATED — DO NOT APPLY

- "Duplicate the ad set and double the budget to exit learning faster" — a relic of the manual era, fragments the signal.
- Hard ad-set budgets as a guarantee — the system can pull up to ~20% between ad sets.
- Daily micro-management (edits every day) — resets learning.
- Catching a "winner" by day 2-3 — on noise.
- Old pre-COVID benchmarks.
