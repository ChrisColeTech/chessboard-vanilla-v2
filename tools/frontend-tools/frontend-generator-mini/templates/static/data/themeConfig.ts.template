/**
 * Theme configuration constants and data
 * Extracted from SettingsPanel for Single Responsibility Principle
 */

import { Sun, Moon, Palette, Lightbulb } from "lucide-react";

/**
 * Chess-themed descriptions for background effects
 */
export const CHESS_EFFECT_DESCRIPTIONS = {
  gaming: "Classic battle atmosphere with floating orbs and chess pieces.",
  minimal: "Clean geometric shapes for focused strategy.",
  particles: "Dynamic particles representing endless possibilities.", 
  abstract: "Mathematical symbols of chess mastery.",
  casino: "High-energy sparkles for tournament intensity."
} as const;

/**
 * Theme pagination configuration
 */
export const THEME_PAGINATION_CONFIG = {
  THEMES_PER_LOAD: 4,
  INITIAL_VISIBLE_COUNT: 4
} as const;

/**
 * Settings section configuration
 */
export const SETTINGS_SECTIONS = {
  BACKGROUND_EFFECTS: {
    title: "Background Effects",
    icon: undefined, // Icon handled by BackgroundEffectsSelector component
    fallbackDescription: "Activate background effects to enhance your chess experience with immersive visual atmospheres."
  },
  BRIGHTNESS: {
    title: "Brightness",
    icon: Lightbulb,
    modes: {
      light: { icon: Sun, label: "Light" },
      dark: { icon: Moon, label: "Dark" }
    }
  },
  THEME: {
    title: "Theme",
    icon: Palette
  }
} as const;

/**
 * Get chess-themed description for a background effect variant
 */
export function getChessDescription(variant: string): string {
  return CHESS_EFFECT_DESCRIPTIONS[variant as keyof typeof CHESS_EFFECT_DESCRIPTIONS] || 
         SETTINGS_SECTIONS.BACKGROUND_EFFECTS.fallbackDescription;
}