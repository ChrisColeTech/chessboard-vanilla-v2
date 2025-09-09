// useWrapperChessBoard.ts - Hook for wrapper-based chess board state management
import { useState, useEffect, useCallback } from 'react';
import { useChessBoardAudio } from '../../hooks/audio/useChessBoardAudio';
import { useChessGameStore } from '../../stores/chessGameStore';
import { PIECE_CONFIGURATIONS } from '../../constants/chess/piece-configurations.constants';
import type { WrapperPiece } from '../../types/chess/wrapper-piece.types';

export const useWrapperChessBoard = (gridSize: number = 6, pieceConfig?: 'drag-test' | 'mobile-test' | 'standard-chess' | 'puzzle') => {
  const [wrapperPieces, setWrapperPieces] = useState<WrapperPiece[]>([]);
  const [isFlipped, setIsFlipped] = useState<boolean>(false);
  
  // Store integration
  const store = useChessGameStore();
  const { 
    selectedCell, 
    draggedPiece,
    capturedPieces,
    setSelectedCell: setStoreSelectedCell,
    setDraggedPiece: setStoreDraggedPiece,
    setPieces: setStorePieces,
    setCapturedPieces: setStoreCapturedPieces,
    addCapturedPiece: addStoreCapturedPiece
  } = store;
  
  const {
    playPieceSelection,
    playPieceDeselection,
    playPieceMove,
    playInvalidMove,
  } = useChessBoardAudio();

  // Convert chess notation to pixel coordinates 
  const chessToPx = useCallback((cellId: string): { x: number; y: number } => {
    const file = cellId[0];
    const rank = parseInt(cellId[1]);
    
    let column = file.charCodeAt(0) - "a".charCodeAt(0);
    let row = gridSize - rank;
    
    // Flip coordinates if board is flipped
    if (isFlipped) {
      column = (gridSize - 1) - column;
      row = (gridSize - 1) - row;
    }
    
    // Calculate pixel position as percentage of container
    const cellPercentage = 100 / gridSize;
    return {
      x: column * cellPercentage + cellPercentage / 2, // Return as percentage
      y: row * cellPercentage + cellPercentage / 2
    };
  }, [gridSize, isFlipped]);

  // Helper to find piece by board position
  const findPieceAt = useCallback((position: string) => {
    return wrapperPieces.find(p => p.boardPosition === position);
  }, [wrapperPieces]);


  // Initialize wrapper pieces with pixel positions
  const initializePieces = useCallback(() => {
    const configKey = pieceConfig || 'mobile-test';
    const pieceConfigs = PIECE_CONFIGURATIONS[configKey];
    
    const initialPieces: WrapperPiece[] = pieceConfigs.map(config => ({
      id: config.id,
      color: config.color,
      type: config.type,
      ...chessToPx(config.boardPosition),
      opacity: 1,
      isAnimating: false,
      boardPosition: config.boardPosition,
      scale: 1
    }));
    
    setWrapperPieces(initialPieces);
  }, [chessToPx, pieceConfig]);

  // Flip board function
  const handleFlipBoard = useCallback(() => {
    setIsFlipped(prev => !prev);
    console.log('🔄 [MOBILE WRAPPER] Board flipped:', !isFlipped);
  }, [isFlipped]);

  // Reset function
  const handleReset = useCallback(() => {
    initializePieces();
    setStoreSelectedCell(null);
    setStoreCapturedPieces([]);
    console.log('🎯 [MOBILE WRAPPER] Board reset to initial position');
  }, [initializePieces, setStoreSelectedCell, setStoreCapturedPieces]);

  // Initialize pieces on mount or gridSize change
  useEffect(() => {
    initializePieces();
  }, [initializePieces]);

  // Sync pieces with store whenever they change
  useEffect(() => {
    setStorePieces(wrapperPieces);
  }, [wrapperPieces, setStorePieces]);

  // Expose reset and flip functions globally
  useEffect(() => {
    (window as any).__wrapperChessBoardReset = handleReset;
    (window as any).__wrapperChessBoardFlip = handleFlipBoard;
    return () => {
      delete (window as any).__wrapperChessBoardReset;
      delete (window as any).__wrapperChessBoardFlip;
    };
  }, [handleReset, handleFlipBoard]);

  const handleCellClick = useCallback((cellId: string) => {
    const pieceAtCell = findPieceAt(cellId);

    if (selectedCell === null) {
      // First click - select cell only if it has a piece
      if (pieceAtCell) {
        setStoreSelectedCell(cellId);
        playPieceSelection();
        console.log(`Selected ${pieceAtCell.color} ${pieceAtCell.type} at: ${cellId}`);
      } else {
        playInvalidMove();
        console.log(`Clicked empty cell: ${cellId}`);
      }
    } else if (selectedCell === cellId) {
      // Clicking same cell - deselect
      setStoreSelectedCell(null);
      playPieceDeselection();
      console.log(`Deselected piece at: ${cellId}`);
    } else {
      // Second click - move piece to new cell
      const movingPiece = findPieceAt(selectedCell);
      if (movingPiece) {
        const targetPiece = findPieceAt(cellId);
        
        // Check if trying to capture own piece
        if (targetPiece && targetPiece.color === movingPiece.color) {
          playInvalidMove();
          console.log(`❌ Cannot capture own piece: ${targetPiece.color} ${targetPiece.type} at ${cellId}`);
          setStoreSelectedCell(null);
          return;
        }
        
        const wasCapture = !!targetPiece;

        // Handle captured piece (shrink and fade out)
        if (wasCapture && targetPiece) {
          // Add to captured pieces list
          addStoreCapturedPiece({
            id: targetPiece.id,
            color: targetPiece.color as any,
            type: targetPiece.type as any,
            position: { 
              file: targetPiece.boardPosition[0] as any, 
              rank: parseInt(targetPiece.boardPosition[1]) as any 
            }
          });
          
          setWrapperPieces(prev => prev.map(p => 
            p.id === targetPiece.id 
              ? { ...p, opacity: 0, scale: 0.1, isAnimating: true }
              : p
          ));
          
          // Remove captured piece after shrink animation
          setTimeout(() => {
            setWrapperPieces(prev => prev.filter(p => p.id !== targetPiece.id));
          }, 180);
        }

        playPieceMove(wasCapture);

        // Animate moving piece to new position
        const newPosition = chessToPx(cellId);
        setWrapperPieces(prev => prev.map(p => {
          if (p.id === movingPiece.id) {
            return {
              ...p,
              x: newPosition.x,
              y: newPosition.y,
              isAnimating: true,
              boardPosition: cellId,
              opacity: 0.7 // Ghost effect during move
            };
          }
          return p;
        }));

        // Complete animation (optimized for smooth movement)
        setTimeout(() => {
          setWrapperPieces(prev => prev.map(p => 
            p.id === movingPiece.id 
              ? { ...p, opacity: 1, isAnimating: false }
              : p
          ));
        }, 250);
      }

      setStoreSelectedCell(null);
      console.log(`Moved piece: ${selectedCell} → ${cellId}`);
    }
  }, [selectedCell, findPieceAt, chessToPx, playPieceSelection, playPieceDeselection, playPieceMove, playInvalidMove]);

  // Piece click handler (same logic as cell click but for pieces)
  const handlePieceClick = useCallback((piece: WrapperPiece) => {
    handleCellClick(piece.boardPosition);
  }, [handleCellClick]);

  // Drag handlers
  const handleDragStart = useCallback((piece: WrapperPiece) => {
    setStoreDraggedPiece(piece);
    setStoreSelectedCell(piece.boardPosition);
    playPieceSelection();
    console.log(`🎯 [DRAG] Started dragging ${piece.color} ${piece.type} from ${piece.boardPosition}`);
    console.log(`🔥 [DRAG] isDragging state will be:`, !!piece);
  }, [playPieceSelection, setStoreDraggedPiece, setStoreSelectedCell]);

  const handleDrop = useCallback((targetSquare: string, dragData: { pieceId: string; fromPosition: string }) => {
    const piece = wrapperPieces.find(p => p.id === dragData.pieceId);
    if (!piece || targetSquare === dragData.fromPosition) {
      setStoreDraggedPiece(null);
      setStoreSelectedCell(null);
      return;
    }

    // Attempt move
    const targetPiece = findPieceAt(targetSquare);
    
    // Check if trying to capture own piece
    if (targetPiece && targetPiece.color === piece.color) {
      console.log(`❌ [DRAG] Cannot capture own piece: ${targetPiece.color} ${targetPiece.type} at ${targetSquare}`);
      setStoreDraggedPiece(null);
      setStoreSelectedCell(null);
      return;
    }
    
    const wasCapture = !!targetPiece;

    console.log(`🎯 [DRAG] Dropping ${piece.color} ${piece.type}: ${dragData.fromPosition} → ${targetSquare}${wasCapture ? ' (capture)' : ''}`);

    // Handle captured piece (shrink and fade out)
    if (wasCapture && targetPiece) {
      // Add to captured pieces list
      addStoreCapturedPiece({
        id: targetPiece.id,
        color: targetPiece.color as any,
        type: targetPiece.type as any,
        position: { 
          file: targetPiece.boardPosition[0] as any, 
          rank: parseInt(targetPiece.boardPosition[1]) as any 
        }
      });
      
      setWrapperPieces(prev => prev.map(p => 
        p.id === targetPiece.id 
          ? { ...p, opacity: 0, scale: 0.1, isAnimating: true }
          : p
      ));
      
      // Remove captured piece after animation
      setTimeout(() => {
        setWrapperPieces(prev => prev.filter(p => p.id !== targetPiece.id));
      }, 180);
    }

    // Move the dragged piece
    const newPosition = chessToPx(targetSquare);
    setWrapperPieces(prev => prev.map(p => {
      if (p.id === piece.id) {
        return {
          ...p,
          x: newPosition.x,
          y: newPosition.y,
          isAnimating: true,
          boardPosition: targetSquare,
          opacity: 0.7
        };
      }
      return p;
    }));

    // Complete animation
    setTimeout(() => {
      setWrapperPieces(prev => prev.map(p => 
        p.id === piece.id 
          ? { ...p, opacity: 1, isAnimating: false }
          : p
      ));
    }, 250);

    playPieceMove(wasCapture);
    console.log(`🔚 [DRAG] Ending drag, setting draggedPiece to null`);
    setStoreDraggedPiece(null);
    setStoreSelectedCell(null);
  }, [wrapperPieces, findPieceAt, chessToPx, playPieceMove, setStoreDraggedPiece, setStoreSelectedCell, addStoreCapturedPiece]);


  // Separate captured pieces by color
  const whiteCapturedPieces = capturedPieces.filter(p => p.color === 'white');
  const blackCapturedPieces = capturedPieces.filter(p => p.color === 'black');

  return {
    wrapperPieces,
    handleCellClick,
    handlePieceClick,
    handleReset,
    handleFlipBoard,
    handleDragStart,
    handleDrop,
    isFlipped,
    findPieceAt,
    isDragging: !!draggedPiece,
    setDraggedPiece: setStoreDraggedPiece, // Expose this so PieceWrapper can manage it directly
    capturedPieces,
    whiteCapturedPieces,
    blackCapturedPieces
  };
};