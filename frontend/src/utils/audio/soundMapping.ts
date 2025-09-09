// soundMapping.ts - Maps UI interaction types to specific sounds

import type { UIInteractionType, UISoundType, UIInteractionConfig } from '../../types/audio/ui-audio.types';
import type { SoundEffect } from '../../services/audio/audioService';

/**
 * Default mapping from UI interactions to sound types
 * For now, we only have 'uiClick' available, but this is extensible
 */
export const UI_SOUND_MAPPING: Record<UIInteractionType, UISoundType> = {
  click: 'uiClick',
  hover: 'uiClick', // Future: could be 'uiHover' when implemented
  focus: 'uiClick', // Future: could be 'uiSelect' when implemented  
  select: 'uiClick' // Future: could be 'uiSelect' when implemented
};

/**
 * Map UI sound types to actual audio service sound effects
 * This bridges the gap between UI-specific sound types and the audio service
 */
export const SOUND_TYPE_TO_AUDIO_SERVICE: Record<UISoundType, SoundEffect> = {
  uiClick: 'capture', // Use capture sound for clicks (pronounced feedback)
  uiHover: 'move', // Use move sound for hover (subtle feedback)
  uiSelect: 'capture', // Use capture sound for selection
  uiError: 'error' // Map to existing error sound
};

/**
 * Default interaction configurations
 */
export const DEFAULT_INTERACTION_CONFIGS: UIInteractionConfig[] = [
  {
    interactionType: 'click',
    soundType: 'uiClick', 
    enabled: true
  },
  {
    interactionType: 'hover',
    soundType: 'uiClick', // Future: uiHover
    enabled: false // Disabled by default to avoid audio spam
  },
  {
    interactionType: 'focus',
    soundType: 'uiClick', // Future: uiSelect
    enabled: false // Disabled by default
  },
  {
    interactionType: 'select',
    soundType: 'uiClick', // Future: uiSelect
    enabled: true
  }
];

/**
 * Get the sound effect that should play for a UI interaction
 */
export function getSoundForInteraction(interactionType: UIInteractionType): SoundEffect {
  const uiSoundType = UI_SOUND_MAPPING[interactionType];
  return SOUND_TYPE_TO_AUDIO_SERVICE[uiSoundType];
}

/**
 * Check if a specific interaction type should play audio
 */
export function isInteractionAudioEnabled(
  interactionType: UIInteractionType,
  configs: UIInteractionConfig[] = DEFAULT_INTERACTION_CONFIGS
): boolean {
  const config = configs.find(c => c.interactionType === interactionType);
  return config?.enabled ?? false;
}

/**
 * Get interaction configuration by type
 */
export function getInteractionConfig(
  interactionType: UIInteractionType,
  configs: UIInteractionConfig[] = DEFAULT_INTERACTION_CONFIGS
): UIInteractionConfig | undefined {
  return configs.find(c => c.interactionType === interactionType);
}

/**
 * Create a custom interaction configuration
 */
export function createInteractionConfig(
  interactionType: UIInteractionType,
  soundType: UISoundType,
  enabled: boolean = true
): UIInteractionConfig {
  return {
    interactionType,
    soundType,
    enabled
  };
}