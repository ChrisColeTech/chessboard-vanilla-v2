// ui-audio.types.ts - UI interaction types and sound mapping interfaces

/**
 * Types of UI interactions that can trigger audio feedback
 */
export type UIInteractionType = 'click' | 'hover' | 'focus' | 'select';

/**
 * Types of UI sounds available for interactions
 */
export type UISoundType = 'uiClick' | 'uiHover' | 'uiSelect' | 'uiError';

/**
 * Configuration for mapping UI interactions to sounds
 */
export interface UIInteractionConfig {
  readonly interactionType: UIInteractionType;
  readonly soundType: UISoundType;
  readonly enabled: boolean;
}

/**
 * Selector configuration for detecting UI elements
 */
export interface UIElementSelector {
  readonly selector: string;
  readonly interactionType: UIInteractionType;
  readonly priority: number;
}

/**
 * Configuration for excluding elements from audio feedback
 */
export interface UIExclusionConfig {
  readonly selector: string;
  readonly reason?: string;
}