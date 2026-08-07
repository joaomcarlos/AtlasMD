<script setup lang="ts">
import type { Lang } from 'shiki-es'
import type { PropType } from 'vue'
import { onBeforeUnmount, onMounted, ref } from 'vue'

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

const hovered = ref(false)
const mermaidSvg = ref<string | null>(null)
const modalIsOpen = ref(false)

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
const closeModal = () => { modalIsOpen.value = false }

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
})
</script>

<template>
  <div v-if="language === 'mermaid'" class="mermaid-diagram" @click.stop="openModal">
    <div v-if="mermaidSvg" class="mermaid-inline" v-html="mermaidSvg" />
    <span v-else style="opacity: 0.5; font-style: italic;">Loading diagram…</span>
  </div>
  <div v-else :class="[`highlight-${language}`]" class="prose-code" @mouseenter="hovered = true"
    @mouseleave="hovered = false">
    <span v-if="filename" class="filename">{{ filename }}</span>
    <slot />
    <ProseCodeCopyButton :show="hovered" :content="code" class="copy-button" />
  </div>

  <Teleport to="body">
    <div v-if="language === 'mermaid' && modalIsOpen" class="mermaid-modal-overlay" role="dialog" aria-modal="true"
      @click.stop="closeModal">
      <div class="mermaid-modal-bg" :style="{
        background: isDarkMode() ? 'rgba(15, 19, 32, 0.98)' : 'rgba(255, 255, 255, 0.98)'
      }" @click.stop="closeModal">
        <div v-if="mermaidSvg" class="mermaid-modal-svg" v-html="mermaidSvg" />
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
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

.mermaid-diagram::before {
  content: "Diagram";
  display: block;
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

.mermaid-inline :deep(svg) {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  height: auto;
}

/* modal — mirrors Fig.vue */
.mermaid-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.mermaid-modal-bg {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 100%;
  border-radius: 8px;
  cursor: zoom-out;
  overflow: auto;
}

.mermaid-modal-svg {
  width: 100%;
}

.mermaid-modal-svg :deep(svg) {
  display: block;
  margin: 0 auto;
  /* Let the SVG expand to fill the modal viewport */
  max-width: 95vw;
  max-height: 90vh;
  width: 100%;
  height: auto;
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
