import { create } from 'zustand'
import { persist, subscribeWithSelector } from 'zustand/middleware'
import type { TabId } from '../components/layout/types'
import type { ThemeId, BaseTheme } from '../components/core/ThemeSwitcher'
import type { BackgroundEffectVariant } from '../types/core/backgroundEffects'
import type { PIECE_SETS } from '../constants/pieces.constants'
import type { BoardColorMode, PremiumBoardStyle } from '../data/boardColorConfig'

// Poker Game Types
export type Card = {
  suit: 'hearts' | 'diamonds' | 'clubs' | 'spades'
  rank: 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K'
}

export type GamePhase = 'waiting' | 'preflop' | 'flop' | 'turn' | 'river' | 'showdown'

export type BetAction = 
  | { type: 'fold' }
  | { type: 'check' }
  | { type: 'call'; amount: number }
  | { type: 'raise'; amount: number }
  | { type: 'all-in'; amount: number }

export type AIPlayer = {
  id: string
  name: string
  chips: number
  hand: [Card, Card] | null
  position: number
  isActive: boolean
  lastAction: BetAction | null
}

interface AppState {
  // Navigation
  selectedTab: TabId
  
  // Child page navigation
  currentChildPage: string | null  // For pages like 'dragtest', 'uiaudiotest'
  
  // Theme
  currentTheme: ThemeId
  isDarkMode: boolean
  selectedBaseTheme: BaseTheme
  
  // Settings
  isSettingsPanelOpen: boolean
  
  // Audio settings
  audioEnabled: boolean
  audioVolume: number
  moveSound: boolean
  captureSound: boolean
  checkSound: boolean
  uiSounds: boolean
  
  // Visual settings
  backgroundEffectVariant: BackgroundEffectVariant
  
  // Board color settings
  boardColorMode: BoardColorMode
  premiumBoardStyle: PremiumBoardStyle
  
  // Chess settings
  selectedPieceSet: keyof typeof PIECE_SETS
  pieceSize: 'small' | 'medium' | 'large'
  
  // UI State
  lastVisited: Date
  
  // Splash Modal State
  splashModalOpen: boolean
  splashModalPage: string | null  // Which splash page to show in modal
  
  // Coins Modal State
  coinsModalOpen: boolean
  
  // Game State
  coinBalance: number
  
  // Poker Game State (Single-player vs Computer)
  pokerGame: {
    gamePhase: GamePhase
    pot: number
    playerBet: number
    dealerBet: number
    playerHand: [Card, Card] | null
    dealerHand: [Card, Card] | null
    communityCards: Card[]
    isPlayerTurn: boolean
    playerChips: number
    handNumber: number
    lastWinner: 'player' | 'dealer' | 'tie' | null
    showDealerCards: boolean
  }
}

interface AppActions {
  // Navigation actions
  setSelectedTab: (tab: TabId) => void
  setCurrentChildPage: (childPage: string | null) => void
  
  // Theme actions
  setTheme: (theme: ThemeId) => void
  setBaseTheme: (baseTheme: BaseTheme) => void
  toggleMode: () => void
  
  // Settings actions
  openSettings: () => void
  closeSettings: () => void
  toggleSettings: () => void
  
  // Audio actions
  setAudioEnabled: (enabled: boolean) => void
  setAudioVolume: (volume: number) => void
  setMoveSound: (enabled: boolean) => void
  setCaptureSound: (enabled: boolean) => void
  setCheckSound: (enabled: boolean) => void
  setUiSounds: (enabled: boolean) => void
  toggleAudio: () => void
  
  // Visual actions
  setBackgroundEffectVariant: (variant: BackgroundEffectVariant) => void
  
  // Board color actions
  setBoardColorMode: (mode: BoardColorMode) => void
  setPremiumBoardStyle: (style: PremiumBoardStyle) => void
  
  // Chess actions
  setPieceSet: (pieceSet: keyof typeof PIECE_SETS) => void
  setPieceSize: (size: 'small' | 'medium' | 'large') => void
  
  // Splash modal actions
  openSplashModal: (page: string) => void
  closeSplashModal: () => void
  
  // Coins modal actions
  openCoinsModal: () => void
  closeCoinsModal: () => void
  
  // Utility actions
  reset: () => void
  
  // Game actions
  setCoinBalance: (balance: number) => void
  
  // Poker actions
  setPokerGamePhase: (phase: GamePhase) => void
  setPlayerHand: (hand: [Card, Card] | null) => void
  setDealerHand: (hand: [Card, Card] | null) => void
  setCommunityCards: (cards: Card[]) => void
  setPlayerChips: (chips: number) => void
  setPot: (pot: number) => void
  setPlayerBet: (bet: number) => void
  setDealerBet: (bet: number) => void
  setIsPlayerTurn: (isPlayerTurn: boolean) => void
  setShowDealerCards: (show: boolean) => void
  setLastWinner: (winner: 'player' | 'dealer' | 'tie' | null) => void
  dealNewHand: () => void
  resetPokerGame: () => void
}

type AppStore = AppState & AppActions

const initialState: AppState = {
  selectedTab: 'settings' as TabId,
  currentChildPage: null,
  currentTheme: 'dark',
  isDarkMode: true,
  selectedBaseTheme: 'default',
  isSettingsPanelOpen: false,
  audioEnabled: true,
  audioVolume: 0.7,
  moveSound: true,
  captureSound: true,
  checkSound: true,
  uiSounds: true,
  backgroundEffectVariant: 'gaming',
  boardColorMode: 'default',
  premiumBoardStyle: 'marble',
  selectedPieceSet: 'classic',
  pieceSize: 'medium',
  lastVisited: new Date(),
  splashModalOpen: false,
  splashModalPage: null,
  coinsModalOpen: false,
  coinBalance: 350,
  pokerGame: {
    gamePhase: 'waiting',
    pot: 0,
    playerBet: 0,
    dealerBet: 0,
    playerHand: null,
    dealerHand: null,
    communityCards: [],
    isPlayerTurn: false,
    playerChips: 1000,
    handNumber: 0,
    lastWinner: null,
    showDealerCards: false,
  },
}

export const useAppStore = create<AppStore>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
      ...initialState,
      
      // Navigation actions
      setSelectedTab: (tab) => set({ selectedTab: tab }),
      setCurrentChildPage: (childPage) => set({ currentChildPage: childPage }),
      
      // Theme actions
      setTheme: (theme) => {
        // Determine base theme and mode from theme ID
        let baseTheme: BaseTheme = 'default'
        let isDark = true
        
        if (theme === 'light' || theme === 'dark') {
          baseTheme = 'default'
          isDark = theme === 'dark'
        } else {
          baseTheme = theme.replace('-light', '') as BaseTheme
          isDark = !theme.endsWith('-light')
        }
        
        set({ 
          currentTheme: theme, 
          selectedBaseTheme: baseTheme,
          isDarkMode: isDark 
        })
        
        // Apply theme to document
        applyThemeToDocument(theme, isDark)
      },
      
      setBaseTheme: (baseTheme) => {
        const { isDarkMode } = get()
        let actualTheme: ThemeId
        
        if (baseTheme === 'default') {
          actualTheme = isDarkMode ? 'dark' : 'light'
        } else {
          // For professional themes, the theme ID stays the same, only isDarkMode matters
          actualTheme = `theme-${baseTheme}` as ThemeId
        }
        
        set({ 
          selectedBaseTheme: baseTheme,
          currentTheme: actualTheme 
        })
        
        applyThemeToDocument(actualTheme, isDarkMode)
      },
      
      toggleMode: () => {
        const { selectedBaseTheme, isDarkMode } = get()
        const newIsDarkMode = !isDarkMode
        let actualTheme: ThemeId
        
        if (selectedBaseTheme === 'default') {
          actualTheme = newIsDarkMode ? 'dark' : 'light'
        } else {
          // For professional themes, the theme ID stays the same, only isDarkMode changes
          actualTheme = `theme-${selectedBaseTheme}` as ThemeId
        }
        
        set({ 
          isDarkMode: newIsDarkMode,
          currentTheme: actualTheme 
        })
        
        applyThemeToDocument(actualTheme, newIsDarkMode)
      },
      
      // Settings actions
      openSettings: () => set({ isSettingsPanelOpen: true }),
      closeSettings: () => set({ isSettingsPanelOpen: false }),
      toggleSettings: () => set((state) => ({ isSettingsPanelOpen: !state.isSettingsPanelOpen })),
      
      // Audio actions
      setAudioEnabled: (enabled) => set({ audioEnabled: enabled }),
      setAudioVolume: (volume) => set({ audioVolume: Math.max(0, Math.min(1, volume)) }),
      setMoveSound: (enabled) => set({ moveSound: enabled }),
      setCaptureSound: (enabled) => set({ captureSound: enabled }),
      setCheckSound: (enabled) => set({ checkSound: enabled }),
      setUiSounds: (enabled) => set({ uiSounds: enabled }),
      toggleAudio: () => set((state) => ({ audioEnabled: !state.audioEnabled })),
      
      // Visual actions
      setBackgroundEffectVariant: (variant) => set({ backgroundEffectVariant: variant }),
      
      // Board color actions
      setBoardColorMode: (mode) => set({ boardColorMode: mode }),
      setPremiumBoardStyle: (style) => set({ premiumBoardStyle: style }),
      
      // Chess actions
      setPieceSet: (pieceSet) => set({ selectedPieceSet: pieceSet }),
      setPieceSize: (size) => set({ pieceSize: size }),
      
      // Splash modal actions
      openSplashModal: (page) => set({ splashModalOpen: true, splashModalPage: page }),
      closeSplashModal: () => set({ splashModalOpen: false, splashModalPage: null }),
      
      // Coins modal actions
      openCoinsModal: () => set({ coinsModalOpen: true }),
      closeCoinsModal: () => set({ coinsModalOpen: false }),
      
      // Utility actions
      reset: () => set(initialState),
      
      // Game actions
      setCoinBalance: (balance) => set({ coinBalance: Math.max(0, balance) }),
      
      // Poker actions
      setPokerGamePhase: (phase) => set((state) => ({
        pokerGame: { ...state.pokerGame, gamePhase: phase }
      })),
      setPlayerHand: (hand) => set((state) => ({
        pokerGame: { ...state.pokerGame, playerHand: hand }
      })),
      setDealerHand: (hand) => set((state) => ({
        pokerGame: { ...state.pokerGame, dealerHand: hand }
      })),
      setCommunityCards: (cards) => set((state) => ({
        pokerGame: { ...state.pokerGame, communityCards: cards }
      })),
      setPlayerChips: (chips) => set((state) => ({
        pokerGame: { ...state.pokerGame, playerChips: chips }
      })),
      setPot: (pot) => set((state) => ({
        pokerGame: { ...state.pokerGame, pot }
      })),
      setPlayerBet: (bet) => set((state) => ({
        pokerGame: { ...state.pokerGame, playerBet: bet }
      })),
      setDealerBet: (bet) => set((state) => ({
        pokerGame: { ...state.pokerGame, dealerBet: bet }
      })),
      setIsPlayerTurn: (isPlayerTurn) => set((state) => ({
        pokerGame: { ...state.pokerGame, isPlayerTurn }
      })),
      setShowDealerCards: (show) => set((state) => ({
        pokerGame: { ...state.pokerGame, showDealerCards: show }
      })),
      setLastWinner: (winner) => set((state) => ({
        pokerGame: { ...state.pokerGame, lastWinner: winner }
      })),
      dealNewHand: () => set((state) => ({
        pokerGame: {
          ...state.pokerGame,
          gamePhase: 'preflop',
          pot: 0,
          playerBet: 0,
          dealerBet: 0,
          playerHand: null,
          dealerHand: null,
          communityCards: [],
          isPlayerTurn: true,
          handNumber: state.pokerGame.handNumber + 1,
          showDealerCards: false,
          lastWinner: null,
        }
      })),
      resetPokerGame: () => set((state) => ({
        pokerGame: {
          ...initialState.pokerGame,
          playerChips: state.pokerGame.playerChips,
        }
      })),
    }),
    {
      name: 'chess-app-store',
      partialize: (state) => ({
        selectedTab: state.selectedTab,
        currentChildPage: state.currentChildPage,
        currentTheme: state.currentTheme,
        isDarkMode: state.isDarkMode,
        selectedBaseTheme: state.selectedBaseTheme,
        audioEnabled: state.audioEnabled,
        audioVolume: state.audioVolume,
        moveSound: state.moveSound,
        captureSound: state.captureSound,
        checkSound: state.checkSound,
        uiSounds: state.uiSounds,
        backgroundEffectVariant: state.backgroundEffectVariant,
        selectedPieceSet: state.selectedPieceSet,
        pieceSize: state.pieceSize,
        lastVisited: new Date(),
        coinBalance: state.coinBalance,
      }),
      onRehydrateStorage: () => (state) => {
        if (state?.currentTheme) {
          // Apply persisted theme to document on load
          applyThemeToDocument(state.currentTheme, state.isDarkMode)
        }
      },
    })
  )
)

// Helper function to apply theme to document
function applyThemeToDocument(theme: ThemeId, isDarkMode?: boolean) {
  const html = document.documentElement
  
  // Remove all theme classes (old and new)
  const themeClasses = [
    'dark', 
    // Old gaming themes
    'theme-cyber-neon', 'theme-cyber-neon-light', 'theme-dragon-gold', 'theme-dragon-gold-light', 
    'theme-shadow-knight', 'theme-shadow-knight-light', 'theme-forest-mystique', 'theme-forest-mystique-light', 
    'theme-royal-purple', 'theme-royal-purple-light',
    // Professional themes  
    'theme-onyx', 'theme-sage', 'theme-amber', 'theme-crimson', 'theme-gold', 'theme-copper', 
    'theme-violet', 'theme-matrix', 'theme-neon', 'theme-scarlet', 'theme-azure', 'theme-bronze', 'theme-teal',
    // Professional light themes  
    'theme-onyx-light', 'theme-sage-light', 'theme-amber-light', 'theme-crimson-light', 'theme-gold-light', 'theme-copper-light', 
    'theme-violet-light', 'theme-matrix-light', 'theme-neon-light', 'theme-scarlet-light', 'theme-azure-light', 'theme-bronze-light', 'theme-teal-light'
  ]
  
  // Also remove any double-prefixed classes from previous bugs
  const currentClasses = Array.from(html.classList)
  currentClasses.forEach(cls => {
    if (cls.startsWith('theme-theme-')) {
      themeClasses.push(cls)
    }
  })
  
  themeClasses.forEach(cls => {
    if (html.classList.contains(cls)) {
      html.classList.remove(cls)
    }
  })
  
  // Add current theme class
  let classesToAdd = []
  if (theme === 'dark') {
    classesToAdd.push('dark')
  } else if (theme !== 'light') {
    // For professional themes, apply theme class and dark class if needed
    if (theme.startsWith('theme-')) {
      classesToAdd.push(theme)
      // Add dark class if isDarkMode is true (from parameter or infer from store)
      const shouldBeDark = isDarkMode !== undefined ? isDarkMode : !theme.endsWith('-light')
      if (shouldBeDark) {
        classesToAdd.push('dark')
      }
    } else {
      // Fallback for any other themes
      classesToAdd.push(theme)
    }
  }
  
  classesToAdd.forEach(cls => html.classList.add(cls))
}

// Convenience selectors for common state
export const useSelectedTab = () => useAppStore((state) => state.selectedTab)

// Individual hooks to prevent object recreation and infinite re-renders
export const useTheme = () => {
  const currentTheme = useAppStore((state) => state.currentTheme)
  const isDarkMode = useAppStore((state) => state.isDarkMode)
  const selectedBaseTheme = useAppStore((state) => state.selectedBaseTheme)
  const setTheme = useAppStore((state) => state.setTheme)
  const setBaseTheme = useAppStore((state) => state.setBaseTheme)
  const toggleMode = useAppStore((state) => state.toggleMode)
  
  return {
    currentTheme,
    isDarkMode,
    selectedBaseTheme,
    setTheme,
    setBaseTheme,
    toggleMode,
  }
}

export const useSettings = () => {
  const isOpen = useAppStore((state) => state.isSettingsPanelOpen)
  const open = useAppStore((state) => state.openSettings)
  const close = useAppStore((state) => state.closeSettings)
  const toggle = useAppStore((state) => state.toggleSettings)
  
  return {
    isOpen,
    open,
    close,
    toggle,
  }
}

export const useAudio = () => {
  const audioEnabled = useAppStore((state) => state.audioEnabled)
  const audioVolume = useAppStore((state) => state.audioVolume)
  const moveSound = useAppStore((state) => state.moveSound)
  const captureSound = useAppStore((state) => state.captureSound)
  const checkSound = useAppStore((state) => state.checkSound)
  const uiSounds = useAppStore((state) => state.uiSounds)
  
  const setAudioEnabled = useAppStore((state) => state.setAudioEnabled)
  const setAudioVolume = useAppStore((state) => state.setAudioVolume)
  const setMoveSound = useAppStore((state) => state.setMoveSound)
  const setCaptureSound = useAppStore((state) => state.setCaptureSound)
  const setCheckSound = useAppStore((state) => state.setCheckSound)
  const setUiSounds = useAppStore((state) => state.setUiSounds)
  const toggleAudio = useAppStore((state) => state.toggleAudio)
  
  return {
    audioEnabled,
    audioVolume,
    moveSound,
    captureSound,
    checkSound,
    uiSounds,
    setAudioEnabled,
    setAudioVolume,
    setMoveSound,
    setCaptureSound,
    setCheckSound,
    setUiSounds,
    toggleAudio,
  }
}

export const useVisual = () => {
  const backgroundEffectVariant = useAppStore((state) => state.backgroundEffectVariant)
  const setBackgroundEffectVariant = useAppStore((state) => state.setBackgroundEffectVariant)
  
  // Backward compatibility - convert variant to boolean
  const backgroundEffectsEnabled = backgroundEffectVariant !== 'off'
  const setBackgroundEffectsEnabled = (enabled: boolean) => {
    setBackgroundEffectVariant(enabled ? 'gaming' : 'off')
  }
  const toggleBackgroundEffects = () => {
    setBackgroundEffectVariant(backgroundEffectVariant === 'off' ? 'gaming' : 'off')
  }

  return {
    // New interface
    backgroundEffectVariant,
    setBackgroundEffectVariant,
    // Backward compatibility
    backgroundEffectsEnabled,
    setBackgroundEffectsEnabled,
    toggleBackgroundEffects,
  }
}

export const useCoinsModal = () => {
  const isOpen = useAppStore((state) => state.coinsModalOpen)
  const open = useAppStore((state) => state.openCoinsModal)
  const close = useAppStore((state) => state.closeCoinsModal)
  const coinBalance = useAppStore((state) => state.coinBalance)
  const setCoinBalance = useAppStore((state) => state.setCoinBalance)
  
  return {
    isOpen,
    open,
    close,
    coinBalance,
    setCoinBalance,
  }
}

export const useChessSettings = () => {
  const selectedPieceSet = useAppStore((state) => state.selectedPieceSet)
  const pieceSize = useAppStore((state) => state.pieceSize)
  const setPieceSet = useAppStore((state) => state.setPieceSet)
  const setPieceSize = useAppStore((state) => state.setPieceSize)
  
  return {
    selectedPieceSet,
    pieceSize,
    setPieceSet,
    setPieceSize,
  }
}