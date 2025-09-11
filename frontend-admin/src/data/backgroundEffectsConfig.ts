/**
 * Background effects configuration constants and data
 * Extracted from SettingsPanel for Single Responsibility Principle
 */

import { Sparkles, X } from "lucide-react";

/**
 * Background effects toggle button configuration
 */
export const BACKGROUND_EFFECTS_TOGGLE_BUTTONS = {
  enabled: {
    icon: Sparkles,
    label: "Enabled"
  },
  disabled: {
    icon: X,
    label: "Disabled"
  }
} as const;

/**
 * Default background effect variant when enabling effects
 */
export const DEFAULT_BACKGROUND_VARIANT = 'gaming' as const;