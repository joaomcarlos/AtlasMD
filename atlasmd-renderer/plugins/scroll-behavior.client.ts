import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  if (typeof window === 'undefined') return

  const router = useRouter()

  // console.log('[scroll-plugin] loaded; registering afterEach for hash scrolling')

  const findEl = (hash: string) => {
    const selector = (globalThis as any).CSS?.escape
      ? '#' + (globalThis as any).CSS.escape(hash.replace(/^#/, ''))
      : hash
    return document.querySelector<HTMLElement>(selector)
  }

  // estimate sticky header height; adjust as needed if theme changes
  const getScrollOffset = (): number => {
    // try to detect a top header; fallback to 80px
    const header = document.querySelector<HTMLElement>('header, .header, .docus-header')
    return header?.offsetHeight ?? 80
  }

  const smoothScrollToEl = (el: HTMLElement) => {
    const offset = getScrollOffset()
    const targetY = el.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top: Math.max(targetY, 0), behavior: 'smooth' })
  }

  const scrollToHash = (hash: string) => {
    let attempts = 0
    const maxAttempts = 50 // ~1s

    const tryScroll = () => {
      const el = findEl(hash)
      if (el) {
        // console.log('[scroll-plugin] element found for', hash, 'scrolling now (with offset)')
        smoothScrollToEl(el)
        return
      }

      if (attempts++ < maxAttempts) {
        setTimeout(tryScroll, 20)
      } else {
        // console.warn('[scroll-plugin] element not found after retries for', hash, '(initial)')
      }
    }

    setTimeout(tryScroll, 0)
  }

  // handle direct load with a hash in the URL
  if (window.location.hash) {
    // console.log('[scroll-plugin] initial page load with hash detected:', window.location.hash)
    // wait for router to be ready, then attempt
    router.isReady().then(() => scrollToHash(window.location.hash))
  }

  router.afterEach((to, from) => {
    // savedPosition is handled by native scroll restoration in SPA; this hook focuses on hash
    if (!to.hash) return

    const hash = to.hash
    // console.log('[scroll-plugin] navigation with hash detected:', hash)

    // queue after navigation/render tick
    setTimeout(() => scrollToHash(hash), 0)
  })
})
