# AtlasMD

## Purpose

Docus/Nuxt documentation rendering engine. Consumer projects mount their markdown content into the AtlasMD Docker image to get a documentation site without any JavaScript tooling.

## Ownership

Standalone project. Two subprojects:

- `atlasmd-renderer/` — builds the `atlasmd:latest` Docker image
- `atlasmd-scaffold/` — template for consumer projects (content + public + docker-compose)
- `.github/workflows/docker-publish.yml` — publishes the image to `ghcr.io/joaomcarlos/atlasmd` on push to main

## Local Contracts

### Consumer Integration

Consumer projects copy `atlasmd-scaffold/` and reference its `docker-compose.yml` from their main compose file. They mount `content/`, `public/`, and `config.toml` into the `ghcr.io/joaomcarlos/atlasmd:latest` image (published automatically on push to main; pull with `docker pull ghcr.io/joaomcarlos/atlasmd:latest`).

### Runtime Mounts

| Mount         | Container path     | Required                             |
| ------------- | ------------------ | ------------------------------------ |
| `content/`    | `/app/content`     | Yes — markdown files and `_dir.yml`  |
| `public/`     | `/app/public`      | Yes — favicons, logos, static images |
| `config.toml` | `/app/config.toml` | Yes — consumer configuration         |

### Configuration

Consumer configuration is read from a TOML file at `/app/config.toml` (loaded by `atlasmd-renderer/config.ts`). Only CI/build-driven values stay as environment variables.

| Field / Variable      | Default                   | Purpose                                        |
| --------------------- | ------------------------- | ---------------------------------------------- |
| `title`               | `Atlas`                   | Project name in header and browser title       |
| `baseUrl`             | `/`                       | Base URL path                                  |
| `socials[].url`       | —                         | Social link URL; one `[[socials]]` per link    |
| `socials[].label`     | —                         | Label for the social link                      |
| `socials[].icon`      | —                         | Iconify icon name (e.g. `simple-icons:gitlab`) |
| `footer.credits.text` | —                         | Footer credits text; omit to hide              |
| `footer.credits.url`  | —                         | Footer credits link URL                        |
| `footer.credits.icon` | `heroicons-outline:cloud` | Footer credits icon                            |
| `footer.text.label`   | —                         | Footer text link label; omit to hide           |
| `footer.text.url`     | —                         | Footer text link URL                           |
| `APP_VERSION` (env)   | —                         | Version chip next to title (build arg)         |
| `CI_PAGES_URL` (env)  | —                         | GitLab Pages URL; overrides `baseUrl`          |
| `PORT` (env)          | `3003`                    | Port the dev server listens on                 |

Logos are convention-based fixed filenames in `public/` — no config needed: `logo-light-mode.png`, `logo-dark-mode.png`, `logo-dark-mode-bg.png`.

## Work Guidance

- Renderer changes require image rebuild (`cd atlasmd-renderer && docker compose build`) and a push to main to publish to ghcr.io
- Scaffold changes do not require image rebuild — content is mounted at runtime
- The published image lives at `ghcr.io/joaomcarlos/atlasmd`; tags are `:latest` and `:sha-<short>`
- First publish: flip the package to public manually at https://github.com/users/joaomcarlos/packages/container/atlasmd/settings (the workflow attempts this via API but may 404 on first run)
- Theme tokens, components, plugins, and CSS live in the renderer — not in consumer repos
- Social links and footer are config-driven; each consumer sets its own `[[socials]]` and `[footer]` in `config.toml`
- Social links are generic — consumer picks url, label, and Iconify icon per link
- Logos are convention-based fixed filenames in `public/`; Logo.vue reads from `runtimeConfig.public`

## Verification

```bash
# Build the image
cd atlasmd-renderer && docker compose build

# Run AtlasMD documenting itself
cd ../atlasmd-scaffold && docker compose up
# Open http://localhost:47145
```

## Child DOX Index

- `atlasmd-renderer/` — Rendering engine (Nuxt + Docus); builds `atlasmd:latest` image
  - `config.ts` — TOML config loader; reads `/app/config.toml` at startup, exports `atlasConfig`
  - `components/` — Vue components (Logo, content components for MDC)
  - `plugins/` — Client plugins (scroll-behavior, sidebar-follow)
  - `assets/css/` — Base styles and image CSS
- `atlasmd-scaffold/` — Template for consumer projects (content + public + config.toml + docker-compose)
  - `content/` — AtlasMD self-documentation (4 sections: getting-started, building-blocks, configuration, development)
    - `2.building-blocks/` — Live-rendered component reference (note, side-note, fig, field, simple-card, example-component, mermaid, docus-builtins, footnotes)
  - `public/` — Favicons, logos, static images
  - `config.toml` — Consumer configuration (title, social links, footer)
