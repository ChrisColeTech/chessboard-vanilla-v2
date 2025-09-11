// globalUIAudio-singleton.ts - HMR-safe singleton for development

import { GlobalUIAudioService } from './globalUIAudioService';
import type { GlobalUIAudioConfigUpdate } from '../../types/audio/global-audio.types';

// CRITICAL: Module-level singleton that survives HMR cycles
let singletonInstance: GlobalUIAudioService | null = null;
let instanceCount = 0;

/**
 * HMR-safe Global UI Audio service singleton
 * 
 * Key behaviors:
 * - Development: Keeps service alive across HMR cycles, reinitializes if needed
 * - Production: Normal creation/destruction with component lifecycle
 * - Event listener management persists across component re-renders
 */
export function getGlobalUIAudioService(
  initialConfig?: GlobalUIAudioConfigUpdate
): GlobalUIAudioService {
  instanceCount++;
  
  const isDevelopment = !import.meta.env.PROD;
  
  if (isDevelopment) {
    // Development mode: Use singleton pattern
    if (!singletonInstance) {
      singletonInstance = new GlobalUIAudioService(initialConfig);
      
      // Expose singleton for debugging
      if (typeof window !== 'undefined') {
        (window as any).__globalUIAudioSingleton = singletonInstance;
      }
      
      // HMR cleanup - only in development
      if (import.meta.hot) {
        import.meta.hot.dispose(() => {
          // Don't destroy the service - let it survive HMR
          // The event listeners will remain attached, which is what we want
        });
      }
    } else {
      
      // Apply configuration updates if provided
      if (initialConfig) {
        singletonInstance.configure(initialConfig);
      }
    }
    
    return singletonInstance;
  } else {
    // Production mode: Always create fresh instances
    return new GlobalUIAudioService(initialConfig);
  }
}

/**
 * Manually destroy the singleton (for testing or forced cleanup)
 * WARNING: This will break HMR behavior in development
 */
export function destroyGlobalUIAudioSingleton(): void {
  if (singletonInstance) {
    singletonInstance.destroy();
    singletonInstance = null;
    instanceCount = 0;
    
    // Clean up debug interface
    if (typeof window !== 'undefined') {
      delete (window as any).__globalUIAudioSingleton;
    }
  } else {
  }
}

/**
 * Get singleton instance stats for debugging
 */
export function getGlobalUIAudioSingletonStats(): {
  hasInstance: boolean;
  instanceCount: number;
  isInitialized: boolean;
  isDevelopment: boolean;
} {
  return {
    hasInstance: singletonInstance !== null,
    instanceCount,
    isInitialized: singletonInstance?.isInitialized() ?? false,
    isDevelopment: !import.meta.env.PROD
  };
}

/**
 * Force reset singleton (for testing)
 * This completely recreates the singleton instance
 */
export function resetGlobalUIAudioSingleton(
  newConfig?: GlobalUIAudioConfigUpdate
): GlobalUIAudioService {
  
  // Destroy existing instance if it exists
  destroyGlobalUIAudioSingleton();
  
  // Create new instance
  return getGlobalUIAudioService(newConfig);
}