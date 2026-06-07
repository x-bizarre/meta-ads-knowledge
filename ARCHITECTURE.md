# Meta Ads — Knowledge base for an advertising agent

A universal expert knowledge base for advertising on Meta (Facebook/Instagram).
Compiled from official Meta documentation and the playbooks of strong agencies,
and run through a critic-agent pass (checking for invented numbers, outdated info, and dangerous advice).

Focus: **B2C sales + traffic/reach**. Current as of May 2026.

---

## How to use this

1. **`AGENT_INSTRUCTIONS.md`** — a short instruction set for the advertising agent. This is what
   gets connected to the agent first. Inside: discipline rules, which MCP to use for editing, and
   links to the other files.

2. **`LAUNCH_PLAYBOOK.md`** — the main document. A step-by-step plan for launching a B2C campaign
   from scratch: from pixel to scaling. The agent works through it like a checklist.

3. **`knowledge/`** — a deep knowledge base by stage (a reference the agent dips into for details):
   - `01_structure.md` — campaign structure (CBO/ABO, Advantage+, how much of what)
   - `02_audiences.md` — audiences and targeting (broad, lookalike, retargeting)
   - `03_creatives.md` — creatives and offers (formats, tests, anti-patterns)
   - `04_optimization.md` — optimization after launch (kill/scale thresholds, benchmarks)
   - `05_pixel_and_coldstart.md` — Pixel/CAPI + cold start for a new account
   - `06_geo_currency.md` — geo/currency/taxes (adjustments for non-US markets)
   - `07_creative_pipeline_and_existing_posts.md` — two launch flows: a new creative
     (generation→upload→ad) AND boosting an existing post (`object_story_id`)
   - `08_benchmarks_us_europe.md` — real CPM/CPC/CTR/CPA for the US (2025), and why there are no
     reliable country-level benchmarks for Europe (collect first-party)

4. **`templates/`** — boilerplate you fill in for your product:
   - `COMMS_STRATEGY_TEMPLATE.md` — comms strategy: product description, ICP, offer, tone of
     voice, communication taboos. The agent reads it before writing any copy.

5. **`analytics/`** — Python post-hoc analytics scripts (precise analysis of results):
   - `creative_analysis.py` — kill/scale decisions for each creative based on the base's thresholds
   - `significance_test.py` — A/B statistical significance (rule 4.5, no scipy)
   - `fatigue_curve.py` — creative fatigue detector over a daily series
   - `meta_client.py` — API client (reads insights, computes honest CPA/ROAS)
   - details in `analytics/README.md`

6. **`creatives/`** — image generation (OpenAI) and upload to Meta (data-URL / hosting).

---

## How to read the reliability tags

Every rule is tagged with how much you can trust it:

- **[OFFICIAL META]** — from official Meta documentation/Blueprint. The most reliable.
- **[AGENCY CONSENSUS]** — several strong agencies agree. Working practice, but not law.
- **[DISPUTED]** — experts disagree. Both camps are presented; the human chooses.
- **[UNVERIFIED]** — the number appears in a single source with no confirmation. Don't use as a benchmark.

**Important:** all benchmarks (CPM/CTR/CPA) are US/global medians. For non-US geos
(non-US markets) the real figures are several times lower. See `knowledge/06_geo_currency.md`.

---

## How to clone it per project

This base is universal. To adapt it to a specific project (your own product or a client):
1. Copy the whole folder: `cp -r meta-ads-knowledge meta-ads-knowledge-myproduct`
2. In the copy, edit only the niche-specific thresholds (target CPA, budgets, geo) in `LAUNCH_PLAYBOOK.md`
   and `06_geo_currency.md`. Don't touch the knowledge itself (`knowledge/01-05`) — it's universal.

---

## What is DELIBERATELY not here

- **Vector database / RAG.** At the current volume of knowledge, plain markdown files work better:
  they fit into the agent's context in full, with no loss from "pulled the wrong chunks," and they
  clone per project in seconds. A vector store only becomes necessary if the knowledge grows to
  literally hundreds of pages.
- **Autopilot.** The agent proposes decisions, a human approves. That's by design.
