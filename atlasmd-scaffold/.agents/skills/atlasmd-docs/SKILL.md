---
name: atlasmd-docs
description: Index to the AtlasMD Documentation Standard. Load when writing, editing, reviewing, or structuring documentation. Points to the exact standard sections to read for each task type.
---

# atlasmd-docs

Index to the AtlasMD Documentation Standard. Load when writing, editing, reviewing, or structuring documentation. Points to the exact standard sections to read for each task type.

## The Standard File

The standard lives at `atlasmd-doc-standards/DOCUMENTATION-STANDARD.md` in the AtlasMD repository. It is the single source of truth. This skill does not duplicate its content — it tells you which sections to read for the task at hand.

Read the standard file before making any documentation changes. Use the task index below to scan only the relevant sections instead of reading the entire file every time.

## Task Index

Look up the task you are performing. Read the listed sections from the standard file before starting. When a task spans multiple categories, read all listed sections.

### Writing a new page

| Read | What it covers |
| ---- | -------------- |
| 1. Scope (all) | Guide types — identify if the project is User Guide only, Tech Guide only, or both |
| 2. Directory Structure (all) | Where the page goes, file naming, section metadata |
| 3. Page Anatomy (all) | Frontmatter, H1, opening paragraph, numbered sections, closing sections |
| 4. Page Types (match your page type) | Required structure for the specific page type you are writing |
| 6. Writing Style (all) | Voice, tone, human voice, no emojis, concrete before abstract |
| 13. Quick Reference Checklist | Final verification before publishing |

### Writing a landing page

| Read | What it covers |
| ---- | -------------- |
| 3.1, 3.2, 3.3 | Frontmatter, H1, opening paragraph |
| 4.1. Landing Page | Template and rules for landing pages |
| 5.8. Landing Page Cards | Card grid structure, icon rules, description source |
| 3.6. Closing Sections | Landing page exception: unnumbered References only |

### Writing an overview page

| Read | What it covers |
| ---- | -------------- |
| 4.2. Overview Page | Template and required sections |
| 3. Page Anatomy (all) | General page structure |
| 6. Writing Style (all) | Voice and tone rules |

### Writing a building block / conceptual deep-dive page

| Read | What it covers |
| ---- | -------------- |
| 4.3. Building Block Page | Template with DTO tables, flow steps, edge cases |
| 5.1. Tables | Field definition tables, endpoint tables |
| 5.2. Diagrams | Architecture, sequence, state machine diagrams |
| 5.5. Side Notes | Process Flow, Step-by-Step labels |
| 5.9. Numbered Lists for Processes | How to write process flows |
| 3.6. Closing Sections | Next Steps, Additional Resources, References order |

### Writing an API endpoint page

| Read | What it covers |
| ---- | -------------- |
| 4.4. API Endpoint Page | Template with resource groups, schemas, endpoint tables |
| 5.1. Tables | Endpoint table format, field definition tables |
| 3.6. Closing Sections | Reference pages have References only (no Next Steps) |

### Writing a data model page

| Read | What it covers |
| ---- | -------------- |
| 4.5. Data Model Page | Template with base model, tables, constraints, enums, properties |
| 5.1. Tables | Field definition tables with constraints column |
| 3.6. Closing Sections | Reference pages have References only (no Next Steps) |

### Writing an integration page

| Read | What it covers |
| ---- | -------------- |
| 4.6. Integration Page | Template with connection methods, operations, post-processing |
| 5.1. Tables | Connection method table, systems table |
| 5.2. Diagrams | System bridge diagrams, sequence diagrams |
| 5.5. Side Notes | Process Flow for operation steps |
| 3.6. Closing Sections | Next Steps, Additional Resources, References order |

### Writing a configuration page

| Read | What it covers |
| ---- | -------------- |
| 4.7. Configuration Page | Template with sections, sub-sections, variable tables |
| 5.1. Tables | Configuration variable table format |
| 3.6. Closing Sections | Reference pages have References only (no Next Steps) |

### Writing release notes

| Read | What it covers |
| ---- | -------------- |
| 4.8. Release Notes Page | Template with version headings, category groups, rules |
| 3.4, 3.5 | Exception: version numbers as H2, category labels as H3 (not sequential numbers) |
| 3.6. Closing Sections | Release notes have no closing sections |

### Setting up directory structure

| Read | What it covers |
| ---- | -------------- |
| 2. Directory Structure (all) | Numbered sections, files, subdirectories, metadata, standard section sets |
| 1.1, 1.2 | Guide types and directory layout (both-guides vs single-guide) |

### Adding diagrams

| Read | What it covers |
| ---- | -------------- |
| 5.2. Diagrams | Types, placement rules, Mermaid examples, before/after paragraphs |
| 7.3. Images and Diagrams | Alt text, color-only meaning, contrast |

### Adding figures / screenshots

| Read | What it covers |
| ---- | -------------- |
| 5.6. Figures | Captions, numbering, light/dark variants, alt text, format, file size |
| 7.3. Images and Diagrams | Accessibility for images |

### Working with links and references

| Read | What it covers |
| ---- | -------------- |
| 8. Cross-References and Links (all) | Internal links, cross-guide links, external links, link verification |
| 5.7. Source References (Footnotes) | Footnote syntax, numbering, References section |
| 3.6. Closing Sections | Additional Resources vs References — order and purpose |
| 9. Search and Discoverability (all) | URL structure, sitemap, metadata for search |

### Reviewing / auditing documentation

| Read | What it covers |
| ---- | -------------- |
| 1.1. Guide Types | Identify guide type (User Guide only, Tech Guide only, or both) before reviewing |
| 13. Quick Reference Checklist | Full pre-publish checklist |
| 12. Maintenance (all) | Sync, ownership, review cycles, stale content, automated checks, quality criteria |
| 6. Writing Style (all) | Voice, tone, human voice, no AI-sounding phrases |
| 7. Accessibility (all) | Semantic structure, tables, images, contrast, keyboard, code blocks |

### Scoring / benchmarking documentation

| Read | What it covers |
| ---- | -------------- |
| 1.1. Guide Types | Identify guide type before scoring — do not penalize for absent sections |
| 12.7. Quality Criteria | Accuracy, completeness, formatting, links, accessibility, discoverability |
| 13. Quick Reference Checklist | Full checklist used as conformance criteria |
| 3. Page Anatomy (all) | Structural conformance criteria |
| 4. Page Types (all present types) | Per-page-type template conformance |
| 5. Information Elements (all) | Tables, diagrams, code blocks, notes, side notes, figures, references, lists |
| 6. Writing Style (all) | Quality criteria for wording, voice, clarity |
| 7. Accessibility (all) | Accessibility conformance criteria |
| 8. Cross-References and Links (all) | Link rules used for link health scoring |

Then load the `atlasmd-docs-conformance-score` skill for the full scoring workflow.

### Fixing or verifying links

| Read | What it covers |
| ---- | -------------- |
| 8. Cross-References and Links (all) | Link rules, internal vs external, verification |
| 5.7. Source References (Footnotes) | Footnote link rules |
| 9.2. URL Structure | Route path rules, no file extensions, stable URLs |

Then load the `atlasmd-docs-link-checker` skill and run the link-checking scripts.

### Working with glossary

| Read | What it covers |
| ---- | -------------- |
| 11. Glossary | Format, categorization, alphabetical ordering, cross-referencing |

### Working with documentation versioning

| Read | What it covers |
| ---- | -------------- |
| 10. Documentation Versioning (all) | Version sets, version selector, what to version, backporting, end of life |

### Writing configuration for accessibility

| Read | What it covers |
| ---- | -------------- |
| 7. Accessibility (all) | Semantic structure, tables, images, contrast, keyboard, code blocks, automated verification |

## Related Skills

- **atlasmd-docs-conformance-score** — Scores documentation against the standard (quality score, conformance score, link health score, detailed per-section analysis). Load when auditing or benchmarking a documentation set.
- **atlasmd-docs-analyzer-mode** — Full analyzer workflow for reviewing and improving documentation. Load for interactive review sessions.
- **atlasmd-docs-link-checker** — Runs the link-checking and link-fixing scripts. Load when verifying or fixing broken links.
