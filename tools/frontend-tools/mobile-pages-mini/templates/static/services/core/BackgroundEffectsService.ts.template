import type {
  BackgroundEffectVariant,
  BackgroundEffectConfig,
  IBackgroundEffectsService,
} from '../../types/core/backgroundEffects'

/**
 * Background Effects Service
 * Manages registration and retrieval of background effect components
 * Follows singleton pattern for centralized effect management
 */
export class BackgroundEffectsService implements IBackgroundEffectsService {
  private static instance: BackgroundEffectsService | null = null
  private registry: Map<BackgroundEffectVariant, BackgroundEffectConfig> = new Map()
  private initialized = false

  private constructor() {
    // Private constructor for singleton pattern
  }

  /**
   * Get singleton instance of the service
   */
  public static getInstance(): BackgroundEffectsService {
    if (!BackgroundEffectsService.instance) {
      BackgroundEffectsService.instance = new BackgroundEffectsService()
    }
    return BackgroundEffectsService.instance
  }

  /**
   * Register a new background effect
   * @param config Effect configuration
   */
  public registerEffect(config: BackgroundEffectConfig): void {
    if (this.registry.has(config.id)) {
      console.warn(`Background effect '${config.id}' is already registered. Overwriting.`)
    }
    
    this.registry.set(config.id, config)
  }

  /**
   * Get a specific background effect configuration
   * @param variant Effect variant to retrieve
   * @returns Effect configuration or null if not found
   */
  public getEffect(variant: BackgroundEffectVariant): BackgroundEffectConfig | null {
    return this.registry.get(variant) || null
  }

  /**
   * Get all registered background effects
   * @returns Array of all effect configurations
   */
  public getAllEffects(): BackgroundEffectConfig[] {
    return Array.from(this.registry.values())
  }

  /**
   * Get all available background effect variants
   * @returns Array of variant IDs
   */
  public getAvailableVariants(): BackgroundEffectVariant[] {
    return Array.from(this.registry.keys())
  }

  /**
   * Check if a variant is registered
   * @param variant Variant to check
   * @returns True if variant is registered
   */
  public isVariantRegistered(variant: BackgroundEffectVariant): boolean {
    return this.registry.has(variant)
  }

  /**
   * Get effects filtered by criteria
   * @param predicate Filter function
   * @returns Filtered array of effect configurations
   */
  public getEffectsWhere(
    predicate: (config: BackgroundEffectConfig) => boolean
  ): BackgroundEffectConfig[] {
    return this.getAllEffects().filter(predicate)
  }

  /**
   * Unregister a background effect
   * @param variant Effect variant to remove
   * @returns True if effect was removed, false if not found
   */
  public unregisterEffect(variant: BackgroundEffectVariant): boolean {
    const wasRemoved = this.registry.delete(variant)
    if (wasRemoved) {
    }
    return wasRemoved
  }

  /**
   * Clear all registered effects
   */
  public clearRegistry(): void {
    this.registry.clear()
  }

  /**
   * Get registry size
   * @returns Number of registered effects
   */
  public getRegistrySize(): number {
    return this.registry.size
  }

  /**
   * Initialize service (for future use)
   */
  public initialize(): void {
    if (this.initialized) {
      return
    }

    this.initialized = true
  }

  /**
   * Check if service is initialized
   */
  public isInitialized(): boolean {
    return this.initialized
  }
}

// Export singleton instance for convenience
export const backgroundEffectsService = BackgroundEffectsService.getInstance()