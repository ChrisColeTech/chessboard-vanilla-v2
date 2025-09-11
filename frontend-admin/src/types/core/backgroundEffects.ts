import type { ComponentType } from 'react'

/**
 * Background effect variant types
 * 'off' - No background effects
 * 'gaming' - Current orbs, chess pieces, sparkles (gaming style)
 * 'minimal' - Subtle geometric shapes
 * 'particles' - Physics-based particles
 * 'abstract' - Abstract mathematical symbols
 * 'casino' - Enhanced gaming with floating orbs and sparkles
 */
export type BackgroundEffectVariant = 'off' | 'gaming' | 'minimal' | 'particles' | 'abstract' | 'casino'

/**
 * Props interface for all background effect components
 */
export interface BackgroundEffectProps {
  className?: string
  variant: BackgroundEffectVariant
}

/**
 * Configuration interface for registering background effects
 */
export interface BackgroundEffectConfig {
  id: BackgroundEffectVariant
  name: string
  description: string
  icon: ComponentType<{ className?: string }>
  preview: string // CSS classes for preview styling
  component: ComponentType<BackgroundEffectProps>
}

/**
 * Service interface for background effects management
 */
export interface IBackgroundEffectsService {
  registerEffect(config: BackgroundEffectConfig): void
  getEffect(variant: BackgroundEffectVariant): BackgroundEffectConfig | null
  getAllEffects(): BackgroundEffectConfig[]
  getAvailableVariants(): BackgroundEffectVariant[]
  isVariantRegistered(variant: BackgroundEffectVariant): boolean
}