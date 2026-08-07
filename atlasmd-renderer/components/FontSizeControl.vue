<script setup lang="ts">
const MIN_PT = 11
const MAX_PT = 21
const STEP = 1
const STORAGE_KEY = 'atlasmd-font-size'

// Body text (Docus --typography-fontSize-base) defaults to 16px = 12pt,
// while headings use --font-size-base at 11pt. The 1pt offset is preserved
// at every zoom level so body and headings scale together by 1pt steps.
const BODY_OFFSET_PT = 1

const currentPt = ref(MIN_PT)

const canDecrease = computed(() => currentPt.value > MIN_PT)
const canIncrease = computed(() => currentPt.value < MAX_PT)

function apply(pt: number) {
  document.documentElement.style.setProperty('--font-size-base', `${pt}pt`)
  document.documentElement.style.setProperty('--typography-fontSize-base', `${pt + BODY_OFFSET_PT}pt`)
}

function increase() {
  if (!canIncrease.value) return
  currentPt.value += STEP
  apply(currentPt.value)
  persist()
}

function decrease() {
  if (!canDecrease.value) return
  currentPt.value -= STEP
  apply(currentPt.value)
  persist()
}

function persist() {
  if (import.meta.client) {
    localStorage.setItem(STORAGE_KEY, String(currentPt.value))
  }
}

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    const pt = parseInt(saved, 10)
    if (!isNaN(pt) && pt >= MIN_PT && pt <= MAX_PT) {
      currentPt.value = pt
      apply(pt)
    }
  }
})
</script>

<template>
  <div class="font-size-control">
    <button aria-label="Increase font size" :disabled="!canIncrease" @click="increase">
      <Icon name="ph:plus" />
    </button>
    <button aria-label="Decrease font size" :disabled="!canDecrease" @click="decrease">
      <Icon name="ph:minus" />
    </button>
  </div>
</template>

<style scoped lang="ts">
css({
  '.font-size-control': {
    display: 'flex',
    alignItems: 'center',
  },

  button: {
    display: 'flex',
    padding: '{space.2}',
    marginLeft: 'calc(0px - {space.1})',
    color: '{color.gray.500}',
    '@dark': {
      color: '{color.gray.400}'
    },

    '&:hover:not(:disabled)': {
      color: '{color.gray.700}',
      '@dark': {
        color: '{color.gray.200}',
      }
    },

    '&:disabled': {
      opacity: '0.55',
      cursor: 'not-allowed',
    },
  }
})
</style>
