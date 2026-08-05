import { atlasConfig } from './config'

// https://github.com/nuxt-themes/docus/blob/main/nuxt.schema.ts
const socials: Record<string, { label: string; icon: string; href: string }> = {}
for (const social of atlasConfig.socials ?? []) {
  // Key by icon name (e.g. "simple-icons:gitlab" → "gitlab"); falls back to index
  const key = social.icon.split(':').pop() || String(Object.keys(socials).length)
  socials[key] = {
    label: social.label,
    icon: social.icon,
    href: social.url,
  }
}

const footer: Record<string, unknown> = {}
// Footer credits — only include when configured
if (atlasConfig.footer?.credits?.text) {
  footer.credits = {
    icon: atlasConfig.footer.credits.icon || 'heroicons-outline:cloud',
    text: atlasConfig.footer.credits.text,
    href: atlasConfig.footer.credits.url,
  }
}
// Footer text link — only include when configured
if (atlasConfig.footer?.text?.label) {
  footer.textLinks = [
    {
      text: atlasConfig.footer.text.label,
      href: atlasConfig.footer.text.url,
      target: '_blank',
      rel: 'noopener'
    }
  ]
}

export default defineAppConfig({
  docus: {
    title: atlasConfig.title,
    description: 'Technical documentation.',
    socials,
    aside: {
      level: 0,
      collapsed: false,
      exclude: []
    },
    main: {
      padded: true,
      fluid: true
    },
    header: {
      logo: true,
      showLinkIcon: true,
      exclude: [],
      fluid: true
    },
    footer
  }
})
