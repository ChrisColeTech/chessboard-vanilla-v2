import { useCallback } from 'react'
import { useAppStore } from '../../stores/appStore'
import { useAppInitialization } from '../core/useAppInitialization'
import { useUIClickSound } from '../audio/useUIClickSound'
import { assetCacheService } from '../../services/preloading/AssetCacheService'

/**
 * Functional splash page actions with real loading coordination
 */
export function useFunctionalSplashActions() {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  const openSplashModal = useAppStore((state) => state.openSplashModal)
  const closeSplashModal = useAppStore((state) => state.closeSplashModal)
  
  const { playUIClick } = useUIClickSound()
  
  const { 
    retryInitialization, 
    skipInitialization,
    progress,
    status,
    stage,
    isInitializing
  } = useAppInitialization()

  const testFunctionalLoading = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Test Real Loading', {
      progress,
      status,
      stage,
      isInitializing
    })
    playUIClick()
    
    // Show current loading state in console for debugging
    console.log('Current loading state:', { progress, status, stage, isInitializing })
  }, [progress, status, stage, isInitializing])

  const retryLoading = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Retry Loading')
    playUIClick()
    retryInitialization()
  }, [retryInitialization])

  const skipLoading = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Skip Loading')
    playUIClick()
    skipInitialization()
  }, [skipInitialization])

  const toggleFullscreen = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Toggle Fullscreen')
    playUIClick()
    openSplashModal('functionalsplash')
  }, [openSplashModal])

  const closeFullscreen = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Close Fullscreen')
    playUIClick()
    closeSplashModal()
  }, [closeSplashModal])

  // Navigation to other splash screens
  const goToMinimal = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Navigate to Minimal')
    playUIClick()
    setCurrentChildPage('minimalsplash')
  }, [setCurrentChildPage])

  const goToAnimated = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Navigate to Animated')
    playUIClick()
    setCurrentChildPage('animatedsplash')
  }, [setCurrentChildPage])

  const goToProgress = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Navigate to Progress')
    playUIClick()
    setCurrentChildPage('loadingprogress')
  }, [setCurrentChildPage])

  const goToBranded = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Navigate to Branded')
    playUIClick()
    setCurrentChildPage('brandedsplash')
  }, [setCurrentChildPage])

  const showCacheStats = useCallback(() => {
    console.log('🎯 [FUNCTIONAL SPLASH] Show Cache Stats')
    playUIClick()
    
    const stats = assetCacheService.getCacheStats()
    console.log('📊 Asset Cache Statistics:', {
      ...stats,
      utilizationPercent: `${stats.utilization.toFixed(1)}%`
    })
    
    alert(`Asset Cache Stats:\n• ${stats.entryCount} files cached\n• ${stats.sizeFormatted} / ${stats.maxSizeFormatted}\n• ${stats.utilization.toFixed(1)}% utilization`)
  }, [playUIClick])

  const clearCache = useCallback(async () => {
    console.log('🎯 [FUNCTIONAL SPLASH] Clear Cache')
    playUIClick()
    
    try {
      await assetCacheService.clearCache()
      alert('✅ Asset cache cleared! Next load will re-download all assets.')
    } catch (error) {
      console.error('Failed to clear cache:', error)
      alert('❌ Failed to clear cache. Check console for details.')
    }
  }, [playUIClick])

  return {
    testFunctionalLoading,
    retryLoading,
    skipLoading,
    toggleFullscreen,
    closeFullscreen,
    goToMinimal,
    goToAnimated,
    goToProgress,
    goToBranded,
    showCacheStats,
    clearCache,
    
    // Expose loading state for debugging
    loadingState: {
      progress,
      status,
      stage,
      isInitializing
    }
  }
}