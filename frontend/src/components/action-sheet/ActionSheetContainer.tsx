/**
 * Container component that wires up page-specific actions with HeadlessUI Popover
 * Works with external MenuButton trigger in TabBar for proper HeadlessUI integration
 */
import { useCallback, useState, useEffect } from 'react'
import { ActionSheet } from './ActionSheet'
import { usePlayActions } from '../../hooks/chess/usePlayActions'
import { useSlotsActions } from '../../hooks/casino/useSlotsActions'
import { useCasinoActions } from '../../hooks/casino/useCasinoActions'
import { useWorkerActions } from '../../hooks/chess/useWorkerActions'
import { useUITestsActions } from '../../hooks/uitests/useUITestsActions'
import { useLayoutActions } from '../../hooks/core/useLayoutActions'
import { useDragTestActions } from '../../hooks/uitests/useDragTestActions'
import { useUIAudioTestActions } from '../../hooks/uitests/useUIAudioTestActions'
import { useSplashActions } from '../../hooks/splash/useSplashActions'
import { useMinimalSplashActions } from '../../hooks/splash/useMinimalSplashActions'
import { useAnimatedSplashActions } from '../../hooks/splash/useAnimatedSplashActions'
import { useLoadingProgressActions } from '../../hooks/splash/useLoadingProgressActions'
import { useBrandedSplashActions } from '../../hooks/splash/useBrandedSplashActions'
import { useLuxurysplashActions } from '../../hooks/splash/useLuxurysplashActions'
import { useFunctionalSplashActions } from '../../hooks/splash/useFunctionalSplashActions'
import { useMobileDragTestActions } from '../../hooks/uitests/useMobileDragTestActions'
import { useUIClickSound } from '../../hooks/audio/useUIClickSound'
import { useUIHoverSound } from '../../hooks/audio/useUIHoverSound'
import { useAppStore } from '../../stores/appStore'
import { useAuthStore } from '../../store/auth.store'
import type { ActionSheetContainerProps, ActionSheetAction } from '../../types/core/action-sheet.types'
import { PAGE_ACTIONS } from '../../constants/actions/page-actions.constants'

export function ActionSheetContainer({ currentPage, className, onClose, isOpen, onOpenSettings }: ActionSheetContainerProps) {
  
  // Use child page if it exists, otherwise use current tab
  const currentChildPage = useAppStore((state) => state.currentChildPage)
  const actionSheetPage = currentChildPage || currentPage
  
  // Add delay when switching action menus (only for child page changes, not main tab changes)
  const [delayedActionSheetPage, setDelayedActionSheetPage] = useState(actionSheetPage)
  
  useEffect(() => {
    // Apply delay only when switching between child pages of the same parent
    // Don't delay when switching main tabs or when no child page is active
    const previousChildPage = delayedActionSheetPage === currentPage ? null : delayedActionSheetPage
    const isSwitchingChildPages = currentChildPage && 
                                  previousChildPage &&
                                  currentChildPage !== previousChildPage
    
    if (isSwitchingChildPages) {
      const timer = setTimeout(() => {
        setDelayedActionSheetPage(actionSheetPage)
      }, 1000) // 1000ms delay when switching between child pages
      
      return () => clearTimeout(timer)
    } else {
      // Immediate update for main tab changes, initial load, or going to child from main
      setDelayedActionSheetPage(actionSheetPage)
    }
  }, [actionSheetPage, currentChildPage, currentPage, delayedActionSheetPage])
  
  // Get actions for current page (with delay)
  const actions = PAGE_ACTIONS[delayedActionSheetPage] || []
  
  // Get page-specific action handlers
  const playActions = usePlayActions()
  const slotsActions = useSlotsActions()
  const casinoActions = useCasinoActions()
  const workerActions = useWorkerActions()
  const uiTestsActions = useUITestsActions()
  const layoutActions = useLayoutActions()
  const dragTestActions = useDragTestActions()
  const uiAudioTestActions = useUIAudioTestActions()
  const splashActions = useSplashActions()
  const minimalSplashActions = useMinimalSplashActions()
  const animatedSplashActions = useAnimatedSplashActions()
  const loadingProgressActions = useLoadingProgressActions()
  const brandedSplashActions = useBrandedSplashActions()
  const luxurysplashActions = useLuxurysplashActions()
  const functionalSplashActions = useFunctionalSplashActions()
  const mobileDragTestActions = useMobileDragTestActions()
  
  // Audio for action clicks and hovers
  const { playUIClick } = useUIClickSound()
  const { playUIHover } = useUIHoverSound()
  
  // Auth store for logout
  const logout = useAuthStore((state) => state.logout)

  // HeadlessUI action handler - fixed typing for string indexing
  const handleAction = useCallback((action: ActionSheetAction, closeCallback: () => void) => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    
    // Map actions to the right page hook functions with proper typing
    type Fn = () => void | Promise<void>
    const actionMap: Record<string, Record<string, Fn>> = {
      play: {
        'go-to-playchess': playActions.goToPlayChess,
        'go-to-playpuzzles': playActions.goToPlayPuzzles
      },
      playchess: {
        'new-game': playActions.newGame,
        'pause-game': playActions.pauseGame,
        'show-moves': playActions.showMoves,
        'undo-move': playActions.undoMove,
        // Navigation actions
        'go-to-playpuzzles': playActions.goToPlayPuzzles
      },
      playpuzzles: {
        'new-puzzle': playActions.newPuzzle,
        'hint': playActions.hint,
        'solve-puzzle': playActions.solvePuzzle,
        // Navigation actions
        'go-to-playchess': playActions.goToPlayChess
      },
      casino: {
        'go-to-slots': casinoActions.goToSlots,
        'go-to-blackjack': casinoActions.goToBlackjack,
        'go-to-holdem': casinoActions.goToHoldem,
        'go-to-roulette': casinoActions.goToRoulette,
        'go-to-craps': casinoActions.goToCraps
      },
      slots: {
        'test-spin': slotsActions.testSpin,
        'reset-coins': slotsActions.resetCoins,
        // Navigation actions
        'go-to-blackjack': casinoActions.goToBlackjack,
        'go-to-holdem': casinoActions.goToHoldem,
        'go-to-roulette': casinoActions.goToRoulette,
        'go-to-craps': casinoActions.goToCraps
      },
      blackjack: {
        'deal-cards': () => console.log('Deal cards - placeholder'),
        // Navigation actions
        'go-to-slots': casinoActions.goToSlots,
        'go-to-holdem': casinoActions.goToHoldem,
        'go-to-roulette': casinoActions.goToRoulette,
        'go-to-craps': casinoActions.goToCraps
      },
      holdem: {
        'new-hand': () => console.log('New hand - placeholder'),
        // Navigation actions
        'go-to-slots': casinoActions.goToSlots,
        'go-to-blackjack': casinoActions.goToBlackjack,
        'go-to-roulette': casinoActions.goToRoulette,
        'go-to-craps': casinoActions.goToCraps
      },
      roulette: {
        'spin-wheel': () => console.log('Spin wheel - placeholder'),
        // Navigation actions
        'go-to-slots': casinoActions.goToSlots,
        'go-to-blackjack': casinoActions.goToBlackjack,
        'go-to-holdem': casinoActions.goToHoldem,
        'go-to-craps': casinoActions.goToCraps
      },
      craps: {
        'roll-dice': () => console.log('Roll dice - placeholder'),
        // Navigation actions
        'go-to-slots': casinoActions.goToSlots,
        'go-to-blackjack': casinoActions.goToBlackjack,
        'go-to-holdem': casinoActions.goToHoldem,
        'go-to-roulette': casinoActions.goToRoulette
      },
      worker: {
        'test-worker-ready': workerActions.testWorkerReady,
        'test-good-move': workerActions.testGoodMove,
        'test-speed': workerActions.testSpeed,
        'run-all-tests': workerActions.runAllTests,
        'clear-test-results': workerActions.clearTestResults
      },
      uitests: {
        'go-to-drag-test': uiTestsActions.goToDragTest,
        'go-to-audio-test': uiTestsActions.goToAudioTest,
        'go-to-layout-test': uiTestsActions.goToLayoutTest,
        'go-to-mobile-drag-test': uiTestsActions.goToMobileDragTest
      },
      layout: {
        'change-background': layoutActions.changeBackground,
        'reset-layout': layoutActions.resetLayout,
        'toggle-effects': layoutActions.toggleEffects,
        'shuffle-theme': layoutActions.shuffleTheme
      },
      dragtest: {
        'reset-board': dragTestActions.resetBoard,
        'test-move-sound': dragTestActions.testMoveSound,
        'test-capture-sound': dragTestActions.testCaptureSound,
        'test-error-sound': dragTestActions.testErrorSound,
        'toggle-pieces-position': dragTestActions.togglePiecesPosition,
        'flip-board': dragTestActions.flipBoard,
        // Navigation actions
        'go-to-audio-test': uiTestsActions.goToAudioTest,
        'go-to-layout-test': uiTestsActions.goToLayoutTest,
        'go-to-mobile-drag-test': uiTestsActions.goToMobileDragTest
      },
      uiaudiotest: {
        'test-move-sound': uiAudioTestActions.testMoveSound,
        'test-capture-sound': uiAudioTestActions.testCaptureSound,
        'test-error-sound': uiAudioTestActions.testErrorSound,
        'reset-audio-settings': uiAudioTestActions.resetAudioSettings,
        // Navigation actions
        'go-to-drag-test': uiTestsActions.goToDragTest,
        'go-to-layout-test': uiTestsActions.goToLayoutTest,
        'go-to-mobile-drag-test': uiTestsActions.goToMobileDragTest
      },
      splash: {
        'go-to-minimal': splashActions.goToMinimal,
        'go-to-animated': splashActions.goToAnimated,
        'go-to-progress': splashActions.goToProgress,
        'go-to-branded': splashActions.goToBranded,
        'go-to-luxurysplash': splashActions.goToLuxurysplash,
        'go-to-functional': splashActions.goToFunctional
      },
      minimalsplash: {
        'test-minimal-load': minimalSplashActions.testMinimalLoad,
        'restart-animation': minimalSplashActions.restartAnimation,
        'toggle-fullscreen': minimalSplashActions.toggleFullscreen,
        'go-to-animated': minimalSplashActions.goToAnimated,
        'go-to-progress': minimalSplashActions.goToProgress,
        'go-to-branded': minimalSplashActions.goToBranded
      },
      animatedsplash: {
        'test-spring-animation': animatedSplashActions.testAnimatedAssembly,
        'restart-animation': animatedSplashActions.restartAnimation,
        'toggle-fullscreen': animatedSplashActions.toggleFullscreen,
        'go-to-minimal': animatedSplashActions.goToMinimal,
        'go-to-progress': animatedSplashActions.goToProgress,
        'go-to-branded': animatedSplashActions.goToBranded
      },
      loadingprogress: {
        'test-progress-bar': loadingProgressActions.testProgressBar,
        'restart-animation': loadingProgressActions.restartAnimation,
        'toggle-fullscreen': loadingProgressActions.toggleFullscreen,
        'go-to-minimal': loadingProgressActions.goToMinimal,
        'go-to-animated': loadingProgressActions.goToAnimated,
        'go-to-branded': loadingProgressActions.goToBranded
      },
      brandedsplash: {
        'test-brand-animation': brandedSplashActions.testBrandAnimation,
        'restart-animation': brandedSplashActions.restartAnimation,
        'toggle-fullscreen': brandedSplashActions.toggleFullscreen,
        'go-to-minimal': brandedSplashActions.goToMinimal,
        'go-to-animated': brandedSplashActions.goToAnimated,
        'go-to-progress': brandedSplashActions.goToProgress
      },
      luxurysplash: {
        'test-luxury': luxurysplashActions.testLuxury,
        'restart-demo': luxurysplashActions.restartDemo
      },
      functionalsplash: {
        'test-functional-loading': functionalSplashActions.testFunctionalLoading,
        'retry-loading': functionalSplashActions.retryLoading,
        'skip-loading': functionalSplashActions.skipLoading,
        'toggle-fullscreen': functionalSplashActions.toggleFullscreen,
        'show-cache-stats': functionalSplashActions.showCacheStats,
        'clear-cache': functionalSplashActions.clearCache,
        'go-to-minimal': functionalSplashActions.goToMinimal,
        'go-to-animated': functionalSplashActions.goToAnimated,
        'go-to-progress': functionalSplashActions.goToProgress,
        'go-to-branded': functionalSplashActions.goToBranded
      },
      layouttest: {
        'toggle-layout-elements': layoutActions.toggleLayoutElements,
        // Navigation actions
        'go-to-drag-test': uiTestsActions.goToDragTest,
        'go-to-audio-test': uiTestsActions.goToAudioTest,
        'go-to-mobile-drag-test': uiTestsActions.goToMobileDragTest
      },
      mobiledragtest: {
        'reset-board': mobileDragTestActions.resetBoard,
        'test-move-sound': mobileDragTestActions.testMoveSound,
        'test-capture-sound': mobileDragTestActions.testCaptureSound,
        'flip-board': mobileDragTestActions.flipBoard,
        // Navigation actions
        'go-to-drag-test': uiTestsActions.goToDragTest,
        'go-to-audio-test': uiTestsActions.goToAudioTest,
        'go-to-layout-test': uiTestsActions.goToLayoutTest
      }
    }
    
    // Handle global settings action
    if (action.id === 'open-settings') {
      onOpenSettings()
      return
    }
    
    // Handle logout action
    if (action.id === 'logout') {
      console.log('🚪 [ACTION SHEET] Logging out user...')
      logout()
      return
    }

    // Call the action function with proper typing
    const pageActions = actionMap[delayedActionSheetPage]          // Record<string, Fn> | undefined
    const actionFunction = pageActions?.[action.id]      // Fn | undefined
    
    if (actionFunction) {
      Promise.resolve(actionFunction()).catch(error => {
        console.error(`❌ [ACTION SHEET] Action ${action.id} failed:`, error)
      })
    } else {
      console.warn(`⚠️ [ACTION SHEET] No handler found for action: ${action.id} on page: ${delayedActionSheetPage}`)
    }
    
    // Use HeadlessUI's close callback AND our onClose
    closeCallback()
    onClose()
  }, [currentPage, playUIClick, playActions, slotsActions, casinoActions, workerActions, uiTestsActions, layoutActions, dragTestActions, uiAudioTestActions, splashActions, minimalSplashActions, animatedSplashActions, loadingProgressActions, brandedSplashActions, luxurysplashActions, functionalSplashActions, mobileDragTestActions, onClose, logout, onOpenSettings])

  const handleHover = useCallback((actionLabel: string) => {
    playUIHover(`Action: ${actionLabel}`)
  }, [playUIHover])

  const handleKeyDown = useCallback((event: React.KeyboardEvent) => {
    if (event.key === 'Escape') {
      onClose()
    }
  }, [onClose])

  // Found ${actions.length} actions for page: ${currentPage}

  return (
    <ActionSheet
      actions={actions}
      onActionClick={handleAction}
      onActionHover={handleHover}
      onKeyDown={handleKeyDown}
      onClose={onClose}
      isOpen={isOpen}
      className={className}
    />
  )
}