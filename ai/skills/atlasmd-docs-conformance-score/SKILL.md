---
name: atlasmd-docs-conformance-score
description: Scores documentation against the AtlasMD Documentation Standard. Produces a quality score, a conformance score, and detailed per-section analysis with improvement feedback. Load when auditing or benchmarking a documentation set.
---

# atlasmd-docs-conformance-score

Scores a documentation set against the AtlasMD Documentation Standard. Produces two headline scores — **Quality** and **Conformance** — plus a detailed per-section breakdown with actionable improvement feedback. The goal is to be a helpful guide, not a harsh critic: the ultimate objective is better docs.

## When to Load

Load this skill when the user asks to:
- Score, grade, benchmark, or audit documentation against the standard
- Get a conformance report for a documentation set
- Measure how well docs follow the AtlasMD Documentation Standard
- Produce a documentation health report

## Philosophy

This skill is a **helpful guide, not a harsh critic**. The purpose of scoring is to identify where docs can improve and to give concrete, actionable feedback — not to punish. Scores are honest but framed constructively. Every finding includes a suggestion for how to improve.

## Prerequisites

Before scoring, you **must**:

1. **Load the `atlasmd-docs` skill** and read the standard file at `atlasmd-doc-standards/DOCUMENTATION-STANDARD.md`. The standard is the source of truth for all conformance criteria.
2. **Read the relevant standard sections** based on what the documentation set contains (use the task index in the `atlasmd-docs` skill to identify which sections apply).

## Workflow

### Step 1: Identify the project type and guide configuration

This is the **first and most important step**. Before scoring anything, determine:

1. **Guide type**: Is this a User Guide only, a Tech Guide only, or both guides (User Guide as primary, Tech Guide under a "Developers" section)?
2. **What sections the standard mentions are present**: Does the project have API reference pages? Data model pages? Integration pages? Configuration pages? Release notes? Glossary? Landing pages? Overview pages? Building block / conceptual pages?
3. **What sections are absent**: Note which standard page types and sections the project does **not** include.

**Critical rule — do not penalize for absence**: If the project is a User Guide only, do not judge it for lacking API reference, data model, or other Tech Guide page types. If it is a Tech Guide only, do not judge it for lacking how-to guides, screenshots, or other User Guide page types. If a section the standard mentions is not present (e.g., no API reference), **mention that it is absent as an observation, but do not include it in the scoring**. Only score what is present.

Record the project type and present/absent sections at the top of the report.

### Step 2: Run the link checker as a sub-agent

Launch a background sub-agent to run the link-checking scripts from the `atlasmd-docs-link-checker` skill. The sub-agent should:

1. Run `fix-common-links.py` first (to normalize links and reduce false positives)
2. Run `check-broken-links.py` second (to find actually broken links)
3. Return: total links checked, number of OK links, number of broken links, and the full list of broken links with file, line, section, resolved URL, and failure type

While the link checker runs in the background, proceed with the content and structure analysis (Steps 3-5). Collect the link checker results when the sub-agent completes.

**If the number of broken links is large** (more than ~20), write the full broken-links list to a separate file (e.g., `conformance-report-broken-links.md` in the project root or a reports directory) and reference that file in the report instead of inlining the entire list. Include a summary count in the report body.

### Step 3: Analyze each present section against the standard

For each section / page type that is **present** in the documentation set, evaluate conformance against the relevant standard sections. Use the task index in the `atlasmd-docs` skill to identify which standard sections apply to each page type.

For each present section, evaluate:

#### Conformance criteria (structural and formatting)

- **Frontmatter**: Has `title` and `description`; title is Title Case; description is one sentence under 150 characters; title matches H1
- **Page anatomy**: One H1; opening paragraph answers what/why/what-reader-sees; H2 sections numbered (`## 1.`, `## 2.`); H3 sub-numbered (`### 1.1.`); no skipped heading levels; no deeper than H4
- **Closing sections**: Conceptual pages have Next Steps; Additional Resources before References when both exist; reference pages have References only; landing pages have unnumbered References only
- **Tables**: Visually aligned; header row present; em-dash for N/A; backticks for identifiers; `string | null` notation for nullable types
- **Diagrams**: Mermaid default; introducing paragraph before; explanation paragraph after; labeled nodes; subgraphs for grouping
- **Code blocks**: Language tag specified; short and relevant; real values not placeholders; plain block for directory trees
- **Notes**: Blockquote with **Note:** or native admonition; one idea per note; used for gotchas not general info
- **Side notes**: Standard labels (Process Flow, Step-by-Step, Reference, Alternative Method); placed immediately before labeled content
- **Figures**: Numbered with "Figure N: " captions; alt text; light/dark variants; SVG for diagrams, PNG/WebP for screenshots; under 500 KB
- **Source references**: Footnote syntax `[^N]`; defined in References section; link + description after em-dash; sequential numbering
- **Lists**: Numbered for processes (actor + one action per step); bullets for unordered (bold term + colon + description); max two levels of nesting
- **Links and cross-references**: No URLs in body text unless explaining a concept about the URL itself; external links in footnotes or Additional Resources; cross-guide links point to correct guide; glossary terms cross-referenced on first introduction
- **Directory structure**: Numbered sections; numbered files (`N.title.md` dot format); index/overview files with `0.` prefix; `_dir.yml` metadata where applicable
- **Accessibility**: Semantic structure; color not sole carrier of meaning; WCAG 2.1 AA contrast; keyboard-reachable interactive elements; accessible code blocks
- **Discoverability**: Stable lowercase hyphen-separated URLs; no file extensions; descriptive searchable headings; description under 150 characters

#### Quality criteria (content and writing)

- **Clarity**: Explanations are clear and understandable; a reader can follow without external context
- **Accuracy**: Statements match the system being documented (verify against code/config where feasible)
- **Completeness**: Happy path, edge cases, and error conditions documented; no obvious gaps
- **Writing style**: Active voice; same word for same thing; concrete examples before abstract explanations; short noun groups; no AI-sounding phrases; no emojis
- **Audience focus**: Content matches its audience (User Guide vs Tech Guide); no audience mixing
- **Depth**: Explanations are thorough enough for the audience without being padded
- **Wording**: Precise, natural, human voice; not robotic or formulaic

### Step 4: Score each section

For each present section, produce:

1. **Section conformance score** (0-100): How well the section follows the structural and formatting rules in the standard. Based only on criteria that apply to this page type.
2. **Section quality score** (0-100): How good the content is — clarity, accuracy, completeness, writing style, wording, depth, audience focus.
3. **Findings list**: Specific issues found, each with:
   - **What**: The issue, described precisely (file, line, heading if applicable)
   - **Severity**: `critical` | `important` | `minor`
   - **Suggestion**: Concrete, actionable advice on how to fix or improve it
4. **Strengths**: What the section does well (always include positives — this is a helpful guide)

### Step 5: Produce the link checker score

From the sub-agent results, produce a **Link Health score** (0-100):

```
Link Health = (OK links / total links checked) * 100
```

Include in the report:
- Total links checked
- OK count
- Broken count
- Breakdown by failure type (not-found, anchor-not-found, unreachable)
- If broken links > ~20: reference to the separate broken-links file
- If broken links <= ~20: list them inline in the report

### Step 6: Compute headline scores

#### Conformance Score (0-100)

The overall conformance score is the average of all **present** section conformance scores. Absent sections are **excluded** from the calculation — they are noted as observations but do not lower the score.

#### Quality Score (0-100)

The overall quality score is the average of all **present** section quality scores. Absent sections are **excluded**.

#### Link Health Score (0-100)

As computed in Step 5. This is reported separately and **included as a sub-score**, not folded into the conformance or quality score (so that a project with great content but broken links is not disproportionately penalized in the main scores, but the link issue is clearly visible).

### Step 7: Write the report

Produce a report in this structure:

```markdown
# Documentation Conformance Report

**Project**: [project name]
**Date**: [date]
**Reviewer**: atlasmd-docs-conformance-score

## Project Identification

- **Guide type**: User Guide only / Tech Guide only / Both (User Guide primary, Tech Guide under Developers)
- **Present sections**: [list]
- **Absent sections**: [list — noted as observations, not scored]

## Headline Scores

| Score | Value | Grade |
|-------|-------|-------|
| Quality | XX/100 | [A-F] |
| Conformance | XX/100 | [A-F] |
| Link Health | XX/100 | [A-F] |

### Grading scale

| Range | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent — meets the standard with minor or no issues |
| 80-89 | B | Good — solid foundation with some areas to improve |
| 70-79 | C | Fair — several issues that should be addressed |
| 60-69 | D | Needs work — significant gaps in conformance or quality |
| Below 60 | F | Major issues — substantial rework needed |

## Link Health

- Total links checked: N
- OK: N
- Broken: N
- Failure breakdown: not-found: N, anchor-not-found: N, unreachable: N

[If broken links > ~20: "Full list of broken links written to: [file path]"]
[If broken links <= ~20: list them inline]

## Section-by-Section Analysis

### [Section name]

**Conformance**: XX/100
**Quality**: XX/100

**Strengths**:
- [what it does well]

**Findings**:
- **[severity]** [what] — [suggestion]
- **[severity]** [what] — [suggestion]

[Repeat for each present section]

## Absent Sections (Observations)

The following standard sections were not found in this documentation set. They are noted for awareness but do **not** affect the scores:

- [section name]: [brief note on what it is and whether it might be relevant to add]

## Top Improvement Priorities

Ranked by impact on quality and conformance:

1. [priority] — [why] — [suggested action]
2. [priority] — [why] — [suggested action]
3. [priority] — [why] — [suggested action]

## Summary

[2-3 paragraph narrative summary. Honest but constructive. Acknowledge what is working well, identify the most impactful areas for improvement, and frame the path forward positively. The goal is better docs.]
```

## Scoring Guidelines

### How to assign section scores

- **90-100**: Section fully conforms to the standard for its page type. Content is clear, accurate, complete, and well-written. Minor issues only.
- **80-89**: Section largely conforms. A few formatting or structural issues. Content quality is good with minor clarity or completeness gaps.
- **70-79**: Section partially conforms. Several structural or formatting issues. Content is adequate but has noticeable clarity, accuracy, or completeness problems.
- **60-69**: Section has significant conformance issues. Multiple standard rules not followed. Content quality is inconsistent.
- **Below 60**: Section largely does not conform. Major structural problems. Content quality is poor.

### Severity definitions

- **critical**: Wrong or misleading information; broken fundamental structure; content that would confuse or mislead a reader.
- **important**: Notable conformance violations or quality issues that should be fixed but do not make the docs unusable.
- **minor**: Small issues, polish opportunities, or best-practice suggestions.

### What to include in findings

Every finding must have a **suggestion** — never just point out a problem without offering a path forward. Suggestions should be specific and actionable:

- **Good**: "The opening paragraph on `3.api-reference/1.overview.md` jumps straight into endpoint lists without explaining what the API is. Add 2-3 sentences answering what the API does, why it exists, and what the reader will find on this page."
- **Bad**: "Opening paragraph needs improvement."

## Important Rules

1. **Identify project type first** — before any scoring. This determines what is scored and what is excluded.
2. **Never penalize for absent sections** — note them as observations only.
3. **Only score what is present** — conformance and quality scores are averages over present sections only.
4. **Always include strengths** — every section analysis must list what is done well.
5. **Always include suggestions** — every finding must have an actionable suggestion.
6. **Run the link checker as a sub-agent** — do not block the content analysis on it; run it in the background and collect results when done.
7. **Write large broken-link lists to a file** — if more than ~20 broken links, write to a separate file and reference it.
8. **Be a helpful guide** — the tone is constructive and encouraging. The goal is better docs, not a grade to feel bad about.
9. **Read the standard before scoring** — the standard is the source of truth. Do not score from memory.
10. **Judge wording and explanation quality** — not just structure. How good are the explanations? Is the wording natural and precise? Would a reader understand this?

## Related Skills

- **atlasmd-docs** — Index to the standard. Load this first to identify which standard sections apply.
- **atlasmd-docs-link-checker** — Provides the link-checking scripts run as a sub-agent in Step 2.
- **atlasmd-docs-analyzer-mode** — For interactive review and improvement sessions after the conformance report identifies areas to fix.
