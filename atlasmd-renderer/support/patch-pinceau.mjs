#!/usr/bin/env node
/**
 * Patch pinceau runtime to use deterministic variant class names.
 *
 * Root cause: pinceau 0.18.10 generates variant class names with nanoid(6)
 * (random), causing Vue hydration class mismatches between SSR and client.
 * Fix: derive the class name from a hash of the deterministic cacheId.
 *
 * Applies to: pinceau/dist/runtime.mjs and runtime.cjs
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs'

const HASH_FN = `function _pvHash(str){let h=5381;let i=str.length;while(i)h=h*33^str.charCodeAt(--i);const _a=(c)=>String.fromCharCode(c+(c>25?39:97));let n="";let x=Math.abs(h>>>0);for(;x>52;x=x/52|0)n=_a(x%52)+n;return _a(x%52)+n}`

const files = [
  'node_modules/pinceau/dist/runtime.mjs',
  'node_modules/pinceau/dist/runtime.cjs',
]

for (const f of files) {
  if (!existsSync(f)) continue
  let src = readFileSync(f, 'utf8')

  // Skip if already patched
  if (src.includes('_pvHash')) {
    console.log(`[patch-pinceau] already patched: ${f}`)
    continue
  }

  // Insert hash function after HYDRATION_SELECTOR line
  const marker = 'const HYDRATION_SELECTOR = ".phy[--]";'
  if (!src.includes(marker)) {
    console.warn(`[patch-pinceau] marker not found in ${f}, skipping`)
    continue
  }
  src = src.replace(marker, marker + '\n' + HASH_FN)

  // Replace nanoid-based variant class with deterministic hash of cacheId
  src = src.replace('`pv-${nanoid.nanoid(6)}`', '`pv-${_pvHash(cacheId)}`')
  src = src.replace('`pv-${nanoid(6)}`', '`pv-${_pvHash(cacheId)}`')

  writeFileSync(f, src)
  console.log(`[patch-pinceau] patched ${f}`)
}
