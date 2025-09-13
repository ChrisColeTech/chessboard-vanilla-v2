// demo-configurations.constants.ts - Demo configuration constants

import type { 
  AudioDemoConfiguration,
  DragTestConfiguration,
  UIInteractionConfig,
  UIElementSelector,
  UIExclusionConfig
} from '../../types';

/**
 * Default audio demo configuration
 */
export const DEFAULT_AUDIO_DEMO_CONFIG: AudioDemoConfiguration = {
  showGlobalUIExamples: true,
  showExclusionExamples: true,
  showChessAudioExamples: true,
  showImplementationTips: true
} as const;

/**
 * Minimal audio demo configuration for basic demos
 */
export const MINIMAL_AUDIO_DEMO_CONFIG: AudioDemoConfiguration = {
  showGlobalUIExamples: true,
  showExclusionExamples: false,
  showChessAudioExamples: false,
  showImplementationTips: false
} as const;

/**
 * Advanced audio demo configuration for comprehensive demos
 */
export const ADVANCED_AUDIO_DEMO_CONFIG: AudioDemoConfiguration = {
  showGlobalUIExamples: true,
  showExclusionExamples: true,
  showChessAudioExamples: true,
  showImplementationTips: true
} as const;

/**
 * Default drag test configuration
 */
export const DEFAULT_DRAG_TEST_CONFIG: DragTestConfiguration = {
  enableVisualFeedback: true,
  showValidMoves: true,
  captureEnabled: true
} as const;

/**
 * Basic drag test configuration for simple testing
 */
export const BASIC_DRAG_TEST_CONFIG: DragTestConfiguration = {
  enableVisualFeedback: true,
  showValidMoves: false,
  captureEnabled: false
} as const;

/**
 * Advanced drag test configuration for full testing
 */
export const ADVANCED_DRAG_TEST_CONFIG: DragTestConfiguration = {
  enableVisualFeedback: true,
  showValidMoves: true,
  captureEnabled: true
} as const;

/**
 * Standard UI interaction configurations for demos
 */
export const STANDARD_UI_INTERACTIONS: readonly UIInteractionConfig[] = [
  {
    interactionType: 'click',
    soundType: 'uiClick',
    enabled: true
  },
  {
    interactionType: 'hover',
    soundType: 'uiHover',
    enabled: true
  },
  {
    interactionType: 'focus',
    soundType: 'uiSelect',
    enabled: true
  },
  {
    interactionType: 'select',
    soundType: 'uiSelect',
    enabled: true
  }
] as const;

/**
 * Standard interactive element selectors for demos
 */
export const STANDARD_INTERACTIVE_SELECTORS: readonly UIElementSelector[] = [
  { selector: 'button', interactionType: 'click', priority: 1 },
  { selector: 'a[href]', interactionType: 'click', priority: 2 },
  { selector: '[role="button"]', interactionType: 'click', priority: 3 },
  { selector: 'input[type="submit"]', interactionType: 'click', priority: 4 },
  { selector: 'input[type="button"]', interactionType: 'click', priority: 5 }
] as const;

/**
 * Standard exclusion configurations for demos
 */
export const STANDARD_EXCLUSIONS: readonly UIExclusionConfig[] = [
  {
    selector: '[data-no-sound]',
    reason: 'Explicitly disabled via data attribute'
  },
  {
    selector: '.no-sound',
    reason: 'Explicitly disabled via CSS class'
  },
  {
    selector: '.chess-piece',
    reason: 'Game elements use manual audio'
  },
  {
    selector: '.chess-square',
    reason: 'Game elements use manual audio'
  },
  {
    selector: '[disabled]',
    reason: 'Disabled elements should not make sounds'
  },
  {
    selector: '.disabled',
    reason: 'Disabled elements should not make sounds'
  }
] as const;

/**
 * Demo section display priorities
 */
export const DEMO_SECTION_PRIORITIES = {
  GLOBAL_UI_EXAMPLES: 1,
  EXCLUSION_EXAMPLES: 2,
  CHESS_AUDIO_EXAMPLES: 3,
  IMPLEMENTATION_TIPS: 4
} as const;

/**
 * Configuration validation rules
 */
export const CONFIG_VALIDATION_RULES = {
  MIN_SECTIONS_ENABLED: 1,
  MAX_SECTIONS_ENABLED: 4,
  REQUIRED_SECTIONS: ['showGlobalUIExamples'] as const
} as const;