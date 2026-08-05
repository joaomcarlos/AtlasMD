---
name: atlasmd-icons
description: Generate all AtlasMD logos and favicons from a single source app icon of any size. Load when setting up branding for a consumer project, replacing logos, or fixing missing favicons.
---

# atlasmd-icons

Generate all AtlasMD logos and favicons from a single source app icon of any size. Load when setting up branding for a consumer project, replacing logos, or fixing missing favicons.

## What This Skill Does

This skill includes a Python script (`generate-icons.py`) that takes any source image and produces every image asset AtlasMD expects in a consumer project's `public/` directory:

**Logos (512x512 PNG by default):**
- `logo-light-mode.png` — transparent subject, used on light backgrounds
- `logo-dark-mode.png` — transparent subject, used on dark backgrounds
- `logo-dark-mode-bg.png` — subject composited on a solid dark background

**Favicons:**
- `favicon.ico` — multi-size ICO (16, 32, 48, 64, 128, 256)
- `favicon-16.png` — 16x16 PNG
- `favicon-32.png` — 32x32 PNG

The script optionally removes the background from the source image using `rembg` (ISNet model), tight-crops the subject, and resizes it to each target size.

## Script Location

```
ai/skills/atlasmd-icons/
  SKILL.md
  generate-icons.py
```

## Prerequisites

- **`uv`** — the Python package manager. The script is self-contained: it declares its own dependencies (Pillow, rembg) via inline script metadata, so `uv run` installs them automatically into an ephemeral environment.

Verify `uv` is installed:
```bash
uv --version
```

## Usage

### Basic (with background removal)

```bash
uv run ai/skills/atlasmd-icons/generate-icons.py \
  --source /path/to/app-icon.png \
  --public atlasmd-scaffold/public
```

### Source already has a transparent background

```bash
uv run ai/skills/atlasmd-icons/generate-icons.py \
  --source /path/to/icon-transparent.png \
  --public atlasmd-scaffold/public \
  --no-bg-removal
```

### Custom logo size and dark background color

```bash
uv run ai/skills/atlasmd-icons/generate-icons.py \
  --source icon.png \
  --public atlasmd-scaffold/public \
  --logo-size 256 \
  --dark-bg "#0d1117"
```

### All options

| Flag | Default | Purpose |
| --- | --- | --- |
| `--source PATH` | (required) | Path to the source app icon (PNG/JPG/WebP) |
| `--public PATH` | (required) | Path to the consumer project's `public/` directory |
| `--logo-size PX` | `512` | Output size for logo PNGs |
| `--no-bg-removal` | off | Skip background removal; use source as-is |
| `--bg-model MODEL` | `isnet-general-use` | rembg model (ignored with `--no-bg-removal`) |
| `--dark-bg COLOR` | `#1a1a1a` | Background color for `logo-dark-mode-bg.png` |

## What AtlasMD Expects

The renderer's `nuxt.config.ts` declares these favicon links in `<head>`:
- `favicon.ico` (type `image/x-icon`)
- `favicon-16.png` (16x16 PNG)
- `favicon-32.png` (32x32 PNG)

The `Logo.vue` component reads logo filenames from `runtimeConfig.public` — by convention these are fixed filenames in `public/`:
- `logo-light-mode.png`
- `logo-dark-mode.png`
- `logo-dark-mode-bg.png`

No configuration is needed for any of these files — they are convention-based. Place them in `public/` and AtlasMD serves them at the root URL.

## Workflow

1. Obtain a source app icon (any size, any reasonable format — PNG with transparency works best)
2. Run the script pointing at the consumer project's `public/` directory
3. If the source has a solid background, let `rembg` remove it (default behavior)
4. If the source already has a transparent background, pass `--no-bg-removal` to skip rembg
5. Rebuild is not needed — `public/` is volume-mounted at runtime, so changes appear on next page reload
6. Hard-refresh the browser (Cmd+Shift+R) to see the new favicon

## Troubleshooting

- **`Could not open source image`** — the file path is wrong or the format is unsupported. Pillow supports PNG, JPG, WebP, BMP, GIF, TIFF. SVG requires ImageMagick or rsvg-convert.
- **`rembg is required`** — this should not happen with `uv run` (it installs rembg automatically). If it does, check that `uv` is up to date and the script's inline metadata is intact.
- **Favicon not updating in browser** — browsers cache favicons aggressively. Hard-refresh (Cmd+Shift+R) or clear the cache. Check the file is served: `curl -s -o /dev/null -w "%{http_code}" http://localhost:47145/favicon.ico` should return `200`.
- **Background removal looks wrong** — try a different rembg model: `--bg-model u2net` (general purpose) or `--bg-model birefnet-general` (higher quality, slower).
