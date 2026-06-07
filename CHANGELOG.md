# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-06-07

First public release.

### Added

- **Knowledge base (knowledge/):** 8 files of rules for setting up and optimizing Meta Ads — campaign structure, audiences, creatives, threshold-based optimization, pixel and cold start, geo/currency, the creative pipeline, and US/Europe benchmarks. Every rule carries a reliability tag ([OFFICIAL META] / [AGENCY CONSENSUS] / [DISPUTED] / [UNVERIFIED]).
- **Communication strategy template (templates/):** COMMS_STRATEGY_TEMPLATE.md — a starting point for planning ad campaigns.
- **Post-hoc analytics scripts (analytics/):**
  - `creative_analysis.py` — analyzes creatives/ad sets with KILL/SCALE/WAIT/KEEP decisions based on the thresholds from the knowledge base.
  - `significance_test.py` — a two-proportion z-test for A/B comparisons without scipy.
  - `fatigue_curve.py` — a creative fatigue detector working off daily series (CTR/frequency/CPM trend).
  - `meta_client.py` — a thin client for the Meta Marketing API with pagination, retry, and action_type alias mapping.
  - Sample data in `sample_data/` so it works without a token.
- **Creative generation and hosting scripts (creatives/):**
  - `generate_creative.py` — generates ad images via the OpenAI Images API (gpt-image-1).
  - `host_image.py` — uploads images to fal / imgbb / Cloudflare R2 and returns a public URL.
  - `to_data_url.py` — converts a local image to a data URL (for APIs that don't accept files).
- **Infrastructure:**
  - Unit tests (tests/) for all analytics scripts — 98 tests with no network access.
  - `pyproject.toml` with pytest configuration and project metadata.
  - `ARCHITECTURE.md` — an overview of the project structure.
  - `AGENT_INSTRUCTIONS.md` — instructions for the AI agent on how to use the knowledge base.
  - `LAUNCH_PLAYBOOK.md` — a step-by-step playbook for launching ads.
  - `CONTRIBUTING.md` — how to clone, test, and propose changes.
