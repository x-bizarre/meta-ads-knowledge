# Creative generation

The "left half" of flow A: generate an ad image → get a file that's ready to upload
to Meta (`upload_ad_image`).

The provider is **OpenAI (gpt-image-1)**. Chosen specifically for its simple **API key**
(rather than an OAuth login) — which is what makes the pipeline genuinely "drop-in": install it,
give it a key, it works.

---

## Installation

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."     # key from the OpenAI platform, do not hardcode it
```

## Usage

A single vertical 9:16 creative (the format for Reels/Stories — `../knowledge/03`):
```bash
python generate_creative.py \
  --prompt "UGC-style photo of a woman holding a family photo book, warm home lighting" \
  --ratio 9:16 --out creative.png
```

Several variants at once (start with 3-6 per ad set — rule 3.1):
```bash
python generate_creative.py --prompt "..." --ratio 9:16 --n 4 --out-dir ./batch
```

## The full flow to a live ad

```
1. generate_creative.py            → creative.png         (this script)
2. file_to_data_url("creative.png")→ data-URL             (to_data_url.py)
3. upload_ad_image(file=data_url)  → image_hash           (Meta MCP)
4. create_ad_creative(...)         → creative_id          (Meta MCP)
5. create_ad(... status=PAUSED)    → ad_id                (Meta MCP)
6. eyeball it → update_ad(status="ACTIVE")
```

Steps 3-6 — details in `../knowledge/07_creative_pipeline_and_existing_posts.md`.

## ⚠️ Uploading a local image to the ad account — two ways

`upload_ad_image(file=...)` expects **not a file path**, but a data-URL/base64 of the image.
Pass it the path `"creative.png"` and Meta gets garbage. But base64 has a limit.

### Way 1 — small image (< ~1.5 MB): data-URL, no cloud
```python
from to_data_url import file_to_data_url
data_url = file_to_data_url("creative.png")
upload_ad_image(account_id="act_XXX", file=data_url)
```
Simple and local. But base64 inflates the image by ~33%.

### Way 2 — large image (≥ ~1.5 MB): hosting → image_url
A large PNG (4-6 MB) becomes 5-8 MB in base64 and **won't fit into Meta's request body** —
which is exactly why "local images wouldn't upload" before. The fix: upload it to a host,
hand over a lightweight URL, and let Meta download it itself.

```python
from host_image import host_image
url = host_image("creative.png", provider="fal")     # you specify the provider explicitly
upload_ad_image(account_id="act_XXX", image_url=url)
```

**Pick the host yourself** (the script doesn't guess — if you don't specify one, it'll ask you to choose):

| Provider | Pros | Cons | For whom |
|---|---|---|---|
| **fal** ★ | Proven on this flow, fast CDN, reliable with Meta | Needs a **paid balance** on fal (otherwise 403). Extra dependency `fal-client` | Recommended, if you have a balance |
| **imgbb** | Free, key in a minute, no balance and no extra dependencies | Public image hosting (fine for ads), less "production-grade" | Getting started / testing / those without fal |
| **r2 / S3** | Your own bucket, your own domain, production-grade, cheap at volume | You have to set up R2/S3 + public access, `boto3` | Production with your own CDN |

```bash
# fal (recommended, needs a balance)
export FAL_KEY=...        && python host_image.py creative.png --provider fal
# imgbb (free)
export IMGBB_API_KEY=...  && python host_image.py creative.png --provider imgbb
# r2 / S3 (your own bucket)
export R2_ENDPOINT=... R2_BUCKET=... R2_ACCESS_KEY=... R2_SECRET_KEY=... R2_PUBLIC_BASE=...
python host_image.py creative.png --provider r2
```

You can lock in the choice once and for all: `export HOST_PROVIDER=imgbb` — then `--provider` isn't needed.

> Simplicity rule: a small 9:16 static is usually < 1 MB → way 1, no cloud.
> Large/heavy images → way 2 (hosting). `gpt-image-1` in high quality often
> returns 2-4 MB — for those, go straight to way 2.

---

## Important

- **Quality = the prompt.** The script executes, but the offer/hook/realism are set in `--prompt`.
  Offer formulas and anti-patterns — in `../knowledge/03_creatives.md`.
- **Key from the environment only.** No token in the code. See `.gitignore` in the root.
- **Want a different generator?** The Meta flow (steps 2-5) doesn't depend on the provider. You can swap
  this script for your own (Midjourney, your own Stable Diffusion, etc.) — the only requirement is that the output
  is an image file or a URL. `upload_ad_image` accepts both `file=` and `image_url=`.
- **Video** is not handled by this script — static only. For video creatives, generate them separately and
  upload them via the MCP video path (`get_ad_video` / video_id).
