import { useCallback } from 'react'
import { useStockfish } from './useStockfish'
import { useWorkerTestStore } from '../../stores/workerTestStore'
import { useChessAudio } from '../../services/audio/audioService'

/**
 * Worker page actions - uses Zustand store for real-time reactive updates
 * This approach allows the action sheet to directly update the page's console
 * without global variables or tight coupling
 */
export function useWorkerActions() {
  const { isReady, requestMove } = useStockfish()
  const { playGameStart } = useChessAudio()
  const { 
    addTestResult, 
    setLastMove, 
    setResponseTime, 
    setIsTestingReady,
    setIsTestingSpeed,
    setIsTestingPosition,
    setIsRunningAllTests,
    clearResults 
  } = useWorkerTestStore()

  const testWorkerReady = useCallback(async () => {
    setIsTestingReady(true)
    addTestResult("🔍 Testing if worker is ready...")
    
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      if (isReady) {
        addTestResult("✅ Worker is ready and responsive!", 'success')
      } else {
        addTestResult("❌ Worker not ready yet", 'error')
      }
    } catch (err) {
      addTestResult("❌ Worker readiness test failed", 'error')
    } finally {
      setIsTestingReady(false)
    }
  }, [isReady, addTestResult, setIsTestingReady])

  const testGoodMove = useCallback(async () => {
    setIsTestingPosition(true)
    addTestResult("🎯 Asking chess computer for a good opening move...")
    const startTime = Date.now()
    
    try {
      const move = await requestMove("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
      const time = Date.now() - startTime
      
      if (move) {
        setLastMove(move)
        setResponseTime(time)
        addTestResult(`✅ Computer suggests: ${move} (${time}ms)`, 'success')
      } else {
        addTestResult("❌ Computer couldn't suggest a move", 'error')
      }
    } catch (err) {
      addTestResult("❌ Error asking for move", 'error')
    } finally {
      setIsTestingPosition(false)
    }
  }, [requestMove, addTestResult, setLastMove, setResponseTime, setIsTestingPosition])

  const testSpeed = useCallback(async () => {
    setIsTestingSpeed(true)
    addTestResult("⚡ Testing response speed with 500ms limit...")
    const startTime = Date.now()
    
    try {
      await requestMove("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", 500)
      const time = Date.now() - startTime
      setResponseTime(time)
      const speedRating = time < 700 ? "Fast ⚡" : time < 1500 ? "Good ⭐" : "Slow 🐌"
      addTestResult(`✅ Response: ${time}ms (${speedRating})`, 'success')
    } catch (err) {
      addTestResult("❌ Speed test failed", 'error')
    } finally {
      setIsTestingSpeed(false)
    }
  }, [requestMove, addTestResult, setResponseTime, setIsTestingSpeed])

  const runAllTests = useCallback(async () => {
    setIsRunningAllTests(true)
    addTestResult("🚀 Running all tests...")
    
    try {
      await testWorkerReady()
      await new Promise(resolve => setTimeout(resolve, 1000))
      await testGoodMove()
      await new Promise(resolve => setTimeout(resolve, 1000))
      await testSpeed()
      addTestResult("🎉 All tests completed!", 'success')
    } finally {
      setIsRunningAllTests(false)
    }
  }, [testWorkerReady, testGoodMove, testSpeed, addTestResult, setIsRunningAllTests])

  const clearTestResults = useCallback(() => {
    clearResults()
    playGameStart() // Play welcome/new game sound when clearing results
    addTestResult("🧹 Results cleared", 'info')
  }, [clearResults, addTestResult, playGameStart])

  return {
    testWorkerReady,
    testGoodMove,
    testSpeed,
    runAllTests,
    clearTestResults
  }
}