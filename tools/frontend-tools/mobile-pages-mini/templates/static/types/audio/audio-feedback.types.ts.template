// audio-feedback.types.ts - Generic audio feedback patterns and configuration types

/**
 * Audio feedback timing configurations
 * Controls when and how audio feedback is triggered
 */
export interface AudioFeedbackTiming {
  /** Delay before playing audio (in milliseconds) */
  readonly delay?: number;
  /** Duration of the audio feedback (in milliseconds) */
  readonly duration?: number;
  /** Whether to interrupt previous audio */
  readonly interrupt?: boolean;
  /** Fade in duration (in milliseconds) */
  readonly fadeIn?: number;
  /** Fade out duration (in milliseconds) */
  readonly fadeOut?: number;
}

/**
 * Audio feedback intensity levels
 * Different levels of audio feedback based on context
 */
export type AudioFeedbackIntensity = 'silent' | 'subtle' | 'normal' | 'prominent';

/**
 * Audio feedback patterns for different interaction types
 */
export interface AudioFeedbackPattern {
  /** Unique identifier for the pattern */
  readonly id: string;
  /** Human-readable name */
  readonly name: string;
  /** Associated sound type */
  readonly soundType: string;
  /** Volume adjustment (multiplier, 0-1) */
  readonly volumeMultiplier: number;
  /** Timing configuration */
  readonly timing: AudioFeedbackTiming;
  /** Intensity level */
  readonly intensity: AudioFeedbackIntensity;
  /** Whether this pattern is enabled */
  readonly enabled: boolean;
}

/**
 * Context for audio feedback decisions
 * Provides information to determine appropriate feedback
 */
export interface AudioFeedbackContext {
  /** Type of interaction triggering the feedback */
  readonly interactionType: string;
  /** Current user context (focus, hover, etc.) */
  readonly userContext?: 'focused' | 'idle' | 'busy';
  /** Time since last audio feedback */
  readonly timeSinceLastFeedback?: number;
  /** Current volume level */
  readonly currentVolume?: number;
  /** Whether user prefers reduced audio */
  readonly reducedAudio?: boolean;
}

/**
 * Audio feedback decision result
 * Result of evaluating whether to play feedback
 */
export interface AudioFeedbackDecision {
  /** Whether to play audio feedback */
  readonly shouldPlay: boolean;
  /** Selected pattern to use */
  readonly pattern?: AudioFeedbackPattern;
  /** Reason for the decision */
  readonly reason?: string;
  /** Adjusted volume to use */
  readonly adjustedVolume?: number;
}

/**
 * Audio feedback configuration for a component
 */
export interface ComponentAudioConfig {
  /** Enable/disable audio for this component */
  readonly enabled: boolean;
  /** Default volume level (0-1) */
  readonly defaultVolume: number;
  /** Available feedback patterns */
  readonly patterns: AudioFeedbackPattern[];
  /** Default pattern to use */
  readonly defaultPattern?: string;
  /** Context-specific overrides */
  readonly contextOverrides?: Record<string, Partial<AudioFeedbackPattern>>;
}

/**
 * Default audio feedback timing
 */
export const DEFAULT_AUDIO_TIMING: AudioFeedbackTiming = {
  delay: 0,
  duration: 200,
  interrupt: false,
  fadeIn: 10,
  fadeOut: 10
} as const;

/**
 * Predefined audio feedback patterns
 */
export const AUDIO_FEEDBACK_PATTERNS = {
  immediate: {
    delay: 0,
    interrupt: true
  },
  delayed: {
    delay: 100,
    interrupt: false
  },
  gentle: {
    fadeIn: 50,
    fadeOut: 100,
    interrupt: false
  },
  urgent: {
    delay: 0,
    interrupt: true,
    fadeIn: 0,
    fadeOut: 0
  }
} as const;