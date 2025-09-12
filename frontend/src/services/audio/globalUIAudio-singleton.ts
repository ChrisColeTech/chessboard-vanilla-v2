// globalUIAudio-singleton.ts - Stub singleton for global UI audio service

import { GlobalUIAudioService } from './globalUIAudioService';
import type { GlobalUIAudioConfigUpdate } from '../../types/audio/global-audio.types';

let singletonInstance: GlobalUIAudioService | null = null;
let instanceCount = 0;

/**
 * Stub Global UI Audio service singleton
 */
export function getGlobalUIAudioService(
  initialConfig?: GlobalUIAudioConfigUpdate
): GlobalUIAudioService {
  if (!singletonInstance) {
    singletonInstance = new GlobalUIAudioService(initialConfig);
  }
  return singletonInstance;
}

/**
 * Destroy the singleton (stub)
 */
export function destroyGlobalUIAudioSingleton(): void {
  // Stub - do nothing
}

/**
 * Get singleton stats (stub)
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
 * Reset singleton (stub)
 */
export function resetGlobalUIAudioSingleton(
  newConfig?: GlobalUIAudioConfigUpdate
): GlobalUIAudioService {
  destroyGlobalUIAudioSingleton();
  return getGlobalUIAudioService(newConfig);
}