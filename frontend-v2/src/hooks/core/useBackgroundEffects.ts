import { useAppStore } from '../../stores/appStore'
import { BackgroundEffectsService } from '../../services/core/BackgroundEffectsService'
import type { BackgroundEffectVariant, BackgroundEffectConfig } from '../../types/core/backgroundEffects'

/**
 * Custom hook for managing background effects
 * Integrates the BackgroundEffectsService with the app store
 */
export const useBackgroundEffects = () => {
  // Get current state from store
  const variant = useAppStore((state) => state.backgroundEffectVariant)
  const setVariant = useAppStore((state) => state.setBackgroundEffectVariant)
  
  // Get service instance
  const service = BackgroundEffectsService.getInstance()
  
  // Get current effect configuration
  const currentEffect = service.getEffect(variant)
  
  // Get all available effects
  const availableEffects = service.getAllEffects()
  
  // Get available variants
  const availableVariants = service.getAvailableVariants()
  
  // Convenience methods
  const isEnabled = variant !== 'off'
  const isRegistered = (checkVariant: BackgroundEffectVariant) => 
    service.isVariantRegistered(checkVariant)
  
  // Effect management
  const enableEffects = () => setVariant('gaming') // Default to gaming
  const disableEffects = () => setVariant('off')
  const toggleEffects = () => setVariant(isEnabled ? 'off' : 'gaming')
  
  // Get effects by type (for UI organization)
  const getEffectsByType = (predicate: (config: BackgroundEffectConfig) => boolean) => 
    service.getEffectsWhere(predicate)
  
  return {
    // Current state
    currentVariant: variant,
    currentEffect,
    isEnabled,
    
    // Available options
    availableEffects,
    availableVariants,
    
    // Actions
    setVariant,
    enableEffects,
    disableEffects,
    toggleEffects,
    
    // Utilities
    isRegistered,
    getEffectsByType,
    
    // Service access (for advanced use)
    service,
  }
}

/**
 * Type guard to check if a variant is valid
 */
export const isValidBackgroundEffectVariant = (
  value: string
): value is BackgroundEffectVariant => {
  const validVariants: BackgroundEffectVariant[] = ['off', 'gaming', 'minimal', 'particles', 'abstract', 'casino']
  return validVariants.includes(value as BackgroundEffectVariant)
}

/**
 * Get default background effect variant
 */
export const getDefaultBackgroundEffectVariant = (): BackgroundEffectVariant => 'gaming'