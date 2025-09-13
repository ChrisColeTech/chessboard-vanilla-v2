// useDragAndDrop.ts - Drag and drop interaction
import { useState, useCallback, useRef } from 'react';
import type { ChessPiece, ChessPosition, ChessGameState } from '../../types/chess/chess.types';
import { positionToSquare } from '../../utils';

export interface UseDragAndDropHook {
  draggedPiece: ChessPiece | null;
  isDragging: boolean;
  dragSource: ChessPosition | null;
  validDropTargets: ChessPosition[];
  selectedSquare: ChessPosition | null;
  handleDragStart: (piece: ChessPiece, position: ChessPosition) => void;
  handleDragEnd: () => void;
  handleDrop: (targetPosition: ChessPosition) => Promise<boolean>;
  handleSquareClick: (position: ChessPosition) => void;
}

export const useDragAndDrop = (
  gameState: ChessGameState | null,
  onMove: (from: string, to: string) => Promise<boolean>,
  getValidMoves: (square?: string) => string[]
): UseDragAndDropHook => {
  const [draggedPiece, setDraggedPiece] = useState<ChessPiece | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragSource, setDragSource] = useState<ChessPosition | null>(null);
  const [validDropTargets, setValidDropTargets] = useState<ChessPosition[]>([]);
  const [selectedSquare, setSelectedSquare] = useState<ChessPosition | null>(null);
  const dragDataRef = useRef<{ piece: ChessPiece; source: ChessPosition } | null>(null);

  const clearDragState = useCallback(() => {
    setDraggedPiece(null);
    setIsDragging(false);
    setDragSource(null);
    setValidDropTargets([]);
    dragDataRef.current = null;
  }, []);

  const handleDragStart = useCallback((piece: ChessPiece, position: ChessPosition) => {
    if (!gameState || gameState.isGameOver) {
      return;
    }

    // Check if it's the current player's turn
    if (piece.color !== gameState.activeColor) {
      return;
    }

    setDraggedPiece(piece);
    setIsDragging(true);
    setDragSource(position);
    dragDataRef.current = { piece, source: position };

    // Get valid moves for this piece - position is already a string
    const sourceSquare = typeof position === 'string' ? position : positionToSquare(position);
    const validMoves = getValidMoves(sourceSquare);
    
    const targets: ChessPosition[] = validMoves.map(move => {
      // Parse UCI move format (e.g., "e2e4") or SAN format
      let to: string;
      if (move.length >= 4) {
        to = move.substring(2, 4);
      } else {
        to = move;
      }
      return to as ChessPosition;
    });

    setValidDropTargets(targets);
  }, [gameState, getValidMoves]);

  const handleDragEnd = useCallback(() => {
    // Small delay to allow drop event to process first
    setTimeout(() => {
      setIsDragging(false);
      // Don't clear other state immediately in case drop is processing
    }, 50);
  }, []);

  const handleDrop = useCallback(async (targetPosition: ChessPosition): Promise<boolean> => {
    if (!dragDataRef.current || !gameState) {
      clearDragState();
      return false;
    }

    const { source } = dragDataRef.current;
    const fromSquare = typeof source === 'string' ? source : positionToSquare(source);
    const toSquare = typeof targetPosition === 'string' ? targetPosition : positionToSquare(targetPosition);

    // Check if this is a valid drop target
    const isValidTarget = validDropTargets.includes(targetPosition);

    if (!isValidTarget) {
      clearDragState();
      return false;
    }

    try {
      const success = await onMove(fromSquare, toSquare);
      clearDragState();
      setSelectedSquare(null);
      return success;
    } catch (error) {
      console.error('Drop move failed:', error);
      clearDragState();
      return false;
    }
  }, [validDropTargets, gameState, onMove, clearDragState]);

  const handleSquareClick = useCallback((position: ChessPosition) => {
    if (!gameState || gameState.isGameOver) {
      return;
    }

    const clickedSquare = typeof position === 'string' ? position : positionToSquare(position);
    const piece = gameState.position.get(clickedSquare);

    // If no piece is selected, select this square (if it has a piece)
    if (!selectedSquare) {
      if (piece && piece.color === gameState.activeColor) {
        setSelectedSquare(position);
        
        // Show valid moves for click-to-move
        const validMoves = getValidMoves(clickedSquare);
        const targets: ChessPosition[] = validMoves.map(move => {
          let to: string;
          if (move.length >= 4) {
            to = move.substring(2, 4);
          } else {
            to = move;
          }
          return to as ChessPosition;
        });
        
        setValidDropTargets(targets);
      }
      return;
    }

    // If same square clicked, deselect
    const selectedSquareStr = typeof selectedSquare === 'string' ? selectedSquare : positionToSquare(selectedSquare);
    if (selectedSquareStr === clickedSquare) {
      setSelectedSquare(null);
      setValidDropTargets([]);
      return;
    }

    // If different piece of same color clicked, select new piece
    if (piece && piece.color === gameState.activeColor) {
      setSelectedSquare(position);
      
      const validMoves = getValidMoves(clickedSquare);
      const targets: ChessPosition[] = validMoves.map(move => {
        let to: string;
        if (move.length >= 4) {
          to = move.substring(2, 4);
        } else {
          to = move;
        }
        return to as ChessPosition;
      });
      
      setValidDropTargets(targets);
      return;
    }

    // Try to make a move from selected square to clicked square
    const fromSquare = selectedSquareStr;
    const toSquare = clickedSquare;

    // Check if this is a valid move
    const isValidMove = validDropTargets.includes(position);

    if (isValidMove) {
      onMove(fromSquare, toSquare).then(() => {
        setSelectedSquare(null);
        setValidDropTargets([]);
      }).catch(error => {
        console.error('Click move failed:', error);
      });
    } else {
      // Invalid move, clear selection
      setSelectedSquare(null);
      setValidDropTargets([]);
    }
  }, [gameState, selectedSquare, validDropTargets, getValidMoves, onMove]);

  return {
    draggedPiece,
    isDragging,
    dragSource,
    validDropTargets,
    selectedSquare,
    handleDragStart,
    handleDragEnd,
    handleDrop,
    handleSquareClick
  };
};