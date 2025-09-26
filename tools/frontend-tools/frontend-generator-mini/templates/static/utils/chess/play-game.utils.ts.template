// play-game.utils.ts - Play game utility functions
// Phase 2: Utilities & Constants - Play game utilities

import type { 
  PlayGameState, 
  PlayGameResult, 
  GameResultType, 
  PlayerInfo,
  PieceColor,
  ComputerDifficulty,
  ChessPiece
} from '../../types';

/**
 * Generate a human-readable message for game results
 * @param result Game result information
 * @returns User-friendly result message
 */
export const getGameResultMessage = (result: PlayGameResult): string => {
  switch (result.type) {
    case 'checkmate':
      if (result.winner === 'white') {
        return 'Checkmate! White wins!';
      } else if (result.winner === 'black') {
        return 'Checkmate! Black wins!';
      }
      return 'Checkmate!';
      
    case 'stalemate':
      return 'Draw by stalemate - no legal moves available';
      
    case 'draw':
      return 'Game drawn';
      
    case 'resignation':
      if (result.winner === 'white') {
        return 'Black resigned - White wins!';
      } else if (result.winner === 'black') {
        return 'White resigned - Black wins!';
      }
      return 'Game ended by resignation';
      
    case 'timeout':
      if (result.winner === 'white') {
        return 'Black ran out of time - White wins!';
      } else if (result.winner === 'black') {
        return 'White ran out of time - Black wins!';
      }
      return 'Game ended by timeout';
      
    case 'ongoing':
      return 'Game in progress';
      
    default:
      return 'Game ended';
  }
};

/**
 * Determine if it's currently the human player's turn
 * @param gameState Current play game state
 * @returns True if it's the player's turn to move
 */
export const isPlayerTurn = (gameState: PlayGameState): boolean => {
  return gameState.currentPlayer === gameState.playerColor;
};

/**
 * Determine if it's currently the computer's turn
 * @param gameState Current play game state
 * @returns True if it's the computer's turn to move
 */
export const isComputerTurn = (gameState: PlayGameState): boolean => {
  return gameState.currentPlayer === gameState.computerColor && 
         gameState.gameMode === 'human-vs-computer';
};

/**
 * Check if the human player can currently make a move
 * @param gameState Current play game state
 * @returns True if the player can make a move
 */
export const canMakeMove = (gameState: PlayGameState): boolean => {
  return !gameState.gameState.isGameOver && 
         isPlayerTurn(gameState) && 
         !gameState.thinkingState.isThinking;
};

/**
 * Check if the computer should make a move
 * @param gameState Current play game state
 * @returns True if the computer should move
 */
export const shouldComputerMove = (gameState: PlayGameState): boolean => {
  return !gameState.gameState.isGameOver &&
         isComputerTurn(gameState) &&
         !gameState.thinkingState.isThinking;
};

/**
 * Get the opponent's color for a given player color
 * @param playerColor The player's color
 * @returns The opponent's color
 */
export const getOpponentColor = (playerColor: PieceColor): PieceColor => {
  return playerColor === 'white' ? 'black' : 'white';
};

/**
 * Create player information objects for display
 * @param gameState Current play game state
 * @returns Player info for both human and computer
 */
export const createPlayerInfos = (gameState: PlayGameState): {
  humanPlayer: PlayerInfo;
  computerPlayer: PlayerInfo;
} => {
  // Extract captured pieces from move history
  const capturedPieces = gameState.gameState.history
    .map(move => move.capturedPiece || move.captured)
    .filter((piece): piece is ChessPiece => piece !== undefined);

  const humanPlayer: PlayerInfo = {
    isHuman: true,
    color: gameState.playerColor,
    name: 'You',
    isCurrentTurn: isPlayerTurn(gameState),
    isThinking: false,
    capturedPieces: capturedPieces.filter(
      piece => piece.color === getOpponentColor(gameState.playerColor)
    )
  };

  const computerPlayer: PlayerInfo = {
    isHuman: false,
    color: gameState.computerColor,
    name: 'Computer',
    isCurrentTurn: isComputerTurn(gameState),
    isThinking: gameState.thinkingState.isThinking,
    capturedPieces: capturedPieces.filter(
      piece => piece.color === gameState.playerColor
    )
  };

  return { humanPlayer, computerPlayer };
};

/**
 * Calculate the total value of captured pieces
 * @param capturedPieces Array of captured pieces
 * @returns Total point value of captured pieces
 */
export const calculateCapturedPieceValue = (capturedPieces: Array<{type: string}>): number => {
  const pieceValues = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0 // King capture ends the game
  };

  return capturedPieces.reduce((total, piece) => {
    return total + (pieceValues[piece.type as keyof typeof pieceValues] || 0);
  }, 0);
};

/**
 * Determine if a game result indicates the human player won
 * @param result Game result
 * @param playerColor Human player's color
 * @returns True if human player won
 */
export const didHumanWin = (result: PlayGameResult, playerColor: PieceColor): boolean => {
  return result.winner === playerColor;
};

/**
 * Determine if a game result indicates the computer won
 * @param result Game result
 * @param playerColor Human player's color
 * @returns True if computer won
 */
export const didComputerWin = (result: PlayGameResult, playerColor: PieceColor): boolean => {
  return result.winner === getOpponentColor(playerColor);
};

/**
 * Create a game result object for various end conditions
 * @param type Type of game ending
 * @param winner Winner if applicable
 * @param additionalDetails Optional additional details
 * @returns Complete game result object
 */
export const createGameResult = (
  type: GameResultType,
  winner?: PieceColor,
  additionalDetails?: Partial<PlayGameResult['details']>
): PlayGameResult => {
  const result: PlayGameResult = {
    type,
    winner,
    message: '',
    isGameOver: type !== 'ongoing'
  };

  // Generate the message
  result.message = getGameResultMessage(result);

  // Add details if provided
  if (additionalDetails) {
    result.details = {
      moveCount: additionalDetails.moveCount || 0,
      duration: additionalDetails.duration || 0,
      finalPosition: additionalDetails.finalPosition || '',
      ...additionalDetails
    };
  }

  return result;
};

/**
 * Format a difficulty level for display
 * @param difficulty Difficulty level (1-10)
 * @returns Formatted difficulty string with description
 */
export const formatDifficultyLevel = (difficulty: ComputerDifficulty): string => {
  const descriptions = {
    1: 'Beginner',
    2: 'Beginner+', 
    3: 'Casual',
    4: 'Casual+',
    5: 'Club Player',
    6: 'Club Player+',
    7: 'Strong Player',
    8: 'Strong Player+',
    9: 'Expert',
    10: 'Master'
  };

  return `Level ${difficulty} (${descriptions[difficulty]})`;
};

/**
 * Validate game state consistency
 * @param gameState Game state to validate
 * @returns Validation result with any issues found
 */
export const validateGameState = (gameState: PlayGameState): {
  isValid: boolean;
  issues: string[];
} => {
  const issues: string[] = [];

  // Check basic consistency
  if (gameState.playerColor === gameState.computerColor) {
    issues.push('Player and computer cannot have the same color');
  }

  // Check difficulty range
  if (gameState.difficulty < 1 || gameState.difficulty > 10) {
    issues.push(`Invalid difficulty level: ${gameState.difficulty}. Must be 1-10`);
  }

  // Check current player is valid
  if (gameState.currentPlayer !== 'white' && gameState.currentPlayer !== 'black') {
    issues.push(`Invalid current player: ${gameState.currentPlayer}`);
  }

  // Check thinking state consistency
  if (gameState.thinkingState.isThinking && gameState.thinkingState.startTime) {
    const now = Date.now();
    const thinkingDuration = now - gameState.thinkingState.startTime;
    
    if (thinkingDuration < 0) {
      issues.push('Thinking start time is in the future');
    }
    
    // Warn about very long thinking times (over 30 seconds)
    if (thinkingDuration > 30000) {
      issues.push('Computer has been thinking for an unusually long time');
    }
  }

  return {
    isValid: issues.length === 0,
    issues
  };
};

/**
 * Get suggested next actions based on current game state
 * @param gameState Current game state
 * @returns Array of suggested actions for the UI
 */
export const getSuggestedActions = (gameState: PlayGameState): string[] => {
  const actions: string[] = [];

  if (gameState.gameState.isGameOver) {
    actions.push('Start new game');
    return actions;
  }

  if (canMakeMove(gameState)) {
    actions.push('Make your move');
    
    if (gameState.gameState.isCheck) {
      actions.push('Your king is in check!');
    }
  }

  if (shouldComputerMove(gameState)) {
    actions.push('Computer is thinking...');
  }

  if (gameState.thinkingState.isThinking) {
    actions.push('Wait for computer move');
  }

  return actions;
};