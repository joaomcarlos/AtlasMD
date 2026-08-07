<script setup lang="ts">
import type { Lang } from 'shiki-es'
import type { PropType } from 'vue'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useClipboard } from '@vueuse/core'

// Fragment component (multiple root nodes: v-if/v-else div + <Teleport>).
// Disable attribute inheritance — Vue can't auto-attach fallthrough attrs
// to a fragment root, which causes "Extraneous non-props attributes" warnings
// when MDC passes meta from fenced code block metadata.
defineOptions({ inheritAttrs: false })

const props = defineProps({
  code: { type: String, default: '' },
  language: { type: String as PropType<Lang>, default: null },
  filename: { type: String, default: null },
  highlights: { type: Array as () => number[], default: () => [] }
})

// --- Language display names ---
const languageLabels: Record<string, string> = {
  ts: 'TypeScript', tsx: 'TypeScript', typescript: 'TypeScript',
  js: 'JavaScript', jsx: 'JavaScript', javascript: 'JavaScript',
  py: 'Python', python: 'Python',
  json: 'JSON', jsonc: 'JSON',
  toml: 'TOML', yaml: 'YAML', yml: 'YAML',
  bash: 'Bash', sh: 'Shell', shell: 'Shell', shellscript: 'Shell', zsh: 'Zsh',
  html: 'HTML', css: 'CSS', scss: 'SCSS',
  vue: 'Vue', sql: 'SQL',
  md: 'Markdown', markdown: 'Markdown',
  dockerfile: 'Dockerfile',
  diff: 'Diff',
  xml: 'XML',
  ini: 'INI',
  text: 'Text',
}

const languageLabel = computed(() => {
  if (!props.language) return ''
  const key = props.language.toLowerCase()
  return languageLabels[key] ?? props.language.toUpperCase()
})

// --- Copy functionality ---
const { copy: copyToClipboard } = useClipboard()
const copied = ref(false)
let copyTimer: ReturnType<typeof setTimeout> | null = null

const copyCode = () => {
  copyToClipboard(props.code)
    .then(() => {
      copied.value = true
      if (copyTimer) clearTimeout(copyTimer)
      copyTimer = setTimeout(() => { copied.value = false }, 1500)
    })
    .catch((err) => console.warn("Couldn't copy to clipboard!", err))
}

// --- Mermaid ---
const hovered = ref(false)
const mermaidSvg = ref<string | null>(null)
const modalIsOpen = ref(false)
const isClosing = ref(false)

const isDarkMode = () => document.documentElement.getAttribute('data-theme') === 'dark'

const renderMermaid = async () => {
  try {
    const mermaid = (await import('mermaid')).default
    const dark = isDarkMode()
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
      themeVariables: dark
        ? {
          background: 'transparent',
          primaryColor: '#1e293b',
          primaryTextColor: '#eaeaea',
          primaryBorderColor: '#4dabf7',
          secondaryColor: '#0f172a',
          tertiaryColor: '#334155',
          lineColor: '#4dabf7',
          textColor: '#e5e7eb',
          fontSize: '11pt',
        }
        : {
          background: 'transparent',
          primaryColor: '#f7fafc',
          primaryTextColor: '#1a365d',
          primaryBorderColor: '#3182ce',
          secondaryColor: '#eef2f7',
          tertiaryColor: '#e6ebf0',
          lineColor: '#4a5568',
          textColor: '#1a365d',
          fontSize: '11pt',
        },
    })
    const id = `mermaid-${Math.random().toString(36).slice(2, 9)}`
    const { svg } = await mermaid.render(id, props.code)
    mermaidSvg.value = svg
  } catch (e) {
    console.error('Mermaid rendering failed:', e)
  }
}

const openModal = () => { modalIsOpen.value = true }
const closeModal = () => {
  if (!modalIsOpen.value) return
  isClosing.value = true
  setTimeout(() => {
    modalIsOpen.value = false
    isClosing.value = false
  }, 250)
}

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && modalIsOpen.value) { closeModal() }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  if (props.language === 'mermaid') {
    renderMermaid()

    // Listen for theme changes
    const html = document.documentElement
    const observer = new MutationObserver(() => {
      renderMermaid()
    })
    observer.observe(html, { attributes: true, attributeFilter: ['data-theme'] })
  }
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  if (copyTimer) clearTimeout(copyTimer)
})
</script>

<template>
  <!-- Mermaid diagram -->
  <div v-if="language === 'mermaid'" class="mermaid-diagram" @click.stop="openModal">
    <div class="mermaid-label">Diagram</div>
    <div v-if="mermaidSvg" class="mermaid-inline" v-html="mermaidSvg" />
    <span v-else class="mermaid-loading">Loading diagram…</span>
  </div>

  <!-- Code block -->
  <div v-else :class="[`highlight-${language}`]" class="prose-code" @mouseenter="hovered = true"
    @mouseleave="hovered = false">
    <div class="code-header">
      <div class="code-header-info">
        <span v-if="languageLabel" class="code-lang">{{ languageLabel }}</span>
        <span v-if="filename" class="code-filename">{{ filename }}</span>
      </div>
      <button class="copy-btn" :class="{ 'is-copied': copied }" @click="copyCode"
        :aria-label="copied ? 'Copied to clipboard' : 'Copy code to clipboard'">
        <Icon :name="copied ? 'ph:check' : 'ph:copy'" size="14" class="copy-icon" />
        <span class="copy-text">{{ copied ? 'Copied' : 'Copy' }}</span>
      </button>
    </div>
    <div class="code-body">
      <slot />
    </div>
  </div>

  <!-- Mermaid modal -->
  <Teleport to="body">
    <div v-if="language === 'mermaid' && modalIsOpen" class="mermaid-modal-overlay" :class="{ 'is-closing': isClosing }"
      role="dialog" aria-modal="true" @click.stop="closeModal">
      <div class="mermaid-modal-bg" :class="{ 'is-closing': isClosing }" :style="{
        background: isDarkMode() ? 'rgba(15, 19, 32, 0.98)' : 'rgba(255, 255, 255, 0.98)'
      }" @click.stop="closeModal">
        <div class="mermaid-label">Diagram</div>
        <div v-if="mermaidSvg" class="mermaid-modal-svg" v-html="mermaidSvg" />
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
/* ===== Container ===== */
.prose-code {
  grid-column: 2 / -2;
  position: relative;
  width: 100%;
  margin: 0 0 var(--baseline, 1.5em) 0;
  border-left: 3px solid var(--accent-color, #3182ce);
  border-radius: 3px;
  overflow: hidden;
  background: var(--code-bg, #f7fafc);
}

/* ===== Header bar ===== */
.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.4em 0.75em;
  border-bottom: 1px solid var(--table-border, #ddd);
  background: var(--code-bg, #f7fafc);
}

.code-header-info {
  display: flex;
  align-items: baseline;
  gap: 0.75em;
  min-width: 0;
  overflow: hidden;
}

.code-lang {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent-color, #3182ce);
  white-space: nowrap;
  flex-shrink: 0;
}

.code-filename {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  color: var(--secondary-color, #4a5568);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ===== Copy button ===== */
.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35em;
  padding: 0.2em 0.5em;
  border: none;
  background: transparent;
  cursor: pointer;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--secondary-color, #4a5568);
  opacity: 0.45;
  transition: opacity 0.2s ease, color 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.prose-code:hover .copy-btn {
  opacity: 1;
}

.copy-btn:hover {
  color: var(--accent-color, #3182ce);
  opacity: 1;
}

.copy-btn.is-copied {
  color: var(--accent-color, #3182ce);
  opacity: 1;
}

.copy-btn:focus-visible {
  outline: 2px solid var(--accent-color, #3182ce);
  outline-offset: 1px;
  opacity: 1;
}

.copy-icon {
  flex-shrink: 0;
}

.copy-text {
  line-height: 1;
}

/* ===== Code body — override base.scss pre styles ===== */
.code-body :deep(pre) {
  border-left: none !important;
  border-radius: 0 !important;
  margin: 0 !important;
  background: transparent !important;
}

.code-body :deep(code) {
  display: block;
}

.code-body :deep(.line) {
  display: block;
  min-height: 1rem;
}

/* Shell prompt prefix */
.prose-code.highlight-zsh .code-body :deep(code .line),
.prose-code.highlight-sh .code-body :deep(code .line),
.prose-code.highlight-bash .code-body :deep(code .line),
.prose-code.highlight-shell .code-body :deep(code .line),
.prose-code.highlight-shellscript .code-body :deep(code .line) {
  position: relative;
  padding-inline-start: 1rem;
}

.prose-code.highlight-zsh .code-body :deep(code .line::before),
.prose-code.highlight-sh .code-body :deep(code .line::before),
.prose-code.highlight-bash .code-body :deep(code .line::before),
.prose-code.highlight-shell .code-body :deep(code .line::before),
.prose-code.highlight-shellscript .code-body :deep(code .line::before) {
  content: '>';
  position: absolute;
  top: 0;
  inset-inline-start: -0.1rem;
  display: block;
  user-select: none;
  font-weight: 700;
  color: var(--accent-color, #3182ce);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* Line highlighting — full-width tinted bar */
.code-body :deep(.line.highlight) {
  background: var(--highlight-target, rgba(255, 235, 59, 0.35));
  margin: 0 -1em;
  padding: 0 1em;
}

/* ===== Dark mode ===== */
:root[data-theme="dark"] .code-header {
  border-bottom-color: var(--table-border, #3b4252);
}

:root[data-theme="dark"] .code-filename {
  color: #9ca3af;
}

:root[data-theme="dark"] .copy-btn {
  color: #9ca3af;
}

/* ===== Mermaid diagram ===== */
.mermaid-diagram {
  width: 100%;
  overflow-x: auto;
  cursor: zoom-in;
  grid-column: 1 / -1;
  background: var(--code-bg, #f7fafc);
  border: 1px solid var(--border-color, #ddd);
  border-radius: 4px;
  padding: 0;
  margin: 0 0 var(--baseline, 1.5em) 0;
}

.mermaid-label {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  text-align: center;
  padding: 0.45em 1em;
  color: var(--accent-color, #3182ce);
  background: var(--code-bg, #f7fafc);
  border-bottom: 1px solid var(--border-color, #ddd);
}

:root[data-theme="dark"] .mermaid-diagram {
  /* Use the dark slate palette from the mermaid themeVariables,
     not --code-bg/--border-color (which are grey/#eaeaea in dark mode). */
  background: #0f172a;
  border-color: #334155;
}

:root[data-theme="dark"] .mermaid-label {
  background: #0f172a;
  border-bottom-color: #334155;
}

/* Inside the modal the label should blend with the modal background
   rather than the opaque --code-bg used by the inline container. */
.mermaid-modal-bg .mermaid-label {
  background: transparent;
  border-bottom-color: var(--border-color, #ddd);
}

:root[data-theme="dark"] .mermaid-modal-bg .mermaid-label {
  border-bottom-color: #334155;
}

.mermaid-loading {
  display: block;
  text-align: center;
  padding: 1.5em;
  opacity: 0.5;
  font-style: italic;
}

.mermaid-inline :deep(svg) {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  height: auto;
}

/* ===== Mermaid modal — mirrors Fig.vue ===== */
.mermaid-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  animation: mermaid-modal-fade-in 0.2s ease-out;
}

.mermaid-modal-bg {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 100%;
  border-radius: 8px;
  cursor: zoom-out;
  overflow: auto;
  animation: mermaid-modal-zoom-in 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  transform-origin: center;
}

@keyframes mermaid-modal-fade-in {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes mermaid-modal-zoom-in {
  from {
    transform: scale(0.85);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {

  .mermaid-modal-overlay,
  .mermaid-modal-bg {
    animation: none;
  }
}

.mermaid-modal-overlay.is-closing {
  animation: mermaid-modal-fade-out 0.25s ease-in forwards;
}

.mermaid-modal-bg.is-closing {
  animation: mermaid-modal-zoom-out 0.25s cubic-bezier(0.4, 0, 1, 1) forwards;
}

@keyframes mermaid-modal-fade-out {
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

@keyframes mermaid-modal-zoom-out {
  from {
    transform: scale(1);
    opacity: 1;
  }

  to {
    transform: scale(0.85);
    opacity: 0;
  }
}

.mermaid-modal-bg .mermaid-label {
  width: 100%;
  flex-shrink: 0;
}

.mermaid-modal-svg {
  width: 100%;
}

.mermaid-modal-svg :deep(svg) {
  display: block;
  margin: 0 auto;
  max-width: 95vw !important;
  max-height: 90vh !important;
  width: 100% !important;
  height: auto !important;
}

/* Isolate Mermaid SVG internals from inherited .page-body styles
   that leak through <foreignObject> HTML elements. */
.mermaid-inline :deep(foreignObject div),
.mermaid-inline :deep(foreignObject span),
.mermaid-inline :deep(foreignObject p),
.mermaid-modal-svg :deep(foreignObject div),
.mermaid-modal-svg :deep(foreignObject span),
.mermaid-modal-svg :deep(foreignObject p) {
  text-indent: 0 !important;
  text-align: center !important;
  font-size: inherit !important;
  line-height: normal !important;
  hyphens: none !important;
  white-space: normal !important;
  overflow: visible !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
}
</style>
