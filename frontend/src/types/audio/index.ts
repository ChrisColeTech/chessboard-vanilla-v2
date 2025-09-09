// types/audio/index.ts - Audio types barrel export

// Existing types
export type {
  UIInteractionType,
  UISoundType,
  UIInteractionConfig,
  UIElementSelector,
  UIExclusionConfig
} from './ui-audio.types';

export type {
  GlobalUIAudioConfig,
  GlobalUIAudioConfigUpdate,
  GlobalUIAudioService,
  GlobalClickHandler,
  ElementDetectionResult
} from './global-audio.types';

// New chess board audio types
export type {
  ChessBoardAudioEvents,
  MoveAudioContext,
  ChessBoardInteractionType,
  ChessBoardAudioConfig
} from './chess-board-audio.types';

export {
  DEFAULT_CHESS_BOARD_AUDIO_CONFIG,
  CHESS_BOARD_AUDIO_PROFILES
} from './chess-board-audio.types';

// New audio feedback types
export type {
  AudioFeedbackTiming,
  AudioFeedbackIntensity,
  AudioFeedbackPattern,
  AudioFeedbackContext,
  AudioFeedbackDecision,
  ComponentAudioConfig
} from './audio-feedback.types';

export {
  DEFAULT_AUDIO_TIMING,
  AUDIO_FEEDBACK_PATTERNS
} from './audio-feedback.types';