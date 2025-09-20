// chess-board-audio.types.ts - Chess board specific audio event types and configurations

/**
 * Chess board audio events configuration
 * Controls which audio events are enabled for chess board interactions
 */
export interface ChessBoardAudioEvents {
  /** Play sound when a piece is selected/clicked */
  readonly pieceSelection: boolean;
  /** Play sound when a piece is moved */
  readonly pieceMovement: boolean;
  /** Play sound for invalid moves or actions */
  readonly invalidMove: boolean;
  /** Play sound when a piece captures another piece */
  readonly capture: boolean;
  /** Play sound when king is in check */
  readonly check: boolean;
  /** Play sound for game events (start, end, etc.) */
  readonly gameEvents: boolean;
}

/**
 * Context information for chess move audio events
 * Provides details about the move to determine appropriate audio feedback
 */
export interface MoveAudioContext {
  /** Type of move being performed */
  readonly moveType: 'normal' | 'capture' | 'castle' | 'enPassant' | 'promotion';
  /** Type of piece being moved */
  readonly pieceType: string;
  /** Whether the move resulted in a capture */
  readonly wasCapture: boolean;
  /** Whether the move resulted in check */
  readonly wasCheck: boolean;
  /** Source square of the move */
  readonly from?: string;
  /** Destination square of the move */
  readonly to?: string;
}

/**
 * Chess board audio interaction types
 * Extends UI interaction types with chess-specific interactions
 */
export type ChessBoardInteractionType = 
  | 'pieceSelection'
  | 'pieceDeselection' 
  | 'pieceMovement'
  | 'invalidMove'
  | 'capture'
  | 'check'
  | 'gameStart'
  | 'gameEnd';

/**
 * Chess board audio configuration
 * Complete configuration for all chess board audio settings
 */
export interface ChessBoardAudioConfig {
  /** Enable/disable all chess board audio */
  readonly enabled: boolean;
  /** Volume level for chess board sounds (0-1) */
  readonly volume: number;
  /** Individual event configurations */
  readonly events: ChessBoardAudioEvents;
  /** Audio profile selection */
  readonly profile: 'silent' | 'minimal' | 'full';
}

/**
 * Default chess board audio configuration
 */
export const DEFAULT_CHESS_BOARD_AUDIO_CONFIG: ChessBoardAudioConfig = {
  enabled: true,
  volume: 0.7,
  events: {
    pieceSelection: true,
    pieceMovement: true,
    invalidMove: true,
    capture: true,
    check: true,
    gameEvents: true
  },
  profile: 'full'
} as const;

/**
 * Chess board audio profiles with predefined settings
 */
export const CHESS_BOARD_AUDIO_PROFILES = {
  silent: {
    pieceSelection: false,
    pieceMovement: false,
    invalidMove: false,
    capture: false,
    check: false,
    gameEvents: false
  },
  minimal: {
    pieceSelection: false,
    pieceMovement: true,
    invalidMove: true,
    capture: true,
    check: true,
    gameEvents: false
  },
  full: {
    pieceSelection: true,
    pieceMovement: true,
    invalidMove: true,
    capture: true,
    check: true,
    gameEvents: true
  }
} as const;