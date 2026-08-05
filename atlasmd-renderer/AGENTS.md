# atlasmd-renderer

## Purpose

Docus/Nuxt documentation rendering engine. Builds the `ghcr.io/joaomcarlos/atlasmd:latest` Docker image that serves
markdown content from mounted `content/` and `public/` directories.

## Ownership

Rendering engine subproject of AtlasMD. Consumed by other projects
via Docker image with volume-mounted content.

## Local Contracts

### Runtime mounts

| Mount         | Container path     | Required                             |
| ------------- | ------------------ | ------------------------------------ |
| `content/`    | `/app/content`     | Yes — markdown files and `_dir.yml`  |
| `public/`     | `/app/public`      | Yes — favicons, logos, static images |
| `config.toml` | `/app/config.toml` | Yes — consumer configuration         |

### Configuration

Consumer configuration is read from a TOML file at `/app/config.toml`, loaded by `config.ts` at startup. Only CI/build-driven values stay as environment variables.

#### Config file fields

| Field                 | Default                   | Purpose                                                              |
| --------------------- | ------------------------- | -------------------------------------------------------------------- |
| `title`               | `AtlasMD`                 | Project name in header and browser title                             |
| `baseUrl`             | `/`                       | Base URL path; `CI_PAGES_URL` overrides at deploy time               |
| `socials[].url`       | —                         | Social link URL; one `[[socials]]` block per link                    |
| `socials[].label`     | —                         | Label for the social link                                            |
| `socials[].icon`      | —                         | Iconify icon name (e.g. `simple-icons:gitlab`, `simple-icons:slack`) |
| `footer.credits.text` | —                         | Footer credits text; omit to hide credits                            |
| `footer.credits.url`  | —                         | Footer credits link URL                                              |
| `footer.credits.icon` | `heroicons-outline:cloud` | Footer credits icon                                                  |
| `footer.text.label`   | —                         | Footer text link label; omit to hide text link                       |
| `footer.text.url`     | —                         | Footer text link URL                                                 |

Logos are convention-based fixed filenames in `public/` — no config needed: `logo-light-mode.png`, `logo-dark-mode.png`, `logo-dark-mode-bg.png`.

#### Environment variables (CI/build-driven only)

| Variable       | Default | Purpose                                               |
| -------------- | ------- | ----------------------------------------------------- |
| `APP_VERSION`  | —       | Version chip next to title (build arg)                |
| `CI_PAGES_URL` | —       | GitLab Pages URL; set by GitLab CI; overrides baseUrl |
| `PORT`         | `3003`  | Port the dev server listens on                        |

### Content conventions

- `1.Title.md` filename format (numeric ordering prefix + dot + title)
- `_dir.yml` in each directory for navigation metadata
- Icons only in top-level `_dir.yml` files
- MDC syntax for rich content (`::note`, `::side-note`, custom components)
- `<DarkLightModeImage>` component for images (if consumer provides it)

## Work Guidance

- Theme tokens, components, plugins, and CSS live here — not in consumer repos
- Social links and footer are config-driven; each consumer sets its own `[[socials]]` and `[footer]` in `config.toml`
- Social links are generic — consumer picks url, label, and Iconify icon per link
- Logos are convention-based fixed filenames in `public/`; Logo.vue reads from `runtimeConfig.public`
- `config.ts` loads `/app/config.toml` (or `./config.toml` locally) at startup and exports `atlasConfig`
- `nuxt.config.ts` has `buildContentRoutes()` that reads `./content` at startup; safe if content is missing (try/catch)
- `support/patch-pinceau.mjs` patches pinceau 0.18.10 at Docker build time: replaces `nanoid(6)` variant class names with a deterministic hash of `cacheId`, fixing SSR hydration class mismatches; idempotent and auto-skips if already patched

