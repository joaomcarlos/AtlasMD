import { readdirSync, statSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { atlasConfig } from './config'

const { CI_PAGES_URL } = process.env
// Derive base path for GitLab Pages (e.g. /group/project/) – fallback to config baseUrl or /
// CI_PAGES_URL stays an env var because GitLab CI sets it automatically at deploy time.
const base = (CI_PAGES_URL) ? new URL(CI_PAGES_URL).pathname : (atlasConfig.baseUrl || '/')
// When baseURL is a subpath (e.g. /my-project/), routes starting with that prefix
// fail crawl validation (Nuxt 3 limitation). Build an ignore pattern from the base path.
const baseSegment = base.replace(/^\/+|\/+$/g, '')
const prerenderIgnore = baseSegment ? [new RegExp(`^/${baseSegment}-`)] : []

/**
 * Recursively walk the docs content directory and build route paths for every markdown file.
 * We remove numeric ordering prefixes like `2.` and drop trailing `index` segments.
 */
function buildContentRoutes() {
  const contentRoot = resolve('./content')
  const routes = new Set(['/'])
  // Only strip numeric ordering prefixes like `8.section` but keep version-like filenames (e.g. 2.1.2.md)
  // Negative lookahead ensures we do NOT match if the dot is followed by another digit (version pattern)
  const orderPrefix = /^\d+\.(?!\d)/

  function walk(dirRel: string) {
    const abs = join(contentRoot, dirRel)
    for (const entry of readdirSync(abs)) {
      if (entry.startsWith('.')) continue
      const relPath = dirRel ? `${dirRel}/${entry}` : entry
      const absPath = join(contentRoot, relPath)
      if (statSync(absPath).isDirectory()) {
        walk(relPath)
        continue
      }
      if (!entry.endsWith('.md')) continue // only markdown files
      if (entry.startsWith('_') && entry.endsWith('.md')) continue // _*.md files are private
      // Split path into segments, strip numeric prefixes & extensions
      const segments = relPath.split('/').map(seg => {
        if (seg === '_dir.yml') return ''
        // Preserve version number segments like 2.1.2 while still removing ordering prefixes
        return seg.replace(orderPrefix, '').replace(/\.md$/, '')
      }).filter(Boolean)
      if (segments.length === 0) return
      if (segments[segments.length - 1] === 'index') {
        segments.pop()
      }
      const route = '/' + segments.join('/')
      routes.add(route || '/')
    }
  }

  try { walk('') } catch (e) { /* ignore in environments without content */ }
  // Ensure predictable order for debugging
  return Array.from(routes).sort()
}

const contentRoutes = buildContentRoutes()
console.info('[prerender] content routes:', contentRoutes.length)

export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      // APP_VERSION is a build arg / CI value, not consumer config.
      atlasAppVersion: process.env.APP_VERSION,
      atlasTitle: atlasConfig.title,
      // Logos are convention-based fixed filenames in public/. No configuration needed.
      atlasLogoLight: '/logo-light-mode.png',
      atlasLogoDark: '/logo-dark-mode.png',
      atlasLogoDarkBg: '/logo-dark-mode-bg.png',
    }
  },
  compatibilityDate: '2024-10-24',
  extends: ['@nuxt-themes/docus'],
  modules: [
    // Remove it if you don't use Plausible analytics
    // https://github.com/nuxt-modules/plausible
    // '@nuxtjs/plausible',
    // '@nuxt/content',
  ],
  plugins: [
    { src: '~/plugins/scroll-behavior.client', mode: 'client' },
    { src: '~/plugins/sidebar-follow.client', mode: 'client' }
  ],
  css: [
    '~/assets/css/images.css',
    '~/assets/css/base.scss',
    '~/assets/css/sidebar.scss',
  ],
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  nitro: {
    prerender: {
      // Follow static links first
      crawlLinks: true,
      // Explicitly add every content-driven route (some nav links may render only after hydration)
      routes: contentRoutes,
      failOnError: false,
      // Ignore routes that fail validation when using baseURL with a subpath (Nuxt 3 limitation)
      // These routes are still prerendered successfully, but cause 404s during crawl validation
      ignore: prerenderIgnore,
      // Compress payload to reduce memory during parallel prerendering
      payloadExtraction: false,
      // Serialize prerendering to eliminate cache race conditions entirely
      concurrency: 1
    },
    // Use in-memory storage for cache during prerendering to prevent filesystem corruption
    storage: {
      cache: {
        driver: 'memory',
      }
    },
    routeRules: {
      '/**': { prerender: true }
    }
  },

  app: {
    baseURL: base,
    head: {
      link: [
        { rel: 'icon', type: 'image/x-icon', href: `${base}favicon.ico` },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: `${base}favicon-16.png` },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: `${base}favicon-32.png` },
      ]
    }
  },
  content: {
    // Disable caching to prevent corruption during prerendering
    cache: {
      maxAge: 0
    },
    watch: {
      ws: {
        port: 4000,
        hostname: '0.0.0.0',
      },
    },
    highlight: {
      // theme:'kanagawa-wave'
      // theme:'kanagawa-dragon'
      // theme:'kanagawa-lotus'
      theme: {
        // default: "everforest-light",
        // default: "kanagawa-lotus",
        default: "github-light",
        // dark: "everforest-dark",
        // dark: "kanagawa-dragon",
        // dark: "kanagawa-wave",
        dark: "github-dark",
        sepia: "monokai",
      },
    },
  },
  mdc: {
    highlight: {
      langs: ['python', 'mermaid', 'jsonc', 'toml']
    }
  },
  vite: {
    build: {
      // Suppress "Some chunks are larger than 500 kB" warnings from Docus theme bundles
      chunkSizeWarningLimit: 1000,
      // Suppress sourcemap warnings from pinceau-transforms plugin (it transforms files
      // without generating sourcemaps; setting this to false avoids the mismatch warning)
      sourcemap: false,
    },
    // Suppress "Unexpected first-child" css-syntax-error warnings from malformed Docus/Pinceau
    // prose selectors (missing colon before :first-child in generated CSS — harmless)
    esbuild: {
      logOverride: {
        'css-syntax-error': 'silent',
      },
    },
  },
})
