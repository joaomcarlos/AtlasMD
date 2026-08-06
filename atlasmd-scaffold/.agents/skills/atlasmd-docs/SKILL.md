---
name: atlasmd-docs
description: Index to the AtlasMD Documentation Standard. Load when writing, editing, reviewing, or structuring documentation. Points to the exact standard sections to read for each task type.
---

# atlasmd-docs

Index to the AtlasMD Documentation Standard. Load when writing, editing, reviewing, or structuring documentation. Points to the exact standard sections to read for each task type.

## The Standard File

The standard lives at `atlasmd-doc-standards/DOCUMENTATION-STANDARD.md` in the AtlasMD repository. It is the single source of truth. This skill does not duplicate its content — it tells you which sections to read for the task at hand.

Read the standard file before making any documentation changes. Use the task index below to read only the relevant line ranges instead of loading the entire file every time. Line numbers refer to `DOCUMENTATION-STANDARD.md`.

## Task Index

Look up the task you are performing. Read the listed sections from the standard file before starting. When a task spans multiple categories, read all listed sections.

### Writing a new page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 1. Scope (all) | 5–41 | Guide types — identify if the project is User Guide only, Tech Guide only, or both |
| 2. Directory Structure (all) | 43–155 | Where the page goes, file naming, section metadata |
| 3. Page Anatomy (all) | 157–282 | Frontmatter, H1, opening paragraph, numbered sections, closing sections |
| 4. Page Types (match your page type) | 284–452 | Required structure for the specific page type you are writing |
| 5.11. AtlasMD Framework Components | 742–922 | MDC component syntax for notes, side notes, figures, fields, cards, snippets, AI prompts |
| 6. Writing Style (all) | 922–989 | Voice, tone, human voice, no emojis, concrete before abstract |
| 13. Quick Reference Checklist | 1290–1332 | Final verification before publishing |

### Writing a landing page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 3.1, 3.2, 3.3 | 161–210 | Frontmatter, H1, opening paragraph |
| 4.1. Landing Page | 288–297 | Template and rules for landing pages |
| 5.8. Landing Page Cards | 697–708 | Card grid structure, icon rules, description source |
| 3.6. Closing Sections | 245–282 | Landing page exception: unnumbered References only |

### Writing an overview page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.2. Overview Page | 299–313 | Template and required sections |
| 3. Page Anatomy (all) | 157–282 | General page structure |
| 6. Writing Style (all) | 922–989 | Voice and tone rules |

### Writing a building block / conceptual deep-dive page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.3. Building Block Page | 315–335 | Template with DTO tables, flow steps, edge cases |
| 5.1. Tables | 458–498 | Field definition tables, endpoint tables |
| 5.2. Diagrams | 500–581 | Architecture, sequence, state machine diagrams |
| 5.5. Side Notes | 616–644 | Process Flow, Step-by-Step labels |
| 5.11. AtlasMD Framework Components | 742–922 | `::field` for individual field definitions, `::side-note` for process flows |
| 5.9. Numbered Lists for Processes | 710–723 | How to write process flows |
| 3.6. Closing Sections | 245–282 | Next Steps, Additional Resources, References order |

### Writing an API endpoint page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.4. API Endpoint Page | 337–357 | Template with resource groups, schemas, endpoint tables |
| 5.1. Tables | 458–498 | Endpoint table format, field definition tables |
| 5.11.4. `::field` | 814–857 | Inline field definitions for request/response schemas |
| 3.6. Closing Sections | 245–282 | Reference pages have References only (no Next Steps) |

### Writing a data model page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.5. Data Model Page | 359–380 | Template with base model, tables, constraints, enums, properties |
| 5.1. Tables | 458–498 | Field definition tables with constraints column |
| 5.11.4. `::field` | 814–857 | Inline field definitions for individual columns with subfields |
| 3.6. Closing Sections | 245–282 | Reference pages have References only (no Next Steps) |

### Writing an integration page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.6. Integration Page | 382–410 | Template with connection methods, operations, post-processing |
| 5.1. Tables | 458–498 | Connection method table, systems table |
| 5.2. Diagrams | 500–581 | System bridge diagrams, sequence diagrams |
| 5.5. Side Notes | 616–644 | Process Flow for operation steps |
| 5.11. AtlasMD Framework Components | 742–922 | `::side-note` for operation flows, `::fig` for sequence diagrams |
| 3.6. Closing Sections | 245–282 | Next Steps, Additional Resources, References order |

### Writing a configuration page

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.7. Configuration Page | 412–426 | Template with sections, sub-sections, variable tables |
| 5.1. Tables | 458–498 | Configuration variable table format |
| 3.6. Closing Sections | 245–282 | Reference pages have References only (no Next Steps) |

### Writing release notes

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 4.8. Release Notes Page | 428–452 | Template with version headings, category groups, rules |
| 3.4, 3.5 | 212–243 | Exception: version numbers as H2, category labels as H3 (not sequential numbers) |
| 3.6. Closing Sections | 245–282 | Release notes have no closing sections |

### Setting up directory structure

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 2. Directory Structure (all) | 43–155 | Numbered sections, files, subdirectories, metadata, standard section sets |
| 1.1, 1.2 | 7–37 | Guide types and directory layout (both-guides vs single-guide) |

### Adding diagrams

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 5.2. Diagrams | 500–581 | Types, placement rules, Mermaid examples, before/after paragraphs |
| 7.3. Images and Diagrams | 1016–1025 | Alt text, color-only meaning, contrast |

### Adding figures / screenshots

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 5.6. Figures | 646–670 | Captions, numbering, light/dark variants, alt text, format, file size |
| 5.11.3. `::fig` | 785–812 | AtlasMD figure component: props, theme switching, zoom modal |
| 7.3. Images and Diagrams | 1016–1025 | Accessibility for images |

### Using AtlasMD framework components

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 5.11. AtlasMD Framework Components (all) | 742–922 | All MDC components: `::note`, `::side-note`, `::fig`, `::field`, `::simple-card`, `::snippet`, `::ai-prompt` |
| 5.4. Notes | 599–614 | Abstract rules for notes (links to `::note`) |
| 5.5. Side Notes | 616–644 | Abstract rules for side notes (links to `::side-note`) |
| 5.6. Figures | 646–670 | Abstract rules for figures (links to `::fig`) |
| 5.1. Tables | 458–498 | Field definition table rules (links to `::field`) |
| 5.3. Code Blocks | 583–597 | Code block rules (links to `::snippet`) |

### Working with links and references

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 8. Cross-References and Links (all) | 1059–1093 | Internal links, cross-guide links, external links, link verification |
| 5.7. Source References (Footnotes) | 672–695 | Footnote syntax, numbering, References section |
| 3.6. Closing Sections | 245–282 | Additional Resources vs References — order and purpose |
| 9. Search and Discoverability (all) | 1095–1145 | URL structure, sitemap, metadata for search |

### Reviewing / auditing documentation

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 1.1. Guide Types | 7–15 | Identify guide type (User Guide only, Tech Guide only, or both) before reviewing |
| 13. Quick Reference Checklist | 1290–1332 | Full pre-publish checklist |
| 12. Maintenance (all) | 1218–1288 | Sync, ownership, review cycles, stale content, automated checks, quality criteria |
| 6. Writing Style (all) | 922–989 | Voice, tone, human voice, no AI-sounding phrases |
| 7. Accessibility (all) | 991–1057 | Semantic structure, tables, images, contrast, keyboard, code blocks |
| 5.11. AtlasMD Framework Components | 742–922 | Verify correct MDC component usage and prop values |

### Scoring / benchmarking documentation

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 1.1. Guide Types | 7–15 | Identify guide type before scoring — do not penalize for absent sections |
| 12.7. Quality Criteria | 1279–1288 | Accuracy, completeness, formatting, links, accessibility, discoverability |
| 13. Quick Reference Checklist | 1290–1332 | Full checklist used as conformance criteria |
| 3. Page Anatomy (all) | 157–282 | Structural conformance criteria |
| 4. Page Types (all present types) | 284–452 | Per-page-type template conformance |
| 5. Information Elements (all) | 454–920 | Tables, diagrams, code blocks, notes, side notes, figures, references, lists, AtlasMD components |
| 6. Writing Style (all) | 922–989 | Quality criteria for wording, voice, clarity |
| 7. Accessibility (all) | 991–1057 | Accessibility conformance criteria |
| 8. Cross-References and Links (all) | 1059–1093 | Link rules used for link health scoring |

Then load the `atlasmd-docs-conformance-score` skill for the full scoring workflow.

### Fixing or verifying links

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 8. Cross-References and Links (all) | 1059–1093 | Link rules, internal vs external, verification |
| 5.7. Source References (Footnotes) | 672–695 | Footnote link rules |
| 9.2. URL Structure | 1109–1117 | Route path rules, no file extensions, stable URLs |

Then load the `atlasmd-docs-link-checker` skill and run the link-checking scripts.

### Working with glossary

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 11. Glossary | 1197–1216 | Format, categorization, alphabetical ordering, cross-referencing |

### Working with documentation versioning

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 10. Documentation Versioning (all) | 1147–1195 | Version sets, version selector, what to version, backporting, end of life |

### Writing configuration for accessibility

| Read | Lines | What it covers |
| ---- | ----- | -------------- |
| 7. Accessibility (all) | 991–1057 | Semantic structure, tables, images, contrast, keyboard, code blocks, automated verification |

## Related Skills

- **atlasmd-docs-conformance-score** — Scores documentation against the standard (quality score, conformance score, link health score, detailed per-section analysis). Load when auditing or benchmarking a documentation set.
- **atlasmd-docs-analyzer-mode** — Full analyzer workflow for reviewing and improving documentation. Load for interactive review sessions.
- **atlasmd-docs-link-checker** — Runs the link-checking and link-fixing scripts. Load when verifying or fixing broken links.
