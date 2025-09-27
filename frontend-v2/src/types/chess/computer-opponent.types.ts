// computer-opponent.types.ts - Computer AI opponent type definitions
// Phase 1: Foundation Types - Computer opponent interfaces

/**
 * Computer difficulty levels on a user-friendly 1-10 scale
 * Maps internally to Stockfish's 0-20 skill level scale
 */
export type ComputerDifficulty = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

/**
 * Request interface for computer move calculations
 */
export interface ComputerMoveRequest {
  /** Current board position in FEN notation */
  fen: string;
  /** Computer difficulty level (1-10) */
  difficulty: ComputerDifficulty;
  /** Optional time limit for move calculation in milliseconds */
  timeLimit?: number;
}

/**
 * Response interface for computer move calculations
 */
export interface ComputerMoveResult {
  /** Move in UCI format (e.g., "e2e4", "e7e8q" for promotion) */
  move: string;
  /** Whether the move calculation was successful */
  success: boolean;
  /** Error message if calculation failed */
  error?: string;
  /** Optional evaluation score in centipawns */
  evaluation?: number;
}

/**
 * Configuration for computer opponent behavior at specific difficulty levels
 */
export interface ComputerOpponentConfig {
  /** User-facing difficulty level (1-10) */
  difficulty: ComputerDifficulty;
  /** Time limit for move calculation in milliseconds */
  timeLimit: number;
  /** Internal Stockfish skill level (0-20 scale) */
  skillLevel: number;
  /** Search depth hint for the engine */
  searchDepth?: number;
}

/**
 * Computer thinking state for UI feedback
 */
export interface ComputerThinkingState {
  /** Whether the computer is currently calculating a move */
  isThinking: boolean;
  /** Timestamp when thinking started */
  startTime?: number;
  /** Expected duration of thinking in milliseconds */
  expectedDuration?: number;
  /** Current thinking progress (0-100) if available */
  progress?: number;
}

/**
 * Computer opponent status information
 */
export interface ComputerOpponentStatus {
  /** Whether the computer opponent is ready to play */
  isReady: boolean;
  /** Current difficulty level */
  difficulty: ComputerDifficulty;
  /** Current thinking state */
  thinking: ComputerThinkingState;
  /** Any error messages */
  error?: string;
  /** Engine statistics if available */
  stats?: {
    movesCalculated: number;
    averageThinkingTime: number;
    currentSearchDepth: number;
  };
}

/**
 * Computer move analysis result
 */
export interface ComputerMoveAnalysis {
  /** The recommended move in UCI format */
  move: string;
  /** Position evaluation in centipawns (positive = advantage for side to move) */
  evaluation: number;
  /** Search depth reached */
  depth: number;
  /** Time spent calculating in milliseconds */
  timeSpent: number;
  /** Principal variation (best line of play) */
  principalVariation?: string[];
}