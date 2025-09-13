/**
 * Board color and style configuration constants and data
 * Following the pattern established by backgroundEffectsConfig
 */

import { Palette, Wand2, Crown } from "lucide-react";

/**
 * Board color modes
 */
export type BoardColorMode = 'default' | 'theme' | 'premium';

/**
 * Premium board styles
 */
export type PremiumBoardStyle = 'marble' | 'wood' | 'metal' | 'crystal' | 'cosmic';

/**
 * Board color mode configuration
 */
export const BOARD_COLOR_MODES = {
  default: {
    id: 'default' as const,
    label: 'Default',
    icon: Palette,
    description: 'Classic black and white chessboard pattern'
  },
  theme: {
    id: 'theme' as const,
    label: 'Theme',
    icon: Wand2,
    description: 'Board colors match your selected theme'
  },
  premium: {
    id: 'premium' as const,
    label: 'Premium',
    icon: Crown,
    description: 'Exclusive premium board styles with custom textures'
  }
} as const;

/**
 * Premium board style configuration
 */
export const PREMIUM_BOARD_STYLES = {
  marble: {
    id: 'marble' as const,
    label: 'Marble',
    icon: Crown,
    description: 'Elegant marble texture with subtle veining'
  },
  wood: {
    id: 'wood' as const,
    label: 'Wood',
    icon: Crown,
    description: 'Rich wooden grain with natural warmth'
  },
  metal: {
    id: 'metal' as const,
    label: 'Metal',
    icon: Crown,
    description: 'Sleek metallic finish with modern appeal'
  },
  crystal: {
    id: 'crystal' as const,
    label: 'Crystal',
    icon: Crown,
    description: 'Translucent crystal with prismatic effects'
  },
  cosmic: {
    id: 'cosmic' as const,
    label: 'Cosmic',
    icon: Crown,
    description: 'Space-themed board with starfield patterns'
  }
} as const;

/**
 * Default values
 */
export const DEFAULT_BOARD_COLOR_MODE: BoardColorMode = 'default';
export const DEFAULT_PREMIUM_BOARD_STYLE: PremiumBoardStyle = 'marble';