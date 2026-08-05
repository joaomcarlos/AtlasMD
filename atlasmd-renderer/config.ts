import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { parse as parseTOML } from 'smol-toml'

export interface AtlasFooterCredits {
  text: string
  url?: string
  icon: string
}

export interface AtlasFooterText {
  label: string
  url?: string
}

export interface AtlasFooter {
  credits?: AtlasFooterCredits
  text?: AtlasFooterText
}

export interface AtlasSocial {
  url: string
  label: string
  icon: string
}

export interface AtlasConfig {
  title: string
  baseUrl: string
  socials?: AtlasSocial[]
  footer?: AtlasFooter
}

const DEFAULTS: AtlasConfig = {
  title: 'Atlas',
  baseUrl: '/',
}

/**
 * Load AtlasMD configuration from a mounted TOML file.
 *
 * Lookup order (first existing file wins):
 *   1. /app/config.toml  — Docker runtime mount
 *   2. ./config.toml     — local dev, next to nuxt.config.ts
 *
 * Only CI/build-driven values stay as env vars: CI_PAGES_URL (GitLab CI),
 * APP_VERSION (build arg), PORT. All consumer configuration lives in the file.
 */
function loadConfig(): AtlasConfig {
  const candidates = ['/app/config.toml', resolve('./config.toml')]
  for (const p of candidates) {
    let raw: string
    try {
      raw = readFileSync(p, 'utf-8')
    } catch {
      continue
    }
    const parsed = parseTOML(raw) as Partial<AtlasConfig>
    return { ...DEFAULTS, ...parsed }
  }
  return DEFAULTS
}

export const atlasConfig = loadConfig()
