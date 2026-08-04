# AtlasMD

## Purpose

Docus/Nuxt documentation rendering engine. Consumer projects mount their markdown content into the AtlasMD Docker image to get a documentation site without any JavaScript tooling.

## Ownership

Standalone project. Two subprojects:

- `atlasmd-renderer/` — builds the `atlasmd:latest` Docker image
- `atlasmd-scaffold/` — template for consumer projects (content + public + docker-compose)

## Local Contracts

### Consumer Integration

Consumer projects copy `atlasmd-scaffold/` and reference its `docker-compose.yml` from their main compose file. They mount `content/` and `public/` into the `atlasmd:latest` image.

### Runtime Mounts

| Mount      | Container path | Required                             |
| ---------- | -------------- | ------------------------------------ |
| `content/` | `/app/content` | Yes — markdown files and `_dir.yml`  |
| `public/`  | `/app/public`  | Yes — favicons, logos, static images |

### Environment Variables

| Variable                    | Default                      | Purpose                                    |
| --------------------------- | ---------------------------- | ------------------------------------------ |
| `ATLAS_TITLE`               | `Atlas`                      | Project name in header and browser title   |
| `ATLAS_GITLAB_URL`          | —                            | GitLab repository URL; omit to hide        |
| `ATLAS_GITLAB_LABEL`        | `View the Gitlab repository` | Label for GitLab social link               |
| `ATLAS_SLACK_URL`           | —                            | Slack channel URL; omit to hide slack link |
| `ATLAS_SLACK_LABEL`         | `Message us on Slack`        | Label for Slack social link                |
| `ATLAS_FOOTER_CREDITS_TEXT` | —                            | Footer credits text; omit to hide          |
| `ATLAS_FOOTER_CREDITS_URL`  | —                            | Footer credits link URL                    |
| `ATLAS_FOOTER_CREDITS_ICON` | `heroicons-outline:cloud`    | Footer credits icon                        |
| `ATLAS_FOOTER_TEXT`         | —                            | Footer text link label; omit to hide       |
| `ATLAS_FOOTER_TEXT_URL`     | —                            | Footer text link URL                       |
| `ATLAS_LOGO_LIGHT`          | `/logo-light.png`            | Light mode logo path (from public/)        |
| `ATLAS_LOGO_DARK`           | `/logo-dark.png`             | Dark mode logo path                        |
| `ATLAS_LOGO_DARK_BG`        | `/logo-dark-bg.png`          | Dark mode logo with background             |
| `ATLAS_BASE_URL`            | `/`                          | Base URL path                              |
| `APP_VERSION`               | —                            | Version chip next to title                 |
| `CI_PAGES_URL`              | —                            | GitLab Pages URL; overrides ATLAS_BASE_URL |

## Work Guidance

- Renderer changes require image rebuild (`cd atlasmd-renderer && docker compose build`)
- Scaffold changes do not require image rebuild — content is mounted at runtime
- Theme tokens, components, plugins, and CSS live in the renderer — not in consumer repos
- Social links and footer are env-var driven; each consumer passes its own URLs
- GitLab social link is env-var driven; each consumer passes its own repo URL
- Logo paths are env-var driven; Logo.vue reads from `runtimeConfig.public`

## Verification

```bash
# Build the image
cd atlasmd-renderer && docker compose build

# Run AtlasMD documenting itself
cd ../atlasmd-scaffold && docker compose up
# Open http://localhost:8770
```

## Child DOX Index

- `atlasmd-renderer/` — Rendering engine (Nuxt + Docus); builds `atlasmd:latest` image
  - `components/` — Vue components (Logo, content components for MDC)
  - `plugins/` — Client plugins (scroll-behavior, sidebar-follow)
  - `assets/css/` — Base styles and image CSS
  - `support/` — Link checker and fixer Python scripts
- `atlasmd-scaffold/` — Template for consumer projects (content + public + docker-compose)
  - `content/` — AtlasMD self-documentation (4 sections: getting-started, building-blocks, configuration, development)
    - `2.building-blocks/` — Live-rendered component reference (note, side-note, fig, field, simple-card, example-component, mermaid, docus-builtins, footnotes)
  - `public/` — Favicons, logos, static images
