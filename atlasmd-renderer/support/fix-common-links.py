#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# ///

"""Safe fixer for common Tech Guide markdown link issues.

- handle both markdown links `[text](...)` and autolinks `<...>`
- do not rewrite specific pages, only apply generic path and anchor rules

run:
  uv run docs/tech-guide/support/fix-common-links.py
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

SITE_BASE = os.environ.get("ATLAS_BASE_URL", "/")

# Reference-style link definitions, e.g.
# [ref]: /site-tech-guide/foo
# [ref]: <http://localhost:3003/site-tech-guide/foo>
REF_DEF_RE = re.compile(
    r"^([ \t]*\[[^\]]+\]:[ \t]*)(<)?((?:/|https?://localhost:3003/)[^>\s]+)(>)?",
    re.MULTILINE,
)

# Matches URL-like segments inside markdown link or autolink
# We touch:
#  - root-relative: /site-tech-guide/...
#  - absolute: http(s)://localhost:3003/site-tech-guide/...
MD_LINK_URL_RE = re.compile(
    r"(?P<prefix>\]\(|<)"
    r"(?P<url>(?:#|\./|\.\./|/|https?://localhost:3003/)[^>\)\s]+)"
    r"(?P<suffix>[>\)])",
    re.IGNORECASE,
)

# 3) heading numeric sequence normalization
# e.g., "## 1.1 Title" -> "## 1.1. Title"
#       "### 1.1.1 Title" -> "### 1.1.1. Title"
HEADING_NUM_DOT_RE = re.compile(
    r"^(?P<prefix>#{1,6}\s+)(?P<num>\d+(?:\.\d+)*)(?P<space>\s+)(?P<title>\S.*)$",
    re.MULTILINE,
)


def _normalize_anchor(anchor: str) -> str:
    """Normalize an anchor fragment to our canonical slug.
    # strict rules mirroring slug creation used by the checker
    # - lowercase
    # - if starts with a digit and no leading underscore, add leading underscore
    # - collapse starting numeric groups like 4-2-2 into 422
    # - convert underscores to dashes except for the single leading underscore
    # - collapse multiple dashes and trim leading/trailing dashes
    """
    f = anchor.lower()
    # ensure leading underscore for numeric-leading anchors
    if f and f[0].isdigit() and not f.startswith("_"):
        f = "_" + f
    # collapse numeric groups like 3-3 or 3-3-1 at the beginning into 33 or 331
    if f.startswith("_"):
        m = re.match(r"^_(\d+(?:-\d+)+)(.*)$", f)
        if m:
            collapsed = m.group(1).replace("-", "")
            f = f"_{collapsed}{m.group(2)}"
        # convert underscores to dashes (preserve a single leading underscore)
        body = re.sub(r"_+", "-", f[1:])
        return "_" + body.strip("-")
    # convert underscores to dashes for non-leading-underscore cases
    return re.sub(r"_+", "-", f).strip("-")


def fix_url(url: str) -> str:
    """Normalize a markdown URL or fragment according to Guide rules.

    - splits absolute localhost urls into host/path for consistent handling
    - normalizes anchors (lowercase, leading underscore for numeric start,
      collapse leading numeric groups, convert underscores to dashes except the
      first underscore, and trim duplicate/edge dashes)
    - removes the redundant ``/site-tech-guide/`` prefix from internal links

    Args:
        url: The raw URL or anchor captured from markdown.

    Returns:
        The normalized URL or anchor string.
    """
    new_url = url

    # handle pure anchor links early
    if new_url.startswith("#"):  # its an anchor
        anchor_part = new_url[1:]
        new_anchor = _normalize_anchor(anchor_part)
        return f"#{new_anchor}"

    # split absolute localhost into host + path for consistent handling
    host = ""
    path = new_url
    if new_url.startswith("http://localhost:3003/"):
        host = "http://localhost:3003"
        path = new_url[len(host) :]
    elif new_url.startswith("https://localhost:3003/"):
        host = "https://localhost:3003"
        path = new_url[len(host) :]

    # 2) anchor handling: split base and fragment without altering path segments
    base_part, anchor_part = (path.split("#", 1) + [""])[:2]

    # 3) uniform anchor normalization
    if anchor_part:
        base, anchor = base_part, anchor_part
        new_anchor = _normalize_anchor(anchor)
        path = f"{base}#{new_anchor}"
    else:
        # no anchor; keep path as-is
        path = base_part

    # 4) drop redundant /site-tech-guide prefix for internal links
    # applies whether original url was absolute localhost or root-relative
    if path.startswith(SITE_BASE):
        path = path[len(SITE_BASE) - 1 :]  # keep leading slash, drop 'site-tech-guide/'

    # reconstruct with host if present
    new_url = f"{host}{path}" if host else path

    return new_url


def fix_file(md_path: Path) -> int:
    """Process a single markdown file and fix links/headings.

    Applies inline link fixes, reference-style link fixes, and heading numeric
    dot normalization in the provided markdown file.

    Args:
        md_path: Path to a ``.md`` file to be processed.

    Returns:
        The number of replacements performed in the file.
    """
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    changes = 0

    def _repl(m: re.Match[str]) -> str:
        nonlocal changes
        prefix, url, suffix = m.group("prefix"), m.group("url"), m.group("suffix")
        fixed = fix_url(url)
        if fixed != url:
            changes += 1
        return f"{prefix}{fixed}{suffix}"

    new_text = MD_LINK_URL_RE.sub(_repl, text)

    # fix reference-style definitions
    def _repl_ref(m: re.Match[str]) -> str:
        nonlocal changes
        prefix, lt, url, gt = m.group(1), m.group(2), m.group(3), m.group(4)
        fixed = fix_url(url)
        if fixed != url:
            changes += 1
        if lt and gt:
            return f"{prefix}<{fixed}>"
        return f"{prefix}{fixed}"

    new_text = REF_DEF_RE.sub(_repl_ref, new_text)

    # heading normalization pass: ensure a trailing dot after numeric sequences
    def _repl_heading(m: re.Match[str]) -> str:
        nonlocal changes
        prefix, num, space, title = (
            m.group("prefix"),
            m.group("num"),
            m.group("space"),
            m.group("title"),
        )
        # if the source already had a dot (e.g., '1. ' or '1.1. '),
        # this regex wouldn't match due to the extra '.' before the space,
        # so here we can safely add the dot
        changes += 1
        return f"{prefix}{num}. {title}"

    new_text = HEADING_NUM_DOT_RE.sub(_repl_heading, new_text)

    if changes > 0:
        md_path.write_text(new_text, encoding="utf-8")

    return changes


def main() -> int:
    """Entry point for scanning and fixing markdown files under content root.

    Returns:
        int: process exit code (0 on success, non-zero on errors)
    """
    if not ROOT.exists() or not ROOT.is_dir():
        print(f"error: content root not found: {ROOT}")
        return 2

    files = sorted(ROOT.glob("**/*.md"))
    total_files = 0
    total_changes = 0

    for f in files:
        c = fix_file(f)
        if c:
            total_files += 1
            total_changes += c

    print(
        f"Fixed {total_changes} links across {total_files} files under {ROOT.relative_to(Path(__file__).resolve().parents[3])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
