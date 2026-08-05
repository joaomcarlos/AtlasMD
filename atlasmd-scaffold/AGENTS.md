# atlasmd-scaffold

## Purpose

Template for consumer projects. Contains content structure, public assets, and a docker-compose.yml that mounts into the `atlasmd:latest` image. Also serves as AtlasMD's own self-documentation.

## Ownership

Content-only subproject of AtlasMD. No JavaScript project — rendering is handled by the AtlasMD Docker image built from `atlasmd-renderer/`.

## Local Contracts

### Structure

```
content/             Markdown files and _dir.yml navigation configs
public/              Favicons, logos, static images (served at root URL)
config.toml          Consumer configuration (title, social links, footer)
docker-compose.yml   Service definition for the atlasmd:latest image
```

### Docker Service

- Port 8770 → container 3003 (web)
- Port 8771 → container 4000 (HMR websocket)
- Mounts `content/` → `/app/content`, `public/` → `/app/public`, `config.toml` → `/app/config.toml`
- Build context: `../atlasmd-renderer`

### Content Conventions

- `1.Title.md` filename format (numeric prefix + dot + title)
- `_dir.yml` in each directory for navigation metadata
- Icons only in top-level `_dir.yml` files
- MDC syntax for rich content (`::note`, `::side-note`, `::fig`, `::field`, `::simple-card`, `::example-component`, mermaid diagrams, Docus built-ins)

## Work Guidance

- Edit only markdown files and `_dir.yml` files here
- Rendering, theme, components, and CSS are in `atlasmd-renderer/` — not here
- To change appearance, modify the renderer and rebuild the image
- Consumer projects copy this folder and adjust `config.toml` and paths

## Verification

```bash
docker compose up
# Open http://localhost:8770
```

## Child DOX Index

- `content/` — AtlasMD self-documentation (4 sections: getting-started, building-blocks, configuration, development)
  - `1.getting-started/` — Overview and integration guide
  - `2.building-blocks/` — Live-rendered component reference (note, side-note, fig, field, simple-card, example-component, mermaid, docus-builtins, footnotes)
  - `3.configuration/` — Configuration file, content conventions, customization
  - `4.development/` — Building the image, running locally, project structure
- `public/` — Favicons, logos, static images
- `config.toml` — Consumer configuration (title, social links, footer)
