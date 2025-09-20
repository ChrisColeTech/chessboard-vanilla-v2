// computer-chess.utils.ts - Computer move parsing and validation utilities
// Phase 2: Utilities & Constants - Computer chess utilities

import type { ComputerDifficulty } from '../../types';

/**
 * Parsed move components from UCI format
 */
export interface ParsedMove {
  /** Source square (e.g., "e2") */
  from: string;
  /** Destination square (e.g., "e4") */
  to: string;
  /** Promotion piece if applicable (e.g., "q", "r", "b", "n") */
  promotion?: string;
}

/**
 * Parse a UCI format move into its components
 * @param move UCI format move string (e.g., "e2e4", "e7e8q")
 * @returns Parsed move components
 * @throws Error if move format is invalid
 */
export const parseEngineMove = (move: string): ParsedMove => {
  if (typeof move !== 'string') {
    throw new Error('Move must be a string');
  }

  const trimmedMove = move.trim();
  
  if (trimmedMove.length < 4) {
    throw new Error(`Invalid move format: "${move}". Expected format like "e2e4" or "e7e8q"`);
  }

  const from = trimmedMove.substring(0, 2);
  const to = trimmedMove.substring(2, 4);
  const promotion = trimmedMove.length > 4 ? trimmedMove[4] : undefined;

  // Validate square format (letter a-h followed by number 1-8)
  const squarePattern = /^[a-h][1-8]$/;
  
  if (!squarePattern.test(from)) {
    throw new Error(`Invalid source square: "${from}". Expected format like "e2"`);
  }
  
  if (!squarePattern.test(to)) {
    throw new Error(`Invalid destination square: "${to}". Expected format like "e4"`);
  }

  // Validate promotion piece if present
  if (promotion && !/^[qrbn]$/.test(promotion)) {
    throw new Error(`Invalid promotion piece: "${promotion}". Expected one of: q, r, b, n`);
  }

  return {
    from,
    to,
    promotion
  };
};

/**
 * Validate UCI move string format
 * @param move Move string to validate
 * @returns True if move format is valid
 */
export const validateMoveFormat = (move: string): boolean => {
  if (typeof move !== 'string') {
    return false;
  }

  // UCI pattern: source square + destination square + optional promotion
  const uciPattern = /^[a-h][1-8][a-h][1-8][qrbn]?$/;
  return uciPattern.test(move.trim());
};

/**
 * Calculate realistic thinking time based on difficulty level
 * Higher difficulties take longer to maintain realism
 * @param difficulty Computer difficulty level (1-10)
 * @returns Thinking time in milliseconds
 */
export const calculateThinkingTime = (difficulty: ComputerDifficulty): number => {
  // Base thinking time in milliseconds
  const baseTime = 500;
  
  // Difficulty multiplier (1-10 maps to 1.0-3.0x)
  const multiplier = 1 + (difficulty - 1) * 0.22;
  
  // Add some randomness for realism (±20%)
  const randomFactor = 0.8 + Math.random() * 0.4;
  
  const thinkingTime = Math.floor(baseTime * multiplier * randomFactor);
  
  // Ensure minimum thinking time for realism
  return Math.max(thinkingTime, 300);
};

/**
 * Format game time duration into human-readable format
 * @param milliseconds Duration in milliseconds
 * @returns Formatted time string (e.g., "2:45", "1:23:45")
 */
export const formatGameTime = (milliseconds: number): string => {
  if (milliseconds < 0) {
    return '0:00';
  }

  const totalSeconds = Math.floor(milliseconds / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
  
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

/**
 * Format thinking time for display purposes
 * @param milliseconds Thinking time in milliseconds
 * @returns Formatted thinking time string
 */
export const formatThinkingTime = (milliseconds: number): string => {
  if (milliseconds < 1000) {
    return `${milliseconds}ms`;
  }
  
  const seconds = (milliseconds / 1000).toFixed(1);
  return `${seconds}s`;
};

/**
 * Generate a variation in move timing to make computer play feel more natural
 * @param baseTime Base time in milliseconds
 * @param variationPercent Variation percentage (default 20%)
 * @returns Time with natural variation
 */
export const addNaturalVariation = (baseTime: number, variationPercent: number = 20): number => {
  const variation = variationPercent / 100;
  const minTime = baseTime * (1 - variation);
  const maxTime = baseTime * (1 + variation);
  
  return Math.floor(minTime + Math.random() * (maxTime - minTime));
};

/**
 * Convert centipawn evaluation to human-readable advantage
 * @param centipawns Evaluation in centipawns (positive = white advantage)
 * @returns Human-readable evaluation string
 */
export const formatEvaluation = (centipawns: number): string => {
  const pawns = Math.abs(centipawns) / 100;
  
  if (Math.abs(centipawns) < 15) {
    return 'Equal position';
  }
  
  if (Math.abs(centipawns) > 500) {
    const advantage = centipawns > 0 ? 'White' : 'Black';
    return `${advantage} winning`;
  }
  
  const advantage = centipawns > 0 ? 'White' : 'Black';
  const pawnValue = pawns.toFixed(1);
  
  return `${advantage} +${pawnValue}`;
};

/**
 * Validate that a move string represents a legal chess move format
 * This only validates format, not whether the move is legal in a given position
 * @param move Move string to validate
 * @returns Validation result with details
 */
export const validateMoveString = (move: string): {
  isValid: boolean;
  error?: string;
  parsed?: ParsedMove;
} => {
  try {
    const parsed = parseEngineMove(move);
    return {
      isValid: true,
      parsed
    };
  } catch (error) {
    return {
      isValid: false,
      error: error instanceof Error ? error.message : 'Invalid move format'
    };
  }
};

/**
 * Create a standard UCI move string from components
 * @param from Source square
 * @param to Destination square  
 * @param promotion Optional promotion piece
 * @returns UCI format move string
 */
export const createUciMove = (from: string, to: string, promotion?: string): string => {
  let move = `${from}${to}`;
  
  if (promotion) {
    // Ensure promotion is lowercase
    move += promotion.toLowerCase();
  }
  
  // Validate the resulting move
  if (!validateMoveFormat(move)) {
    throw new Error(`Generated invalid UCI move: ${move}`);
  }
  
  return move;
};