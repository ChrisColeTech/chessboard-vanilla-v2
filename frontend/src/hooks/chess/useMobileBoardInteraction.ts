// useMobileBoardInteraction.ts - Clean mobile chess board interaction logic
import { useCallback, useEffect } from 'react';
import { useMobileChess } from './useMobileChess';
import { useDrag } from '../../providers/DragProvider';
import { useChessAudio } from '../../services/audio/audioService';
import type { ChessPosition, ChessPiece } from '../../types';

export const useMobileBoardInteraction = (initialFen?: string) => {
  // Core game logic
  const mobileChess = useMobileChess(initialFen);
  const { makeMove, getValidMoves } = mobileChess;
  
  // Drag system
  const drag = useDrag();
  const { setMoveHandler } = drag;
  
  // Audio feedback
  const audio = useChessAudio();
  const { playMove, playCheck } = audio;

  // Unified move handler for both tap-to-move and drag-and-drop
  const handleMove = useCallback(async (from: ChessPosition, to: ChessPosition): Promise<boolean> => {
    console.log(`🎯 [MOBILE INTERACTION] Move: ${from} → ${to}`);
    
    const result = await makeMove(from, to);
    
    if (result.isValid) {
      // Play appropriate audio feedback
      if (result.gameState.isCheckmate) {
        playCheck(); 
      } else if (result.gameState.isCheck) {
        playCheck();
      } else {
        playMove(!!result.move?.capturedPiece);
      }
      
      return true;
    } else {
      console.warn('❌ [MOBILE INTERACTION] Invalid move:', result.error);
      return false;
    }
  }, [makeMove, playMove, playCheck]);

  // Set up drag move handler
  useEffect(() => {
    const dragMoveHandler = async (move: { from: ChessPosition; to: ChessPosition }): Promise<boolean> => {
      return await handleMove(move.from, move.to);
    };
    
    setMoveHandler(dragMoveHandler);
  }, [handleMove, setMoveHandler]);

  // Tap-to-move handler
  const handleSquareTap = useCallback(async (square: ChessPosition) => {
    const { gameState } = mobileChess;
    if (!gameState) return;

    const mobileState = gameState.mobileState;
    
    // If we have a selected square and tapped a valid move target, make the move
    if (mobileState.selectedSquare && mobileState.validMoves.includes(square)) {
      await handleMove(mobileState.selectedSquare, square);
    } else {
      // Select/deselect square
      mobileChess.selectSquare(square);
    }
  }, [mobileChess, handleMove]);

  // Drag start handler
  const handleDragStart = useCallback((piece: ChessPiece, square: ChessPosition, pieceSize: number) => {
    const validMoves = getValidMoves(square);
    drag.startDrag(piece, square, validMoves, pieceSize);
  }, [getValidMoves, drag]);

  return {
    // Core game state
    ...mobileChess,
    
    // Interaction handlers
    handleSquareTap,
    handleDragStart,
    
    // Drag system
    ...drag,
    
    // Move handler for external use
    handleMove
  };
};