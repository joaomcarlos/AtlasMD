#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Markdown link checker for AtlasMD documentation.

Scans markdown files under a content directory, extracts links, resolves them
against a base URL, and verifies they point to real pages with valid anchors.
Reports broken links with file, section, and line context.

Usage:
  uv run check-broken-links.py --docs-root path/to/content
  uv run check-broken-links.py --docs-root path/to/content --base-url http://localhost:3003
  uv run check-broken-links.py --docs-root path/to/content --base-url http://localhost:3003 --concurrency 50

Exit code is non-zero if any broken links are found.

Finds the following problems:
- Broken links (target page does not exist on the filesystem)
- Broken anchors (target page exists but the anchor id is not present)
- Unreachable links (timeouts, DNS failures, connection errors via HTTP fallback)
"""

import argparse
import asyncio
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

DEFAULT_BASE_URL = "http://localhost:3003"


@dataclass(frozen=True)
class MdLink:
    file: Path
    line_no: int
    section: str
    text: str
    url: str


@dataclass(frozen=True)
class CheckResult:
    link: MdLink
    resolved: str
    ok: bool
    status: int | None
    error: str | None


def _candidate_fragments(frag: str) -> list[str]:
    f = frag.lower()
    nf = f
    if nf and nf[0].isdigit() and not nf.startswith("_"):
        nf = "_" + nf
    if nf.startswith("_"):
        m = re.match(r"^_(\d+(?:-\d+)+)(.*)$", nf)
        if m:
            collapsed = m.group(1).replace("-", "")
            nf = f"_{collapsed}{m.group(2)}"
    if nf.startswith("_"):
        body = re.sub(r"_+", "-", nf[1:])
        nf = "_" + body.strip("-")
    else:
        nf = re.sub(r"_+", "-", nf).strip("-")
    cands: list[str] = [f]
    if nf != f:
        cands.append(nf)
    seen: set[str] = set()
    uniq: list[str] = []
    for x in cands:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def iter_markdown_files(root: Path, pattern: str = "**/*.md") -> Iterator[Path]:
    yield from root.glob(pattern)


def _is_in_code_fence(line: str, fence_state: str | None) -> str | None:
    m = re.match(r"^(\s*)([`~]{3,})(.*)$", line)
    if m:
        fence = m.group(2)[0]
        marker = fence * len(m.group(2))
        if fence_state is None:
            return marker
        if fence_state[0] == fence:
            return None
    return fence_state


MD_LINK_RE = re.compile(
    r"(?<!\\)!?\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)(?:\s+\"[^\"]*\")?\)",
)
AUTOLINK_RE = re.compile(r"<(?P<url>https?://[^>\s]+)>")
HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<text>.+?)\s*$")


def extract_links(md_path: Path) -> list[MdLink]:
    links: list[MdLink] = []
    section = ""
    fence: str | None = None
    text = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, line in enumerate(text, start=1):
        fence = _is_in_code_fence(line, fence)
        if fence is not None:
            continue
        if (m_h := HEADING_RE.match(line)) is not None:
            section = m_h.group("text").strip()
        for m in MD_LINK_RE.finditer(line):
            raw = m.group(0)
            if raw.startswith("!"):
                continue
            url = m.group("url").strip()
            if url.startswith("mailto:") or url.startswith("tel:"):
                continue
            links.append(
                MdLink(
                    file=md_path,
                    line_no=i,
                    section=section,
                    text=m.group("text").strip(),
                    url=url,
                )
            )
        for m in AUTOLINK_RE.finditer(line):
            url = m.group("url").strip()
            links.append(
                MdLink(
                    file=md_path,
                    line_no=i,
                    section=section,
                    text=url,
                    url=url,
                )
            )
    return links


def resolve_url(url: str, base_url: str) -> str:
    if re.match(r"^https?://", url):
        return url
    if url.startswith("/"):
        b = urlparse(base_url)
        base_path = b.path.rstrip("/")
        new_path = f"{base_path}{url}"
        return urlunparse((b.scheme, b.netloc, new_path, "", "", ""))
    return urljoin(base_url.rstrip("/") + "/", url)


def _clean_numbered_segments(url: str) -> str:
    p = urlparse(url)
    parts = [seg for seg in p.path.split("/") if seg != ""]
    cleaned = [re.sub(r"^\d+\.(.+)$", r"\1", seg) for seg in parts]
    new_path = "/" + "/".join(cleaned)
    return urlunparse((p.scheme, p.netloc, new_path, p.params, p.query, p.fragment))


def _compute_page_base_url(md_path: Path, docs_root: Path, base_url: str) -> str:
    rel = md_path.relative_to(docs_root)
    parts = list(rel.parts)
    if parts:
        parts[-1] = parts[-1].rsplit(".", 1)[0]
    clean_parts = [re.sub(r"^\d+\.(.+)$", r"\1", p) for p in parts]
    b = urlparse(base_url)
    base_path = b.path.rstrip("/")
    page_path = "/" + "/".join(clean_parts)
    full_path = f"{base_path}{page_path}"
    return urlunparse((b.scheme, b.netloc, full_path, "", "", ""))


def _build_site_index(docs_root: Path, base_url: str) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for md in iter_markdown_files(docs_root, pattern="**/*.md"):
        url = _compute_page_base_url(md, docs_root, base_url)
        path = urlparse(url).path
        index[path] = md
    return index


def _slugify_heading(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9_]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if s and s[0].isdigit() and not s.startswith("_"):
        s = "_" + s
    if s.startswith("_"):
        m = re.match(r"^_(\d+(?:-\d+)+)(.*)$", s)
        if m:
            s = f"_{m.group(1).replace('-', '')}{m.group(2)}"
    if s.startswith("_"):
        s = "_" + re.sub(r"_+", "-", s[1:]).strip("-")
    else:
        s = re.sub(r"_+", "-", s).strip("-")
    return s


def _extract_ids_from_markdown(md_path: Path) -> set[str]:
    ids: set[str] = set()
    text = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in text:
        if (m := HEADING_RE.match(line)) is not None:
            ids.add(_slugify_heading(m.group("text").strip()))
        for m in re.finditer(r"(id|name)=[\"']([^\"']+)[\"']", line, re.IGNORECASE):
            ids.add(m.group(2))
    return ids


async def check_links(
    links: Sequence[MdLink],
    docs_root: Path,
    base_url: str,
    include_external: bool,
    concurrency: int,
    timeout_s: float,
) -> list[CheckResult]:
    sem = asyncio.Semaphore(concurrency)
    site_index = _build_site_index(docs_root, base_url)

    async def worker(link: MdLink) -> CheckResult:
        page_base = _compute_page_base_url(link.file, docs_root, base_url)
        if re.match(r"^https?://", link.url):
            resolved = link.url
        elif link.url.startswith("/"):
            b = urlparse(base_url)
            base_path = b.path.rstrip("/")
            new_path = f"{base_path}{link.url}"
            resolved = urlunparse((b.scheme, b.netloc, new_path, "", "", ""))
        elif link.url.startswith("#"):
            resolved = page_base + link.url
        else:
            resolved = urljoin(page_base.rstrip("/") + "/", link.url)
        is_external = re.match(r"^https?://", link.url) is not None
        if is_external and not include_external:
            return CheckResult(link, resolved, ok=True, status=None, error=None)

        async with sem:
            base_no_frag, frag = urldefrag(resolved)
            path = urlparse(base_no_frag).path
            target_md = site_index.get(path)
            if target_md is None:
                alt = urlparse(_clean_numbered_segments(base_no_frag)).path
                target_md = site_index.get(alt)
                if target_md is None:
                    return CheckResult(
                        link, resolved, ok=False, status=404, error="not-found"
                    )
            if frag:
                ids = _extract_ids_from_markdown(target_md)
                if frag not in ids:
                    return CheckResult(
                        link, resolved, ok=False, status=200,
                        error=f"anchor-not-found: #{frag}",
                    )
            return CheckResult(link, resolved, ok=True, status=200, error=None)

    tasks = [asyncio.create_task(worker(link)) for link in links]
    return await asyncio.gather(*tasks)


def format_result(res: CheckResult, project_root: Path) -> str:
    try:
        rel = res.link.file.relative_to(project_root)
    except ValueError:
        rel = res.link.file
    loc = f"{rel}:{res.link.line_no}"
    sec = f" | section: {res.link.section}" if res.link.section else ""
    if res.ok:
        return f"OK   {loc}{sec} -> {res.resolved}"
    status = res.status if res.status is not None else "ERR"
    err = f" ({res.error})" if res.error else ""
    return f"FAIL {loc}{sec} -> {res.resolved} [status={status}]{err}"


def _http_fetch(url: str, timeout_s: float) -> tuple[int, str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "atlasmd-link-checker/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            status = getattr(resp, "status", 200)
            body = None
            if status == 200:
                try:
                    body = resp.read().decode("utf-8", errors="ignore")
                except Exception:
                    body = None
            return status, body
    except urllib.error.HTTPError as e:
        status = getattr(e, "code", 0) or 0
        try:
            body = e.read().decode("utf-8", errors="ignore")
        except Exception:
            body = None
        return status, body
    except urllib.error.URLError:
        return 0, None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check markdown links in AtlasMD documentation."
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        required=True,
        help="Path to the documentation content directory to scan.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Base URL for resolving relative links (default: {DEFAULT_BASE_URL}).",
    )
    parser.add_argument(
        "--include-external",
        action="store_true",
        help="Also check external http(s) links (off by default).",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=30,
        help="Maximum concurrent HTTP requests (default: 30).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Per-request timeout in seconds (default: 10.0).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root for relative path display (default: docs-root parent).",
    )
    args = parser.parse_args(argv)

    root: Path = args.docs_root
    base_url: str = args.base_url

    if not root.exists() or not root.is_dir():
        print(f"error: content root not found: {root}")
        return 2

    files = sorted(iter_markdown_files(root, pattern="**/*.md"))
    all_links: list[MdLink] = []
    for f in files:
        all_links.extend(extract_links(f))

    print(
        f"Scanning {len(files)} files, found {len(all_links)} links. Base: {base_url}"
    )

    results = asyncio.run(
        check_links(
            all_links,
            docs_root=root,
            base_url=base_url,
            include_external=args.include_external,
            concurrency=args.concurrency,
            timeout_s=args.timeout,
        )
    )

    project_root = args.project_root if args.project_root else root.parent
    broken = [r for r in results if not r.ok]

    # second pass: http verification to filter false failures due to redirects
    base_host = urlparse(base_url).netloc
    filtered: list[CheckResult] = []
    for r in broken:
        p = urlparse(r.resolved)
        if p.scheme.startswith("http") and p.netloc == base_host:
            base_no_frag, frag = urldefrag(r.resolved)
            status, body = _http_fetch(base_no_frag, timeout_s=args.timeout)
            if status == 200:
                if not frag:
                    continue
                if body and re.search(rf"id=\"{re.escape(frag)}\"", body):
                    continue
        filtered.append(r)
    broken = filtered

    for r in broken:
        print(format_result(r, project_root))

    print()
    print(f"OK: {len(results) - len(broken)}  |  FAIL: {len(broken)}")

    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
