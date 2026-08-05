// This file is shipped to the client. It must not import config.ts (which uses
// node:fs). Instead it imports config.value.json, a plain JSON file generated
// by config.ts at build startup.
import atlasConfig from './config.value.json'

// https://github.com/nuxt-themes/docus/blob/main/nuxt.schema.ts
const socials: Record<string, { label: string; icon: string; href: string }> = {}
for (const social of atlasConfig.socials ?? []) {
  const key = social.icon.split(':').pop() || String(Object.keys(socials).length)
  socials[key] = { label: social.label, icon: social.icon, href: social.url }
}

const footer: Record<string, unknown> = {}
if (atlasConfig.footer?.credits?.text) {
  footer.credits = {
    icon: atlasConfig.footer.credits.icon || 'heroicons-outline:cloud',
    text: atlasConfig.footer.credits.text,
    href: atlasConfig.footer.credits.url,
  }
} else {
  footer.credits = {
    icon: 'heroicons-outline:cloud',
    text: 'AtlasMD',
    href: 'https://github.com/joaomcarlos/AtlasMD',
  }
}
if (atlasConfig.footer?.text?.label) {
  footer.textLinks = [
    { text: atlasConfig.footer.text.label, href: atlasConfig.footer.text.url, target: '_blank', rel: 'noopener' }
  ]
} else {
  footer.textLinks = [
    { text: 'Built with passion by the AtlasMD team 🚀', href: 'https://github.com/joaomcarlos/AtlasMD', target: '_blank', rel: 'noopener' }
  ]
}

export default defineAppConfig({
  docus: {
    title: atlasConfig.title,
    description: 'Technical documentation.',
    socials,
    aside: { level: 0, collapsed: false, exclude: [] },
    main: { padded: true, fluid: true },
    header: { logo: true, showLinkIcon: true, exclude: [], fluid: true },
    footer,
  }
})
