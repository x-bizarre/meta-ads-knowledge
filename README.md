# Meta Ads AI Agent — knowledge base + analytics for launching ads

A ready-to-use "brain" for an AI agent (Claude, Cursor, any LLM with MCP) that launches and
runs ads on Meta (Facebook/Instagram) like a seasoned performance marketer — not like a beginner
making up numbers.

Inside:
- **Expert knowledge base** — thresholds, benchmarks, and decision discipline drawn from official
  Meta documentation and the playbooks of strong agencies. Every rule is tagged with a reliability level.
- **Step-by-step playbook** for launching a campaign from scratch (steps 0-7).
- **Comms strategy template** — fill it in for your product, and the agent writes in your voice.
- **Python post-hoc analytics scripts** — statistical significance, creative fatigue, kill/scale decisions.

> This is the "brain" (the knowledge). The "hands" (pressing buttons in your Meta ad account) are
> any Meta Ads MCP server. Tested with a fork of `pipeboard-meta-ads-mcp`. The knowledge base does
> not depend on any specific server.

---

## Why you need this

An LLM on its own hallucinates about ads: it invents CPA figures, recommends outdated narrow
targeting, and kills ad sets after three clicks. This knowledge base gives it **discipline and
proven numbers**, and the scripts give it **precise math** instead of eyeballing.

The core principles it instills in the agent:
- don't draw conclusions from noise (let the ad set exit the learning phase);
- cut based on money, not cosmetics (a low CTR is not a reason to kill);
- scale gradually or by duplication, without breaking learning;
- compute thresholds from your own geo, not from US medians;
- don't present Meta's marketing numbers as a guarantee.

---

## Quick start (5 minutes)

### 0. First, verify the analytics works — on demo data, no account needed
Run the scripts on the bundled sample CSVs. They read numbers from a file, not from the Meta API,
so no token, key, or money is involved — it just proves the tool computes correctly:
```bash
pip install -r requirements.txt
python analytics/creative_analysis.py --csv analytics/sample_data/sample_insights.csv --target-cpa 8
python analytics/fatigue_curve.py --csv analytics/sample_data/sample_daily.csv
python analytics/significance_test.py --a 12 380 --b 7 410
```
You'll see kill/scale decisions, the fatigue detector, and a significance test on demo data.

### 1. Connect the knowledge to your agent
Copy the folder and point the agent to read `AGENT_INSTRUCTIONS.md` first. In Claude Code/Cursor —
place it next to your project or build a skill that pulls in these files.

### 2. Fill in the comms strategy for your product
```bash
cp templates/COMMS_STRATEGY_TEMPLATE.md comms-myproduct.md
# open it and fill in: product, ICP, offer, tone of voice, TABOOS, target CPA
```

### 3. Connect a Meta Ads MCP server (the "hands")
Any server that exposes the tools `create_campaign / create_adset / create_ad_creative /
create_ad / update_* / get_insights`. This is what the agent actually uses to edit the ad account.

### 4. Creative generation (optional, "turnkey")
```bash
cd creatives
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."         # a simple API key, not OAuth
python generate_creative.py --prompt "UGC photo ..." --ratio 9:16 --out creative.png
# then: upload_ad_image(file="creative.png") → create_ad_creative → create_ad
```

### 5. For post-hoc analytics — install the scripts
```bash
cd analytics
pip install -r requirements.txt
export META_ACCESS_TOKEN="EAAB..."     # a long-lived token from your ad account
python creative_analysis.py --account act_XXX --target-cpa 8
```

---

## Project structure

```
AGENT_INSTRUCTIONS.md   ← the agent reads this FIRST: discipline and operating rules
LAUNCH_PLAYBOOK.md      ← step-by-step campaign launch (steps 0-7)
ARCHITECTURE.md         ← how the base is built, reliability tags, how to clone it per project

knowledge/              ← deep knowledge base by stage
  01_structure.md         campaign structure (CBO/ABO, Advantage+)
  02_audiences.md         audiences (broad, lookalike, retargeting)
  03_creatives.md         creatives and offers (formats, anti-patterns)
  04_optimization.md      kill/scale thresholds, benchmarks
  05_pixel_and_coldstart.md  Pixel/CAPI, event ladder, cold start
  06_geo_currency.md      adjustments for non-US geo, currency, taxes
  07_creative_pipeline_and_existing_posts.md  ← two flows: new creative AND boosting an existing post
  08_benchmarks_us_europe.md  ← real CPM/CPC/CTR/CPA for the US (Europe — why there's no data)

templates/
  COMMS_STRATEGY_TEMPLATE.md  ← comms strategy template for your product

creatives/              ← turnkey creative generation and upload
  generate_creative.py    OpenAI gpt-image-1 → image file
  to_data_url.py          small image → data-URL for upload_ad_image(file=)
  host_image.py           large image → hosting (fal/imgbb/r2) → image_url=
  README.md               how to use it

analytics/              ← Python post-hoc analytics scripts
  meta_client.py          API client (honest CPA/ROAS from raw conversions)
  creative_analysis.py    kill/scale decisions for each ad
  significance_test.py    A/B statistical significance (no scipy)
  fatigue_curve.py        creative fatigue detector by day
  README.md               how to use the scripts
```

---

## Two launch flows (important)

The agent handles both (details in `knowledge/07`):
- **A — new creative:** generation/file → `upload_ad_image` → `create_ad_creative` → `create_ad`.
- **B — boosting an existing post:** `create_ad_creative(object_story_id="{page_id}_{post_id}")` →
  promotes a live IG/FB post while preserving its likes/comments (social proof).

---

## Reliability tags

Every rule in the base is tagged with how much you can trust it:
- **[OFFICIAL META]** — from official documentation/Blueprint. The most reliable.
- **[AGENCY CONSENSUS]** — working practice from strong agencies.
- **[DISPUTED]** — experts disagree; both camps are presented.
- **[UNVERIFIED]** — a single source with no confirmation; don't use as a benchmark.

⚠️ All benchmarks (CPM/CTR/CPA) are US/global medians. For non-US markets, divide them down — see
`knowledge/06_geo_currency.md`.

---

## What is DELIBERATELY not here

- **Vector database / RAG.** At this volume, markdown in the context window works better and clones
  per project in seconds.
- **Autopilot.** The agent proposes decisions — a human approves them. That's by design: ads = money.
- **Your secrets.** Tokens live only in environment variables, never in code. See `.gitignore`.

---

## Contributing

Contributions are welcome. Posting fixes, new knowledge, or extra providers — all via Pull Request.
See `CONTRIBUTING.md` for how to clone, install, run the tests, and propose changes. No one can push
to this repository directly: outside changes come as Pull Requests that the maintainer reviews and merges.

## Support

- **Found a bug or have a question?** Open an issue: [GitHub Issues](../../issues)
- **Direct contact:** nadezhda.pak.13@gmail.com

---

## License

MIT — take it, deploy it, change it. See `LICENSE`.

Knowledge current as of ~May 2026. Meta changes its API and rules often — check the official docs
before launching, and update the thresholds against your own baseline.
