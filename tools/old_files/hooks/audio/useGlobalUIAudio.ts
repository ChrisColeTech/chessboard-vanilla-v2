// useGlobalUIAudio.ts - React hook for global UI audio service integration

import { useEffect, useCallback, useRef } from 'react';
import { getGlobalUIAudioService } from '../../services/audio/globalUIAudio-singleton';
import type { 
  GlobalUIAudioConfigUpdate, 
  GlobalUIAudioService 
} from '../../types/audio/global-audio.types';
import type { UIElementSelector } from '../../types/audio/ui-audio.types';

/**
 * Configuration options for the useGlobalUIAudio hook
 */
interface UseGlobalUIAudioOptions {
  /**
   * Whether to automatically initialize the service on mount
   * @default true
   */
  autoInitialize?: boolean;
  
  /**
   * Initial configuration for the service
   */
  initialConfig?: GlobalUIAudioConfigUpdate;
  
  /**
   * Whether to automatically destroy the service on unmount
   * Note: In development, the singleton survives component unmounts for HMR
   * @default false
   */
  destroyOnUnmount?: boolean;
}

/**
 * Return type for the useGlobalUIAudio hook
 */
interface UseGlobalUIAudioReturn {
  /**
   * Initialize the global UI audio service manually
   */
  initialize: () => void;
  
  /**
   * Destroy the global UI audio service manually
   */
  destroy: () => void;
  
  /**
   * Configure the service with new settings
   */
  configure: (config: GlobalUIAudioConfigUpdate) => void;
  
  /**
   * Add a custom element selector for audio detection
   */
  addCustomSelector: (selector: UIElementSelector) => void;
  
  /**
   * Remove a custom element selector
   */
  removeCustomSelector: (selectorString: string) => void;
  
  /**
   * Check if the service is currently initialized
   */
  isInitialized: () => boolean;
  
  /**
   * Get the current service configuration
   */
  getConfig: () => ReturnType<GlobalUIAudioService['getConfig']>;
}

/**
 * React hook for integrating the Global UI Audio Service
 * 
 * This hook provides a clean interface for React components to initialize
 * and configure the global UI audio system. It handles the service lifecycle
 * automatically and provides methods for configuration and control.
 * 
 * @param options Configuration options for the hook
 * @returns Object with methods to control the global UI audio service
 * 
 * @example
 * ```tsx
 * function App() {
 *   const { initialize, configure } = useGlobalUIAudio({
 *     autoInitialize: true,
 *     initialConfig: {
 *       enabled: true,
 *       excludeSelectors: ['.no-sound', '[data-no-audio]']
 *     }
 *   });
 * 
 *   // Service is automatically initialized
 *   // Additional configuration can be done via the returned methods
 * }
 * ```
 */
export function useGlobalUIAudio(options: UseGlobalUIAudioOptions = {}): UseGlobalUIAudioReturn {
  const {
    autoInitialize = true,
    initialConfig,
    destroyOnUnmount = false
  } = options;
  
  // Use ref to maintain stable reference to the service
  const serviceRef = useRef<GlobalUIAudioService | null>(null);
  
  // Get or create the service instance
  const getService = useCallback((): GlobalUIAudioService => {
    if (!serviceRef.current) {
      serviceRef.current = getGlobalUIAudioService(initialConfig);
    }
    return serviceRef.current;
  }, [initialConfig]);
  
  // Initialize the service
  const initialize = useCallback((): void => {
    const service = getService();
    service.initialize();
  }, [getService]);
  
  // Destroy the service
  const destroy = useCallback((): void => {
    const service = getService();
    service.destroy();
  }, [getService]);
  
  // Configure the service
  const configure = useCallback((config: GlobalUIAudioConfigUpdate): void => {
    const service = getService();
    service.configure(config);
  }, [getService]);
  
  // Add custom selector
  const addCustomSelector = useCallback((selector: UIElementSelector): void => {
    const service = getService();
    service.addCustomSelector(selector);
  }, [getService]);
  
  // Remove custom selector
  const removeCustomSelector = useCallback((selectorString: string): void => {
    const service = getService();
    service.removeCustomSelector(selectorString);
  }, [getService]);
  
  // Check if service is initialized
  const isInitialized = useCallback((): boolean => {
    const service = getService();
    return service.isInitialized();
  }, [getService]);
  
  // Get current configuration
  const getConfig = useCallback(() => {
    const service = getService();
    return service.getConfig();
  }, [getService]);
  
  // Effect for auto-initialization and cleanup
  useEffect(() => {
    if (autoInitialize) {
      initialize();
    }
    
    // Cleanup function
    return () => {
      if (destroyOnUnmount) {
        destroy();
      }
    };
  }, [autoInitialize, destroyOnUnmount, initialize, destroy]);
  
  // Return the hook interface
  return {
    initialize,
    destroy,
    configure,
    addCustomSelector,
    removeCustomSelector,
    isInitialized,
    getConfig
  };
}

/**
 * Simplified hook for basic usage with minimal configuration
 * 
 * @example
 * ```tsx
 * function App() {
 *   useGlobalUIAudioBasic(); // Just enable with defaults
 * }
 * ```
 */
export function useGlobalUIAudioBasic(): void {
  useGlobalUIAudio({
    autoInitialize: true,
    initialConfig: {
      enabled: true,
      autoDetection: true
    }
  });
}