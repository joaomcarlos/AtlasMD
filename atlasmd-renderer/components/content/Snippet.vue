<script setup lang="ts">
import { PropType } from 'vue'

const props = defineProps({
  content: {
    type: [Array, String] as PropType<string[] | string>,
    required: true
  }
})
</script>

<template>
  <div class="snippet">
    <Terminal :content="props.content" />
  </div>
</template>

<style>
.snippet .terminal {
  height: auto !important;
  max-width: 100% !important;
  margin-bottom: 10px;
}

.snippet .terminal .prompt {
  position: absolute;
  bottom: 4px;
  left: 0;
  right: 0;
  background: var(--color-gray-100);
  padding: 10px 0;
}

@media (prefers-color-scheme: dark) {
  .snippet .terminal .prompt {
    background: var(--color-primary-900);
  }
}
</style>
