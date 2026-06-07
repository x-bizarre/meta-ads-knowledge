# 07 — Creative pipeline + advertising existing posts (two launch flows)

> This was missing from the first version of the base. The playbook only described launching NEW creatives,
> and the chain "generated an image → uploaded it → ad" was broken. Here both flows are
> laid out by the tools of the Meta Ads MCP server.

---

## Two different ways to make an ad

In Meta there are TWO fundamentally different paths, and both are supported by the MCP server:

| Flow | When to use | Media source |
|---|---|---|
| **A. New creative** | You're building an ad from scratch: your own image/video + ad copy | An image/video file or any image generator |
| **B. Existing post** | You already have an organic post in IG/FB with likes/comments — you want to "boost" it | `object_story_id` of the existing post |

Previously the base only had flow A. Flow B (advertising existing content) **exists in the MCP code**,
but was undocumented — now it is.

---

## FLOW A — New creative (generation → ad)

The full chain from image to a launched ad. Each step is a real MCP tool.

```
1. Generate/grab an image or video
   └─ READY SCRIPT: creatives/generate_creative.py (OpenAI gpt-image-1, via API key)
      python generate_creative.py --prompt "..." --ratio 9:16 --out creative.png
   └─ Or any generator of your own / a ready file
   └─ Format: vertical 9:16 (rule 3.3), hook in the first 3 sec for video

2. upload_ad_image(account_id, file=data-URL OR image_url=link)
   └─ ⚠️ file expects NOT a path, but a data-URL/base64. Two methods (see below):
      • small (<1.5MB): to_data_url.file_to_data_url() → file=data_url
      • large (≥1.5MB): host_image.host_image() → image_url=url   ← gpt-image-1 usually goes here
   └─ Returns image_hash. Video is uploaded via a separate path (video_id)

3. compute_image_crops(...)   [optional]
   └─ Compute crops for different placements if the image isn't 9:16

4. create_ad_creative(account_id, image_hash=..., page_id=..., link_url=...,
                      message="text", headline="headline",
                      call_to_action_type="SHOP_NOW")
   └─ Assembles the creative. You can pass several texts/headlines at once
      (messages=[...], headlines=[...]) for dynamic creative.
   └─ Returns creative_id

5. create_ad(account_id, name=..., adset_id=..., creative_id=..., status="PAUSED")
   └─ Creates the ad. IMPORTANT: status="PAUSED" by default —
      check before launch, then update_ad(status="ACTIVE")
```

### Linking with the creative generator

The project has a ready script `creatives/generate_creative.py` — it generates an image
via OpenAI (gpt-image-1) with a simple API key and saves the file. Then:

```
generate_creative.py → creative.png → file_to_data_url() → upload_ad_image(file=data_url) → ...
```

### ⚠️ Uploading a local image — TWO methods (important)
`upload_ad_image(file=...)` expects **NOT a file path, but the image's data-URL/base64**. If you pass
the path `"creative.png"` — Meta gets garbage. But base64 has a size limit.

**Method 1 — small image (< ~1.5 MB): data-URL, no cloud**
```python
from to_data_url import file_to_data_url     # creatives/to_data_url.py
data_url = file_to_data_url("creative.png")
upload_ad_image(account_id="act_XXX", file=data_url)
```

**Method 2 — large image (≥ ~1.5 MB): hosting → image_url**
base64 inflates by ~33%. A 4-6 MB PNG → 5-8 MB in the request body and **won't fit through Meta**
(the MCP doesn't compress — it sends as is). This is exactly why "local images wouldn't upload."
The fix: upload to a host, hand over a light URL — Meta downloads it itself.
```python
from host_image import host_image            # creatives/host_image.py
url = host_image("creative.png", provider="fal")   # pick: fal★(balance) / imgbb(free) / r2
upload_ad_image(account_id="act_XXX", image_url=url)
```
`gpt-image-1` in high quality often returns 2-4 MB → for it, go straight to method 2.

> ⚠️ Face realism, format, anti-AI style — that's the generator's (and prompt's) job, not Meta's.
> The OpenAI script is the "turnkey" default; you can swap in your own generator, the Meta flow doesn't depend on it.

### How many creatives
Start with 3-6 strong ones per ad set, top up to 10-20 (rule 3.1). That means steps 1-4
are repeated for several variants, step 5 — for each one, into one ad set.

---

## FLOW B — Advertising an existing post (object_story_id)

When you already have a live post in the Instagram/Facebook feed — with reactions,
comments, shares — and you want to run **that exact post** as an ad
(the social proof carries over to the ad).

```
1. Get the post ID
   └─ object_story_id format: {page_id}_{post_id}
      Example: "{PAGE_ID}_{POST_ID}" (e.g. "1234567890_9876543210")
   └─ page_id — via get_account_pages / search_pages_by_name
   └─ post_id — from the post link or get_ad_creatives of existing ads

2. create_ad_creative(account_id, object_story_id="{page_id}_{post_id}")
   └─ No need for image_hash, link_url, message — media and text are already in the post
   └─ instagram_actor_id — if you're promoting an Instagram post specifically
   └─ Returns creative_id

3. create_ad(account_id, name=..., adset_id=..., creative_id=..., status="PAUSED")
   └─ Then as usual
```

### How flow B differs and why it's valuable
- **Social proof is preserved.** The likes and comments of the organic post
  stay on the ad — this works better than a "cold" brand-new ad.
- **You can pool engagement on one post.** If you run the same
  `object_story_id` across different ad sets — reactions accumulate in one place instead of being spread thin.
- **Good for UGC and reviews.** A real customer post → into the ad without rebuilding it.

### Limitations (important)
- **The content of an existing post can't be changed via the API** (you can't edit text/image) — but
  you don't need to, you're promoting it as is.
- To promote a post, you need rights to the source page.
- `source_instagram_media_id` (promoting an IG medium specifically) — a separate case, support
  depends on the specific MCP server (not all implement it).

---

## Which flow to choose

| Situation | Flow |
|---|---|
| Launch from scratch, your own/generated image | **A** |
| You already have a successful organic post with reactions | **B** |
| You want to pool social proof on one ad | **B** (one object_story_id across different ad sets) |
| UGC/customer review published as a post | **B** |
| You need several text/image variants for a test | **A** (dynamic creative: messages[], headlines[]) |

---

## Checklist before `status="ACTIVE"`
- [ ] Ad created as PAUSED, eyeballed in Ads Manager
- [ ] Creative linked to the right page (page_id) and Instagram account
- [ ] Link/CTA points where it should (for flow A)
- [ ] Ad set with the right optimization event and budget (playbook steps 2-3)
- [ ] Pixel/CAPI catching events (Step 0 — without it, optimization is blind)
- [ ] Only then — `update_ad(status="ACTIVE")`

**Tool reliability:** all listed (`upload_ad_image`, `create_ad_creative`
with `image_hash`/`object_story_id`, `create_ad`, `update_ad`) — verified in the code of the
`pipeboard-meta-ads-mcp` fork (any server with the same tool set will work).
