"""
generate_creative.py — generate an ad image via OpenAI and prepare it for upload to Meta.

This is the "left half" of flow A in knowledge/07: generating the image.
Next, the finished file is fed into the Meta MCP: upload_ad_image(file=path) → create_ad_creative → create_ad.

Why OpenAI: a simple API KEY (not an OAuth login). That makes the pipeline truly
"deployable": install dependencies, provide a key — it works. No tokens in the code.

Install:
    pip install -r requirements.txt
    export OPENAI_API_KEY="sk-..."

Run:
    # One vertical 9:16 creative (recommended for Reels/Stories — see knowledge/03)
    python generate_creative.py --prompt "UGC-style photo of a woman holding a family photo book, warm home lighting" --ratio 9:16 --out creative.png

    # Several variants at once (start with 3-6 per ad set — rule 3.1)
    python generate_creative.py --prompt "..." --ratio 9:16 --n 4 --out-dir ./creatives_batch

IMPORTANT: the quality of the offer/hook/realism lives in the PROMPT. The script only executes.
Offer formulas and anti-patterns are in knowledge/03_creatives.md.
"""

import argparse
import base64
import os
import sys
from typing import List

import requests

OPENAI_URL = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-1"

# Aspect ratio → a size that gpt-image-1 supports.
# 9:16 (vertical) — the primary format for Meta (Reels/Stories/feed), see knowledge/03 rule 3.3.
RATIO_TO_SIZE = {
    "9:16": "1024x1536",   # vertical — the default for Meta
    "1:1": "1024x1024",    # square — feed
    "16:9": "1536x1024",   # horizontal — rare, desktop
    "4:5": "1024x1536",    # feed portrait (gpt-image-1 returns the closest vertical)
}


def generate(prompt: str, ratio: str, n: int, quality: str) -> List[bytes]:
    """
    Generate n images. Returns a list of PNG bytes.

    gpt-image-1 does NOT support n>1 — for a batch we make n separate requests.
    Raises a clear error if there is no key or the API complained.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No key. Set the OPENAI_API_KEY environment variable (sk-...). "
            "Get the key on the OpenAI platform; don't put it in the code."
        )

    size = RATIO_TO_SIZE.get(ratio)
    if not size:
        raise RuntimeError(f"Unknown ratio '{ratio}'. Available: {', '.join(RATIO_TO_SIZE)}")

    # gpt-image-1 does not support n>1 — make n separate calls
    images = []
    for i in range(n):
        if n > 1:
            print(f"  Generating {i + 1}/{n}...")

        payload = {
            "model": MODEL,
            "prompt": prompt,
            "size": size,
            "quality": quality,            # "low" / "medium" / "high"
        }
        # IMPORTANT: gpt-image-1 ALWAYS returns b64_json and does NOT accept a
        # response_format parameter (unlike DALL-E). Passing response_format = a 400 error.

        resp = requests.post(
            OPENAI_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=180,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"OpenAI API error {resp.status_code}: {resp.text}")

        data = resp.json().get("data", [])
        if not data:
            raise RuntimeError(f"OpenAI returned an empty result (request {i + 1}/{n}).")

        b64 = data[0].get("b64_json")
        if not b64:
            raise RuntimeError(
                f"No b64_json in the response (request {i + 1}/{n}). "
                "gpt-image-1 normally always returns b64_json — check the model and the API response."
            )
        images.append(base64.b64decode(b64))

    return images


def save(images: List[bytes], out: str, out_dir: str) -> List[str]:
    """Save the images to disk. Returns a list of paths."""
    paths = []
    if len(images) == 1 and out:
        with open(out, "wb") as f:
            f.write(images[0])
        paths.append(out)
    else:
        target_dir = out_dir or "."
        os.makedirs(target_dir, exist_ok=True)
        for i, img in enumerate(images, 1):
            p = os.path.join(target_dir, f"creative_{i}.png")
            with open(p, "wb") as f:
                f.write(img)
            paths.append(p)
    return paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an ad creative via OpenAI")
    parser.add_argument("--prompt", required=True, help="Image prompt (the offer/hook is set HERE)")
    parser.add_argument("--ratio", default="9:16", choices=list(RATIO_TO_SIZE),
                        help="Aspect ratio (9:16 — the default for Meta)")
    parser.add_argument("--n", type=int, default=1, help="How many variants to generate")
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    parser.add_argument("--out", default="creative.png", help="File path (if --n 1)")
    parser.add_argument("--out-dir", help="Folder for multiple variants (if --n > 1)")
    args = parser.parse_args()

    try:
        imgs = generate(args.prompt, args.ratio, args.n, args.quality)
        files = save(imgs, args.out, args.out_dir)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Done, generated {len(files)} images:")
    for p in files:
        print(f"  {p}")

    # IMPORTANT: upload_ad_image(file=...) expects NOT a path, but a data-URL/base64.
    # high quality is often >1.5MB → base64 won't fit into Meta. We hint based on size.
    first = files[0]
    size_mb = os.path.getsize(first) / 1_000_000
    print("\nNext — upload to Meta via the MCP:")
    if size_mb >= 1.5:
        print(f"  Image is {size_mb:.1f} MB — large, use HOSTING (host_image.py):")
        print("  from host_image import host_image")
        print(f'  url = host_image("{first}", provider="fal")   # fal★/imgbb/r2 — your choice')
        print('  upload_ad_image(account_id="act_XXX", image_url=url)')
    else:
        print(f"  Image is {size_mb:.1f} MB — small, a data-URL is fine (to_data_url.py):")
        print("  from to_data_url import file_to_data_url")
        print(f'  data_url = file_to_data_url("{first}")')
        print('  upload_ad_image(account_id="act_XXX", file=data_url)')
    print("  → image_hash → create_ad_creative(...) → create_ad(...)   (see knowledge/07)")
