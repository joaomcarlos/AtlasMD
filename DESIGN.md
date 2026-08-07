---
name: AtlasMD
description: Technical manual documentation engine — print craft translated to screen
colors:
  slate-ink-900: "#0f1320"
  slate-ink-800: "#141a2a"
  slate-ink-700: "#1a2237"
  slate-ink-600: "#212b42"
  slate-ink-500: "#36496e"
  slate-ink-400: "#3b475e"
  slate-ink-300: "#bac9d7"
  slate-ink-200: "#d1dbe4"
  slate-ink-100: "#e6ebf0"
  slate-ink-50: "#f0f8fc"
  blueprint-blue-light: "#3182ce"
  blueprint-blue-dark: "#4dabf7"
  margin-gray-50: "#fbfbfb"
  margin-gray-100: "#f5f5f5"
  margin-gray-200: "#eaeaea"
  margin-gray-300: "#d7d7d7"
  margin-gray-400: "#bfbfbf"
  margin-gray-500: "#939393"
  margin-gray-600: "#626262"
  margin-gray-700: "#323232"
  margin-gray-800: "#1d1d1d"
  margin-gray-900: "#111111"
  warning-vermilion-400: "#FF7353"
  warning-vermilion-500: "#FF3B10"
  warning-vermilion-600: "#BB2402"
  dark-slate-900: "#0f172a"
  dark-slate-800: "#1e293b"
  dark-slate-700: "#334155"
  dark-slate-border: "#3b4252"
  code-bg-light: "#f7fafc"
  code-bg-dark: "#2d2d2d"
  body-text-light: "#1d1d1d"
  body-text-dark: "oklch(70.7% 0.022 261.325)"
  heading-light: "#111111"
  heading-dark: "#eaeaea"
  overlay-scrim: "rgba(0, 0, 0, 0.6)"
  highlight-target: "rgba(255, 235, 59, 0.35)"
typography:
  body:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif"
    fontSize: "11pt"
    fontWeight: 400
    lineHeight: "1.4"
  callout-serif:
    fontFamily: "'Computer Modern Serif', 'Charter', 'Bitstream Charter', 'Sitka Text', 'Georgia', serif"
    fontSize: "0.8em"
    fontWeight: 400
  code-mono:
    fontFamily: "'Fira Code', 'Roboto Mono', 'Consolas', 'Monaco', 'Andale Mono', monospace"
    fontSize: "0.9em"
    fontWeight: 400
    lineHeight: "1.5"
  heading-h1:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "16pt"
    fontWeight: 700
    lineHeight: "1.5em"
    letterSpacing: "normal"
  heading-h2:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "14pt"
    fontWeight: 700
    lineHeight: "1.5em"
  heading-h3:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "14pt"
    fontWeight: 700
  heading-h4:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "11pt"
    fontWeight: 700
  heading-h5:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "10pt"
    fontWeight: 700
  heading-h6:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "9pt"
    fontWeight: 700
  field-name:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
  field-type:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 400
  caption:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "0.9em"
    fontWeight: 400
    fontStyle: "italic"
  label-uppercase:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: "0.75rem"
    fontWeight: 600
    letterSpacing: "0.05em"
rounded:
  none: "0px"
  xs: "3px"
  sm: "4px"
  md: "8px"
  lg: "10px"
  pill: "25px"
spacing:
  page-width: "8.5in"
  content-width: "4.5in"
  margin-width: "1.5in"
  gutter: "0.5in"
  baseline: "1.5em"
  space-1: "0.25rem"
  space-2: "0.5rem"
  space-3: "0.75rem"
  space-4: "1rem"
  space-6: "1.5rem"
  space-8: "2rem"
components:
  note-callout:
    backgroundColor: "{colors.code-bg-light}"
    textColor: "{colors.body-text-light}"
    rounded: "{rounded.xs}"
    padding: "0.5em 1em 0.5em 4em"
  side-note:
    textColor: "{colors.margin-gray-600}"
    fontSize: "0.8em"
  figure-inline:
    rounded: "{rounded.md}"
    width: "100%"
  figure-modal-overlay:
    backgroundColor: "{colors.overlay-scrim}"
  simple-card:
    backgroundColor: "{colors.margin-gray-50}"
    borderColor: "{colors.margin-gray-200}"
    rounded: "{rounded.lg}"
    padding: "0.75rem 0.75rem 0.25rem 0.75rem"
  simple-card-dark:
    backgroundColor: "{colors.slate-ink-800}"
    borderColor: "{colors.slate-ink-700}"
  field-definition:
    textColor: "{colors.slate-ink-600}"
    fontStyle: "italic"
  field-required:
    textColor: "{colors.warning-vermilion-600}"
    fontWeight: "700"
  ai-prompt:
    backgroundColor: "{colors.margin-gray-50}"
    borderColor: "{colors.margin-gray-200}"
    rounded: "{rounded.lg}"
  ai-prompt-dark:
    backgroundColor: "{colors.slate-ink-800}"
    borderColor: "{colors.slate-ink-700}"
  ai-prompt-header:
    backgroundColor: "{colors.margin-gray-100}"
    textColor: "{colors.slate-ink-600}"
  ai-prompt-header-dark:
    backgroundColor: "{colors.slate-ink-900}"
    textColor: "{colors.slate-ink-300}"
  code-block:
    fontFamily: "'Fira Code', 'Roboto Mono', 'Consolas', monospace"
    fontSize: "0.9em"
    rounded: "{rounded.xs}"
    padding: "1em"
  table-header:
    backgroundColor: "{colors.code-bg-light}"
    fontWeight: "600"
  version-chip:
    backgroundColor: "{colors.margin-gray-800}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
    padding: "2px 7px"
    fontSize: "12px"
  version-chip-dark:
    backgroundColor: "{colors.margin-gray-500}"
    textColor: "#ffffff"
---

# Design System: AtlasMD

## Overview

### Creative North Star — "The Technical Manual"

AtlasMD renders technical documentation as a typeset manual translated to screen. The page is a grid with a marginalia column, justified body text with first-line indents, ruled section headings with top and bottom borders, and serif callouts that break from the sans-serif body to mark notes and asides. The aesthetic is technical and dense — information density is high but legible, and the reader is here to work, not to browse.

The dark mode does not abandon the manual metaphor; it deepens it. Light mode uses warm neutrals (paper-white backgrounds, gray-200 heading bands, blueprint-blue accents). Dark mode shifts to a slate palette — the primary navy ramp becomes the surface, the accent shifts to a brighter blueprint blue, and the marginalia and callouts inherit the same structural rules in inverted tones. The grid, the rules, the justified text, and the accent left-rules persist across both modes.

Components are tactile and responsive. They are quiet at rest — thin borders, muted backgrounds, no heavy affordances — and responsive when touched: figures zoom to a modal on click, AI prompts copy to clipboard with feedback, code blocks reveal a copy button on hover, mermaid diagrams scale on hover and open in a modal. The rest state belongs to the manual; the interaction state belongs to the tool.

**Key Characteristics:**

- Print-derived grid: margin column (1.5in), content column (4.5in), 1fr remainder, 0.5in gutter
- Justified body text with automatic hyphenation and 1.5em first-line indent
- Ruled H2 headings (top + bottom 1px borders) and accent left-rules on callouts and code blocks
- Serif callouts (Computer Modern Serif / Charter / Georgia) breaking from sans-serif body
- Dual-mode palette: warm neutrals + blueprint blue (light), slate navy + brighter blue (dark)
- Small radii (3-8px) — the form language is architectural, not soft
- Functional shadows only: figures, cards, and modals; content surfaces are flat with tonal layering

## Colors

The palette is a dual-mode system: warm neutrals with a blueprint-blue accent in light mode, slate navy with a brighter blue accent in dark mode. Semantic colors (red, green, yellow) are defined but used sparingly — the manual is mostly monochrome with accent punctuation.

### Primary

- **Slate Ink** (#212b42–#36496e, ramp 50–900): The primary palette — a deep navy-blue that serves as the dark-mode surface family and the accent for active states, links, and structural elements. In light mode, the 600–900 steps appear in field descriptions, heading colors, and the version chip; in dark mode, the 700–900 steps are the body, backdrop, and card backgrounds.
- **Blueprint Blue** (#3182ce light / #4dabf7 dark): The accent color. Used for the accent left-rule on notes, code blocks, and blockquotes; for bullet markers; for mermaid diagram borders and lines; for footnote reference links; and for the "Note:" label prefix. Rare and functional — it is the single voice of color in an otherwise neutral system.

### Neutral

- **Margin Gray** (#fbfbfb–#111111, ramp 50–900): The true neutral ramp. Light mode uses 50–200 for backgrounds, borders, and heading bands; 600–900 for body text and headings. Dark mode uses 400–500 for muted text and the dark-mode version chip.
- **Dark Slate** (#0f172a, #1e293b, #334155, #3b4252): Dark-mode-specific surface colors for tables, mermaid diagrams, and code blocks. These are cooler and bluer than the margin-gray ramp, giving dark mode its distinct slate character.
- **Code Background** (#f7fafc light / #2d2d2d dark): The dedicated code and note background. Slightly cooler than the body background to create tonal separation without a border.

### Semantic

- **Warning Vermilion** (#FF3B10, #FF7353, #BB2402): Used only for the required-field asterisk in `::field` components. Red is otherwise absent from the system.

### Named Rules

**The One Accent Rule.** Blueprint Blue is the only chromatic accent in the system. It appears as left-rules, bullet markers, link colors, and diagram strokes — never as a fill on large surfaces. Its rarity is the point; it functions as a margin annotation, not a brand color.

**The Mode-Shift Rule.** Dark mode is not an inverted light mode. It shifts to a cooler, bluer palette: the primary navy ramp becomes the surface family, the accent brightens, and the dark-slate table colors replace the warm neutral table colors. The grid, rules, and typography persist unchanged.

## Typography

**Body Font:** ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif (Pinceau `font.sans`)
**Callout Font:** Computer Modern Serif, Charter, Bitstream Charter, Sitka Text, Georgia, serif
**Code Font:** Fira Code, Roboto Mono, Consolas, Monaco, Andale Mono, monospace
**Label Font:** ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas (Pinceau `font.mono`)

**Character:** The body is a clean system sans-serif — neutral, legible, engineered for screen reading at 11pt with 1.4 line-height. The callout serif (Computer Modern Serif with Charter/Georgia fallback) is the personality voice: it marks notes, marginalia, and asides as something other than body text — a typographic shift that signals "stop reading forward, read this instead." The code font is Fira Code with ligatures enabled, sized at 0.9em with 1.5 line-height for dense but readable code blocks.

### Hierarchy

- **H1** (700, 16pt, 1.5em, uppercase, centered, 2px bottom border): Document title. The only uppercase, centered heading. Appears once per page.
- **H2** (700, 14pt, 1.5em, ruled top + bottom 1px border): Major section headings. The rules create a horizontal band that separates sections the way a printed manual does. Padding: 0.5em 0 0.5em 1em.
- **H3** (700, 14pt): Subsection headings. Same size as H2 but without the rules — distinguished by position and indentation (1em left padding).
- **H4** (700, 11pt): Sub-subsection headings. Same weight as H3, smaller size.
- **H5** (700, 10pt): Minor headings.
- **H6** (700, 9pt): The smallest heading — used for fine-grained structural labels.
- **Body** (400, 11pt, 1.4 line-height, justified, 1.5em first-line indent): The reading surface. Justified with `text-justify: inter-word` and `hyphens: auto`. First-line indent of 1.5em on paragraphs (suppressed after headings in the commented-out rule).
- **Caption** (400, 0.9em, italic): Figure and table captions. Centered, muted color.
- **Field Name** (600, 0.875rem): The name of a field in `::field` components. Bold, gray-900/100.
- **Field Type** (400, 0.75rem, gray-500/400): The type annotation in parentheses after a field name. Muted, smaller.
- **Label Uppercase** (600, 0.75rem, 0.05em letter-spacing, uppercase): The AI prompt header label. Monospace, centered, blueprint blue.

### Typography Rules

**The Serif Break Rule.** Notes, marginalia, and asides use the callout serif (Computer Modern Serif / Charter / Georgia). Body text, headings, and code use sans-serif or monospace. The serif is the signal that the reader has left the main argument and entered an annotation.

**The Justified Text Rule.** Body paragraphs are justified with inter-word spacing and automatic hyphenation. This is a deliberate print-craft choice — it creates the even right margin of a typeset manual. The first-line indent of 1.5em reinforces the print metaphor. Do not switch to left-aligned without an explicit product decision.

## Layout

The page is a CSS grid with three columns: a 1.5in margin column (for marginalia/side notes), a 4.5in content column (for body text, headings, figures, tables), and a 1fr remainder column. The grid column gap is 0.5in. The total page width is capped at 8.5in, centered with `margin: 0 auto`.

Content elements (p, ul, ol, blockquote, figure, table, .note) are placed in grid-column 2 / -2. Marginalia (.marginalia) is placed in grid-column 1, right-aligned, at 0.8em font size. Mermaid diagrams span the full grid (1 / -1) to avoid being squeezed into the narrow margin column.

The vertical rhythm is governed by `--baseline: 1.5em` — every element after the first gets `margin-top: var(--baseline)`. This creates a consistent vertical beat across the page.

The Docus shell wraps this grid: a 64px header with logo + title + version chip, a left sidebar with navigation tree, and a footer (145px on mobile, 100px on sm+). The `readableLine` is 78ch. The main content area is padded and fluid.

Responsive behavior: the Pinceau media queries are xs (475px), sm (640px), md (768px), lg (1024px), xl (1280px), xxl (1536px). The header logo height shifts from `space.6` (1.5rem) to `space.7` (1.75rem) at sm. The footer height shifts from 145px to 100px at sm. The search results window gets margin, border-radius, and max-height at sm.

**The Grid Persistence Rule.** The three-column grid is the structural identity of the page. It does not collapse to a single column on smaller screens — the marginalia column narrows but persists. If a future responsive redesign collapses the grid, it is replacing the manual metaphor, not refining it.

## Elevation & Depth

The system is hybrid: flat surfaces for content, functional shadows for interactive elements and overlays. Depth is conveyed primarily through tonal layering (dark slate surfaces, border rules, accent left-rules) and only secondarily through shadows.

### Shadow Vocabulary

- **Figure Shadow** (`box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)`): On `figure img` — a light ambient shadow that lifts the figure slightly off the page. The only shadow on content imagery.
- **Card Shadow** (`box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03)`): On `.simple-card` — a barely-perceptible shadow that separates the card from the background. More tonal than spatial.
- **Modal Overlay** (`background: rgba(0, 0, 0, 0.6)`): On `.modal-image-overlay` and `.mermaid-modal-overlay` — a scrim that dims the page behind the modal. The modal itself has an 8px radius and a solid or near-solid background (white / rgba(15, 19, 32, 0.95)).
- **Pinceau Shadow Ramp** (xs through 2xl): Defined in tokens but not actively used by AtlasMD components. Available for future elevation needs.

### Elevation Rules

**The Functional Shadow Rule.** Shadows appear only on elements that lift or overlay: figures, cards, and modals. Content surfaces (body text, headings, tables, code blocks, notes) are flat — depth is conveyed through tonal layering and border rules. A shadow on a content surface is a bug.

## Shapes

The form language is architectural — small radii, thin borders, ruled headings. The system avoids soft, rounded shapes in favor of precise, structural ones.

- **Content radii** (3px): Code blocks, pre elements, mermaid diagrams. The smallest radius — nearly square, just enough to soften the corner.
- **Figure radii** (8px): Inline images and modal backgrounds. Slightly softer than content but still architectural.
- **Card radii** (10px, Pinceau `radii.md`): Simple cards and AI prompts. The softest radius in the system, but still restrained.
- **Table radii** (none): Tables have square corners — borders define the cells, not radii.
- **Version chip** (25px pill): The only fully-rounded element. A small pill shape for the version number next to the title.
- **Note callout** (0 3px 3px 0): Asymmetric — square on the left (where the accent left-rule sits), 3px on the right.
- **Border rules** (1px solid): The primary structural device. H2 headings have top + bottom borders. Tables have cell borders. Code blocks and notes have a 3px accent left-border. Blockquotes have a 4px accent left-border. Subfield containers have a 2px left border.

**The Rule-Not-Shadow Rule.** Structural separation is achieved with border rules, not shadows. A section break is a 1px line, not a drop shadow. An accent is a 3px left-rule, not a glow. The system prefers drawn lines over cast shadows.

## Components

### Notes (::note)

- **Shape:** Asymmetric radius (0 3px 3px 0), 3px accent left-rule (blueprint blue)
- **Background:** Code background (#f7fafc light / dark-slate in dark mode)
- **Padding:** 0.5em 1em 0.5em 4em (extra left padding for the "Note:" prefix)
- **Prefix:** "Note:" in bold, accent color, positioned absolute at left 0.5em
- **Font:** Callout serif (Computer Modern Serif / Charter / Georgia)
- **Behavior:** Static — no hover or interaction states

### Side Notes (::side-note)

- **Placement:** Grid column 1 (margin column), right-aligned
- **Font:** Callout serif, 0.8em, secondary color (margin-gray-600)
- **Behavior:** In dark mode, gets a 1px border, 1rem radius, and tight padding (0.15rem 0.6rem) — becomes a small bordered pill in the margin

### Figures (::fig)

- **Shape:** 8px radius on inline images
- **Hover:** `transform: scale(1.02)` with 0.2s ease transition
- **Modal:** Full-screen overlay (rgba(0,0,0,0.6) scrim), modal background is white (light) or rgba(15,19,32,0.95) (dark), 8px radius, max 95vw/95vh image
- **Dark mode:** Supports separate light/dark image sources via `src` / `darkmodeSrc` props
- **Accessibility:** `role="dialog"`, `aria-modal="true"`, Escape key closes
- **Props:** `src`, `darkmodeSrc`, `caption`, `width`, `srcModal`, `darkmodeSrcModal`, `allowZoom`, `keepTransparentBg`

### Field Definitions (::field)

- **Layout:** Flex, baseline-aligned, 0.25rem gap
- **Field name:** 600 weight, 0.875rem, gray-900/100
- **Field type:** 0.75rem, gray-500/400, in parentheses
- **Required marker:** Bold, warning-vermilion-600/400, asterisk
- **Description:** Italic, slate-ink-600/300, 0.875rem paragraphs
- **Subfields:** 0.75rem left padding, 2px left border (margin-gray-200 light / slate-ink-600 dark)

### Simple Cards (::simple-card)

- **Shape:** 10px radius (Pinceau `radii.md`), 1px border
- **Background:** Margin-gray-50 (light) / slate-ink-800 (dark)
- **Border:** Margin-gray-200 (light) / slate-ink-700 (dark)
- **Shadow:** `0 1px 2px 0 rgba(0,0,0,0.03)` — barely perceptible
- **Padding:** 0.75rem top, 0.25rem bottom, 0.75rem left, 0.75rem right margin
- **Font:** 0.875rem (Pinceau `fontSize.sm`)

### AI Prompts (::ai-prompt)

- **Shape:** 10px radius, 1px border, overflow hidden
- **Background:** Margin-gray-50 (light) / slate-ink-800 (dark)
- **Border:** Margin-gray-200 (light) / slate-ink-700 (dark), shifts to slate-ink-400 on hover
- **Header:** Separate bar with border-bottom, margin-gray-100 background (light) / slate-ink-900 (dark)
- **Header label:** Monospace, 0.75rem, 600 weight, 0.05em letter-spacing, uppercase, centered, slate-ink-600/300
- **Copy hint:** Absolute-positioned right, opacity 0 → 1 on hover, 0.2s transition
- **Content:** 12px padding, 0.875rem, 1.5 line-height
- **Behavior:** Click anywhere copies slot content to clipboard; shows "Copied!" for 1s then reverts

### Code Blocks (ProseCode)

- **Font:** Fira Code / Roboto Mono / Consolas, 0.9em, 1.5 line-height
- **Shape:** 3px radius, 3px accent left-rule
- **Padding:** 1em for pre blocks, 0.2em 0.4em for inline code
- **Copy button:** Appears on hover (ProseCodeCopyButton)
- **Mermaid:** Full-width grid span (1 / -1), 3px radius, 1px border, hover scale(1.01), click opens modal
- **Mermaid modal:** Same overlay pattern as Fig — rgba(0,0,0,0.6) scrim, white/slate background, 8px radius
- **Mermaid theme:** Custom light/dark variables — slate node colors, blueprint-blue borders and lines
- **Highlighting:** github-light (default) / github-dark (dark) / monokai (sepia)

### Tables

- **Shape:** Square corners, 1px cell borders, 2px header bottom border
- **Header:** Code-bg background (light) / dark-slate-800 (dark), 600 weight, white text in dark mode
- **Rows:** Alternating backgrounds — white/rgba(0,0,0,0.02) (light), dark-slate-800/900 (dark)
- **Hover:** Row background shifts to table-hover-bg, text to white (dark)
- **Width:** 100%, border-collapse

### Logo + Header

- **Logo:** 50px × 50px image, convention-based filenames (logo-light-mode.png, logo-dark-mode.png, logo-dark-mode-bg.png)
- **Title:** 30px, bold, slate-ink-900 (light) / white (dark), 5px left/right margin
- **Version chip:** 12px, 25px pill radius, white text on margin-gray-800 (light) / margin-gray-500 (dark), 2px 7px padding
- **Header height:** 64px

### Navigation (Docus sidebar)

- **Behavior:** `sidebar-follow` plugin auto-expands the navigation tree to the current page and collapses siblings. Active link scrolls into view smoothly.
- **Scroll:** `scroll-behavior` plugin handles hash navigation with sticky-header offset (estimates header height, falls back to 80px). Retries for up to 1s to find the target element after navigation.
- **Section headers:** Docus default — sans-serif, 14px, 600 weight, no text-transform or letter-spacing. Collapsible with chevron icon.
- **Leaf links:** Sans-serif, 14px, 400 weight, gray-500 (#939393) at rest. Active page gets primary-500 (#36496e) text and 500 weight. No accent left-rule or tree guide lines.
- **Container:** 1px border-right (gray-100 / #f5f5f5). Default browser scrollbar.

### Right-side Table of Contents (page-level)

- **Title:** Docus default — sans-serif, 14px, 600 weight, "Table of Contents". Hidden on mobile (<lg); the mobile collapsible button shows the same title with a chevron.
- **Links:** Sans-serif, 14px, 400 weight, gray-500 (#939393) at rest, darkening on hover. The active heading gets primary-500 (#36496e) text. No accent left-rule or tree guide lines.
- **Depth indentation:** depth-3 headings indent 12px (Pinceau `space.3`); deeper levels indent further via the Docus default ramp.
- **Container:** 1px border-left (gray-100 / #f5f5f5). Sticky, full viewport height minus header.

## Do's and Don'ts

### Do

- **Do** use the callout serif (Computer Modern Serif / Charter / Georgia) for notes, marginalia, and asides — the serif break is the signal that the reader has entered an annotation.
- **Do** justify body text with inter-word spacing and automatic hyphenation — the even right margin is the print-craft signature.
- **Do** use the 3px accent left-rule (blueprint blue) on notes, code blocks, and blockquotes — it is the primary structural accent device.
- **Do** keep radii small (3-8px for content, 10px for cards) — the form language is architectural, not soft.
- **Do** use tonal layering (slate surfaces, border rules) for depth on content surfaces — reserve shadows for figures, cards, and modals.
- **Do** span mermaid diagrams across the full grid (1 / -1) — they must not be squeezed into the margin column.
- **Do** support separate light/dark image sources in `::fig` — the manual metaphor persists in both modes.
- **Do** keep the version chip as the only fully-rounded element — it is a small, deliberate exception to the architectural form language.

### Don't

- **Don't** use blueprint blue as a fill on large surfaces — it is an accent, not a brand color. Its rarity is the point.
- **Don't** add shadows to content surfaces (body text, headings, tables, code blocks, notes) — depth is conveyed through tonal layering and border rules.
- **Don't** collapse the three-column grid (margin / content / 1fr) into a single column without an explicit product decision — the grid is the structural identity of the manual.
- **Don't** switch body text from justified to left-aligned without an explicit product decision — the even right margin is a deliberate print-craft choice.
- **Don't** use red outside of the required-field asterisk — warning vermilion is reserved for that single purpose.
- **Don't** use rounded corners larger than 10px on content components — the system's maximum content radius is 10px (cards). Larger radii break the architectural form language.
- **Don't** treat dark mode as an inverted light mode — it shifts to a cooler, bluer palette with distinct surface colors (dark-slate family) for tables and diagrams.
