import { useEffect } from 'react'
import { useAppStore } from '../../stores/appStore'

/**
 * Hook to automatically set the current child page for action sheet context
 * This mirrors the pattern used by usePageInstructions but uses the app store
 */
export const usePageActions = (pageId: string) => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  
  useEffect(() => {
    // Set the current child page in the store
    setCurrentChildPage(pageId)
    
    // Cleanup: clear child page when component unmounts
    return () => {
      setCurrentChildPage(null)
    }
  }, [pageId, setCurrentChildPage])
}