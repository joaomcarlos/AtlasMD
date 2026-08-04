// https://github.com/nuxt-themes/docus/blob/main/nuxt.schema.ts
const socials: Record<string, { label: string; icon: string; href: string }> = {}
// Slack social link — only include when ATLAS_SLACK_URL is provided
if (process.env.ATLAS_SLACK_URL) {
  socials.slack = {
    label: process.env.ATLAS_SLACK_LABEL || 'Message us on Slack',
    icon: 'simple-icons:slack',
    href: process.env.ATLAS_SLACK_URL,
  }
}
// Git repo URL is project-specific — only include when provided
if (process.env.ATLAS_GITLAB_URL) {
  socials.gitlab = {
    label: process.env.ATLAS_GITLAB_LABEL || 'View the Gitlab repository',
    icon: 'simple-icons:gitlab',
    href: process.env.ATLAS_GITLAB_URL,
  }
}

const footer: Record<string, unknown> = {}
// Footer credits — only include when ATLAS_FOOTER_CREDITS_TEXT is provided
if (process.env.ATLAS_FOOTER_CREDITS_TEXT) {
  footer.credits = {
    icon: process.env.ATLAS_FOOTER_CREDITS_ICON || 'heroicons-outline:cloud',
    text: process.env.ATLAS_FOOTER_CREDITS_TEXT,
    href: process.env.ATLAS_FOOTER_CREDITS_URL,
  }
}
// Footer text link — only include when ATLAS_FOOTER_TEXT is provided
if (process.env.ATLAS_FOOTER_TEXT) {
  footer.textLinks = [
    {
      text: process.env.ATLAS_FOOTER_TEXT,
      href: process.env.ATLAS_FOOTER_TEXT_URL,
      target: '_blank',
      rel: 'noopener'
    }
  ]
}

export default defineAppConfig({
  docus: {
    title: process.env.ATLAS_TITLE || 'Atlas',
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
