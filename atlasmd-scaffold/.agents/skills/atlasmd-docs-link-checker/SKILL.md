---
name: atlasmd-docs-link-checker
description: Checks and fixes broken links in AtlasMD documentation projects. Self-contained — includes the scripts. Load when verifying documentation links, fixing link formatting, or running link validation.
---

# atlasmd-docs-link-checker

Checks and fixes broken links in AtlasMD documentation projects. Self-contained — the scripts are bundled in this skill directory. Load when verifying documentation links, fixing link formatting, or running link validation.

## What This Skill Does

This skill includes two Python scripts in its own directory:

1. **`fix-common-links.py`** — Normalizes link formatting (anchors, prefixes, heading numbering). Run this first.
2. **`check-broken-links.py`** — Scans all markdown files, extracts links, and verifies they resolve to real pages with valid anchors. Run this second.

Both scripts are dependency-free (Python 3.10+ stdlib only) and are invoked with `uv run`. They accept `--docs-root` to point at any content directory.

## Script Locations

The scripts are in this skill's directory:

```
ai/skills/atlasmd-docs-link-checker/
  SKILL.md
  check-broken-links.py
  fix-common-links.py
```

## Prerequisites

- **Python 3.10+** — the scripts use stdlib only, no pip dependencies
- **`uv`** — the Python package manager used to run the scripts
- **Dev server running** (optional) — the checker does filesystem-based validation by default, but a running dev server enables HTTP fallback verification for same-host links

Verify `uv` is installed:
```bash
uv --version
```

If not installed, install it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Workflow

### Step 1: Fix link formatting

Run the fixer first to normalize all links before checking them. This prevents false positives caused by formatting inconsistencies.

```bash
# Basic usage — point at the content directory
uv run ai/skills/atlasmd-docs-link-checker/fix-common-links.py \
  --docs-root docs/tech-guide/content

# With site-base and host overrides for projects with a URL prefix
uv run ai/skills/atlasmd-docs-link-checker/fix-common-links.py \
  --docs-root docs/tech-guide/content \
  --site-base /site-tech-guide/ \
  --host localhost:3003
```

**Arguments:**
- `--docs-root` (required): Path to the documentation content directory to fix
- `--site-base` (default `/`): Site base prefix to strip from internal links. Use `/site-tech-guide/` for CBS, `/palermo/` for Palermo, or `/` if no prefix.
- `--host` (default `localhost:3003`): Host used in absolute URLs to normalize

**What the fixer does:**
- Normalizes anchor fragments (lowercase, leading underscore for numeric start, collapse numeric groups like `3-3-1` to `331`, convert underscores to dashes)
- Removes redundant site-base prefixes from internal links (e.g., strips `/site-tech-guide/` from internal paths)
- Normalizes heading numbering format (`## 1.1 Title` becomes `## 1.1. Title`)
- Handles inline links `[text](url)`, autolinks `<url>`, and reference-style definitions `[ref]: url`

**Output:**
```
Fixed X links across Y files under docs/tech-guide/content
```

**Exit codes:**
- `0`: Success (changes may or may not have been made)
- `2`: Content root not found

### Step 2: Check for broken links

After fixing, run the checker to find links that point to non-existent pages or anchors.

```bash
# Basic usage
uv run ai/skills/atlasmd-docs-link-checker/check-broken-links.py \
  --docs-root docs/tech-guide/content

# With custom base URL (for projects with a URL prefix or different port)
uv run ai/skills/atlasmd-docs-link-checker/check-broken-links.py \
  --docs-root docs/tech-guide/content \
  --base-url http://localhost:3003/site-tech-guide \
  --concurrency 50
```

**Arguments:**
- `--docs-root` (required): Path to the documentation content directory to scan
- `--base-url` (default `http://localhost:3003`): Base URL for resolving relative links. Include a path prefix if the site uses one (e.g., `http://localhost:3003/site-tech-guide`).
- `--include-external` (flag): Also check external http(s) links (off by default)
- `--concurrency` (default `30`): Maximum concurrent HTTP requests
- `--timeout` (default `10.0`): Per-request timeout in seconds
- `--project-root` (optional): Project root for relative path display in output

**What the checker does:**
1. Scans all `**/*.md` files under the content directory
2. Extracts markdown links and autolinks, skipping:
   - Image links (starting with `!`)
   - `mailto:` and `tel:` schemes
   - Links inside code fences (``` or ~~~)
3. Resolves URLs relative to the base URL:
   - Absolute http(s) URLs returned as-is
   - Root-relative paths (`/`) joined to base host
   - Pure anchors (`#...`) resolved against base_url
   - Relative paths (`../x`, `x/y`) joined to base_url path
4. Filesystem-based checking:
   - Builds a site index mapping paths to markdown files
   - Checks if target markdown file exists
   - Checks if anchor fragment exists in target file
   - Strips numeric prefixes from path segments (e.g., `5.features` becomes `features`)
5. Second pass: HTTP verification for same-host links to filter false failures from redirects

**Output format:**
```
Scanning X files, found Y links. Base: http://localhost:3003
FAIL docs/tech-guide/content/file.md:123 | section: Section Name -> http://localhost:3003/page#anchor [status=404] (not-found)
FAIL docs/tech-guide/content/file.md:456 | section: Section Name -> http://localhost:3003/page#anchor [status=200] (anchor-not-found: #anchor)

OK: X  |  FAIL: Y
```

**Exit codes:**
- `0`: All links OK
- `1`: Broken links found
- `2`: Content root not found

## Interpreting Results

### Failure types

| Status | Meaning | Action |
| ------ | ------- | ------ |
| `not-found` | The target page does not exist (404) | Fix the link path or create the missing page |
| `anchor-not-found` | The page exists but the anchor (heading) does not | Fix the anchor or update the heading text |
| `unreachable` | Timeout, DNS failure, or connection error | Check if the dev server is running, or the external site is down |

### Reading the output

Each `FAIL` line shows:
- **File path**: The markdown file containing the broken link
- **Line number**: Where the link is in the file
- **Section**: The most recent heading above the link (for context)
- **Resolved URL**: The full URL the link resolves to
- **Status**: HTTP status code (if checked via HTTP)
- **Failure type**: `not-found`, `anchor-not-found`, or `unreachable`

### Common issues and fixes

**Broken internal link (not-found):**
- The link points to a page that does not exist
- Check if the page was renamed, moved, or deleted
- Update the link to the correct path, or create the missing page
- Remember: the checker strips numeric prefixes, so `/5.features/rr-scheduling` is checked as `/features/rr-scheduling`

**Broken anchor (anchor-not-found):**
- The page exists but the heading anchor does not
- The anchor is derived from the heading text with normalization (lowercase, underscores to dashes, etc.)
- Check the actual heading text in the target page and update the anchor to match
- Run `fix-common-links.py` first — it normalizes anchors automatically

**Redundant prefix in link:**
- Internal links should not include the site-base prefix (e.g., `/site-tech-guide/`)
- Run `fix-common-links.py` with `--site-base /site-tech-guide/` to strip redundant prefixes automatically

**Heading numbering format:**
- Headings like `## 1.1 Title` should be `## 1.1. Title` (dot after the number)
- Run `fix-common-links.py` to normalize heading numbering automatically

## Anchor Normalization Rules

Both scripts use the same anchor normalization. Understanding these rules helps when manually fixing links:

1. Lowercase the entire anchor
2. If the anchor starts with a digit and has no leading underscore, prefix with `_` (e.g., `3-features` becomes `_3-features`)
3. Collapse leading numeric groups: `3-3-1` becomes `331` (e.g., `_3-3-1-foo` becomes `_331-foo`)
4. Convert underscores to dashes, except for a single leading underscore (e.g., `_foo_bar` becomes `_foo-bar`)
5. Collapse multiple dashes and trim leading/trailing dashes

## Path Segment Cleaning

The checker strips numeric ordering prefixes from path segments when resolving links:

- `/developers/5.features/rr-scheduling` is checked as `/developers/features/rr-scheduling`
- This matches the documentation standard's route path rules (see Standard section 8.1)

## Documentation Format Compatibility

These scripts are designed for the AtlasMD Documentation Standard and handle its specific conventions:

- **File naming**: `N.title.md` format (numeric prefix + dot + title)
- **Directory structure**: Numbered sections (e.g., `1.getting-started/`), `_dir.yml` for metadata
- **MDC syntax**: Links inside MDC components are handled like normal markdown links
- **Route paths**: Numeric prefixes are stripped when resolving links (the route path differs from the file path)

The scripts do not modify documentation content beyond link and heading normalization. They do not:
- Add or remove pages
- Change page structure or sections
- Modify frontmatter
- Touch non-link text

## Known Project Configurations

| Project | `--docs-root` | `--base-url` | `--site-base` | `--host` |
| ------- | ------------- | ------------ | ------------- | -------- |
| CBS | `docs/tech-guide/content` | `http://localhost:3003/site-tech-guide` | `/site-tech-guide/` | `localhost:3003` |
| Palermo / AtlasMD renderer | `content` | `http://localhost:8768/palermo` | `/palermo/` | `localhost:8768` |

## When to Use This Skill

- After writing or updating documentation pages with internal or external links
- Before publishing documentation changes
- When investigating reported broken links
- As part of a documentation review cycle (see Standard section 12.4)
- After renaming or moving documentation pages (to find links that need updating)

## Operational Notes

- Run the fixer before the checker to avoid false positives from formatting issues
- The checker does filesystem-based validation by default — a dev server is not strictly required
- External link checking is disabled by default; use `--include-external` to enable it
- The checker uses concurrency (default 30) and a timeout (default 10 seconds) for HTTP verification
- Both scripts are safe to run repeatedly — the fixer only writes when changes are needed
