#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Markdown link checker for the Tech Guide.

Scans markdown files under the content directory, extracts links, resolves them
against a base URL, and checks their HTTP status concurrently. Reports broken
links with file, section, and line context.

Usage examples:
  uv run python docs/tech-guide/support/check-broken-links.py
  uv run python docs/tech-guide/support/check-broken-links.py \
    --base-url http://localhost:3003/site-tech-guide --concurrency 50

Exit code is non-zero if any broken links are found.

Finds the following problems:
- Broken links (HTTP 4xx/5xx)
- Broken anchors (target page returns 200 but the anchor id is not present)
- Unreachable links (timeouts, DNS failures, connection errors)

"""

import asyncio
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

# defaults aligned with a local dev setup; override via --base-url
DEFAULT_BASE_URL = "http://localhost:3003"

# directory layout: this script lives in docs/tech-guide/support/
# content is at docs/tech-guide/content/
DEFAULT_DOCS_ROOT = Path(__file__).resolve().parent.parent / "content"


@dataclass(frozen=True)
class MdLink:
    """A markdown link occurrence.

    Attributes:
        file: Path to the markdown file containing the link.
        line_no: 1-based line number of the link.
        section: The most recent heading text (e.g., from `# Title`).
        text: The link text (label) from `[text](url)`.
        url: The raw URL as written in markdown.
    """

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
    """Generate possible anchor ids using a single normalization rule.

    Rule (matches fixer):
      - lowercase
      - if starts with a digit and no leading underscore, prefix with '_'
      - preserve a single leading underscore if present
      - convert remaining underscores to dashes
      - trim extraneous leading/trailing dashes

    Returns a small set: [original-lowercased, normalized].
    """

    f = frag.lower()

    # normalized (mirror fixer)
    nf = f
    if nf and nf[0].isdigit() and not nf.startswith("_"):
        nf = "_" + nf
    # collapse numeric groups like 3-3 or 3-3-1 at the beginning into 33 or 331
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

    cands: list[str] = []
    cands.append(f)
    if nf != f:
        cands.append(nf)

    # de-duplicate while keeping order
    seen = set()
    uniq: list[str] = []
    for x in cands:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def iter_markdown_files(root: Path, pattern: str = "**/*.md") -> Iterator[Path]:
    """Yield markdown files under a root matching a glob pattern.

    Args:
        root: Directory to search under.
        pattern: Glob to include files.

    Yields:
        Paths to markdown files.
    """

    yield from root.glob(pattern)


def _is_in_code_fence(line: str, fence_state: str | None) -> str | None:
    """Track fenced code block state for markdown parsing.

    Args:
        line: Current line.
        fence_state: Current fence marker (``` or ~~~) or None if outside.

    Returns:
        Updated fence state.
    """

    # detect opening/closing fences using backticks or tildes
    m = re.match(r"^(\s*)([`~]{3,})(.*)$", line)
    if m:
        fence = m.group(2)[0]  # ` or ~
        marker = fence * len(m.group(2))
        if fence_state is None:
            return marker
        # close only if the same fence is used
        if fence_state[0] == fence:
            return None
    return fence_state


MD_LINK_RE = re.compile(
    r"(?<!\\)!?\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)(?:\s+\"[^\"]*\")?\)",
)

AUTOLINK_RE = re.compile(r"<(?P<url>https?://[^>\s]+)>")

HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<text>.+?)\s*$")


def extract_links(md_path: Path) -> list[MdLink]:
    """Extract links from a markdown file with context.

    Skips image links, mailto/tel schemes, and links inside code fences.

    Args:
        md_path: Path to a markdown file.

    Returns:
        A list of `MdLink` occurrences.
    """

    links: list[MdLink] = []
    section = ""
    fence: str | None = None

    text = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, line in enumerate(text, start=1):
        fence = _is_in_code_fence(line, fence)
        if fence is not None:
            continue

        # track latest heading
        if (m_h := HEADING_RE.match(line)) is not None:
            section = m_h.group("text").strip()

        # standard markdown links (ignore images)
        for m in MD_LINK_RE.finditer(line):
            raw = m.group(0)
            if raw.startswith("!"):
                continue  # image
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

        # autolinks like <https://example.com>
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
    """Resolve a markdown URL relative to a base site URL.

    Rules:
      - Absolute http(s) URLs are returned as-is.
      - Root-relative paths (starting with '/') are joined to base host.
      - Pure anchors ('#...') are resolved against base_url (left as-is path).
      - Relative paths ('../x', 'x/y') are joined to base_url path.

    Args:
        url: The markdown URL.
        base_url: The base site URL.

    Returns:
        A fully qualified URL string.
    """

    if re.match(r"^https?://", url):
        return url

    # special handling: root-relative paths should retain the base path prefix
    # e.g., base=http://h/site-tech-guide, url=/overview -> http://h/site-tech-guide/overview
    if url.startswith("/"):
        b = urlparse(base_url)
        base_path = b.path.rstrip("/")
        new_path = f"{base_path}{url}"
        return urlunparse((b.scheme, b.netloc, new_path, "", "", ""))

    # treat anchors and relative paths via urljoin against the full base
    return urljoin(base_url.rstrip("/") + "/", url)


# http checking removed: we resolve links to filesystem only


def _clean_numbered_segments(url: str) -> str:
    """Remove numeric prefixes like '3.' from each path segment.

    Example: /developers/5.features/rr-scheduling -> /developers/features/rr-scheduling
    """

    p = urlparse(url)
    parts = [seg for seg in p.path.split("/") if seg != ""]
    cleaned = [re.sub(r"^\d+\.(.+)$", r"\1", seg) for seg in parts]
    new_path = "/" + "/".join(cleaned)
    return urlunparse((p.scheme, p.netloc, new_path, p.params, p.query, p.fragment))


def _compute_page_base_url(md_path: Path, docs_root: Path, base_url: str) -> str:
    """Compute the site URL for a given markdown file.

    Example: content/7.developers/5.features/rr-scheduling.md ->
      {base}/developers/features/rr-scheduling
    """

    rel = md_path.relative_to(docs_root)
    parts = list(rel.parts)
    # drop extension from last part
    if parts:
        parts[-1] = parts[-1].rsplit(".", 1)[0]
    # remove numeric prefixes like '7.' from each path segment
    clean_parts = [re.sub(r"^\d+\.(.+)$", r"\1", p) for p in parts]

    # join with base_url preserving its existing base path
    b = urlparse(base_url)
    base_path = b.path.rstrip("/")
    page_path = "/" + "/".join(clean_parts)
    full_path = f"{base_path}{page_path}"
    return urlunparse((b.scheme, b.netloc, full_path, "", "", ""))


def _build_site_index(docs_root: Path, base_url: str) -> dict[str, Path]:
    """Build a mapping from site paths to markdown files.

    Example key: "/site-tech-guide/developers/features/rr-scheduling"
    """

    index: dict[str, Path] = {}
    b = urlparse(base_url)
    base_path = b.path.rstrip("/")
    for md in iter_markdown_files(docs_root, pattern="**/*.md"):
        url = _compute_page_base_url(md, docs_root, base_url)
        path = urlparse(url).path
        index[path] = md
    return index


def _slugify_heading(text: str) -> str:
    """Generate a strict id for a markdown heading text.

    Rules modeled after our fixer and site behavior:
      - lowercase
      - replace any non [a-z0-9_] with dash
      - collapse multiple dashes
      - trim leading/trailing dashes
      - if starts with digit, prefix underscore
      - collapse starting numeric groups like "3-3-1" to "331"
    """

    s = text.strip().lower()
    # keep digits/letters/underscore, others to '-'
    s = re.sub(r"[^a-z0-9_]", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if s and s[0].isdigit() and not s.startswith("_"):
        s = "_" + s
    if s.startswith("_"):
        m = re.match(r"^_(\d+(?:-\d+)+)(.*)$", s)
        if m:
            s = f"_{m.group(1).replace('-', '')}{m.group(2)}"
    # convert remaining underscores (except leading) to dashes
    if s.startswith("_"):
        s = "_" + re.sub(r"_+", "-", s[1:]).strip("-")
    else:
        s = re.sub(r"_+", "-", s).strip("-")
    return s


def _extract_ids_from_markdown(md_path: Path) -> set[str]:
    """Collect candidate anchor ids from markdown source.

    - Generated from headings using _slugify_heading
    - Explicit id/name attributes in inline HTML
    """

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
    base_url: str,
    include_external: bool,
    concurrency: int,
    timeout_s: float,
    try_clean_slugs: bool = True,
) -> list[CheckResult]:
    """Check links concurrently with bounded concurrency.

    Args:
        links: Links to check.
        base_url: Base URL for resolving relative paths.
        include_external: Whether to check external http(s) links.
        concurrency: Maximum concurrent HTTP requests.
        timeout_s: Per-request timeout in seconds.

    Returns:
        List of `CheckResult`.
    """

    sem = asyncio.Semaphore(concurrency)
    # build index of site path -> markdown file
    site_index = _build_site_index(DEFAULT_DOCS_ROOT, base_url)

    async def worker(link: MdLink) -> CheckResult:
        page_base = _compute_page_base_url(link.file, DEFAULT_DOCS_ROOT, base_url)
        # resolve against the current page for relative/anchor links
        if re.match(r"^https?://", link.url):
            resolved = link.url
        elif link.url.startswith("/"):
            # root-relative: keep the base path of the site
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
            # resolve to filesystem path via site index
            base_no_frag, frag = urldefrag(resolved)
            path = urlparse(base_no_frag).path
            target_md = site_index.get(path)
            if target_md is None:
                # try cleaning numbered segments in the link path as a fallback
                alt = urlparse(_clean_numbered_segments(base_no_frag)).path
                target_md = site_index.get(alt)
                if target_md is None:
                    return CheckResult(
                        link,
                        resolved,
                        ok=False,
                        status=404,
                        error="not-found",
                    )

            # anchor checking
            if frag:
                ids = _extract_ids_from_markdown(target_md)
                if frag not in ids:
                    # Strict behavior: require exact match against ids extracted from markdown
                    # Slug rules applied when extracting ids from headings:
                    # - lowercase all characters
                    # - replace any char not in [a-z0-9_] with '-'
                    # - collapse multiple consecutive dashes to a single dash
                    # - trim leading and trailing dashes
                    # - if the result starts with a digit, prefix a single leading underscore
                    # - collapse starting numeric groups like 4.2.2. into 422 (keeps leading underscore)
                    # - convert underscores to dashes except for the single leading underscore if present
                    return CheckResult(
                        link,
                        resolved,
                        ok=False,
                        status=200,
                        error=f"anchor-not-found: #{frag}",
                    )

            return CheckResult(link, resolved, ok=True, status=200, error=None)

    tasks = [asyncio.create_task(worker(link)) for link in links]
    return await asyncio.gather(*tasks)


def format_result(res: CheckResult, project_root: Path) -> str:
    """Human-readable single line output for a result."""

    rel = res.link.file.relative_to(project_root)
    loc = f"{rel}:{res.link.line_no}"
    sec = f" | section: {res.link.section}" if res.link.section else ""
    if res.ok:
        return f"OK   {loc}{sec} -> {res.resolved}"
    status = res.status if res.status is not None else "ERR"
    err = f" ({res.error})" if res.error else ""
    return f"FAIL {loc}{sec} -> {res.resolved} [status={status}]{err}"


def _http_fetch(url: str, timeout_s: float) -> tuple[int, str | None]:
    """Fetch a URL and return status and body snippet.

    Args:
        url: Fully qualified URL.
        timeout_s: Timeout seconds.

    Returns:
        Tuple (status_code, body_text_or_none).
    """

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
            # only read body when 200 to allow anchor checks
            if status == 200:
                try:
                    body = resp.read().decode("utf-8", errors="ignore")
                except Exception:
                    body = None
            return status, body
    except urllib.error.HTTPError as e:
        # HTTPError is also a file-like object; capture status
        status = getattr(e, "code", 0) or 0
        try:
            body = e.read().decode("utf-8", errors="ignore")
        except Exception:
            body = None
        return status, body
    except urllib.error.URLError:
        return 0, None


def main(argv: Sequence[str] | None = None) -> int:
    """Entrypoint.

    Returns:
        Process exit code (0 when all links are OK, 1 otherwise).
    """

    # assume defaults; no CLI args
    root: Path = DEFAULT_DOCS_ROOT
    base_url: str = DEFAULT_BASE_URL
    include_external: bool = False
    concurrency: int = 30
    timeout_s: float = 10.0
    try_clean_slugs: bool = True

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
            base_url=base_url,
            include_external=include_external,
            concurrency=concurrency,
            timeout_s=timeout_s,
            try_clean_slugs=try_clean_slugs,
        )
    )

    project_root = Path(__file__).resolve().parents[3]  # repository root
    broken = [r for r in results if not r.ok]

    # second pass: http verification to filter false failures due to redirects
    # we only verify against the same host as base_url
    base_host = urlparse(base_url).netloc
    filtered: list[CheckResult] = []
    for r in broken:
        p = urlparse(r.resolved)
        if p.scheme.startswith("http") and p.netloc == base_host:
            base_no_frag, frag = urldefrag(r.resolved)
            status, body = _http_fetch(base_no_frag, timeout_s=timeout_s)
            if status == 200:
                if not frag:
                    # page exists via http (likely redirected); treat as ok
                    continue
                # verify anchor presence in rendered html
                if body and re.search(rf"id=\"{re.escape(frag)}\"", body):
                    continue
        # keep as real failure
        filtered.append(r)
    broken = filtered

    # only output failures
    for r in broken:
        print(format_result(r, project_root))

    print()
    print(f"OK: {len(results) - len(broken)}  |  FAIL: {len(broken)}")

    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
