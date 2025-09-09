// mobile-chess.types.ts - Mobile-specific chess type definitions
// Phase 1: Foundation Types - Mobile chess interfaces

import type { 
  ChessPosition, 
  ChessPiece, 
  ChessGameState,
  ChessMove
} from './chess.types';

/**
 * Configuration for mobile chess board behavior
 * Defines how the mobile board should behave and appear
 */
export interface MobileChessConfig {
  /** Board size preset for different mobile devices */
  readonly boardSize: 'small' | 'medium' | 'large' | 'auto';
  /** Minimum touch target size in pixels (iOS/Android recommend 44px minimum) */
  readonly touchTargetSize: number;
  /** Whether drag and drop is enabled (secondary to tap-to-move) */
  readonly enableDragAndDrop: boolean;
  /** Primary interaction method - tap to select then tap to move */
  readonly tapToMoveEnabled: boolean;
  /** Show visual indicators for valid moves */
  readonly showValidMoves: boolean;
  /** Animation duration in milliseconds for piece movements */
  readonly animationDuration: number;
  /** Enable haptic feedback for interactions (if supported) */
  readonly enableHapticFeedback: boolean;
  /** Auto-rotate board based on player color */
  readonly autoRotateBoard: boolean;
}

/**
 * Touch interaction data for mobile chess
 * Captures touch events and gestures on the board
 */
export interface MobileChessInteraction {
  /** Type of interaction performed */
  readonly type: 'tap' | 'drag' | 'long-press' | 'double-tap';
  /** Chess square that was interacted with */
  readonly square: ChessPosition;
  /** Timestamp when interaction occurred */
  readonly timestamp: number;
  /** Screen coordinates of the interaction */
  readonly coords: { 
    readonly x: number; 
    readonly y: number; 
  };
  /** Duration of interaction (for long-press detection) */
  readonly duration?: number;
  /** Force/pressure of touch (if supported by device) */
  readonly force?: number;
}

/**
 * Mobile-specific board visual state
 * Manages UI state separate from game logic state
 */
export interface MobileBoardState {
  /** Currently selected square (tap-to-move first selection) */
  readonly selectedSquare: ChessPosition | null;
  /** Valid destination squares for the selected piece */
  readonly validMoves: readonly ChessPosition[];
  /** Last move made (for highlighting) */
  readonly lastMove: { 
    readonly from: ChessPosition; 
    readonly to: ChessPosition; 
  } | null;
  /** Squares to highlight (check, threats, etc.) */
  readonly highlightedSquares: readonly ChessPosition[];
  /** Whether it's the human player's turn (affects interactivity) */
  readonly isPlayerTurn: boolean;
  /** Whether the board is flipped (black pieces at bottom) */
  readonly isBoardFlipped: boolean;
  /** Animation state for piece movements */
  readonly animatingMove: {
    readonly from: ChessPosition;
    readonly to: ChessPosition;
    readonly piece: ChessPiece;
    readonly startTime: number;
  } | null;
}

/**
 * Extended game state for mobile chess
 * Includes mobile-specific state alongside standard chess state
 */
export interface MobileChessGameState extends ChessGameState {
  /** Mobile-specific board visual state */
  readonly mobileState: MobileBoardState;
  /** Current mobile configuration */
  readonly mobileConfig: MobileChessConfig;
  /** Touch interaction history for gesture recognition */
  readonly interactionHistory: readonly MobileChessInteraction[];
}

/**
 * Individual square state for mobile optimization
 * Used for efficient re-rendering of individual squares
 */
export interface MobileSquareState {
  /** Chess position of this square */
  readonly position: ChessPosition;
  /** Piece on this square (if any) */
  readonly piece: ChessPiece | null;
  /** Whether this square is selected */
  readonly isSelected: boolean;
  /** Whether this square is a valid move destination */
  readonly isValidMove: boolean;
  /** Whether this square is part of the last move */
  readonly isLastMove: boolean;
  /** Whether this square is highlighted (check, threat, etc.) */
  readonly isHighlighted: boolean;
  /** Whether this square is being animated */
  readonly isAnimating: boolean;
}

/**
 * Mobile touch event data
 * Standardizes touch event information across different devices
 */
export interface MobileTouchEvent {
  /** Original touch event */
  readonly originalEvent: TouchEvent;
  /** Touch coordinates relative to board */
  readonly boardCoords: { 
    readonly x: number; 
    readonly y: number; 
  };
  /** Chess square touched (if any) */
  readonly square: ChessPosition | null;
  /** Type of touch gesture */
  readonly gesture: 'start' | 'move' | 'end' | 'cancel';
  /** Touch identifier for multi-touch support */
  readonly touchId: number;
}

/**
 * Mobile chess move validation result
 * Extends standard move validation with mobile-specific feedback
 */
export interface MobileChessMoveResult {
  /** Whether the move is valid */
  readonly isValid: boolean;
  /** The executed move (if valid) */
  readonly move: ChessMove | null;
  /** Updated game state after move */
  readonly gameState: MobileChessGameState;
  /** Error message (if invalid) */
  readonly error: string | null;
  /** Mobile-specific feedback */
  readonly feedback: {
    /** Whether to play success sound */
    readonly playSuccessSound: boolean;
    /** Whether to play error sound */
    readonly playErrorSound: boolean;
    /** Whether to trigger haptic feedback */
    readonly triggerHaptic: boolean;
    /** Visual feedback type */
    readonly visualFeedback: 'none' | 'success' | 'error' | 'check' | 'checkmate';
  };
}

/**
 * Mobile board sizing information
 * Calculated dimensions for responsive board rendering
 */
export interface MobileBoardDimensions {
  /** Container width in pixels */
  readonly containerWidth: number;
  /** Container height in pixels */
  readonly containerHeight: number;
  /** Calculated board size (square) in pixels */
  readonly boardSize: number;
  /** Individual square size in pixels */
  readonly squareSize: number;
  /** Touch target size in pixels (may be larger than visual square) */
  readonly touchTargetSize: number;
  /** Board padding in pixels */
  readonly padding: number;
  /** Whether the board fits comfortably in the container */
  readonly fitsComfortably: boolean;
}

/**
 * Mobile chess piece animation data
 * Defines how pieces should animate during moves
 */
export interface MobilePieceAnimation {
  /** Piece being animated */
  readonly piece: ChessPiece;
  /** Animation start position */
  readonly fromPosition: ChessPosition;
  /** Animation end position */
  readonly toPosition: ChessPosition;
  /** Animation start time */
  readonly startTime: number;
  /** Animation duration in milliseconds */
  readonly duration: number;
  /** Animation easing function */
  readonly easing: 'linear' | 'ease-in' | 'ease-out' | 'ease-in-out';
  /** Whether this is a capture animation */
  readonly isCapture: boolean;
}

/**
 * Default mobile chess configuration
 * Provides sensible defaults for mobile chess behavior
 */
export const DEFAULT_MOBILE_CHESS_CONFIG: MobileChessConfig = {
  boardSize: 'auto',
  touchTargetSize: 44, // iOS/Android minimum recommendation
  enableDragAndDrop: true, // Secondary to tap-to-move
  tapToMoveEnabled: true, // Primary interaction method
  showValidMoves: true,
  animationDuration: 250, // Quarter second for smooth feel
  enableHapticFeedback: true,
  autoRotateBoard: false // Player preference
} as const;

/**
 * Board size presets for different mobile devices
 * Provides optimized sizes for common mobile screen sizes
 */
export const MOBILE_BOARD_SIZE_PRESETS = {
  small: 280,  // Small phones (iPhone SE, etc.)
  medium: 320, // Standard phones (iPhone 12, etc.)  
  large: 380,  // Large phones and small tablets
  auto: 0      // Calculate based on container
} as const;

/**
 * Touch gesture thresholds for mobile interaction
 * Defines timing and distance thresholds for gesture recognition
 */
export const MOBILE_TOUCH_THRESHOLDS = {
  /** Maximum time for a tap (milliseconds) */
  tapMaxDuration: 200,
  /** Minimum time for a long press (milliseconds) */
  longPressMinDuration: 500,
  /** Maximum movement distance for a tap (pixels) */
  tapMaxMovement: 10,
  /** Minimum movement distance to trigger drag (pixels) */
  dragMinMovement: 15,
  /** Time window for double tap detection (milliseconds) */
  doubleTapWindow: 300
} as const;