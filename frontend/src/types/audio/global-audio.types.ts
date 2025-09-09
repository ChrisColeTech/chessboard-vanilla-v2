// global-audio.types.ts - Service configuration and lifecycle types

import type { UIElementSelector, UIExclusionConfig } from './ui-audio.types';

/**
 * Configuration for the Global UI Audio Service
 */
export interface GlobalUIAudioConfig {
  readonly enabled: boolean;
  readonly autoDetection: boolean;
  readonly customSelectors: UIElementSelector[];
  readonly excludeSelectors: string[];
  readonly exclusions: UIExclusionConfig[];
}

/**
 * Partial configuration for updates
 */
export type GlobalUIAudioConfigUpdate = Partial<GlobalUIAudioConfig>;

/**
 * Global UI Audio Service interface
 */
export interface GlobalUIAudioService {
  /**
   * Initialize the service and start event listening
   */
  initialize(): void;

  /**
   * Destroy the service and clean up event listeners
   */
  destroy(): void;

  /**
   * Configure the service with new settings
   */
  configure(config: GlobalUIAudioConfigUpdate): void;

  /**
   * Add a custom element selector for audio detection
   */
  addCustomSelector(selector: UIElementSelector): void;

  /**
   * Remove a custom element selector
   */
  removeCustomSelector(selectorString: string): void;

  /**
   * Get current configuration
   */
  getConfig(): GlobalUIAudioConfig;

  /**
   * Check if service is initialized
   */
  isInitialized(): boolean;
}

/**
 * Event handler for global click detection
 */
export interface GlobalClickHandler {
  (event: Event): void;
}

/**
 * Element detection result
 */
export interface ElementDetectionResult {
  readonly shouldPlaySound: boolean;
  readonly element: Element;
  readonly matchedSelector?: string;
  readonly priority?: number;
}