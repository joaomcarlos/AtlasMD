# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Engineering teams who need to publish technical documentation — API references, architecture guides, data models, integrations, configuration references — without maintaining a JavaScript toolchain in their own repository. The consumer's job is to write markdown that conforms to the AtlasMD Documentation Standard and ship it; AtlasMD handles the rendering, navigation, theming, and deployment surface.

## Product Purpose

AtlasMD exists to give engineering teams a complete, polished documentation site with zero frontend tooling in the consumer repo. Success means a team can copy the scaffold, drop in markdown content, run `docker compose up`, and have a production-grade docs site that enforces a consistent documentation standard across every project that adopts it.

## Positioning

AtlasMD pairs a strict, authored documentation standard (structure, page types, MDC components, writing style, accessibility rules) with a renderer that implements it. The standard is the product; the renderer serves it. A neighboring tool — Docus, VitePress, MkDocs, GitBook — can render markdown, but none ships an enforced documentation standard as a single mount-and-serve artifact. The standard and the renderer are one deliverable, not two.

## Operating Context

- Consumer projects copy `atlasmd-scaffold/` and reference its `compose.yml` from their main compose file.
- Content is markdown files with numeric ordering prefixes (`1.Title.md`) and `_dir.yml` navigation metadata, mounted into the prebuilt Docker image at runtime.
- The image is published to `ghcr.io/joaomcarlos/atlasmd:latest` (and `:sha-<short>`) on push to main.
- Local development runs the renderer via `docker compose up` (port 47145) or `nuxi dev` (port 3003) inside `atlasmd-renderer/`.
- Deployment targets include GitLab Pages (`CI_PAGES_URL` overrides `baseUrl` at deploy time) and any static host serving the prerendered output.
- The documentation standard lives in `DOCUMENTATION-STANDARD.md` and is synced to the scaffold via `sync-to-scaffold.sh`.

## Capabilities and Constraints

- Renderer is built on Docus + Nuxt 3 + Pinceau tokens + Mermaid diagrams. This stack is fixed; design work happens within it, not replacing it.
- The Docker mount contract is fixed: `content/`, `public/`, and `config.toml` mounted at `/app/`. Design must not require consumers to change their repo structure.
- Branding is config-driven via `config.toml`: `title`, `socials`, `footer`, and convention-based logo filenames in `public/` (`logo-light-mode.png`, `logo-dark-mode.png`, `logo-dark-mode-bg.png`). Design must not hardcode consumer-specific branding.
- The AtlasMD Documentation Standard (`DOCUMENTATION-STANDARD.md`) and its MDC components (`::note`, `::side-note`, `::fig`, `::field`, `::simple-card`, `::snippet`, `::ai-prompt`) are authoritative. Design supports the standard, not the other way around.
- Code highlighting uses `github-light` / `github-dark` themes; Mermaid, Python, JSONC, and TOML are registered languages.
- Prerendering is serial (`concurrency: 1`) with in-memory cache to prevent filesystem corruption during builds.

## Brand Commitments

- Name: AtlasMD.
- Voice: technical, precise, human — per the Documentation Standard's writing style rules (no emojis in content, concrete before abstract, no AI-sounding phrases).
- Default footer copy: "Built with passion by the AtlasMD team" with a link to the GitHub repository. Consumers override this in `config.toml`.
- Default social link: the AtlasMD GitHub repository. Consumers override this in `config.toml`.
- No binding visual identity (palette, typography, logo artwork) has been pinned beyond what the current tokens and components express; the incumbent visual world is evidence, not a commitment.

## Evidence on Hand

- `atlasmd-renderer/` — the full renderer source: `nuxt.config.ts`, `config.ts`, `app.config.ts`, `tokens.config.ts`, `components/`, `plugins/`, `assets/css/`, `Dockerfile`.
- `atlasmd-scaffold/` — the consumer template: `compose.yml`, `config.toml`, `content/`, `public/`.
- `DOCUMENTATION-STANDARD.md` (in `atlasmd-doc-standards/`, `ai/skills/atlasmd-docs/`, and synced to `atlasmd-scaffold/.agents/skills/atlasmd-docs/`) — the enforced documentation standard.
- `ai/skills/atlasmd-docs/SKILL.md` — the skill that indexes the standard for documentation tasks.
- `sync-to-scaffold.sh` — the sync script that propagates standard and skill changes to the scaffold.
- `.github/workflows/docker-publish.yml` — the CI that publishes the image to ghcr.io.
- Absences: no real customer testimonials, usage metrics, case studies, or press exist. Future work must not fabricate them.

## Product Principles

1. **The standard is the product.** The renderer exists to serve the documentation standard; every rendering decision should make standard-conformant content look and read better, not invent parallel conventions.
2. **Zero tooling in the consumer repo.** The consumer writes markdown and mounts it. Any feature that requires the consumer to install JS dependencies, run a build step, or edit renderer internals is a regression.
3. **Config-driven, not code-driven, branding.** Every consumer-visible identity element (title, logos, socials, footer) is set in `config.toml` or convention-based filenames. The renderer ships no consumer-specific branding.
4. **Mount-and-serve is the contract.** The Docker image is the delivery artifact. The boundary between renderer and consumer is the mount contract; design and features respect that boundary.
5. **Read mode is the default surface.** AtlasMD's surfaces are documentation — structure for comprehension first, then make the reading experience worth staying in. Scanability, navigation, and long-form reading comfort outrank expression.
