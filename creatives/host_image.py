"""
host_image.py — upload a local image to a host and get a PUBLIC URL.

WHY: base64 inflates an image by ~33%. A large PNG (4-6 MB) in base64 won't fit
into Meta's request body — `upload_ad_image(file=...)` fails. The fix: upload the
image to a host, get a lightweight public URL, and pass it to
`upload_ad_image(image_url=URL)` — Meta downloads it itself, and the request body is tiny.

PICK A HOST YOURSELF (the script does NOT guess for you):

  ┌──────────┬──────────────────────────────────────────┬───────────────────────────────┐
  │ Provider │ Pros                                     │ Cons                          │
  ├──────────┼──────────────────────────────────────────┼───────────────────────────────┤
  │ fal      │ ★ RECOMMENDED. Proven on this flow,      │ Needs a PAID fal balance —    │
  │ (★)      │ fast CDN, official client, works         │ without it, 403 Exhausted.    │
  │          │ reliably with Meta.                      │ Extra dependency: fal-client. │
  ├──────────┼──────────────────────────────────────────┼───────────────────────────────┤
  │ imgbb    │ FREE, a key in a minute, no balance and  │ Public image hosting          │
  │          │ no extra dependencies. Works for anyone. │ (fine for ad creatives).      │
  │          │ Good for getting started / testing.      │ Less "production-grade."      │
  ├──────────┼──────────────────────────────────────────┼───────────────────────────────┤
  │ r2 (S3)  │ Your own bucket = full control, your     │ Need to set up R2/S3, enable  │
  │          │ domain, production-grade, cheap at scale.│ public access. boto3 + env.   │
  └──────────┴──────────────────────────────────────────┴───────────────────────────────┘

How to choose:
  - just want to try it / no paid fal → imgbb
  - have a fal balance, want the proven reliable path → fal (recommended)
  - production, your own CDN/domain → r2

Specify the provider via the --provider flag or the HOST_PROVIDER variable.
If not specified, the script does NOT choose silently — it asks you to pick (see below).

Usage (as a module):
    from host_image import host_image
    url = host_image("creative.png", provider="fal")     # provider specified explicitly
    url = host_image("creative.png")                     # taken from env HOST_PROVIDER
    # then:  upload_ad_image(account_id="act_XXX", image_url=url)

From the terminal:
    python host_image.py creative.png --provider fal
    python host_image.py creative.png --provider imgbb

Keys come ONLY from environment variables. They are not in the code.
"""

import argparse
import base64
import os
import sys
from typing import Optional
from uuid import uuid4

import requests


CHOOSE_HINT = (
    "No host selected. Specify a provider explicitly:\n"
    "  --provider fal     (★ recommended, proven — but needs a PAID fal balance)\n"
    "  --provider imgbb   (free, no balance — for getting started/testing)\n"
    "  --provider r2      (your own S3/Cloudflare R2 — production, your domain)\n"
    "Or set the HOST_PROVIDER environment variable."
)


def host_image(path: str, provider: Optional[str] = None) -> str:
    """
    Upload a file and return a public URL.
    The provider comes from the argument or env HOST_PROVIDER. If not set, the
    script does NOT choose silently (so it doesn't unexpectedly spend fal money) — it asks you to pick.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    provider = (provider or os.environ.get("HOST_PROVIDER") or "").lower()
    if not provider:
        raise ValueError(CHOOSE_HINT)

    if provider == "fal":
        return _upload_fal(path)
    if provider == "imgbb":
        return _upload_imgbb(path)
    if provider == "r2":
        return _upload_r2(path)
    raise ValueError(f"Unknown provider '{provider}'. Available: fal, imgbb, r2")


def _upload_fal(path: str) -> str:
    """
    fal.ai storage. Uses the official fal_client (more reliable than raw HTTP).
    Needs:  pip install fal-client   and   export FAL_KEY=...
    ⚠️ Requires an active (paid) fal balance — otherwise 403 Exhausted.
    """
    if not os.environ.get("FAL_KEY"):
        raise RuntimeError("No fal key. Set the FAL_KEY environment variable.")
    try:
        import fal_client
    except ImportError:
        raise RuntimeError(
            "fal-client is not installed. Install it: pip install fal-client "
            "(or use --provider imgbb, which has no extra dependencies)."
        )
    # upload_file detects the content-type itself and returns a public CDN URL
    return fal_client.upload_file(path)


def _upload_imgbb(path: str) -> str:
    """
    imgbb.com — free image hosting. Needs a free IMGBB_API_KEY key.
    Simple REST, no extra dependencies and no paid balance.
    """
    api_key = os.environ.get("IMGBB_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No imgbb key. Get a free one at https://api.imgbb.com/ "
            "and set IMGBB_API_KEY."
        )
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": api_key, "image": encoded},
        timeout=120,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"imgbb error {resp.status_code}: {resp.text}")
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"imgbb returned an error: {data}")
    return data["data"]["url"]


def _upload_r2(path: str) -> str:
    """
    Cloudflare R2 / any S3-compatible bucket. Needs boto3 and env:
      R2_ENDPOINT, R2_BUCKET, R2_ACCESS_KEY, R2_SECRET_KEY, R2_PUBLIC_BASE
    R2_PUBLIC_BASE — the bucket's public domain (e.g. https://cdn.example.com).
    """
    required = ["R2_ENDPOINT", "R2_BUCKET", "R2_ACCESS_KEY", "R2_SECRET_KEY", "R2_PUBLIC_BASE"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        raise RuntimeError(f"Missing environment variables for R2: {', '.join(missing)}")
    try:
        import boto3
    except ImportError:
        raise RuntimeError("boto3 is not installed. Install it: pip install boto3")

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY"],
        aws_secret_access_key=os.environ["R2_SECRET_KEY"],
    )
    # Unique key: UUID prefix + filename, so we don't overwrite a file with the same name
    key = f"{uuid4().hex[:8]}_{os.path.basename(path)}"
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    content_type = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                    "webp": "image/webp"}.get(ext, "application/octet-stream")
    s3.upload_file(path, os.environ["R2_BUCKET"], key,
                   ExtraArgs={"ContentType": content_type})
    base = os.environ["R2_PUBLIC_BASE"].rstrip("/")
    return f"{base}/{key}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a local image to a host → public URL for upload_ad_image"
    )
    parser.add_argument("path", help="Path to the local image")
    parser.add_argument("--provider", choices=["fal", "imgbb", "r2"],
                        help="Host (defaults to env HOST_PROVIDER; if not set — asks you to pick)")
    args = parser.parse_args()

    try:
        url = host_image(args.path, provider=args.provider)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(url)
    print("\nNext — to Meta via the MCP:", file=sys.stderr)
    print(f'  upload_ad_image(account_id="act_XXX", image_url="{url}")', file=sys.stderr)
