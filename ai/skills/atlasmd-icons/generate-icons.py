#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
#     "rembg",
# ]
# ///

"""Generate AtlasMD logos and favicons from a single source image.

Takes an app icon of any size and produces all the image assets AtlasMD expects
in a consumer project's public/ directory:

  Logos (512x512 PNG):
    logo-light-mode.png      Used on light backgrounds (header, light mode)
    logo-dark-mode.png       Used on dark backgrounds (header, dark mode)
    logo-dark-mode-bg.png    Used when a solid background is needed behind the logo

  Favicons:
    favicon.ico              Multi-size ICO (16, 32, 48, 64, 128, 256)
    favicon-16.png           16x16 PNG
    favicon-32.png           32x32 PNG

Usage:
  uv run generate-icons.py --source <path-to-icon> --public <path-to-public-dir>
  python3 generate-icons.py --source icon.png --public ../atlasmd-scaffold/public

Options:
  --source PATH        Path to the source app icon (any size, PNG/JPG/WebP/SVG*)
  --public PATH        Path to the consumer project's public/ directory
  --logo-size PX       Output size for logo PNGs (default: 512)
  --no-bg-removal      Skip background removal; use the source image as-is for
                       all three logos (use this if the source already has a
                       transparent background)
  --bg-model MODEL     rembg model to use for background removal
                       (default: isnet-general-use). Ignored if --no-bg-removal.
  --dark-bg COLOR      Background color (hex or name) for logo-dark-mode-bg.png
                       (default: #1a1a1a). Ignored if --no-bg-removal.

* SVG requires ImageMagick or rsvg-convert; Pillow alone cannot read SVG.

Requirements:
  - Python 3.10+
  - Pillow (pip install Pillow)
  - rembg (pip install rembg) — only needed if background removal is not skipped
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip install Pillow", file=sys.stderr)
    sys.exit(1)


LOGO_FILES = [
    "logo-light-mode.png",
    "logo-dark-mode.png",
    "logo-dark-mode-bg.png",
]

FAVICON_PNG_SIZES = {
    "favicon-16.png": 16,
    "favicon-32.png": 32,
}

FAVICON_ICO_SIZES = [16, 32, 48, 64, 128, 256]

DEFAULT_LOGO_SIZE = 512
DEFAULT_DARK_BG = "#1a1a1a"
DEFAULT_REMBG_MODEL = "isnet-general-use"


def load_source(path: Path) -> Image.Image:
    """Load the source image, converting to RGBA."""
    if not path.exists():
        print(f"Source image not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        img = Image.open(path)
    except Exception as exc:
        print(f"Could not open source image {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    return img.convert("RGBA")


def remove_background(img: Image.Image, model: str) -> Image.Image:
    """Remove the background using rembg. Returns RGBA image."""
    try:
        from rembg import remove
    except ImportError:
        print(
            "rembg is required for background removal: pip install rembg\n"
            "Or re-run with --no-bg-removal if the source already has a "
            "transparent background.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Removing background with rembg model '{model}'...")
    return remove(img, model_name=model).convert("RGBA")


def tight_crop(img: Image.Image) -> Image.Image:
    """Crop transparent borders so the subject fills the frame."""
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def resize_square(img: Image.Image, size: int) -> Image.Image:
    """Resize an image to a square of the given size using Lanczos."""
    return img.resize((size, size), Image.LANCZOS)


def composite_on_bg(img: Image.Image, bg_color: str) -> Image.Image:
    """Composite an RGBA image onto a solid background color."""
    bg = Image.new("RGBA", img.size, bg_color)
    return Image.alpha_composite(bg, img)


def generate_logos(
    source: Image.Image,
    public_dir: Path,
    logo_size: int,
    remove_bg: bool,
    bg_model: str,
    dark_bg: str,
) -> None:
    """Generate the three logo PNGs."""
    if remove_bg:
        subject = remove_background(source, bg_model)
        subject = tight_crop(subject)
    else:
        subject = source

    square = resize_square(subject, logo_size)

    # logo-light-mode.png — transparent subject for light backgrounds
    square.save(public_dir / "logo-light-mode.png")
    print(f"  wrote logo-light-mode.png ({logo_size}x{logo_size}, transparent)")

    # logo-dark-mode.png — same transparent subject, used on dark backgrounds
    square.save(public_dir / "logo-dark-mode.png")
    print(f"  wrote logo-dark-mode.png ({logo_size}x{logo_size}, transparent)")

    # logo-dark-mode-bg.png — subject composited on a solid dark background
    with_bg = composite_on_bg(square, dark_bg)
    with_bg.save(public_dir / "logo-dark-mode-bg.png")
    print(f"  wrote logo-dark-mode-bg.png ({logo_size}x{logo_size}, bg={dark_bg})")


def generate_favicons(
    source: Image.Image,
    public_dir: Path,
    remove_bg: bool,
    bg_model: str,
) -> None:
    """Generate favicon PNGs and the multi-size ICO."""
    if remove_bg:
        subject = remove_background(source, bg_model)
        subject = tight_crop(subject)
    else:
        subject = source

    # PNG favicons
    for filename, size in FAVICON_PNG_SIZES.items():
        resized = resize_square(subject, size)
        resized.save(public_dir / filename)
        print(f"  wrote {filename} ({size}x{size})")

    # Multi-size ICO
    ico_images = [resize_square(subject, s) for s in FAVICON_ICO_SIZES]
    ico_images[0].save(
        public_dir / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in FAVICON_ICO_SIZES],
        append_images=ico_images[1:],
    )
    print(f"  wrote favicon.ico (sizes: {FAVICON_ICO_SIZES})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate AtlasMD logos and favicons from a single source image.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the source app icon (any size, PNG/JPG/WebP)",
    )
    parser.add_argument(
        "--public",
        type=Path,
        required=True,
        help="Path to the consumer project's public/ directory",
    )
    parser.add_argument(
        "--logo-size",
        type=int,
        default=DEFAULT_LOGO_SIZE,
        help=f"Output size for logo PNGs in pixels (default: {DEFAULT_LOGO_SIZE})",
    )
    parser.add_argument(
        "--no-bg-removal",
        action="store_true",
        help="Skip background removal; use the source image as-is for all logos",
    )
    parser.add_argument(
        "--bg-model",
        default=DEFAULT_REMBG_MODEL,
        help=f"rembg model for background removal (default: {DEFAULT_REMBG_MODEL})",
    )
    parser.add_argument(
        "--dark-bg",
        default=DEFAULT_DARK_BG,
        help=f"Background color for logo-dark-mode-bg.png (default: {DEFAULT_DARK_BG})",
    )
    args = parser.parse_args()

    if not args.public.is_dir():
        print(f"Public directory not found: {args.public}", file=sys.stderr)
        sys.exit(1)

    source = load_source(args.source)
    print(f"Source image: {args.source} ({source.width}x{source.height})")
    print(f"Output directory: {args.public}")
    print(
        f"Background removal: {'off' if args.no_bg_removal else f'on (model={args.bg_model})'}"
    )
    print()

    print("Generating logos...")
    generate_logos(
        source=source,
        public_dir=args.public,
        logo_size=args.logo_size,
        remove_bg=not args.no_bg_removal,
        bg_model=args.bg_model,
        dark_bg=args.dark_bg,
    )

    print()
    print("Generating favicons...")
    generate_favicons(
        source=source,
        public_dir=args.public,
        remove_bg=not args.no_bg_removal,
        bg_model=args.bg_model,
    )

    print()
    print("Done. All image assets generated successfully.")


if __name__ == "__main__":
    main()
