// Common action configurations that can be reused across different page groups
import { 
  Navigation, SkipForward, Clock, Target, Maximize2, RotateCcw,
  Eye, Move, VolumeX, Coins, Spade, Crown, Disc, Dices, Gamepad2, Brain
} from 'lucide-react'
import type { ActionSheetAction } from '../../types/core/action-sheet.types'

/**
 * Common action types that can be shared across different page groups
 */
export interface CommonActionConfig {
  /** Navigation actions to sibling pages */
  siblingNavigation?: string[]
  /** Common utility actions (fullscreen, restart, etc.) */
  utilities?: string[]
  /** Test-specific actions */
  tests?: string[]
}

/**
 * Predefined common actions that can be referenced by name
 */
export const COMMON_ACTIONS: Record<string, ActionSheetAction> = {
  // Navigation actions
  'go-to-minimal': {
    id: 'go-to-minimal',
    label: '→ Minimal',
    icon: Navigation,
    variant: 'secondary'
  },
  'go-to-animated': {
    id: 'go-to-animated', 
    label: '→ Animated',
    icon: SkipForward,
    variant: 'secondary'
  },
  'go-to-progress': {
    id: 'go-to-progress',
    label: '→ Progress', 
    icon: Clock,
    variant: 'secondary'
  },
  'go-to-branded': {
    id: 'go-to-branded',
    label: '→ Branded',
    icon: Target,
    variant: 'secondary'
  },
  'go-to-luxurysplash': {
    id: 'go-to-luxurysplash',
    label: 'Go to Luxurysplash',
    icon: Navigation,
    variant: 'secondary'
  },
  'go-to-drag-test': {
    id: 'go-to-drag-test',
    label: 'Go to Drag Test',
    icon: Navigation,
    variant: 'secondary'
  },
  'go-to-audio-test': {
    id: 'go-to-audio-test',
    label: 'Go to Audio Test',
    icon: VolumeX,
    variant: 'secondary'
  },
  'go-to-layout-test': {
    id: 'go-to-layout-test',
    label: 'Go to Layout Test',
    icon: Eye,
    variant: 'secondary'
  },
  'go-to-mobile-drag-test': {
    id: 'go-to-mobile-drag-test',
    label: 'Go to Mobile Drag Test',
    icon: Move,
    variant: 'secondary'
  },
  
  // Casino navigation actions
  'go-to-slots': {
    id: 'go-to-slots',
    label: '→ Slots',
    icon: Coins,
    variant: 'secondary'
  },
  'go-to-blackjack': {
    id: 'go-to-blackjack',
    label: '→ Blackjack',
    icon: Spade,
    variant: 'secondary'
  },
  'go-to-holdem': {
    id: 'go-to-holdem',
    label: '→ Hold\'em',
    icon: Crown,
    variant: 'secondary'
  },
  'go-to-roulette': {
    id: 'go-to-roulette',
    label: '→ Roulette',
    icon: Disc,
    variant: 'secondary'
  },
  'go-to-craps': {
    id: 'go-to-craps',
    label: '→ Craps',
    icon: Dices,
    variant: 'secondary'
  },
  
  // Play navigation actions
  'go-to-playchess': {
    id: 'go-to-playchess',
    label: '→ Play Chess',
    icon: Gamepad2,
    variant: 'secondary'
  },
  'go-to-playpuzzles': {
    id: 'go-to-playpuzzles',
    label: '→ Puzzles',
    icon: Brain,
    variant: 'secondary'
  },
  
  // Utility actions
  'toggle-fullscreen': {
    id: 'toggle-fullscreen',
    label: 'Toggle Fullscreen',
    icon: Maximize2,
    variant: 'default',
    shortcut: 'F11'
  },
  'restart-animation': {
    id: 'restart-animation',
    label: 'Restart Animation',
    icon: RotateCcw,
    variant: 'secondary'
  }
}

/**
 * Predefined action groups for common page types
 */
export const COMMON_ACTION_GROUPS = {
  // Splash page siblings (child pages)
  splashSiblings: [
    'go-to-minimal',
    'go-to-animated', 
    'go-to-progress',
    'go-to-branded'
  ],
  
  // UI test siblings (child pages)
  uitestSiblings: [
    'go-to-drag-test',
    'go-to-audio-test',
    'go-to-layout-test',
    'go-to-mobile-drag-test'
  ],
  
  // Casino game siblings (child pages)
  casinoSiblings: [
    'go-to-slots',
    'go-to-blackjack',
    'go-to-holdem',
    'go-to-roulette',
    'go-to-craps'
  ],
  
  // Play mode siblings (child pages)
  playSiblings: [
    'go-to-playchess',
    'go-to-playpuzzles'
  ],
  
  // Common utilities for demo/test pages
  demoUtilities: [
    'toggle-fullscreen',
    'restart-animation'
  ]
}

/**
 * Helper function to build actions from common action names
 */
export function buildCommonActions(actionNames: string[]): ActionSheetAction[] {
  return actionNames
    .map(name => COMMON_ACTIONS[name])
    .filter(Boolean) // Remove any undefined actions
}

/**
 * Helper function to merge page-specific actions with common actions
 */
export function mergeWithCommonActions(
  pageActions: ActionSheetAction[],
  commonActionNames: string[]
): ActionSheetAction[] {
  const commonActions = buildCommonActions(commonActionNames)
  return [...pageActions, ...commonActions]
}