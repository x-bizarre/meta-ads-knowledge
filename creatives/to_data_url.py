"""
to_data_url.py — turn a LOCAL image into a data-URL for upload_ad_image.

SOLVES a common problem: `upload_ad_image(file="/path/creative.png")` does NOT work,
because the `file` parameter expects not a path but a base64/data-URL of the image
itself. Previously this forced you to upload the image to a third-party host (fal/CDN)
just to get a public URL. That's not needed: we encode the file into a data-URL locally — and upload directly.

Usage (as a module — the primary way):
    from to_data_url import file_to_data_url
    data_url = file_to_data_url("creative.png")
    # then via the Meta MCP:
    # upload_ad_image(account_id="act_XXX", file=data_url)

Usage (from the terminal — to copy the string):
    python to_data_url.py creative.png            # prints the data-URL to stdout
    python to_data_url.py creative.png --clip      # also copies it to the clipboard (macOS)
"""

import argparse
import base64
import os
import sys

# MIME types by extension — the ones Meta accepts (see the upload_ad_image code)
MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
}


def file_to_data_url(path: str) -> str:
    """
    Read a local image file and return a data-URL:
        "data:image/png;base64,iVBORw0KG..."
    This is exactly the string that upload_ad_image(file=...) accepts.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    mime = MIME_BY_EXT.get(ext)
    if not mime:
        raise ValueError(
            f"Unsupported extension '{ext}'. "
            f"Supported: {', '.join(MIME_BY_EXT)}"
        )

    with open(path, "rb") as f:
        raw = f.read()
    # base64 inflates by ~33%. A large file won't fit into Meta's request body.
    # Warning threshold ~1.5 MB of source (≈2 MB in base64) — beyond that, prefer hosting.
    if len(raw) > 1_500_000:
        size_mb = len(raw) / 1_000_000
        print(
            f"[WARNING] Image is {size_mb:.1f} MB — in base64 it will be ~{size_mb*1.33:.1f} MB "
            f"and may fail to upload to Meta. For large images use "
            f"host_image.py (upload to a host → pass image_url).",
            file=sys.stderr,
        )
    encoded = base64.b64encode(raw).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def _copy_to_clipboard(text: str) -> bool:
    """Put text on the clipboard (macOS pbcopy). Returns success."""
    try:
        import subprocess
        subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Local image → data-URL for upload_ad_image (no fal/CDN)"
    )
    parser.add_argument("path", help="Path to the local image (.png/.jpg/...)")
    parser.add_argument("--clip", action="store_true",
                        help="Copy the data-URL to the clipboard (macOS)")
    args = parser.parse_args()

    try:
        data_url = file_to_data_url(args.path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # The data-URL is long — for convenience we print a short note + the full string
    size_kb = len(data_url) / 1024
    print(data_url)

    if args.clip:
        if _copy_to_clipboard(data_url):
            print(f"\n[copied to clipboard, ~{size_kb:.0f} KB]", file=sys.stderr)
        else:
            print("\n[could not copy — pbcopy unavailable]", file=sys.stderr)
