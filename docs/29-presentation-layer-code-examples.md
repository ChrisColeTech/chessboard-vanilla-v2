# Document 29: Presentation Layer Code Examples

## Overview
This document contains comprehensive code examples for the React presentation layer implementation. These examples support the implementation phases outlined in Document 28.

---

## Core Architecture Components

### AppLayout.tsx - Main Layout Container
```typescript
// src/components/layout/AppLayout.tsx
import type { ReactNode } from 'react'
import { BackgroundEffects } from './BackgroundEffects'
import { Header } from './Header'
import { TabBar } from './TabBar'
import { SettingsPanel } from '../SettingsPanel'
import { useSettings } from '../../stores/appStore'
import type { TabId } from './types'

interface AppLayoutProps {
  children: ReactNode
  currentTab: TabId
  onTabChange: (tab: TabId) => void
}

export function AppLayout({ children, currentTab, onTabChange }: AppLayoutProps) {
  const { isOpen: isSettingsPanelOpen, open: openSettings, close: closeSettings } = useSettings()

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      <BackgroundEffects />
      
      {/* Header - fixed height, not fixed position */}
      <header className="flex-shrink-0 relative z-20">
        <Header 
          onOpenSettings={openSettings} 
          isSettingsOpen={isSettingsPanelOpen} 
        />
      </header>
        
        {/* Main Content Area - with overlay settings */}
        <div className="flex-1 relative z-10 overflow-hidden">
          {/* Primary Content */}
          <main className="w-full h-full overflow-auto">
            <div className="container mx-auto px-6 py-8 h-full">
              {children}
            </div>
          </main>
          
          {/* Settings Panel - overlays main content from right */}
          <>
            {/* Backdrop - covers entire main content */}
            <div 
              className={`absolute inset-0 bg-black/20 backdrop-blur-sm z-20 transition-opacity duration-300 ease-out ${
                isSettingsPanelOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
              }`}
              onClick={closeSettings}
            />
            
            {/* Settings Panel */}
            <aside className={`absolute top-0 right-0 h-full z-30 transform transition-transform duration-300 ease-out ${
              isSettingsPanelOpen ? 'translate-x-0' : 'translate-x-full'
            }`}>
              <SettingsPanel 
                isOpen={isSettingsPanelOpen}
                onClose={closeSettings}
              />
            </aside>
          </>
        </div>
        
        {/* TabBar - fixed height, not fixed position */}
        <footer className="flex-shrink-0 relative z-20">
          <TabBar currentTab={currentTab} onTabChange={onTabChange} />
        </footer>
    </div>
  )
}
```

### Header.tsx - Application Header
```typescript
// src/components/layout/Header.tsx
import { Crown } from 'lucide-react'
import { ThemeSwitcher } from '../ThemeSwitcher'

interface HeaderProps {
  onOpenSettings: () => void
  isSettingsOpen: boolean
}

export function Header({ onOpenSettings, isSettingsOpen }: HeaderProps) {
  return (
    <div className="w-full glass border-b border-border/20 h-16">
      <div className="container mx-auto px-6 h-full">
        <div className="flex items-center justify-between h-full">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg border border-primary/20">
              <Crown className="w-5 h-5 text-primary" />
            </div>
            <h1 className="text-xl font-semibold text-foreground">
              Responsive Chessboard
            </h1>
            <span className="bg-muted text-muted-foreground px-2 py-1 rounded-lg text-xs font-medium border border-border">
              POC
            </span>
          </div>
          <ThemeSwitcher onOpenSettings={onOpenSettings} isSettingsOpen={isSettingsOpen} />
        </div>
      </div>
    </div>
  )
}
```

### TabBar.tsx - iPad-Style Navigation
```typescript
// src/components/layout/TabBar.tsx
import { Layout, Settings, Target } from 'lucide-react'
import type { TabId } from './types'

interface TabBarProps {
  currentTab: TabId
  onTabChange: (tab: TabId) => void
}

interface Tab {
  id: TabId
  label: string
  icon: React.ComponentType<{ className?: string }>
  description: string
}

const tabs: Tab[] = [
  {
    id: 'layout',
    label: 'Layout',
    icon: Layout,
    description: 'Background Test'
  },
  {
    id: 'worker',
    label: 'Stockfish',
    icon: Settings,
    description: 'Engine Testing'
  },
  {
    id: 'drag',
    label: 'Drag Test',
    icon: Target,
    description: 'Drag & Drop'
  }
]

export function TabBar({ currentTab, onTabChange }: TabBarProps) {
  return (
    <div className="w-full h-[84px] glass border-t border-border/20 shadow-gaming">
      <div className="flex h-full">
        {tabs.map((tab) => {
          const isActive = currentTab === tab.id
          const IconComponent = tab.icon
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`
                flex-1 flex flex-col items-center justify-center gap-1 py-2 border-none
                bg-transparent cursor-pointer transition-all duration-300 text-xs font-medium
                ${isActive 
                  ? 'bg-foreground/10 text-foreground -translate-y-1 shadow-lg border-t-2 border-foreground/50' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-foreground/5 hover:-translate-y-0.5'
                }
              `}
            >
              <IconComponent className={`w-6 h-6 mb-1 transition-all duration-300 ${isActive ? 'scale-110' : ''}`} />
              <span className="leading-tight font-medium">
                {tab.label}
              </span>
              {isActive && (
                <span className="text-[10px] opacity-70 font-normal -mt-0.5">
                  {tab.description}
                </span>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
```

### BackgroundEffects.tsx - Gaming Background
```typescript
// src/components/layout/BackgroundEffects.tsx
import { useEffect, useState } from 'react'

export function BackgroundEffects({ className = '' }: { className?: string }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      {/* Full-screen theme gradient background */}
      <div className="absolute inset-0 bg-theme-gradient" />
      
      {/* Floating Orbs - Gaming Style */}
      <div className="absolute top-20 left-20 w-32 h-32 bg-gradient-to-br from-blue-400/20 to-blue-600/30 rounded-full blur-sm animate-pulse-glow animate-drift animation-delay-500" />
      <div className="absolute top-40 right-32 w-24 h-24 bg-gradient-to-br from-green-400/20 to-green-600/30 rounded-full blur-sm animate-pulse-glow animate-hover animation-delay-1000" />
      
      {/* Floating Chess Pieces */}
      <div className="absolute top-1/4 left-1/4 text-8xl text-gray-700/15 dark:text-white/25 animate-float animation-delay-100">♛</div>
      <div className="absolute top-1/3 right-1/3 text-7xl text-gray-700/20 dark:text-white/30 animate-float animation-delay-500">♔</div>
      
      {/* Sparkle Effects */}
      <div className="absolute top-1/4 right-1/4 w-2 h-2 bg-gray-700 dark:bg-white rounded-full animate-twinkle animation-delay-100" />
      <div className="absolute top-1/3 left-1/3 w-1.5 h-1.5 bg-gray-700 dark:bg-white rounded-full animate-twinkle animation-delay-500" />
    </div>
  )
}
```

---

## State Management System

### Zustand Store Implementation
```typescript
// src/stores/appStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { TabId } from '../components/layout/types'
import type { ThemeId, BaseTheme } from '../components/ThemeSwitcher'

interface AppState {
  // Navigation
  selectedTab: TabId
  
  // Theme
  currentTheme: ThemeId
  isDarkMode: boolean
  selectedBaseTheme: BaseTheme
  
  // Settings
  isSettingsPanelOpen: boolean
  
  // UI State
  lastVisited: Date
}

interface AppActions {
  // Navigation actions
  setSelectedTab: (tab: TabId) => void
  
  // Theme actions
  setTheme: (theme: ThemeId) => void
  setBaseTheme: (baseTheme: BaseTheme) => void
  toggleMode: () => void
  
  // Settings actions
  openSettings: () => void
  closeSettings: () => void
  toggleSettings: () => void
  
  // Utility actions
  reset: () => void
}

type AppStore = AppState & AppActions

const initialState: AppState = {
  selectedTab: 'layout',
  currentTheme: 'dark',
  isDarkMode: true,
  selectedBaseTheme: 'default',
  isSettingsPanelOpen: false,
  lastVisited: new Date(),
}

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      ...initialState,
      
      // Navigation actions
      setSelectedTab: (tab) => set({ selectedTab: tab }),
      
      // Theme actions with document integration
      setTheme: (theme) => {
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
        
        applyThemeToDocument(theme)
      },
      
      setBaseTheme: (baseTheme) => {
        const { isDarkMode } = get()
        let actualTheme: ThemeId
        
        if (baseTheme === 'default') {
          actualTheme = isDarkMode ? 'dark' : 'light'
        } else {
          actualTheme = isDarkMode ? baseTheme : `${baseTheme}-light` as ThemeId
        }
        
        set({ 
          selectedBaseTheme: baseTheme,
          currentTheme: actualTheme 
        })
        
        applyThemeToDocument(actualTheme)
      },
      
      toggleMode: () => {
        const { selectedBaseTheme, isDarkMode } = get()
        const newIsDarkMode = !isDarkMode
        let actualTheme: ThemeId
        
        if (selectedBaseTheme === 'default') {
          actualTheme = newIsDarkMode ? 'dark' : 'light'
        } else {
          actualTheme = newIsDarkMode ? selectedBaseTheme : `${selectedBaseTheme}-light` as ThemeId
        }
        
        set({ 
          isDarkMode: newIsDarkMode,
          currentTheme: actualTheme 
        })
        
        applyThemeToDocument(actualTheme)
      },
      
      // Settings actions
      openSettings: () => set({ isSettingsPanelOpen: true }),
      closeSettings: () => set({ isSettingsPanelOpen: false }),
      toggleSettings: () => set((state) => ({ isSettingsPanelOpen: !state.isSettingsPanelOpen })),
      
      // Utility actions
      reset: () => set(initialState),
    }),
    {
      name: 'chess-app-store',
      partialize: (state) => ({
        selectedTab: state.selectedTab,
        currentTheme: state.currentTheme,
        isDarkMode: state.isDarkMode,
        selectedBaseTheme: state.selectedBaseTheme,
        lastVisited: new Date(),
      }),
      onRehydrateStorage: () => (state) => {
        if (state?.currentTheme) {
          applyThemeToDocument(state.currentTheme)
        }
      },
    }
  )
)

// Helper function to apply theme to document
function applyThemeToDocument(theme: ThemeId) {
  const html = document.documentElement
  
  // Remove all theme classes
  const themeClasses = [
    'dark', 
    'theme-cyber-neon', 
    'theme-cyber-neon-light', 
    'theme-dragon-gold', 
    'theme-dragon-gold-light', 
    'theme-shadow-knight', 
    'theme-shadow-knight-light', 
    'theme-forest-mystique', 
    'theme-forest-mystique-light', 
    'theme-royal-purple', 
    'theme-royal-purple-light'
  ]
  themeClasses.forEach(cls => html.classList.remove(cls))
  
  // Add current theme class
  if (theme === 'dark') {
    html.classList.add('dark')
  } else if (theme !== 'light') {
    html.classList.add(`theme-${theme}`)
  }
}

// Convenience selectors for common state
export const useSelectedTab = () => useAppStore((state) => state.selectedTab)
export const useTheme = () => useAppStore((state) => ({
  currentTheme: state.currentTheme,
  isDarkMode: state.isDarkMode,
  selectedBaseTheme: state.selectedBaseTheme,
  setTheme: state.setTheme,
  setBaseTheme: state.setBaseTheme,
  toggleMode: state.toggleMode,
}))
export const useSettings = () => useAppStore((state) => ({
  isOpen: state.isSettingsPanelOpen,
  open: state.openSettings,
  close: state.closeSettings,
  toggle: state.toggleSettings,
}))
```

---

## Theme System Components

### ThemeSwitcher.tsx - Settings Button
```typescript
// src/components/ThemeSwitcher.tsx
import { Settings } from 'lucide-react'

export type ThemeId = 'light' | 'dark' | 'cyber-neon' | 'cyber-neon-light' | 'dragon-gold' | 'dragon-gold-light' | 'shadow-knight' | 'shadow-knight-light' | 'forest-mystique' | 'forest-mystique-light' | 'royal-purple' | 'royal-purple-light'

export type BaseTheme = 'default' | 'cyber-neon' | 'dragon-gold' | 'shadow-knight' | 'forest-mystique' | 'royal-purple'

interface BaseThemeConfig {
  id: BaseTheme
  name: string
  description: string
  icon: React.ComponentType<{ className?: string }>
  darkPreview: string
  lightPreview: string
}

export const baseThemes: BaseThemeConfig[] = [
  {
    id: 'default',
    name: 'Default',
    description: 'Classic clean theme',
    icon: Settings,
    darkPreview: 'bg-gray-900 border-gray-600',
    lightPreview: 'bg-slate-50 border-slate-200'
  },
  {
    id: 'cyber-neon',
    name: 'Cyber Neon',
    description: 'Electric neon gaming',
    icon: Zap,
    darkPreview: 'bg-gray-900 border-pink-500',
    lightPreview: 'bg-purple-50 border-pink-400'
  },
  // ... additional themes
]

interface ThemeSwitcherProps {
  onOpenSettings: () => void
  isSettingsOpen?: boolean
}

export function ThemeSwitcher({ onOpenSettings, isSettingsOpen = false }: ThemeSwitcherProps) {
  return (
    <button
      onClick={onOpenSettings}
      className={`flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10 border border-primary/20 text-primary hover:bg-primary/20 transition-all ${isSettingsOpen ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
      title="Change Theme"
    >
      <Settings className="w-5 h-5" />
    </button>
  )
}
```

### SettingsPanel.tsx - Professional Settings Panel
```typescript
// src/components/SettingsPanel.tsx
import { Settings, X, Sun, Moon } from 'lucide-react'
import { baseThemes, type BaseTheme } from './ThemeSwitcher'
import { useTheme } from '../stores/appStore'

interface SettingsPanelProps {
  isOpen: boolean
  onClose: () => void
}

export function SettingsPanel({ onClose }: SettingsPanelProps) {
  const { isDarkMode, selectedBaseTheme, setBaseTheme, toggleMode } = useTheme()

  const handleBaseThemeChange = (baseThemeId: BaseTheme) => {
    setBaseTheme(baseThemeId)
  }
  
  const handleModeToggle = () => {
    toggleMode()
  }

  return (
    <div className="w-80 sm:w-96 h-full bg-background border-l border-border shadow-2xl">
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          <div className="flex items-center gap-2">
            <Settings className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-muted/50 hover:bg-muted flex items-center justify-center text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Settings Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          
          {/* Light/Dark Mode Toggle */}
          <div>
            <h3 className="text-base font-semibold text-foreground mb-3 flex items-center gap-2">
              <Settings className="w-4 h-4" />
              Brightness
            </h3>
            <div className="flex items-center justify-center p-1 bg-muted/30 rounded-lg border border-border">
              <button
                onClick={handleModeToggle}
                className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all flex-1 justify-center ${
                  !isDarkMode 
                    ? 'bg-primary text-primary-foreground shadow-md' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                }`}
              >
                <Sun className="w-4 h-4" />
                <span className="text-sm font-medium">Light</span>
              </button>
              <button
                onClick={handleModeToggle}
                className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all flex-1 justify-center ${
                  isDarkMode 
                    ? 'bg-primary text-primary-foreground shadow-md' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                }`}
              >
                <Moon className="w-4 h-4" />
                <span className="text-sm font-medium">Dark</span>
              </button>
            </div>
          </div>

          {/* Theme Section */}
          <div>
            <h3 className="text-base font-semibold text-foreground mb-3 flex items-center gap-2">
              <Settings className="w-4 h-4" />
              Theme
            </h3>
            <div className="grid grid-cols-2 gap-3">
            {baseThemes.map((baseTheme) => {
              const isActive = selectedBaseTheme === baseTheme.id
              const ThemeIcon = baseTheme.icon
              const preview = isDarkMode ? baseTheme.darkPreview : baseTheme.lightPreview
              
              return (
                <button
                  key={baseTheme.id}
                  onClick={() => handleBaseThemeChange(baseTheme.id)}
                  className={`
                    flex flex-col items-center gap-3 p-4 rounded-xl border transition-all
                    ${isActive 
                      ? 'bg-primary/20 border-primary text-primary shadow-lg ring-2 ring-primary/30' 
                      : 'bg-muted/30 border-border hover:bg-muted/50 hover:border-primary/50 text-muted-foreground hover:text-foreground'
                    }
                  `}
                >
                  <div className={`w-12 h-12 rounded-full border-2 ${preview} flex items-center justify-center`}>
                    <ThemeIcon className="w-6 h-6" />
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-medium">{baseTheme.name}</div>
                    <div className="text-xs opacity-70 leading-tight mt-1">{baseTheme.description}</div>
                  </div>
                </button>
              )
            })}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border">
          <div className="text-xs text-muted-foreground text-center">
            Settings Panel - Theme & More
          </div>
        </div>
      </div>
    </div>
  )
}
```

---

## Page Components

### App.tsx - Main Application Structure
```typescript
// src/App.tsx
import { AppLayout } from './components/layout'
import { DragTestPage, LayoutTestPage, WorkerTestPage } from './pages'
import { DragProvider, useDrag } from './providers/DragProvider'
import { DraggedPiece } from './components/DraggedPiece'
import { useSelectedTab, useAppStore } from './stores/appStore'

function AppContent() {
  const selectedTab = useSelectedTab()
  const setSelectedTab = useAppStore((state) => state.setSelectedTab)
  const { draggedPiece, cursorPosition } = useDrag()

  return (
    <AppLayout 
      currentTab={selectedTab} 
      onTabChange={setSelectedTab}
    >
      {/* Page routing */}
      {selectedTab === 'layout' && <LayoutTestPage />}
      {selectedTab === 'worker' && <WorkerTestPage />}
      {selectedTab === 'drag' && <DragTestPage />}
      
      {/* Global drag overlay */}
      {draggedPiece && (
        <DraggedPiece
          piece={draggedPiece}
          position={cursorPosition}
          size={60}
        />
      )}
    </AppLayout>
  )
}

function App() {
  return (
    <DragProvider>
      <AppContent />
    </DragProvider>
  )
}

export default App
```

### LayoutTestPage.tsx - Minimal Test Page
```typescript
// src/pages/LayoutTestPage.tsx
import React from 'react'

export const LayoutTestPage: React.FC = () => {
  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <p className="text-muted-foreground text-center">
          This is a minimal test page to view the background effects, floating chess pieces, 
          and theme styling without any other content interfering.
        </p>
      </div>
    </section>
  )
}
```

---

## Gaming UI Components & Styling

### Gaming CSS Component Library
```css
/* src/index.css - Gaming Component Classes */

/* Gaming Component Library */
@layer components {
  /* Gaming Buttons */
  .btn-gaming-primary {
    @apply px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-300 ease-out;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: var(--primary-foreground);
    box-shadow: 
      0 4px 15px -3px rgba(var(--primary) / 0.4),
      0 0 20px rgba(var(--primary) / 0.3);
    border: 1px solid rgba(var(--primary) / 0.3);
  }
  
  .btn-gaming-primary:hover {
    transform: translateY(-2px);
    box-shadow: 
      0 8px 25px -3px rgba(var(--primary) / 0.6),
      0 0 30px rgba(var(--primary) / 0.4);
  }

  /* Gaming Cards */
  .card-gaming {
    @apply bg-card/80 backdrop-blur-xl border border-border/50 rounded-2xl;
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }
  
  .card-gaming:hover {
    @apply border-primary/30;
    box-shadow: 
      0 12px 48px rgba(0, 0, 0, 0.15),
      0 4px 16px rgba(0, 0, 0, 0.1),
      0 0 0 1px rgba(var(--primary) / 0.1);
  }

  /* Glass Effects */
  .glass {
    backdrop-filter: blur(24px) saturate(180%);
    background-color: color-mix(in srgb, var(--card) 80%, transparent);
    border: 1px solid color-mix(in srgb, var(--border) 20%, transparent);
  }
}

/* Gaming Theme Classes */
.theme-cyber-neon {
  --background: #0a0a0a;
  --foreground: #ff0080;
  --card: #1a0a1a;
  --primary: #ff0080;
  --secondary: #00ff41;
  --border: #ff0080;
}

.theme-dragon-gold {
  --background: #1a0f0a;
  --foreground: #fff4e6;
  --primary: #ffd700;
  --secondary: #dc2626;
  --border: #dc2626;
}

/* Animation Keyframes */
@keyframes pulse-glow {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(2deg); }
}
```

### TestBoard.tsx - Drag Testing Component
```typescript
// src/components/TestBoard.tsx
import { useState, useEffect } from 'react'
import type { ChessPiece, ChessPosition } from '../types'
import { useDrag } from '../providers/DragProvider'

const initialTestPieces: Record<string, ChessPiece> = {
  a2: {
    id: 'test-white-queen-a2',
    type: 'queen',
    color: 'white',
    position: { file: 'a', rank: 2 }
  },
  b1: {
    id: 'test-black-pawn-b1',
    type: 'pawn',
    color: 'black',
    position: { file: 'b', rank: 1 }
  }
}

export function TestBoard() {
  const [testPieces, setTestPieces] = useState(initialTestPieces)
  const [capturedPieces, setCapturedPieces] = useState<ChessPiece[]>([])
  const { setMoveHandler } = useDrag()

  const handleTestMove = async (move: { from: string; to: string }) => {
    const newPieces = { ...testPieces }
    const piece = newPieces[move.from]
    const capturedPiece = newPieces[move.to]

    if (piece) {
      // Handle capturing
      if (capturedPiece) {
        setCapturedPieces(prev => [...prev, capturedPiece])
        console.log(`🧪 [TEST BOARD] Piece captured: ${capturedPiece.color} ${capturedPiece.type}`)
      }
      
      // Move piece
      delete newPieces[move.from]
      newPieces[move.to] = {
        ...piece,
        position: { 
          file: move.to[0] as any, 
          rank: parseInt(move.to[1]) as any 
        }
      }
    }

    setTestPieces(newPieces)
    return true
  }

  const handleReset = () => {
    setTestPieces(initialTestPieces)
    setCapturedPieces([])
    console.log('🧪 [TEST BOARD] Board reset to initial position')
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      setMoveHandler(handleTestMove)
    }, 0)
    return () => clearTimeout(timer)
  }, [setMoveHandler])

  return (
    <div className="card-gaming p-6">
      <div className="grid grid-cols-2 gap-1 bg-muted/20 p-2 rounded-lg w-fit mx-auto">
        {/* 2x2 board implementation */}
      </div>
      
      {/* Reset Button */}
      <div className="mt-4 text-center">
        <button onClick={handleReset} className="btn-gaming-primary">
          Reset Board
        </button>
      </div>

      {/* Captured Pieces Display */}
      {capturedPieces.length > 0 && (
        <div className="mt-4 p-4 bg-destructive/10 rounded-lg text-center">
          <div className="text-sm font-bold text-destructive mb-2">
            Captured Pieces
          </div>
          <div className="flex justify-center gap-2">
            {capturedPieces.map((piece, index) => (
              <img
                key={`${piece.id}-${index}`}
                src={getPieceImagePath(piece.color, piece.type, STABLE_PIECE_SET)}
                className="w-5 h-5 opacity-70"
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
```

---

## Type Definitions

### Layout Types
```typescript
// src/components/layout/types.ts
export type TabId = 'layout' | 'worker' | 'drag'
```

### Component Index Files
```typescript
// src/components/layout/index.ts
export { AppLayout } from './AppLayout'
export { Header } from './Header'
export { TabBar } from './TabBar'
export { BackgroundEffects } from './BackgroundEffects'
export { MainContent } from './MainContent'
export type { TabId } from './types'

// src/pages/index.ts
export { DragTestPage } from './DragTestPage'
export { LayoutTestPage } from './LayoutTestPage'
export { WorkerTestPage } from './WorkerTestPage'

// src/components/index.ts
export { TestBoard } from './TestBoard'
export { DraggedPiece } from './DraggedPiece'
export { ThemeSwitcher } from './ThemeSwitcher'
export { SettingsPanel } from './SettingsPanel'
```

---

## Integration Patterns

### Drop Detection Fix
```typescript
// Drop detection with dragged piece interference fix
const handleGlobalMouseUp = (upEvent: MouseEvent) => {
  cleanup()
  
  // Temporarily hide dragged piece to detect element underneath
  const draggedElement = document.querySelector('[style*="position: fixed"][style*="z-index: 1000"]') as HTMLElement
  const originalDisplay = draggedElement?.style.display
  if (draggedElement) {
    draggedElement.style.display = 'none'
  }
  
  // Use elementFromPoint to find drop target
  const targetElement = document.elementFromPoint(upEvent.clientX, upEvent.clientY)
  const targetSquare = targetElement?.getAttribute('data-square')
  
  // Restore dragged piece visibility
  if (draggedElement && originalDisplay !== undefined) {
    draggedElement.style.display = originalDisplay
  }
  
  if (targetSquare) {
    endDrag(targetSquare as ChessPosition)
  } else {
    // Check parent elements for data-square
    let element = targetElement
    while (element && element !== document.body) {
      const square = element.getAttribute('data-square')
      if (square) {
        endDrag(square as ChessPosition)
        return
      }
      element = element.parentElement
    }
    clearDrag()
  }
}
```

### Global Reset Access Pattern
```typescript
// Global window reference for external reset triggers
useEffect(() => {
  if (typeof window !== 'undefined') {
    (window as any).__testBoardReset = handleReset
  }
}, [])
```

---

## Conclusion

This document provides comprehensive code examples supporting the implementation phases in Document 28. All examples follow the established patterns of semantic HTML structure, modern React practices, advanced theme integration, and professional gaming UI aesthetics.