# 08 — Meta Ads benchmarks: US and Europe (2025)

> Real CPM/CPC/CTR/CPA reference points, so you can set target CPA without flying blind.
> Gathered via multi-source research with every number verified (single-source filtered out).
> Data ~2025. Meta prices keep rising — refresh every six months.
>
> ⚠️ KEY POINT: a benchmark ≠ a target. It's a reference for "what's normal." Your real target is
> your own historical baseline. The benchmark is only there to tell you what order of magnitude you're in.

---

## US — reliable data exists

### Lead-gen campaigns (WordStream/LocaliQ, 2025, US only) — [RELIABLE, 3-0]
Source: 726 US lead campaigns, April 2024 – June 2025. All numbers are **medians**.

| Metric | Median | YoY trend |
|---|---|---|
| CPC | **$1.92** | ↑ from $1.88 |
| CTR | **2.59%** | ≈ flat (was 2.58%) |
| CPL (cost per lead) | **$27.66** | ↑ ~21% (was $22.87) |
| Conversion rate | 7.72% | ↓ from 8.67% |

The spread across industries is wide: CPC from $0.74 (Restaurants) to $9.78 (Dentists);
CPL from $3.16 (Restaurants) to $76.71 (Dentists). For comparison: Google's CPL is ~$70 —
Facebook is cheaper per lead. ⚠️ The mix skews toward local services (dentists, lawyers) —
which inflates the top of the range relative to typical B2C e-commerce.

### Traffic campaigns (WordStream/LocaliQ, 2025, US only) — [RELIABLE, 3-0]
Source: 554 US traffic campaigns. Medians.

| Metric | Median | Trend |
|---|---|---|
| CPC | **$0.70** | ↓ 6.7% (was $0.77) |
| CTR | **1.71%** | ↑ (was 1.57%) |

CPC by industry: from $0.34 (Shopping/Gifts) to $1.22 (Finance). ⚠️ Note:
traffic-CPC ($0.70) is ~2.7× cheaper than lead-CPC ($1.92) — **the campaign objective heavily
influences the benchmark**. Compare against the right objective.

### E-commerce / DTC (Triple Whale, all of 2025, ~35,000 brands) — [RELIABLE, 3-0 on trend]
The best source for the conversion side of e-commerce. Medians.

| Metric | Median | YoY trend |
|---|---|---|
| CPM | **$14.19** | ↑ ~20% (was $11.82) |
| CTR | **2.19%** | — |
| CVR (conversion rate) | **1.6%** | — |
| CPA | **$38.19** | — |
| ROAS | **1.86** | — |

⚠️ Triple Whale does NOT publish CPC (for CPC — WordStream above). The panel skews toward DTC and the US,
but is aggregated globally with no geo split. The ~20% CPM rise is independently confirmed
(RightSideUp Q1 2025: Meta CPM +19% YoY). Some secondary summaries give CPM $13.48 —
that's a different slice of the same table, same order of magnitude.

### Retail/E-commerce additional slice (TwoMinuteReports, 2025) — [MEDIUM, 2-1]
Medians: CPC **$0.72**, CTR **2.30%**, ROAS **1.75x**. ⚠️ A reporting vendor, not a benchmark
authority, with a self-selected sample. ROAS 1.75 is noticeably BELOW typical e-commerce
(2-4x) — treat it as a directional cross-check, not as the norm.

---

## Europe — there are NO reliable country-level benchmarks

> This is an honest research result, not a gap in the gathering. Say so to the client.

- **Both authoritative sources (WordStream and Triple Whale) provide NO geo split.**
  WordStream is US-only by design. Triple Whale aggregates globally with no split.
- **All the per-country European CPM/CPC tables found (Lebesgue, Trendtrack,
  BusinessOfApps, Vaizle) were DISPROVEN** on inspection: single-source, undisclosed methodology,
  internal contradictions. They can't be used as norms.
- The only thing that "survived" inspection was one vendor number with no methodology
  (Lebesgue: US CPM $16.08 as the most expensive Western market, 2026). And even that should be treated
  as the lower-middle point of a wide **$13–$23** range, not a target. Other sources for the same
  period give US CPM from $13.48 (Triple Whale) to $23 (AdAmigo) — the spread is enormous.

### What to do about Europe (practical takeaway)
1. **The US numbers above — as a thinking framework, not an absolute for the EU.** The order of magnitude is the same,
   but absolute values for different EU countries are not reliably known.
2. **Western Europe (UK/DE/FR/NL) is closer to the US** in cost (but usually cheaper).
   **Southern/Eastern (ES/IT/PL) is noticeably cheaper.** That's a direction, not numbers.
3. **The only correct EU target is your own first-party baseline.** Run a
   small test budget, gather your own CPM/CPC/CPA for the specific country over 1-2 weeks —
   that becomes your reference. See file 06 (the geo adjustment).

---

## How to use this with the analytics scripts

The script `analytics/creative_analysis.py` requires `--target-cpa` explicitly. Where to get it:

| Your case | Where to get the starting reference |
|---|---|
| US lead-gen | CPL median $27.66, adjust for your industry (WordStream table) |
| US e-commerce | CPA median $38.19 (Triple Whale) |
| Europe | take the US number as a CEILING, gather the real CPA via a test launch (file 06) |
| Any non-US | never take a US number as is — it's a ceiling, not a target |

⚠️ All these numbers are **medians from specific reports of a specific year**, not eternal truth.
Don't trust the false precision of "$38.19" to the cent — it's the center of a distribution; your real
CPA depends on niche, offer, geo and season.

---

## Sources (verified)
- WordStream/LocaliQ Facebook Ads Benchmarks 2025 — https://www.wordstream.com/blog/facebook-ads-benchmarks-2025 [RELIABLE]
- Triple Whale Facebook Ads Benchmarks (2025) — https://www.triplewhale.com/blog/facebook-ads-benchmarks [RELIABLE]
- Search Engine Land (WordStream confirmation) — https://searchengineland.com/facebook-ad-costs-jump-beat-google-461690 [confirmation]
- TwoMinuteReports (2025) — https://twominutereports.com/blog/facebook-ads-benchmarks [MEDIUM, single source]
- Lebesgue CPM by country (2026) — only as an illustration of the spread, country numbers DISPROVEN [DO NOT USE as a norm]
