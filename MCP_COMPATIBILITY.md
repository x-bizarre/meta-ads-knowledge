# MCP compatibility

This knowledge base is the **brain**. To actually launch and edit ads you also need an
**MCP server** — the **hands** that call the Meta Marketing API. This file tells you what
your MCP server must expose for the full workflow to work.

This project is server-agnostic: any MCP server that provides the tools below will work.

---

## Required tool contract

Check your MCP server against this list. If it has these tools (names may differ slightly,
but the capability must exist), the full launch + optimize + analyze loop works.

### Read (needed for analytics & decisions)
| Capability | Used for |
|---|---|
| `get_ad_accounts` | find your account ID |
| `get_account_pages` | the Page behind a creative |
| `get_insights` | performance data → all kill/scale decisions |
| `get_campaigns` / `get_adsets` / `get_ads` | see what already exists |

### Create (needed to launch from scratch — flow A in `knowledge/07`)
| Capability | Used for |
|---|---|
| `upload_ad_image` | push a creative image (accepts a URL or base64/data-URL) |
| `create_ad_creative` | assemble image + copy + headline + CTA + link |
| `create_campaign` | the campaign (objective, budget) |
| `create_adset` | targeting, optimization goal, budget |
| `create_ad` | the ad itself, from a creative |

### Edit (needed to optimize after launch — the core value of this project)
| Capability | Used for |
|---|---|
| `update_campaign` | budget, **pause/resume** (`status=PAUSED/ACTIVE`), status=DELETED to remove |
| `update_adset` | budget, targeting, bid, optimization event, schedule |
| `update_ad` | status, swap creative (`creative_id=...`) |
| `update_ad_creative` | rename / optimization settings (content of an existing creative is immutable — Meta limitation, not the server's) |

> ⚠️ The single most important capability is the **`update_*` family**. Some servers only read
> and create — without `update_*` the agent can't optimize, and you'll falsely conclude "the API
> won't let me edit." It will; you just need a server that exposes these. (See `AGENT_INSTRUCTIONS.md`.)

---

## Tested servers

| Server | Status | Notes |
|---|---|---|
| [`pipeboard-meta-ads-mcp`](https://github.com/pipeboard-co/meta-ads-mcp) | ✅ **Tested end-to-end** | The full pipeline was run on a live account: generate image → host → `upload_ad_image` → `create_ad_creative` → `create_campaign`/`create_adset`/`create_ad` (all PAUSED) → cleanup. Has the complete `update_*` family. |
| Any other MCP server | ⚪ **Untested — should work if it exposes the tools above** | Not personally verified. Match it against the contract list. If something is missing, the corresponding step won't work. |

We deliberately don't rate servers we haven't tested. If you verify another server against
this contract, a PR adding it here (with what you tested) is very welcome.

---

## How to verify your server in 2 minutes

1. List the tools your MCP server exposes.
2. Tick them off against the **Required tool contract** above.
3. If `get_insights` + the `create_*` set + the `update_*` set are all present → you're good.
4. If only read/create exist (no `update_*`) → you can launch but not optimize; pick a fuller server.

No `update_*`? Don't conclude "Meta's API can't edit ads." It can. The gap is the server, not Meta.
