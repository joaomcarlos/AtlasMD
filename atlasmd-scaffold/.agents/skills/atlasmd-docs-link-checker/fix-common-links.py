#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Safe fixer for common AtlasMD documentation markdown link issues.

- handle both markdown links `[text](...)` and autolinks `<...>`
- normalize anchors, remove redundant site-base prefixes, fix heading numbering
- do not rewrite specific pages, only apply generic path and anchor rules

Usage:
  uv run fix-common-links.py --docs-root path/to/content
  uv run fix-common-links.py --docs-root path/to/content --site-base /palermo/ --host localhost:3003
"""

import argparse
import re
from pathlib import Path


def _normalize_anchor(anchor: str) -> str:
    f = anchor.lower()
    if f and f[0].isdigit() and not f.startswith("_"):
        f = "_" + f
    if f.startswith("_"):
        m = re.match(r"^_(\d+(?:-\d+)+)(.*)$", f)
        if m:
            collapsed = m.group(1).replace("-", "")
            f = f"_{collapsed}{m.group(2)}"
        body = re.sub(r"_+", "-", f[1:])
        return "_" + body.strip("-")
    return re.sub(r"_+", "-", f).strip("-")


def _build_regexes(host: str, site_base: str):
    """Build regex patterns parameterized by host and site base."""
    host_escaped = re.escape(host)

    ref_def_re = re.compile(
        rf"^([ \t]*\[[^\]]+\]:[ \t]*)(<)?((?:/|https?://{host_escaped}/)[^>\s]+)(>)?",
        re.MULTILINE,
    )

    md_link_url_re = re.compile(
        rf"(?P<prefix>\]\(|<)"
        rf"(?P<url>(?:#|\./|\.\./|/|https?://{host_escaped}/)[^>\)\s]+)"
        rf"(?P<suffix>[>\)])",
        re.IGNORECASE,
    )

    heading_num_dot_re = re.compile(
        r"^(?P<prefix>#{1,6}\s+)(?P<num>\d+(?:\.\d+)*)(?P<space>\s+)(?P<title>\S.*)$",
        re.MULTILINE,
    )

    return ref_def_re, md_link_url_re, heading_num_dot_re


def fix_url(url: str, host: str, site_base: str) -> str:
    new_url = url

    if new_url.startswith("#"):
        anchor_part = new_url[1:]
        new_anchor = _normalize_anchor(anchor_part)
        return f"#{new_anchor}"

    host_prefix = f"{host}/"
    host_str = ""
    path = new_url
    if new_url.startswith(f"http://{host_prefix}"):
        host_str = f"http://{host}"
        path = new_url[len(host_str):]
    elif new_url.startswith(f"https://{host_prefix}"):
        host_str = f"https://{host}"
        path = new_url[len(host_str):]

    base_part, anchor_part = (path.split("#", 1) + [""])[:2]

    if anchor_part:
        new_anchor = _normalize_anchor(anchor_part)
        path = f"{base_part}#{new_anchor}"
    else:
        path = base_part

    if site_base != "/" and path.startswith(site_base):
        path = path[len(site_base) - 1:]

    new_url = f"{host_str}{path}" if host_str else path
    return new_url


def fix_file(
    md_path: Path,
    ref_def_re: re.Pattern,
    md_link_url_re: re.Pattern,
    heading_num_dot_re: re.Pattern,
    host: str,
    site_base: str,
) -> int:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    changes = 0

    def _repl(m: re.Match) -> str:
        nonlocal changes
        prefix, url, suffix = m.group("prefix"), m.group("url"), m.group("suffix")
        fixed = fix_url(url, host, site_base)
        if fixed != url:
            changes += 1
        return f"{prefix}{fixed}{suffix}"

    new_text = md_link_url_re.sub(_repl, text)

    def _repl_ref(m: re.Match) -> str:
        nonlocal changes
        prefix, lt, url, gt = m.group(1), m.group(2), m.group(3), m.group(4)
        fixed = fix_url(url, host, site_base)
        if fixed != url:
            changes += 1
        if lt and gt:
            return f"{prefix}<{fixed}>"
        return f"{prefix}{fixed}"

    new_text = ref_def_re.sub(_repl_ref, new_text)

    def _repl_heading(m: re.Match) -> str:
        nonlocal changes
        prefix, num, space, title = (
            m.group("prefix"),
            m.group("num"),
            m.group("space"),
            m.group("title"),
        )
        changes += 1
        return f"{prefix}{num}. {title}"

    new_text = heading_num_dot_re.sub(_repl_heading, new_text)

    if changes > 0:
        md_path.write_text(new_text, encoding="utf-8")

    return changes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Fix common markdown link issues in AtlasMD documentation."
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        required=True,
        help="Path to the documentation content directory to fix.",
    )
    parser.add_argument(
        "--site-base",
        default="/",
        help="Site base prefix to strip from internal links (default: /).",
    )
    parser.add_argument(
        "--host",
        default="localhost:3003",
        help="Host used in absolute URLs to normalize (default: localhost:3003).",
    )
    args = parser.parse_args(argv)

    root: Path = args.docs_root
    site_base: str = args.site_base
    host: str = args.host

    if not root.exists() or not root.is_dir():
        print(f"error: content root not found: {root}")
        return 2

    ref_def_re, md_link_url_re, heading_num_dot_re = _build_regexes(host, site_base)

    files = sorted(root.glob("**/*.md"))
    total_files = 0
    total_changes = 0

    for f in files:
        c = fix_file(f, ref_def_re, md_link_url_re, heading_num_dot_re, host, site_base)
        if c:
            total_files += 1
            total_changes += c

    print(f"Fixed {total_changes} links across {total_files} files under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
