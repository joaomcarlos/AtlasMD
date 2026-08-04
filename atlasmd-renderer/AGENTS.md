# atlasmd-renderer

## Purpose

Docus/Nuxt documentation rendering engine. Builds the `atlasmd:latest` Docker image that serves
markdown content from mounted `content/` and `public/` directories.

## Ownership

Rendering engine subproject of AtlasMD. Consumed by other projects
via Docker image with volume-mounted content.

## Local Contracts

### Runtime mounts

| Mount      | Container path | Required                             |
| ---------- | -------------- | ------------------------------------ |
| `content/` | `/app/content` | Yes — markdown files and `_dir.yml`  |
| `public/`  | `/app/public`  | Yes — favicons, logos, static images |

### Environment variables

| Variable                    | Default                      | Purpose                                                                |
| --------------------------- | ---------------------------- | ---------------------------------------------------------------------- |
| `ATLAS_TITLE`               | `Atlas`                      | Project name in header and browser title                               |
| `ATLAS_GITLAB_URL`          | —                            | Gitlab repository URL for header social link; omit to hide gitlab link |
| `ATLAS_GITLAB_LABEL`        | `View the Gitlab repository` | Label for the gitlab social link                                       |
| `ATLAS_SLACK_URL`           | —                            | Slack channel URL for header social link; omit to hide slack link      |
| `ATLAS_SLACK_LABEL`         | `Message us on Slack`        | Label for the slack social link                                        |
| `ATLAS_FOOTER_CREDITS_TEXT` | —                            | Footer credits text; omit to hide credits                              |
| `ATLAS_FOOTER_CREDITS_URL`  | —                            | Footer credits link URL                                                |
| `ATLAS_FOOTER_CREDITS_ICON` | `heroicons-outline:cloud`    | Footer credits icon                                                    |
| `ATLAS_FOOTER_TEXT`         | —                            | Footer text link label; omit to hide text link                         |
| `ATLAS_FOOTER_TEXT_URL`     | —                            | Footer text link URL                                                   |
| `ATLAS_LOGO_LIGHT`          | `/logo-light.png`            | Light mode logo path (from public/)                                    |
| `ATLAS_LOGO_DARK`           | `/logo-dark.png`             | Dark mode logo path                                                    |
| `ATLAS_LOGO_DARK_BG`        | `/logo-dark-bg.png`          | Dark mode logo with background                                         |
| `ATLAS_BASE_URL`            | `/`                          | Base URL path                                                          |
| `APP_VERSION`               | —                            | Version chip next to title                                             |
| `CI_PAGES_URL`              | —                            | GitLab Pages URL; overrides ATLAS_BASE_URL                             |

### Content conventions

- `1.Title.md` filename format (numeric ordering prefix + dot + title)
- `_dir.yml` in each directory for navigation metadata
- Icons only in top-level `_dir.yml` files
- MDC syntax for rich content (`::note`, `::side-note`, custom components)
- `<DarkLightModeImage>` component for images (if consumer provides it)

## Work Guidance

- Theme tokens, components, plugins, and CSS live here — not in consumer repos
- Social links and footer are env-var driven; each consumer passes its own URLs
- Gitlab social link is env-var driven (`ATLAS_GITLAB_URL`); each consumer passes its own repo URL
- Logo paths are env-var driven; Logo.vue reads from `runtimeConfig.public`
- `nuxt.config.ts` has `buildContentRoutes()` that reads `./content` at startup; safe if content is missing (try/catch)

## Verification

```bash
just build    # build Docker image
just watch    # run with docker watch
```

## Child DOX Index

- `components/` — Vue components (Logo, content components for MDC)
- `plugins/` — Client plugins (scroll-behavior, sidebar-follow)
- `assets/css/` — Base styles and image CSS
- `support/` — Link checker and fixer Python scripts
