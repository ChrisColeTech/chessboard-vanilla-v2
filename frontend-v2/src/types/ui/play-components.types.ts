// play-components.types.ts - Play page UI component interface definitions
// Phase 1: Foundation Types - Play UI component interfaces

import type { ChessPiece, PieceColor, ChessPosition } from '../chess/chess.types';
import type { ComputerDifficulty, ComputerThinkingState } from '../chess/computer-opponent.types';
import type { PlayGameResult, PlayerInfo } from '../chess/play-game.types';

/**
 * Props for PlayerStatus component - displays human/computer player information
 */
export interface PlayerStatusProps {
  /** Whether this is the human player */
  isHuman: boolean;
  /** Player's piece color */
  color: PieceColor;
  /** Whether it's currently this player's turn */
  isCurrentTurn: boolean;
  /** Whether the player is thinking/calculating a move */
  isThinking?: boolean;
  /** Player's display name */
  playerName?: string;
  /** Pieces captured by this player */
  capturedPieces: ChessPiece[];
  /** Optional additional player information */
  playerInfo?: PlayerInfo;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for GameControls component - game management buttons
 */
export interface GameControlsProps {
  /** Handler for starting a new game */
  onNewGame: () => void;
  /** Handler for resigning the current game */
  onResign: () => void;
  /** Handler for flipping the board orientation */
  onFlipBoard: () => void;
  /** Handler for undoing the last move */
  onUndoMove?: () => void;
  /** Whether a game is currently active */
  isGameActive: boolean;
  /** Whether undo is available */
  canUndo?: boolean;
  /** Whether controls should be disabled */
  disabled?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for DifficultySelector component - AI skill level selection
 */
export interface DifficultyLevelProps {
  /** Current difficulty level (1-10) */
  currentLevel: ComputerDifficulty;
  /** Handler for difficulty level changes */
  onLevelChange: (level: ComputerDifficulty) => void;
  /** Whether the selector should be disabled */
  disabled?: boolean;
  /** Whether to show difficulty descriptions */
  showDescriptions?: boolean;
  /** Compact display mode */
  compact?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for ComputerThinking component - AI processing indicator
 */
export interface ComputerThinkingProps {
  /** Computer thinking state */
  thinkingState: ComputerThinkingState;
  /** Current difficulty level for context */
  difficulty: ComputerDifficulty;
  /** Whether to show progress information */
  showProgress?: boolean;
  /** Whether to animate the thinking indicator */
  animated?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for GameStatusBar component - current game status display
 */
export interface GameStatusBarProps {
  /** Current player's turn */
  currentPlayer: PieceColor;
  /** Game result information */
  gameResult?: PlayGameResult;
  /** Whether the computer is thinking */
  isComputerThinking: boolean;
  /** Current move number */
  moveNumber?: number;
  /** Game timer information */
  gameTime?: {
    total: number;
    current: number;
  };
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for PlaySettings component - game settings panel
 */
export interface PlaySettingsProps {
  /** Handler for player color change */
  onPlayerColorChange: (color: PieceColor) => void;
  /** Handler for difficulty change */
  onDifficultyChange: (level: ComputerDifficulty) => void;
  /** Handler for audio settings change */
  onAudioToggle: (enabled: boolean) => void;
  /** Handler for move hints toggle */
  onMoveHintsToggle: (enabled: boolean) => void;
  /** Current player color */
  playerColor: PieceColor;
  /** Current difficulty level */
  difficulty: ComputerDifficulty;
  /** Whether audio is enabled */
  audioEnabled: boolean;
  /** Whether move hints are enabled */
  moveHintsEnabled: boolean;
  /** Whether settings should be disabled during gameplay */
  disabled?: boolean;
  /** Whether to show advanced settings */
  showAdvanced?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for PlayChessboard component - specialized chessboard for play mode
 */
export interface PlayChessboardProps {
  /** Board orientation */
  orientation: PieceColor;
  /** Whether the board should be interactive */
  interactive: boolean;
  /** Whether to highlight valid moves */
  highlightValidMoves?: boolean;
  /** Whether to highlight the last move */
  highlightLastMove?: boolean;
  /** Whether to show coordinates */
  showCoordinates?: boolean;
  /** Custom board size */
  boardSize?: number;
  /** Handler for square clicks */
  onSquareClick?: (square: ChessPosition) => void;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for MoveHistory component - display game move history
 */
export interface MoveHistoryProps {
  /** List of moves in the game */
  moves: Array<{
    moveNumber: number;
    white: string;
    black?: string;
    isCurrentMove?: boolean;
  }>;
  /** Handler for clicking on a move */
  onMoveClick?: (moveIndex: number) => void;
  /** Whether the history should be scrollable */
  scrollable?: boolean;
  /** Maximum height for scrollable history */
  maxHeight?: number;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Props for GameResult modal - display game outcome
 */
export interface GameResultModalProps {
  /** Whether the modal is open */
  isOpen: boolean;
  /** Game result information */
  result: PlayGameResult;
  /** Handler for starting a new game */
  onNewGame: () => void;
  /** Handler for closing the modal */
  onClose: () => void;
  /** Handler for reviewing the game */
  onReviewGame?: () => void;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Common props for all play page components
 */
export interface BasePlayComponentProps {
  /** Custom CSS classes */
  className?: string;
  /** Whether the component should be disabled */
  disabled?: boolean;
  /** Custom data attributes */
  'data-testid'?: string;
}

/**
 * Theme variant options for play components
 */
export type PlayComponentTheme = 'light' | 'dark' | 'auto';

/**
 * Size variants for play components
 */
export type PlayComponentSize = 'small' | 'medium' | 'large';

/**
 * Animation preferences for play components
 */
export interface PlayComponentAnimation {
  /** Whether animations are enabled */
  enabled: boolean;
  /** Animation duration in milliseconds */
  duration?: number;
  /** Animation easing function */
  easing?: string;
}