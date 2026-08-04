import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  if (typeof window === 'undefined') return

  const router = useRouter()
  const { navigation } = useContent()

  // Find all ancestors of a given path in the navigation tree
  const findAncestors = (tree: any[], targetPath: string): any[] => {
    const ancestors: any[] = []

    const search = (nodes: any[], path: string[] = []): boolean => {
      for (const node of nodes) {
        const currentPath = [...path, node]

        // Compare resolved paths to handle base URL correctly
        const resolvedNodePath = router.resolve(node._path).path
        const resolvedTargetPath = router.resolve(targetPath).path

        if (resolvedNodePath === resolvedTargetPath) {
          ancestors.push(...currentPath)
          return true
        }

        if (node.children && search(node.children, currentPath)) {
          return true
        }
      }
      return false
    }

    search(tree)
    return ancestors
  }

  // Update collapse states to expand the path to the current page
  const updateSidebarState = async (currentPath: string) => {
    try {
      const nav = await navigation.value
      if (!nav) return

      const ancestors = findAncestors(nav, currentPath)

      // Group ancestors by their parent path to update the correct collapse maps
      const collapseUpdates = new Map<string, Set<string>>()

      for (let i = 0; i < ancestors.length; i++) {
        const node = ancestors[i]
        const parent = i > 0 ? ancestors[i - 1] : null
        const parentPath = parent?._path || '/'

        if (!collapseUpdates.has(parentPath)) {
          collapseUpdates.set(parentPath, new Set())
        }

        // Mark this node as expanded (false = not collapsed)
        collapseUpdates.get(parentPath)!.add(node._path)
      }

      // Update each collapse map
      for (const [parentPath, expandedPaths] of collapseUpdates) {
        const stateKey = `docus-docs-aside-collapse-map-${parentPath}`
        const collapseMap = useState(stateKey, () => ({}))

        // Get all children at this level to collapse siblings
        const findChildren = (tree: any[], targetParentPath: string): any[] => {
          if (targetParentPath === '/') {
            return tree
          }

          const search = (nodes: any[]): any[] => {
            for (const node of nodes) {
              if (router.resolve(node._path).path === router.resolve(targetParentPath).path) {
                return node.children || []
              }
              if (node.children) {
                const result = search(node.children)
                if (result.length > 0) return result
              }
            }
            return []
          }

          return search(nav)
        }

        const children = findChildren(nav, parentPath)

        // Collapse all siblings, expand only those in the active path
        for (const child of children) {
          if (child.children) {
            (collapseMap.value as Record<string, boolean>)[child._path] = !expandedPaths.has(child._path)
          }
        }
      }

      // Scroll active item into view after a short delay
      setTimeout(() => {
        const activeLink = document.querySelector('.docs-aside-tree .link.active')
        if (activeLink) {
          activeLink.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'nearest'
          })
        }
      }, 100)

    } catch (error) {
      console.warn('[sidebar-follow] Failed to update sidebar state:', error)
    }
  }

  // Handle initial page load
  router.isReady().then(() => {
    updateSidebarState(router.currentRoute.value.path)
  })

  // Handle route changes
  router.afterEach((to) => {
    updateSidebarState(to.path)
  })
})
