# AtlasMD AI

## Documentation

When working on documentation (writing, editing, reviewing, structuring, or fixing links), force-load the `atlasmd-docs` skill from `ai/skills/atlasmd-docs/SKILL.md`. It indexes the AtlasMD Documentation Standard so you read only the relevant sections for the task type.

For interactive review sessions, also load `atlasmd-docs-analyzer-mode`. For link checking, also load `atlasmd-docs-link-checker`. For scoring and benchmarking documentation against the standard, also load `atlasmd-docs-conformance-score`.

## Branding Assets

When generating logos or favicons for a consumer project (or fixing missing favicons), force-load the `atlasmd-icons` skill from `ai/skills/atlasmd-icons/SKILL.md`. It bundles a Python script that takes any source app icon and produces all the correctly-sized logos and favicons AtlasMD expects in `public/`.
