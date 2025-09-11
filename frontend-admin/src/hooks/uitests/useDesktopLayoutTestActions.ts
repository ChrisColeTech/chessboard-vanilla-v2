import { useCallback } from 'react'
import { useAppStore } from '../../stores/appStore'

/**
 * Desktop Layout Test page actions hook
 * Handles actions specific to the desktop layout testing page
 */
export function useDesktopLayoutTestActions() {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)

  const toggleLayoutElements = useCallback(() => {
    console.log('🖥️ [DESKTOP LAYOUT TEST] Toggle layout elements')
    // Dispatch custom event to the DesktopLayoutTestPage component
    window.dispatchEvent(new CustomEvent('desktop-layout-toggle-elements'))
  }, [])

  // Navigation actions to other UI test pages
  const goToDragTest = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('dragtest')
    }, 100)
  }, [setCurrentChildPage])

  const goToAudioTest = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('uiaudiotest')
    }, 100)
  }, [setCurrentChildPage])

  const goToLayoutTest = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('layouttest')
    }, 100)
  }, [setCurrentChildPage])

  const goToMobileDragTest = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('mobiledragtest')
    }, 100)
  }, [setCurrentChildPage])

  return {
    toggleLayoutElements,
    goToDragTest,
    goToAudioTest,
    goToLayoutTest,
    goToMobileDragTest
  }
}