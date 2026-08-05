<script setup lang="ts">
import { useClipboard } from '@vueuse/core'

const { copy: copyToClipboard } = useClipboard()
const state = ref('init')

const props = defineProps({
  label: {
    type: String,
    default: 'AI Prompt'
  }
})

const slotContent = ref('')

onMounted(() => {
  slotContent.value = (templateRef('content')?.$el?.textContent ?? '').trim()
})

const copy = () => {
  copyToClipboard(slotContent.value)
    .then(() => {
      state.value = 'copied'
      setTimeout(() => { state.value = 'init' }, 1000)
    })
    .catch(() => console.warn("Couldn't copy to clipboard!"))
}
</script>

<template>
  <div class="ai-prompt" @click="copy">
    <div class="header">
      <span class="label">{{ props.label }}</span>
      <span class="copy-hint">{{ state === 'copied' ? 'Copied!' : 'Click to copy' }}</span>
    </div>
    <div ref="content" class="content">
      <slot />
    </div>
  </div>
</template>

<style>
.ai-prompt {
  position: relative;
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radii-md);
  background: var(--color-gray-50);
  margin-bottom: 10px;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.2s;
}

.ai-prompt:hover {
  border-color: var(--color-primary-400);
}

.ai-prompt .header {
  position: relative;
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border-bottom: 1px solid var(--color-gray-200);
  background: var(--color-gray-100);
  font-size: 0.75rem;
  font-weight: 600;
  font-family: var(--font-mono);
}

.ai-prompt .label {
  flex: 1;
  text-align: center;
  color: var(--color-primary-600);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.ai-prompt .copy-hint {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-gray-400);
  opacity: 0;
  transition: opacity 0.2s;
}

.ai-prompt:hover .copy-hint {
  opacity: 1;
}

.ai-prompt .content {
  padding: 12px;
  font-size: 0.875rem;
  line-height: 1.5;
}

@media (prefers-color-scheme: dark) {
  .ai-prompt {
    border-color: var(--color-primary-700);
    background: var(--color-primary-800);
  }

  .ai-prompt .header {
    border-color: var(--color-primary-700);
    background: var(--color-primary-900);
  }

  .ai-prompt .label {
    color: var(--color-primary-300);
  }

  .ai-prompt .copy-hint {
    color: var(--color-gray-500);
  }
}
</style>
