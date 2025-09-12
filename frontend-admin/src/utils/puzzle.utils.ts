// puzzle.utils.ts - Utility functions for puzzle handling
import { ChessGameService } from '../services/chess/ChessGameService';
import { PIECE_CONFIGURATIONS } from '../constants/chess/piece-configurations.constants';
import type { PieceConfig } from '../constants/chess/piece-configurations.constants';

/**
 * Convert FEN position to piece configuration array for MobileChessBoard
 */
export const fenToPieceConfiguration = (fen: string): PieceConfig[] => {
  try {
    // Create chess service to parse FEN
    const chess = new ChessGameService(fen);
    const gameState = chess.getCurrentState();
    
    // Convert pieces to configuration format
    const pieces: PieceConfig[] = [];
    let pieceCounter = 1;
    
    // Iterate through the position map and create piece configs
    gameState.position.forEach((piece, square) => {
      if (piece) {
        pieces.push({
          id: `${piece.color}-${piece.type}-${pieceCounter++}`,
          color: piece.color,
          type: piece.type,
          boardPosition: square
        });
      }
    });
    
    console.log('🧩 [PUZZLE UTILS] Converted FEN to piece config:', {
      fen: fen.split(' ')[0], // Just piece placement part
      pieceCount: pieces.length,
      pieces: pieces.map(p => `${p.color[0]}${p.type[0]} at ${p.boardPosition}`)
    });
    
    return pieces;
  } catch (error) {
    console.error('Failed to parse FEN:', fen, error);
    // Return empty configuration on error
    return [];
  }
};

/**
 * Update the global puzzle piece configuration
 */
export const updatePuzzleConfiguration = (fen: string): void => {
  const puzzlePieces = fenToPieceConfiguration(fen);
  
  // Update the global PIECE_CONFIGURATIONS object
  (PIECE_CONFIGURATIONS as any)['puzzle'] = puzzlePieces;
  console.log('🧩 [PUZZLE UTILS] Updated global puzzle configuration');
};

/**
 * Simple validation to check if a FEN string looks valid
 */
export const isValidFen = (fen: string): boolean => {
  if (!fen || typeof fen !== 'string') return false;
  
  const parts = fen.trim().split(' ');
  if (parts.length !== 6) return false;
  
  // Basic validation of piece placement (first part)
  const piecePlacement = parts[0];
  if (!piecePlacement || piecePlacement.length === 0) return false;
  
  return true;
};