// https://github.com/nuxt-themes/docus/blob/main/nuxt.schema.ts
const socials: Record<string, { label: string; icon: string; href: string }> = {
  // Slack channel is shared across all AtlasMD projects
  slack: {
    label: 'Message us on Slack',
    icon: 'simple-icons:slack',
    href: 'https://example.slack.com/archives/C05FJE4BKC0',
  },
}
// Gitlab repo URL is project-specific — only include when provided
if (process.env.ATLAS_GITLAB_URL) {
  socials.gitlab = {
    label: process.env.ATLAS_GITLAB_LABEL || 'View the Gitlab repository',
    icon: 'simple-icons:gitlab',
    href: process.env.ATLAS_GITLAB_URL,
  }
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
    footer: {
      credits: {
        icon: 'heroicons-outline:cloud',
        text: 'AtlasMD',
        href: 'https://example.com/',
      },
      textLinks: [
        {
          text: 'Built with passion by the AtlasMD team',
          href: 'https://git.example.com/groups/eu-system-integrations/-/group_members',
          target: '_blank',
          rel: 'noopener'
        }
      ]
    }
  }
})
