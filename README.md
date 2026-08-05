<div align="center">

# AtlasMD

**A documentation standard. A rendering engine that publishes it. A maintenance process that keeps it current.**

[![License: MIT](https://img.shields.io/badge/License-MIT-020420.svg?style=flat&colorA=020420&colorB=00DC82)](https://github.com/joaomcarlos/AtlasMD/blob/main/atlasmd-renderer/package.json)
[![Docker](https://img.shields.io/badge/Docker-atlasmd%3Alatest-020420.svg?style=flat&colorA=020420&colorB=2496ED&logo=docker&logoColor=white)](#atlasmd-renderer)
[![Nuxt](https://img.shields.io/badge/Nuxt-3.x-020420.svg?style=flat&colorA=020420&colorB=00DC82&logo=nuxt.js&logoColor=white)](https://nuxt.com)
[![Docus](https://img.shields.io/badge/Docus-1.x-020420.svg?style=flat&colorA=020420&colorB=00DC82)](https://docus.dev)
[![Made with Vue](https://img.shields.io/badge/Made%20with-Vue-020420.svg?style=flat&colorA=020420&colorB=42b883&logo=vue.js&logoColor=white)](https://vuejs.org)

</div>

---

Most documentation is a set of markdown files that someone wrote once and nobody maintains. It goes out of sync with the code, the links break, the screenshots go out of date, and the structure follows whatever the first author chose that day. Six months in, it is a set of good intentions. A year in, it is a risk.

AtlasMD is the answer to that. It is not a "docs tool." It is an engineering discipline, delivered as software.

Two things in one repository:

1. **Documentation standard** — framework-agnostic, opinionated, and strict. It defines how to structure content, how to build pages, how to write prose, how to keep the site accessible, how to align versions, and how to keep maintenance recurring. Implement it in Docus, MkDocs, Docusaurus, Antora, or a stack of static HTML files if you want. The standard does not care about your framework. It cares about your discipline.
2. **A rendering engine** — a Docus/Nuxt application sealed inside a Docker image. You mount your Markdown. It gives you a themed, searchable, dark-mode-ready, WCAG-AA-compliant documentation site. No `node_modules`. No build pipeline. No frontend dependencies to maintain. No JavaScript knowledge required from the people writing the docs.

The standard defines the structure. The engine renders it. The result is documentation that does not go out of date — because the structure prevents it, the tooling catches it, and the maintenance process enforces it.

> This README is rendered by AtlasMD. The site you get from running the scaffold is the very documentation you are reading. The engine documents itself. If the tool cannot document itself, it cannot document anything.

## Table of Contents

- [AtlasMD](#atlasmd)
  - [Table of Contents](#table-of-contents)
  - [The Problem AtlasMD Solves](#the-problem-atlasmd-solves)
  - [The AtlasMD Documentation Standard](#the-atlasmd-documentation-standard)
    - [Scope: User Guide, Tech Guide, or Both](#scope-user-guide-tech-guide-or-both)
    - [Directory Structure](#directory-structure)
    - [Page Anatomy](#page-anatomy)
    - [Page Types](#page-types)
    - [Information Elements](#information-elements)
    - [Writing Style](#writing-style)
    - [Accessibility](#accessibility)
    - [Cross-References and Links](#cross-references-and-links)
    - [Search and Discoverability](#search-and-discoverability)
    - [Documentation Versioning](#documentation-versioning)
    - [Glossary](#glossary)
    - [Maintenance](#maintenance)
    - [Quick Reference Checklist](#quick-reference-checklist)
  - [The Rendering Engine](#the-rendering-engine)
  - [Repository Structure](#repository-structure)
  - [atlasmd-renderer](#atlasmd-renderer)
    - [Build the Image](#build-the-image)
    - [Configuration (Reference)](#configuration-reference)
      - [Config File](#config-file)
      - [Branding](#branding)
      - [Social Links](#social-links)
      - [Footer](#footer)
      - [Deployment](#deployment)
    - [Runtime Mounts](#runtime-mounts)
    - [Development](#development)
      - [Ports](#ports)
      - [Renderer vs. Scaffold](#renderer-vs-scaffold)
  - [atlasmd-scaffold](#atlasmd-scaffold)
    - [Quick Start](#quick-start)
    - [Add AtlasMD to Your Project](#add-atlasmd-to-your-project)
      - [1. Build the Image](#1-build-the-image)
      - [2. Copy the Scaffold](#2-copy-the-scaffold)
      - [3. Reference the Compose File](#3-reference-the-compose-file)
      - [4. Configure for Your Project](#4-configure-for-your-project)
      - [5. Add Content and Assets](#5-add-content-and-assets)
      - [6. Run](#6-run)
    - [Configuration (Consumer Setup)](#configuration-consumer-setup)
    - [Content Conventions](#content-conventions)
    - [Consumer Checklist](#consumer-checklist)
  - [AI Tooling](#ai-tooling)
  - [License](#license)

---

## The Problem AtlasMD Solves

Documentation does not fail because people write badly. It fails because the structure is wrong.

A page that covers too much. A section that mixes audiences — end users reading about database internals, developers reading about business workflows. A navigation tree that does not match the reader's mental model. A screenshot from three releases ago. A link that 404s. A glossary term defined differently on three pages. A version selector that does not exist. An owner who left the company two years ago.

These are not writing problems. They are engineering problems. You solve them the way you solve any engineering problem: with a specification, with tooling that enforces it, and with a process that keeps it current.

AtlasMD is that specification, that tooling, and that process.

- **The structure** — numbered sections, numbered files, a standard section set per guide type, metadata-driven navigation. The reader always knows where they are.
- **The pages** — frontmatter, one H1, an opening paragraph that orients, numbered sections that progress, closing sections that point forward. Every page has the same skeleton. The reader learns the shape once and navigates faster forever.
- **The prose** — active voice, same word for same thing, concrete before abstract, no emojis, no AI-sounding filler. The text is scannable, translatable, and searchable.
- **The accessibility** — WCAG 2.1 AA in both themes, keyboard navigation, semantic headings, alt text on every image. The site works for every reader, on every device, under every condition.
- **The versions** — documentation versioned with the product, version selector on every page, backports alongside code backports, end-of-life archival. A reader on version 2.3 gets the 2.3 docs, not the latest.
- **The maintenance** — ownership per section, review cycles per release, stale content detection via source references, automated checks on every PR. Drift is caught before the reader sees it.

## The AtlasMD Documentation Standard

The full standard lives in [`atlasmd-doc-standards/DOCUMENTATION-STANDARD.md`](atlasmd-doc-standards/DOCUMENTATION-STANDARD.md). It is 1,165 lines across 13 sections. What follows is the substance of each, and the impact it has on the documentation site.

This is not a style guide. A style guide tells you whether to use Oxford commas. This is a structural specification. It tells you what a page must contain, in what order, for what audience, and how to verify it.

### Scope: User Guide, Tech Guide, or Both

A documentation set is one of three configurations:

- **User Guide only** — for end users and operators. How-to guides, workflows, screenshots. The reader interacts with the system but does not read code.
- **Tech Guide only** — for developers and integrators. APIs, data models, configuration, internals. The reader reads code and writes integrations.
- **Both** — the User Guide is the root. The Tech Guide lives under a "Developers" section within the User Guide's navigation. The reader browsing the docs lands on user-facing content first. The Tech Guide is reachable, not peer.

When both guides exist, they are separate content trees sharing a single navigation. A user guide page that needs technical depth links to the tech guide: `For technical details, see the [Tech Guide](/developers/...)`. Content is never duplicated. Write it once in the guide it serves, link from the other.

**Impact:** Reviewers identify the configuration first, then apply only the criteria that apply. A User Guide only project is not penalized for lacking API reference pages. A Tech Guide only project is not penalized for lacking screenshots. The standard adapts to the project, not the other way around.

### Directory Structure

Organize documentation into numbered top-level sections. The number controls display order. This is not cosmetic — it is deterministic.

```
content/
  0.index.md              # landing page
  1.getting-started/      # orientation
  2.understanding/        # conceptual deep-dive
  3.api-reference/        # contract reference
  4.integrations/         # per-system integration pages
  5.development/          # config, testing, deployment
  6.additional-resources/ # learn-more section (optional)
  8.release-notes.md      # changelog (high number = end of file ordering)
```

Files inside a section use the same `N.title.md` convention. Dot separator, not hyphen — the dot format sorts correctly in file explorers and is compatible with more frameworks. Version-like artifacts use the version as the filename (`2.1.2.md`), because the version is the name.

Each directory has a metadata file (`_dir.yml` in Docus) with `title`, `description`, optional `icon` (top-level sections only — never subdirectories, never individual pages), and optional `redirect`. The `description` in the metadata file is the single source of truth for the section summary. Reuse it in landing page cards and cross-references. Do not paraphrase it elsewhere.

A numbering gap between the last regular section and release notes (5 then 8) leaves room to insert new sections without renumbering existing ones. Renumbering is a chore that introduces merge conflicts. The gap prevents it.

**Impact:** File explorers sort correctly. Navigation order is deterministic — no "why is this section third when it should be second?" debates. New sections slot in without touching existing files. The metadata description is written once and reused everywhere, so the section summary never goes out of sync between the nav, the landing page, and the cross-reference.

### Page Anatomy

Every page follows this structure, top to bottom. Not every page has every part, but the order is fixed. You do not improvise the structure.

1. **Frontmatter** — `title` (Title Case, matches the H1 exactly), `description` (one sentence — if you cannot describe the page in one sentence, the page covers too much and you split it), optional `navigation`, `noindex`, `layout`.
2. **H1 heading** — one per page. No exceptions. Matches the frontmatter title.
3. **Opening paragraph** — 1-3 paragraphs answering: What is this? Why does it exist? What is the reader looking at? Start with the subject directly. The opening paragraph is the reader's orientation — it tells them whether they are on the right page before they scroll.
4. **Numbered H2 sections** — `## 1.`, `## 2.`, ... Explanatory sections use "How [subject] [verb]". Reference sections use noun phrases ("API Endpoints", "Configuration Variables"). The section title describes the content.
5. **Sub-numbered H3 sections** — `### 1.1.`, `### 1.2.`, ... The sub-number includes the parent. No deeper than H4. If you need H5, the page is too long — split it into two pages.
6. **Closing sections** — Next Steps (links to related pages the reader should visit next), Additional Resources (external further reading), References (footnote definitions for source citations). When both Additional Resources and References exist, Additional Resources comes first. References is the last numbered section — it is the appendix, the least important to the reader's next action.

**Impact:** Readers reference specific parts by number ("see section 3.2"). Screen readers navigate a predictable heading hierarchy with no skipped levels. The opening paragraph tells the reader whether they are on the right page in three seconds. The one-sentence description rule forces page scope to stay narrow — if you cannot describe it in one sentence, it is two pages.

### Page Types

Different page types have different required sections. You do not write a landing page the same way you write an API reference. The standard defines eight templates:

- **Landing page** — cards, not prose. No Next Steps, no Additional Resources, no numbered References. The home page is a directory, not an essay.
- **Overview page** — conceptual introduction to a section. Has Next Steps.
- **Building block page** — one component or subsystem, explained end to end. Has Next Steps.
- **API reference page** — endpoint tables, request/response schemas. References only. No Next Steps — readers navigate by lookup, not by reading sequentially.
- **Data model page** — base model, per-table sections, references.
- **Integration page** — connection methods, identifiers, operations, post-processing, Next Steps, Additional Resources, References. The most structured page type.
- **Configuration page** — grouped variables with prefixes, references.
- **Release notes page** — version numbers as H2 (`## X.Y.Z`), category labels as H3 (`### Features`, `### Fixes`). No closing sections. A flat list of version entries.

**Impact:** Authors pick the right template for the right content. Reviewers check structure against the template — the template is the spec, the page is the implementation. Readers learn the shape of each page type and navigate faster on every subsequent visit.

### Information Elements

Each element has a specific purpose. Use the right element for the right content. This is not a suggestion — it is a rule.

| Element               | Purpose                                                                                                                                                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Tables**            | The primary structure for reference data: field definitions, endpoint lists, status codes, configuration variables, enum values. If it is reference data, it is a table.                                                                         |
| **Diagrams**          | Architecture overviews, system bridges, sequence flows, dependency graphs, state machines. Mermaid is the default — text-based, renders in-framework, diff-friendly in source control. A diagram that is a PNG is a diagram that nobody updates. |
| **Code blocks**       | Commands, configuration, directory trees, message payloads. Always tagged with a language. No language tag, no syntax highlighting.                                                                                                              |
| **Notes**             | Gotchas, constraints, tips the reader would regret missing. One idea per note. Used sparingly — if every paragraph has a note, notes stop working. They are not for general information.                                                         |
| **Side notes**        | Category labels for the content that follows: Process Flow (descriptive — what the system does), Step-by-Step (imperative — what the reader does), Reference, Alternative Method.                                                                |
| **Figures**           | Screenshots and image-rendered diagrams. Numbered, captioned ("Figure N: ..."), with alt text and optional dark-mode variant. Every figure has alt text — decorative images use empty alt so the screen reader skips them.                       |
| **Fields**            | Key/value definition lists for inline reference.                                                                                                                                                                                                 |
| **Simple cards**      | Card grids for navigation or feature highlights.                                                                                                                                                                                                 |
| **Source references** | Footnotes linking to source code. These are not just citations — they tie each page to the code file it documents, which enables stale content detection. Every footnote connects a page to the code file it documents.                          |

**Impact:** Reference data is scannable in a table, not buried in prose. Diagrams carry context before and explanation after — a diagram without context gives the reader no way to interpret it. Notes stay impactful because they are rare. Source references enable automated stale detection: when the code file changes, the tool flags the page that references it for review.

### Writing Style

The standard does not care about your Oxford commas. It cares about these:

- **Active voice.** Name the actor. "The system creates a record" not "A record is created." Passive voice hides responsibility and adds words.
- **Same word for same thing.** If you call it "export job" on page 1, call it "export job" on page 10. Do not vary terms to avoid repetition. Repetition aids clarity. Synonyms aid confusion.
- **Concrete before abstract.** Show the concrete thing, then the explanation. The reader understands the example, then the abstraction makes sense. Not the other way around.
- **Direct instructions.** State the condition, the action, the expected outcome. "Run `just test` to execute the test suite."
- **No metaphors or figures of speech.** Technical writing is literal. A metaphor that one reader gets is a metaphor that another reader misreads.
- **Short words and sentences.** If a short word works, use it. If a sentence can be shorter, make it shorter. If removing a word does not change the meaning, remove it.
- **No emojis.** Not in headings, not in body text, not in tables, not in notes. They render inconsistently across platforms, they do not translate, and they are not accessible.
- **No AI-sounding phrases.** The standard lists them by name:

| Avoid                            | Do instead                |
| -------------------------------- | ------------------------- |
| "Moving forward, ..."            | Start with the point      |
| "It's important to note that..." | State the thing directly  |
| "In this section, we will..."    | Start with the content    |
| "This page describes..."         | Start with the subject    |
| "As mentioned earlier..."        | Trust the reader's memory |
| "Let's dive into..."             | Start with the content    |
| "It's worth noting that..."      | State the thing directly  |
| "Please note that..."            | State the thing directly  |
| "Leverage" (as a verb)           | Use                       |
| "Utilize"                        | Use                       |
| "In order to"                    | To                        |

**Impact:** Prose is scannable, translatable, and searchable. Search engines and on-site search index the concrete terms readers actually type. Vale prose lint catches the banned phrases automatically — a failing check blocks the merge.

### Accessibility

Accessibility is a requirement, not an enhancement. Every page must be usable with a keyboard, readable by a screen reader, and legible at high contrast. If your docs do not work for a reader using a screen reader, your docs do not work.

- **Semantic structure** — one H1, no skipped heading levels, no bold-as-heading. Screen readers navigate by heading level. Skipping levels breaks navigation.
- **Tables** — every table has a header row. No tables for layout. Reading order matches visual order. Screen readers read cell by cell.
- **Images and diagrams** — every figure has alt text describing the relationships, not the visual layout. "The client sends a request to the service, which queries the database and returns a job ID" — not "a flowchart with three boxes and arrows." No color-only meaning — pair color with a text label, an icon, or a pattern.
- **Color and contrast** — WCAG 2.1 AA in both light and dark themes. 4.5:1 for normal text, 3:1 for large text. Code syntax highlighting must pass too. A color combination that passes in light mode may fail in dark mode — verify both.
- **Keyboard navigation** — every interactive element reachable with Tab. Visible focus indicator — never remove the default focus outline without a replacement. Tab order follows reading order. Skip-to-content links on pages with long navigation.
- **Code blocks** — focusable for horizontal scroll (`tabindex="0"` on `<pre>`). Text selection never disabled — readers copy code. Copy buttons have `aria-label`, not just an icon.
- **Automated verification** — accessibility regressions are bugs. Verify with a tool that checks the rendered output, not just the markdown source.

**Impact:** The site works for readers with different abilities, devices, and network conditions. Automated checks catch regressions before they reach production. Verify the dark theme, do not assume it. A reader using a keyboard only, or a screen reader, or a monochrome display, or a high-contrast theme gets the same information as everyone else.

### Cross-References and Links

- **Link text is descriptive.** `See the [Export Service](/understanding/building-blocks/export-service)` not `See [here](/...)`. Screen readers read link text out of context. "Here" means nothing.
- **No URLs in body text** unless the text explains a concept about the URL itself. Use link text.
- **Internal links are relative** (`/understanding/...`), not absolute (`https://site.com/understanding/...`). Relative links survive domain changes and version prefixes. Absolute links break.
- **Cross-guide links** point to the correct guide. User Guide links to Tech Guide and vice versa, with a note explaining the jump.
- **Source references use footnotes**, not inline links. Footnotes keep body prose clean and collect all source citations in the References section, where you can check them, map them to code files, and use them for stale detection.
- **Link checking is automated.** Broken links never reach production.

**Impact:** Links survive domain and version changes. Screen readers announce meaningful destinations. The checks catch broken links before they reach production.

### Search and Discoverability

- **URLs are stable, lowercase, hyphen-separated, no file extension.** Once published, a URL does not change. If you need to move a page, add a redirect.
- **Every page has a title and description under 150 characters** for search snippets. The description is the one-sentence frontmatter field.
- **Headings are descriptive, not vague.** "How the System Creates Jobs" not "Overview". Vague headings contain no searchable terms. Descriptive headings contain the terms a reader actually types.
- **Search engines index the opening paragraph after the H1 heavily.** Put the most important terms there. This is where Google and the site's own search look first.
- **Sitemap is generated explicitly.** Every published page is listed. The sitemap excludes pages with `noindex: true` and they carry a `<meta name="robots" content="noindex">` tag.
- **Hiding a page from navigation is not hiding it from search.** `navigation: false` removes a page from the sidebar. It does not add `noindex`. A page can be absent from navigation and still indexed — a standalone landing page linked from external sources, for example.
- **Built-in search is on every page.** It is the first interactive element in the header. The index covers titles, headings, and body text.

**Impact:** Readers find pages via Google and via the site's own search. URLs do not break. SEO and on-site search pull from the same descriptive headings and opening paragraphs. Control the sitemap, do not leave it to chance.

### Documentation Versioning

When the product has multiple supported versions, the documentation supports them too. A reader on version 2.3 needs the 2.3 docs, not the latest. This is not optional.

- **Version the documentation set alongside the product.** When the product releases 2.4, the docs have a 2.4 snapshot.
- **The latest version lives at the default URL.** Older versions live under a version prefix (`/2.3/...`). This avoids breaking existing links when you release a new version — the old latest moves to its prefixed URL, the new latest takes the default URL with a redirect from the old content.
- **Version selector on every page.** Lets the reader switch versions while staying on the same logical page. If the page does not exist in the selected version, redirect to the closest equivalent. If no equivalent exists, show a page that says the topic was introduced in a later version, with a link to the latest.
- **Version the whole set, not pieces.** A reader on 2.3 sees the 2.3 tech guide and the 2.3 user guide. Not 2.3 tech guide with 2.4 user guide.
- **Backport documentation alongside code.** A code backport without a docs backport leaves the older docs wrong. The backport is a separate commit against the older version's content tree. Record it in the older version's release notes.
- **End-of-life versions stay available but archived.** Pages carry a banner: `This version is no longer supported. See the [latest version](/...).` Do not delete end-of-life docs — readers on legacy systems still need them. Remove archived versions from the version selector after a grace period (e.g. one year), but keep the pages accessible by direct URL.

**Impact:** Readers on legacy systems find the docs that match their version. Links do not break when you release a new version. End-of-life docs do not disappear — mark them, do not delete them.

### Glossary

Every documentation set has a glossary page in the Getting Started section. It defines domain-specific terms, external system names, and project-specific terms. Group entries by category (H2 per category), list them alphabetically within each category, and define them in one or two sentences. If it takes more than two sentences, it belongs in a building block page.

Other pages cross-reference the glossary when introducing a term for the first time. Link the term to the glossary entry.

**Impact:** Terms are defined once, in one place. Writers do not redefine terms on every page. Readers have a single lookup point. The glossary is versioned with the docs — terms change across versions.

### Maintenance

Documentation goes out of date. Code changes, pages do not, and the two go out of sync. Maintenance is the process of keeping them aligned. It is not a one-time cleanup. It is a recurring practice — the same way you do not test once, you do not review docs once.

- **Keep docs in sync.** A pull request that changes behavior includes the documentation update in the same pull request. Do not defer documentation to a follow-up. If the update is large, open a tracking issue in the same PR and link to it. Do not leave it untracked.
- **Preserve existing content.** Overwrite only when inaccurate, outdated, or conflicting. When you overwrite, replace — do not leave the old version alongside the new. Maintain consistency with the rest of the documentation set.
- **Ownership per section.** Recorded in `_dir.yml` or `CODEOWNERS` — one or the other, not both. The owner reviews accuracy first, then style. When ownership changes, update the record in the same change that transfers responsibility. A section without an owner is unmaintained — flag it in the build output.
- **Review cycles.** Each page records its last review date. A page older than two release cycles without a review is stale. A review checks accuracy, completeness, links, screenshots, and formatting.
- **Stale content.** Publish a stale page anyway — hiding it leaves the reader with nothing. It shows a notice: "This page may be out of date. Last reviewed [date]." The notice links to the owner or tracking issue. Remove the notice once a review confirms the page is current.
- **Automated checks.** The following checks verify the documentation:

| Check           | What it verifies                                     |
| --------------- | ---------------------------------------------------- |
| Link checking   | Broken internal and external links                   |
| Accessibility   | Missing alt text, contrast failures, keyboard issues |
| Markdown lint   | Heading order, trailing whitespace, list style       |
| Spelling        | Typos and inconsistent terms                         |
| Prose lint      | AI-sounding phrases, passive voice, banned words     |
| Screenshot diff | UI changes that make screenshots stale               |

Configure spelling and prose linters with a project dictionary so the linters do not flag domain terms and product names.

**Impact:** The checks catch pages that go out of sync before the reader sees them. Ownership is explicit — no "who wrote this?" questions. Stale pages are visible, not hidden. Automated checks enforce the standard consistently across every contributor, every PR, every time.

### Quick Reference Checklist

Before publishing a page, verify (full list is 33 items in the standard):

- [ ] Frontmatter has `title` and `description`
- [ ] One H1 heading, matching the frontmatter title
- [ ] Opening paragraph answers what, why, and what the reader is looking at
- [ ] Sections are numbered (`## 1.`, `## 2.`, ...)
- [ ] Sub-sections are sub-numbered (`### 1.1.`, `### 1.2.`, ...)
- [ ] Tables are visually aligned with correct column types
- [ ] Diagrams have an introducing paragraph before and an explanation after
- [ ] Code blocks have language tags
- [ ] Notes are used for gotchas, not for general information
- [ ] Side notes label the content that follows them
- [ ] Figures are numbered with captions and alt text
- [ ] Source references use footnotes, defined in the References section
- [ ] Conceptual pages have a Next Steps section
- [ ] No emojis, no AI-sounding phrases, active voice throughout
- [ ] Same word for same thing, concrete examples before abstract explanations
- [ ] All links are functional; no URLs in body text
- [ ] Heading hierarchy has no skipped levels
- [ ] Every table has a header row; no tables used for layout
- [ ] Every image has alt text (empty alt for decorative images)
- [ ] Color is not the sole carrier of meaning in diagrams and UI elements
- [ ] Text meets WCAG 2.1 AA contrast in both light and dark themes
- [ ] All interactive elements are keyboard-reachable with a visible focus indicator
- [ ] Description is under 150 characters for search snippets
- [ ] URL is stable, lowercase, hyphen-separated, no file extension
- [ ] Page owner is recorded and the last review date is current

---

## The Rendering Engine

The standard defines the structure. The engine renders it. The engine is a Docus/Nuxt application sealed inside a Docker image — you mount your Markdown, it gives you a documentation site.

```
Your Project                       AtlasMD Image
┌───────────────┐                 ┌──────────────────────────┐
│  content/     │── volume ─────▶ │  Nuxt + Docus            │──▶ Browser
│  public/      │── volume ─────▶ │  (renderer, prebuilt)    │
│  compose.yml  │                 └──────────────────────────┘
└───────────────┘
```

Consumer projects keep only Markdown files, `_dir.yml` navigation configs, and static assets. The AtlasMD image contains the entire rendering engine — Nuxt, Docus, Vue components, theme tokens, CSS, plugins — built in at build time.

This separation is the whole point:

- **Consumer repos stay tiny.** No `node_modules`. No `package.json`. No build pipeline. No frontend dependencies to audit, upgrade, or break.
- **Renderer upgrades happen in one place.** Rebuild the image once, every consumer picks it up. No "run `npm update` in 14 repos."
- **Content authors work in Markdown.** No Vue, no Nuxt, no JavaScript. The MDC components (`::note`, `::side-note`, `::fig`, `::field`, `::simple-card`, Mermaid) are the only non-Markdown syntax, and they map directly to the standard's information elements.
- **Hot reload via Docker Compose `develop.watch`.** Content and `public/` changes sync into the running container. No rebuild, no restart.

The engine provides MDC components that map one-to-one to the standard's information elements. See the **[Building Blocks](atlasmd-scaffold/content/2.building-blocks/)** section of the self-documentation for live-rendered examples of every component.

## Repository Structure

```
AtlasMD/
├── atlasmd-doc-standards/   # The documentation standard (framework-agnostic)
│   └── DOCUMENTATION-STANDARD.md   1,165 lines, 13 sections
│
├── atlasmd-renderer/        # The rendering engine — builds the `atlasmd:latest` image
│   ├── components/          #   Vue components (Logo + MDC content components)
│   ├── plugins/             #   Client plugins (scroll-behavior, sidebar-follow)
│   ├── assets/css/          #   Base styles and image CSS
│   ├── Dockerfile           #   Image definition
│   └── docker-compose.yml
│
├── atlasmd-scaffold/        # Template for consumer projects — copy this to start
│   ├── content/             #   Markdown files + _dir.yml navigation
│   │   ├── 1.getting-started/
│   │   ├── 2.building-blocks/       # Live-rendered component reference
│   │   ├── 3.configuration/
│   │   └── 4.development/
│   ├── public/              #   Favicons, logos, static images
│   └── docker-compose.yml
│
└── ai/                      # AI skills for working with the standard
    ├── agents.md
    └── skills/
        ├── atlasmd-docs/
        ├── atlasmd-docs-analyzer-mode/
        ├── atlasmd-docs-conformance-score/
        └── atlasmd-docs-link-checker/
```

## atlasmd-renderer

The rendering engine. Builds the `atlasmd:latest` Docker image. Contains every theme token, every Vue component, every plugin, every line of CSS, and the Nuxt config. Consumer repos never touch this. They consume it through the image. You use the engine, you do not modify it.

### Build the Image

```bash
cd atlasmd-renderer
docker compose build
```

This produces `atlasmd:latest`. You do this once. You do it again only when you upgrade the renderer.

The Dockerfile is deliberately simple — no multi-stage builds, no build-time secrets, no surprises:

```dockerfile
FROM node:lts-alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn YARN_CACHE_FOLDER=/root/.yarn yarn install
COPY . .
RUN mkdir -p content public
ENV PORT=3003
CMD ["yarn", "run", "dev"]
```

`content/` and `public/` are empty directories in the image. They are volume-mounted at runtime by consumer projects. The image is the engine; the content is the payload.

### Configuration (Reference)

The renderer reads consumer configuration from a TOML file at `/app/config.toml` (loaded by `config.ts` at startup). Only CI/build-driven values stay as environment variables. This is the complete reference — every setting the engine knows about. Consumer projects set the ones they need in their scaffold's `config.toml` (see [atlasmd-scaffold](#atlasmd-scaffold)).

#### Config File

```toml
title = "AtlasMD"

[[socials]]
url = "https://github.com/joaomcarlos/AtlasMD"
label = "View the AtlasMD repository"
icon = "simple-icons:gitlab"

# [[socials]]
# url = "https://example.slack.com/archives/C123"
# label = "Message us on Slack"
# icon = "simple-icons:slack"

# [footer.credits]
# text = "MyCompany"
# url = "https://example.com"
# icon = "heroicons-outline:cloud"

# [footer.text]
# label = "Built by MyCompany"
# url = "https://example.com"

# baseUrl = "/"
```

#### Branding

| Field               | Default | Purpose                                  |
| ------------------- | ------- | ---------------------------------------- |
| `title`             | `Atlas` | Project name in header and browser title |
| `APP_VERSION` (env) | —       | Version chip next to title (build arg)   |

Logos are convention-based fixed filenames in `public/` — no config needed:

| Theme state               | Filename                |
| ------------------------- | ----------------------- |
| Light mode                | `logo-light-mode.png`   |
| Dark mode                 | `logo-dark-mode.png`    |
| Dark mode with background | `logo-dark-mode-bg.png` |

#### Social Links

| Field             | Default | Purpose                                                              |
| ----------------- | ------- | -------------------------------------------------------------------- |
| `socials[].url`   | —       | Social link URL; add one `[[socials]]` block per link                |
| `socials[].label` | —       | Label for the social link                                            |
| `socials[].icon`  | —       | Iconify icon name (e.g. `simple-icons:gitlab`, `simple-icons:slack`) |

#### Footer

| Field                 | Default                   | Purpose                              |
| --------------------- | ------------------------- | ------------------------------------ |
| `footer.credits.text` | —                         | Footer credits text; omit to hide    |
| `footer.credits.url`  | —                         | Footer credits link URL              |
| `footer.credits.icon` | `heroicons-outline:cloud` | Footer credits icon                  |
| `footer.text.label`   | —                         | Footer text link label; omit to hide |
| `footer.text.url`     | —                         | Footer text link URL                 |

#### Deployment

| Field / Variable     | Default | Purpose                                                               |
| -------------------- | ------- | --------------------------------------------------------------------- |
| `baseUrl`            | `/`     | Base URL path (for GitLab Pages subpaths)                             |
| `CI_PAGES_URL` (env) | —       | GitLab Pages URL; set automatically by GitLab CI; overrides `baseUrl` |
| `PORT` (env)         | `3003`  | Port the dev server listens on                                        |

### Runtime Mounts

| Mount         | Container path     | Required                             |
| ------------- | ------------------ | ------------------------------------ |
| `content/`    | `/app/content`     | Yes — Markdown files and `_dir.yml`  |
| `public/`     | `/app/public`      | Yes — favicons, logos, static images |
| `config.toml` | `/app/config.toml` | Yes — consumer configuration         |

### Development

To develop the renderer itself or preview its self-documentation with hot reload:

```bash
cd atlasmd-scaffold
docker compose up
```

Open **http://localhost:8770**. Content and `public/` changes sync automatically via Docker Compose `develop.watch` — no rebuild, no restart, no extra steps.

To rebuild the image after renderer changes (components, CSS, plugins, Nuxt config):

```bash
cd atlasmd-renderer
docker compose build
```

#### Ports

| Host port | Container port | Purpose                    |
| --------- | -------------- | -------------------------- |
| `8770`    | `3003`         | Web server (HTTP)          |
| `8771`    | `4000`         | HMR websocket (hot reload) |

#### Renderer vs. Scaffold

- **Renderer changes** (theme, components, plugins, CSS) require an image rebuild. The engine changes, the image changes.
- **Scaffold changes** (content, `_dir.yml`, `public/` assets) do not. The runtime mounts them. The payload changes, the engine does not.
- Theme tokens, components, plugins, and CSS live in `atlasmd-renderer/` — never in consumer repos. You do not modify the engine while it runs.

## atlasmd-scaffold

The template for consumer projects. Contains the content structure, public assets, and a `docker-compose.yml` that mounts into the `atlasmd:latest` image. Also serves as AtlasMD's own self-documentation — the scaffold's `content/` folder is AtlasMD documenting itself, and it is a live, end-to-end reference for every convention the standard defines.

### Quick Start

The fastest way to see AtlasMD running:

```bash
git clone https://github.com/joaomcarlos/AtlasMD.git
cd AtlasMD/atlasmd-scaffold
docker compose up
```

Open **http://localhost:8770**. That is AtlasMD rendering its own docs, by its own engine, to its own standard. AtlasMD documents itself.

### Add AtlasMD to Your Project

#### 1. Build the Image

```bash
cd atlasmd-renderer
docker compose build
```

Produces `atlasmd:latest`. Once per renderer version.

#### 2. Copy the Scaffold

Copy `atlasmd-scaffold/` into your project and rename it to fit (e.g. `docs/`):

```bash
cp -r /path/to/AtlasMD/atlasmd-scaffold /path/to/your-project/docs
```

#### 3. Reference the Compose File

In your project's main `docker-compose.yml`, include the scaffold's compose file:

```yaml
include:
  - docs/docker-compose.yml
```

Or copy the service definition from `atlasmd-scaffold/docker-compose.yml` directly into your compose file and adjust the paths.

#### 4. Configure for Your Project

Edit `config.toml` for your project (see [Configuration (Consumer Setup)](#configuration-consumer-setup)) and adjust the volume mount paths to match where you placed the scaffold relative to your main compose file:

```yaml
volumes:
  - ./docs/content:/app/content
  - ./docs/public:/app/public
  - ./docs/config.toml:/app/config.toml
```

#### 5. Add Content and Assets

- Write Markdown files in `content/` using the `1.Title.md` naming convention. The numeric prefix controls ordering. The dot separator sorts correctly in file explorers.
- Add `_dir.yml` files in each directory for navigation metadata (`title`, `description`, `icon` for top-level only, `redirect` to the first content page).
- Place favicons and logos in `public/` — the site serves them at the root.

See the scaffold's own `content/` folder for a live, end-to-end example. It is the real documentation, written to the real standard, rendered by the real engine.

#### 6. Run

```bash
docker compose up
```

Open **http://localhost:8770**.

### Configuration (Consumer Setup)

Consumers set these in the scaffold's `config.toml`, mounted at `/app/config.toml`. The full reference with defaults is in [atlasmd-renderer](#configuration-reference). The typical consumer setup:

```toml
title = "My Project"

[[socials]]
url = "https://github.com/my-org/my-project"
label = "View the repository"
icon = "simple-icons:gitlab"
```

| Field                 | Set to                                    | Required             |
| --------------------- | ----------------------------------------- | -------------------- |
| `title`               | Your project name                         | Yes                  |
| `socials[].url`       | Social link URL                           | No — omit to hide    |
| `socials[].label`     | Label for the social link                 | No                   |
| `socials[].icon`      | Iconify icon name                         | No                   |
| `footer.credits.text` | Footer credits text                       | No — omit to hide    |
| `footer.text.label`   | Footer text link label                    | No — omit to hide    |
| `baseUrl`             | Base URL path (for GitLab Pages subpaths) | No — defaults to `/` |

Logos are convention-based — drop `logo-light-mode.png`, `logo-dark-mode.png`, and `logo-dark-mode-bg.png` into `public/` (no config needed). `APP_VERSION` stays an env var / build arg.

### Content Conventions

- `1.Title.md` filename format. Numeric ordering prefix, dot separator, title. Not hyphen — dot. The dot sorts correctly and is compatible with more frameworks.
- `_dir.yml` in each directory for navigation metadata. `title` and `description` are required. `icon` is top-level sections only — never subdirectories, never individual pages. `redirect` sends the reader to the first content page when they click the section name.
- MDC syntax for rich content: `::note`, `::side-note`, `::fig`, `::field`, `::simple-card`, `::example-component`, Mermaid diagrams, and Docus built-ins (`::block-hero`, `::card-grid`, `::card`). These map one-to-one to the standard's information elements.

### Consumer Checklist

- [ ] `atlasmd:latest` image built and available
- [ ] Scaffold copied into your project (e.g. `docs/`)
- [ ] Compose file referenced via `include:` or service definition copied
- [ ] `config.toml` set for your project
- [ ] Volume mount paths adjusted to match your layout
- [ ] Content written in `content/` using `1.Title.md` convention
- [ ] `_dir.yml` navigation configs added per section
- [ ] Logos and favicons placed in `public/` (logos use fixed filenames)
- [ ] Port `8770` does not conflict with other services

## AI Tooling

AtlasMD provides AI skills for working with the documentation standard. AI agents (Devin, Claude, Cursor, etc.) load these when editing, reviewing, or scoring documentation. The skills index the standard so the agent reads only the relevant sections for the task — it does not load 1,165 lines into context when you ask it to fix a link.

| Skill                            | Purpose                                                                                                                                        |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `atlasmd-docs`                   | Indexes the standard. Load when writing, editing, reviewing, or structuring docs. The agent reads only the sections relevant to the task type. |
| `atlasmd-docs-analyzer-mode`     | Interactive review session. Walks the agent through a page-by-page conformance check against the standard.                                     |
| `atlasmd-docs-conformance-score` | Scores and benchmarks documentation against the standard. Quantitative, not vibes.                                                             |
| `atlasmd-docs-link-checker`      | Checks and fixes broken links per the standard's cross-reference rules.                                                                        |

See `ai/agents.md` for the load instructions agents follow.

The `atlasmd-docs-link-checker` skill includes Python scripts for checking and fixing links:

- `check-broken-links.py` — scans markdown files for broken links and anchors.
- `fix-common-links.py` — normalizes link formatting (anchors, prefixes, heading numbering).

## License

[MIT](https://github.com/joaomcarlos/AtlasMD/blob/main/atlasmd-renderer/package.json) — see the `license` field in `atlasmd-renderer/package.json`.

<div align="center">

— The standard defines the structure. The engine renders it. The maintenance keeps it current. —

</div>
