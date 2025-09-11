import { useState, useEffect, useCallback, useRef } from 'react'
import { useAppStore } from '../../stores/appStore'
import { preloadingService, type LoadingProgress } from '../../services/preloading/PreloadingService'

export interface AppInitializationState {
  isInitialized: boolean
  isInitializing: boolean
  progress: number
  status: string
  stage: string
  error: string | null
  canHideSplash: boolean
  initializationTime: number
}

export interface AppInitializationActions {
  startInitialization: () => Promise<void>
  skipInitialization: () => void
  retryInitialization: () => Promise<void>
}

/**
 * Hook for managing app initialization with real asset preloading
 * Coordinates with Zustand store and PreloadingService
 */
export function useAppInitialization(): AppInitializationState & AppInitializationActions {
  // App store integration
  const selectedPieceSet = useAppStore((state) => state.selectedPieceSet)
  const audioEnabled = useAppStore((state) => state.audioEnabled)
  const currentTheme = useAppStore((state) => state.currentTheme)
  const lastVisited = useAppStore((state) => state.lastVisited)
  
  // Initialization state
  const [isInitialized, setIsInitialized] = useState(false)
  const [isInitializing, setIsInitializing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Initializing...')
  const [stage, setStage] = useState('idle')
  const [error, setError] = useState<string | null>(null)
  const [minTimeElapsed, setMinTimeElapsed] = useState(false)
  const [initializationTime, setInitializationTime] = useState(0)
  
  // Refs for cleanup
  const initializationStartTime = useRef<number>(0)
  const minTimeTimer = useRef<NodeJS.Timeout | null>(null)
  const isComponentMounted = useRef(true)

  // Derived state
  const canHideSplash = isInitialized && minTimeElapsed

  /**
   * Handle progress updates from PreloadingService
   */
  const handleProgress = useCallback((loadingProgress: LoadingProgress) => {
    if (!isComponentMounted.current) return
    
    setProgress(loadingProgress.progress)
    setStatus(loadingProgress.status)
    setStage(loadingProgress.stage)
  }, [])

  /**
   * Start the initialization process
   */
  const startInitialization = useCallback(async () => {
    if (isInitializing || isInitialized) return

    setIsInitializing(true)
    setError(null)
    setProgress(0)
    setStatus('Starting initialization...')
    initializationStartTime.current = Date.now()

    // Set minimum display time (800ms to prevent flash)
    minTimeTimer.current = setTimeout(() => {
      if (isComponentMounted.current) {
        setMinTimeElapsed(true)
      }
    }, 800)

    try {
      // Subscribe to progress updates
      preloadingService.onProgress(handleProgress)

      // Get user preferences for asset prioritization
      const userPrefs = {
        selectedPieceSet,
        audioEnabled,
        currentTheme,
        lastVisited
      }

      // Start preloading sequence
      const results = await preloadingService.preloadAll(userPrefs)
      
      if (!isComponentMounted.current) return

      // Log results for debugging
      console.log('🎯 Initialization Results:', {
        criticalAssets: results.critical,
        importantAssets: results.important,
        totalTime: results.totalTime,
        userPrefs
      })

      // Mark as initialized
      setIsInitialized(true)
      setInitializationTime(Date.now() - initializationStartTime.current)
      setProgress(100)
      setStatus('Ready to play!')
      setStage('completed')

    } catch (initError) {
      console.error('❌ Initialization failed:', initError)
      
      if (isComponentMounted.current) {
        setError(initError instanceof Error ? initError.message : 'Initialization failed')
        setStatus('Initialization failed - Click to retry')
        setStage('error')
      }
    } finally {
      if (isComponentMounted.current) {
        setIsInitializing(false)
      }
    }
  }, [isInitializing, isInitialized, selectedPieceSet, audioEnabled, currentTheme, lastVisited, handleProgress])

  /**
   * Skip initialization and continue with degraded experience
   */
  const skipInitialization = useCallback(() => {
    console.log('⏭️ Skipping initialization - degraded experience mode')
    
    if (minTimeTimer.current) {
      clearTimeout(minTimeTimer.current)
    }
    
    setIsInitialized(true)
    setMinTimeElapsed(true)
    setProgress(100)
    setStatus('Continuing with basic assets...')
    setStage('skipped')
    setInitializationTime(Date.now() - initializationStartTime.current)
  }, [])

  /**
   * Retry initialization after failure
   */
  const retryInitialization = useCallback(async () => {
    console.log('🔄 Retrying initialization...')
    
    // Reset state
    setIsInitialized(false)
    setMinTimeElapsed(false)
    setError(null)
    
    // Restart initialization
    await startInitialization()
  }, [startInitialization])

  /**
   * Auto-start initialization on first mount
   */
  useEffect(() => {
    let mounted = true
    
    // Small delay to ensure store is rehydrated
    const initTimer = setTimeout(() => {
      if (mounted && !isInitializing && !isInitialized) {
        startInitialization()
      }
    }, 100)

    return () => {
      mounted = false
      clearTimeout(initTimer)
    }
  }, [startInitialization, isInitializing, isInitialized])

  /**
   * Cleanup on unmount
   */
  useEffect(() => {
    return () => {
      isComponentMounted.current = false
      
      if (minTimeTimer.current) {
        clearTimeout(minTimeTimer.current)
      }
    }
  }, [])

  /**
   * Handle store changes - restart initialization if critical preferences change
   */
  const prevPrefsRef = useRef({ selectedPieceSet, audioEnabled, currentTheme })
  
  useEffect(() => {
    const prevPrefs = prevPrefsRef.current
    const currentPrefs = { selectedPieceSet, audioEnabled, currentTheme }
    
    // Check if critical preferences changed after initialization
    if (isInitialized && (
      prevPrefs.selectedPieceSet !== selectedPieceSet ||
      prevPrefs.currentTheme !== currentTheme
    )) {
      console.log('🔄 Critical preferences changed, reinitializing...', {
        from: prevPrefs,
        to: currentPrefs
      })
      
      // Reset and restart initialization
      setIsInitialized(false)
      setMinTimeElapsed(false)
      startInitialization()
    }
    
    prevPrefsRef.current = currentPrefs
  }, [selectedPieceSet, audioEnabled, currentTheme, isInitialized, startInitialization])

  return {
    // State
    isInitialized,
    isInitializing,
    progress,
    status,
    stage,
    error,
    canHideSplash,
    initializationTime,
    
    // Actions
    startInitialization,
    skipInitialization,
    retryInitialization
  }
}