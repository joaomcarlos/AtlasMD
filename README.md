# AtlasMD

Docus/Nuxt documentation rendering engine. Consumer projects mount their markdown content into the AtlasMD Docker image to get a full documentation site without any JavaScript tooling.

## How It Works

```
Your Project                    AtlasMD Image
┌─────────────┐                ┌──────────────────────┐
│  content/   │── volume ──▶   │  Nuxt + Docus        │──▶ Browser
│  public/    │── volume ──▶   │  (renderer)          │
└─────────────┘                └──────────────────────┘
```

Consumer projects keep only markdown and static assets. The AtlasMD image provides the rendering engine.

## Repository Structure

| Folder | Purpose |
|---|---|
| `atlasmd-renderer/` | The rendering engine — Nuxt config, components, CSS, Dockerfile. Builds the `atlasmd:latest` image. |
| `atlasmd-scaffold/` | Template for consumer projects — content structure, public assets, docker-compose.yml. Copy this to start. |

## Add AtlasMD to Your Project

### 1. Build the Image

```bash
cd atlasmd-renderer
docker compose build
```

This produces `atlasmd:latest`.

### 2. Copy the Scaffold

Copy `atlasmd-scaffold/` into your project. Rename it to fit your project (e.g. `docs/`).

```bash
cp -r /path/to/AtlasMD/atlasmd-scaffold /path/to/your-project/docs
```

### 3. Reference the Compose File

In your project's main `docker-compose.yml`, include the scaffold's compose file:

```yaml
include:
  - docs/docker-compose.yml
```

Or copy the service definition from `atlasmd-scaffold/docker-compose.yml` directly into your compose file and adjust the paths.

### 4. Configure for Your Project

Edit the scaffold's `docker-compose.yml`:

| Variable | Set to |
|---|---|
| `ATLAS_TITLE` | Your project name |
| `ATLAS_GITLAB_URL` | Your GitLab repository URL |
| `ATLAS_GITLAB_LABEL` | Label for the GitLab link |
| `ATLAS_LOGO_LIGHT` | Path to your light mode logo in `public/` |
| `ATLAS_LOGO_DARK` | Path to your dark mode logo in `public/` |
| `ATLAS_LOGO_DARK_BG` | Path to your dark mode logo with background |
| `APP_VERSION` | Your app version |

Adjust the volume mount paths to match where you placed the scaffold relative to your main compose file:

```yaml
volumes:
  - ./docs/content:/app/content
  - ./docs/public:/app/public
```

### 5. Add Content and Assets

- Write markdown files in `content/` using the `1.Title.md` naming convention
- Add `_dir.yml` files for navigation metadata
- Place favicons and logos in `public/`

See the scaffold's own content for a live example — this repository uses AtlasMD to document itself.

### 6. Run

```bash
docker compose up
```

Open `http://localhost:8770`.

## Consumer Project Checklist

- [ ] `atlasmd:latest` image built and available
- [ ] Scaffold copied into your project
- [ ] Compose file referenced or service definition copied
- [ ] Environment variables set for your project
- [ ] Volume mount paths adjusted
- [ ] Content written in `content/`
- [ ] Logos and favicons placed in `public/`
- [ ] Port does not conflict with other services

## Development

To develop AtlasMD itself or run its self-documentation:

```bash
cd atlasmd-scaffold
docker compose up
```

Open `http://localhost:8770` to view the AtlasMD documentation (rendered by AtlasMD).

To rebuild the image after renderer changes:

```bash
cd atlasmd-renderer
docker compose build
```

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ATLAS_TITLE` | `Atlas` | Project name in header and browser title |
| `ATLAS_GITLAB_URL` | — | GitLab repository URL; omit to hide the link |
| `ATLAS_GITLAB_LABEL` | `View the Gitlab repository` | Label for the GitLab link |
| `ATLAS_LOGO_LIGHT` | `/logo-light.png` | Light mode logo path (from `public/`) |
| `ATLAS_LOGO_DARK` | `/logo-dark.png` | Dark mode logo path |
| `ATLAS_LOGO_DARK_BG` | `/logo-dark-bg.png` | Dark mode logo with background |
| `ATLAS_BASE_URL` | `/` | Base URL path (for GitLab Pages subpaths) |
| `APP_VERSION` | — | Version chip next to title |
| `CI_PAGES_URL` | — | GitLab Pages URL; overrides `ATLAS_BASE_URL` |
