// play-game.types.ts - Play page specific game state type definitions
// Phase 1: Foundation Types - Play game interfaces

import type { ChessGameState, ChessPiece, PieceColor, PieceType } from './chess.types';
import type { ComputerDifficulty, ComputerThinkingState } from './computer-opponent.types';

/**
 * Game modes supported by the play system
 */
export type PlayGameMode = 'human-vs-computer' | 'human-vs-human';

/**
 * Complete game state for human vs computer play
 */
export interface PlayGameState {
  /** Core chess game state from chess.js */
  gameState: ChessGameState;
  /** Current active player */
  currentPlayer: PieceColor;
  /** Human player's piece color */
  playerColor: PieceColor;
  /** Computer opponent's piece color */
  computerColor: PieceColor;
  /** Current game mode */
  gameMode: PlayGameMode;
  /** Computer difficulty level (1-10) */
  difficulty: ComputerDifficulty;
  /** Whether it's currently the computer's turn */
  isComputerTurn: boolean;
  /** Computer thinking state for UI feedback */
  thinkingState: ComputerThinkingState;
  /** Game settings and preferences */
  settings: GameSettings;
}

/**
 * Actions available for play game management
 */
export interface PlayGameActions {
  /** Make a move as the human player */
  makePlayerMove: (from: string, to: string, promotion?: PieceType) => Promise<boolean>;
  /** Request the computer to make a move */
  requestComputerMove: () => Promise<void>;
  /** Update computer difficulty level */
  updateDifficulty: (level: ComputerDifficulty) => Promise<void>;
  /** Reset/restart the game */
  resetGame: (playerColor?: PieceColor) => void;
  /** Resign the current game */
  resignGame: () => void;
  /** Undo the last move (if supported) */
  undoLastMove: () => boolean;
}

/**
 * Game result types and outcomes
 */
export type GameResultType = 'checkmate' | 'stalemate' | 'draw' | 'resignation' | 'timeout' | 'ongoing';

/**
 * Extended game result information for play mode (extends base GameResult)
 */
export interface PlayGameResult {
  /** Type of game ending */
  type: GameResultType;
  /** Winner if applicable */
  winner?: PieceColor;
  /** Human-readable result message */
  message: string;
  /** Whether the game has ended */
  isGameOver: boolean;
  /** Additional result details */
  details?: {
    /** Number of moves played */
    moveCount: number;
    /** Game duration in milliseconds */
    duration: number;
    /** Final position FEN */
    finalPosition: string;
  };
}

/**
 * Game settings and preferences
 */
export interface GameSettings {
  /** Human player's piece color preference */
  playerColor: PieceColor;
  /** Computer difficulty level */
  difficulty: ComputerDifficulty;
  /** Time limit for computer moves in milliseconds */
  computerTimeLimit: number;
  /** Whether audio feedback is enabled */
  audioEnabled: boolean;
  /** Whether to show valid move hints */
  showMoveHints: boolean;
  /** Whether to highlight the last move */
  highlightLastMove: boolean;
  /** Board orientation preference */
  boardOrientation: PieceColor;
}

/**
 * Player information for status display
 */
export interface PlayerInfo {
  /** Whether this is the human player */
  isHuman: boolean;
  /** Player's piece color */
  color: PieceColor;
  /** Player's display name */
  name: string;
  /** Whether it's currently this player's turn */
  isCurrentTurn: boolean;
  /** Whether the player is currently thinking/calculating */
  isThinking: boolean;
  /** Pieces captured by this player */
  capturedPieces: ChessPiece[];
  /** Additional player statistics */
  stats?: {
    movesPlayed: number;
    averageMoveTime: number;
    capturedPieceValue: number;
  };
}

/**
 * Game session information for analytics and history
 */
export interface GameSession {
  /** Unique session identifier */
  id: string;
  /** Session start timestamp */
  startTime: number;
  /** Session end timestamp if completed */
  endTime?: number;
  /** Initial game settings */
  initialSettings: GameSettings;
  /** Final game result */
  result?: PlayGameResult;
  /** Move history for the session */
  moves: GameMoveRecord[];
}

/**
 * Individual move record for game history
 */
export interface GameMoveRecord {
  /** Move number in the game */
  moveNumber: number;
  /** Which player made the move */
  player: PieceColor;
  /** Move in standard algebraic notation */
  san: string;
  /** Move in UCI format */
  uci: string;
  /** Timestamp when move was made */
  timestamp: number;
  /** Time taken to make the move in milliseconds */
  thinkingTime: number;
  /** Whether this move was made by the computer */
  isComputerMove: boolean;
}