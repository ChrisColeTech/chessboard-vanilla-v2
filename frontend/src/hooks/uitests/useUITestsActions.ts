import { useCallback, useState } from 'react'
import { useChessAudio } from '../../services/audio/audioService'
import { useAppStore } from '../../stores/appStore'

/**
 * UI Tests page actions - placeholder implementations
 */
export function useUITestsActions() {
  const { playError } = useChessAudio()
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  const [testResults, setTestResults] = useState<string[]>([])

  const addTestResult = (message: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`])
  }

  const runUITests = useCallback(() => {
    console.log('🧪 [UI TESTS ACTIONS] Running UI tests')
    addTestResult("🧪 Starting UI component tests...")
    
    // Simulate test execution
    setTimeout(() => {
      addTestResult("✅ Button components: PASS")
      addTestResult("✅ Layout responsive: PASS") 
      addTestResult("✅ Color themes: PASS")
      addTestResult("🎉 All UI tests completed!")
    }, 1000)
  }, [])

  const clearUIResults = useCallback(() => {
    console.log('🗑️ [UI TESTS ACTIONS] Clearing UI test results')
    setTestResults([])
  }, [])

  const exportResults = useCallback(() => {
    const results = testResults.join('\n')
    const blob = new Blob([results], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'ui-test-results.txt'
    link.click()
    URL.revokeObjectURL(url)
  }, [testResults])

  const resetUITests = useCallback(() => {
    console.log('🔄 [UI TESTS ACTIONS] Resetting UI tests')
    setTestResults([])
    playError()
    addTestResult("🔄 UI tests have been reset")
  }, [playError])

  const goToDragTest = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('dragtest')
    }, 100)
  }, [setCurrentChildPage])

  const goToAudioTest = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('uiaudiotest')
    }, 100)
  }, [setCurrentChildPage])

  const goToLayoutTest = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('layouttest')
    }, 100)
  }, [setCurrentChildPage])

  const goToMobileDragTest = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('mobiledragtest')
    }, 100)
  }, [setCurrentChildPage])

  return {
    runUITests,
    clearUIResults,
    exportResults,
    resetUITests,
    goToDragTest,
    goToAudioTest,
    goToLayoutTest,
    goToMobileDragTest,
    testResults
  }
}