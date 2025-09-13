// mobileBoardUtils.ts - Utility functions for mobile chess board
import type { ChessPiece, ChessPosition, MobileChessGameState } from '../../types';

/**
 * Generate all 64 squares for 8x8 board (arranged from rank 8 to rank 1, left to right)
 */
export const generateChessSquares = (): ChessPosition[] => {
  const squares: ChessPosition[] = [];
  const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
  const ranks = [8, 7, 6, 5, 4, 3, 2, 1]; // Top to bottom (black to white perspective)

  for (const rank of ranks) {
    for (const file of files) {
      squares.push(`${file}${rank}` as ChessPosition);
    }
  }
  return squares;
};

/**
 * Convert game state position map to pieces object
 */
export const getPiecesFromGameState = (gameState: MobileChessGameState | null): Record<string, ChessPiece> => {
  if (!gameState) return {};
  
  const pieces: Record<string, ChessPiece> = {};
  gameState.position.forEach((piece, square) => {
    pieces[square] = piece;
  });
  return pieces;
};

/**
 * Check if a square has a king in check
 */
export const isKingInCheck = (
  _square: ChessPosition, 
  piece: ChessPiece | null, 
  gameState: MobileChessGameState | null
): boolean => {
  return piece?.type === 'king' && 
         gameState?.isCheck === true &&
         piece.color === gameState.activeColor;
};

/**
 * Check if square is part of the last move
 */
export const isLastMoveSquare = (
  square: ChessPosition,
  gameState: MobileChessGameState | null
): boolean => {
  const lastMove = gameState?.mobileState.lastMove;
  return lastMove?.from === square || lastMove?.to === square;
};

/**
 * Get mobile board state with safe defaults
 */
export const getMobileBoardState = (gameState: MobileChessGameState | null) => {
  return gameState?.mobileState || {
    selectedSquare: null,
    validMoves: [],
    lastMove: null,
    highlightedSquares: [],
    isPlayerTurn: true,
    isBoardFlipped: false,
    animatingMove: null
  };
};