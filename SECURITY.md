# Security

This project works with ad accounts and money. Treat your credentials and business
data with care. A few rules keep you safe.

## Never commit secrets

The `.gitignore` already excludes the common offenders, but the rule comes first:

- **Never commit `.env`** or any file holding an API key / token
  (`OPENAI_API_KEY`, `META_ACCESS_TOKEN`, `FAL_KEY`, `IMGBB_API_KEY`, R2 keys).
  All keys are read from environment variables — never hardcode them in code.
- **Never commit Ads Manager exports** (`*.csv` you pulled from your real account).
  They contain account IDs, spend, and performance data. `.gitignore` blocks `*.csv`
  except the synthetic files in `analytics/sample_data/`.
- **Never commit a filled-in comms strategy.** `templates/COMMS_STRATEGY_TEMPLATE.md`
  is a blank template. A completed `comms-*.md` may contain real budgets, target CPA,
  audience definitions, and client business info — `.gitignore` excludes `comms-*.md`.

## Before you push

- Run a secret scanner on your working tree, e.g.
  [`gitleaks detect`](https://github.com/gitleaks/gitleaks) — it catches keys you
  may have pasted into a file by accident.
- Confirm `git status` shows no `.env`, no real `*.csv` export, no `comms-*.md`.
- If you forked/cloned and added your own keys, double-check they live only in env
  vars or a local `.env` that is git-ignored.

## A note on the demo data

Everything in `analytics/sample_data/` is **synthetic** — made-up ad IDs and numbers
to let you try the scripts without a token. It contains no real account data.

## Reporting a vulnerability

If you find a security issue in this project, please open a
[GitHub issue](../../issues) or email nadezhda.pak.13@gmail.com. Avoid posting real
tokens or account data in the report.
