import { useState, useCallback } from 'react'

export interface NavigationPage {
  id: string
  component: React.ComponentType
  title?: string
}

export function useNavigationStack(initialPage: NavigationPage) {
  const [stack, setStack] = useState<NavigationPage[]>([initialPage])

  const push = useCallback((page: NavigationPage) => {
    setStack(prev => [...prev, page])
  }, [])

  const pop = useCallback(() => {
    setStack(prev => prev.length > 1 ? prev.slice(0, -1) : prev)
  }, [])

  const popToRoot = useCallback(() => {
    setStack(prev => [prev[0]])
  }, [])

  const getCurrentPage = useCallback(() => {
    return stack[stack.length - 1]
  }, [stack])

  const canGoBack = useCallback(() => {
    return stack.length > 1
  }, [stack])

  return {
    stack,
    push,
    pop,
    popToRoot,
    getCurrentPage,
    canGoBack,
    stackDepth: stack.length
  }
}