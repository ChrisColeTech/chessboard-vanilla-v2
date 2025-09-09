import React from 'react';
import { generateChessGridCells } from '../../utils/grid-generator.utils';
import { useChessGameStore } from '../../stores/chessGameStore';

interface ChessOverlayProps {
  gridSize: number;
  isFlipped?: boolean;
}

export const ChessOverlay: React.FC<ChessOverlayProps> = ({ 
  gridSize, 
  isFlipped = false 
}) => {
  const numCells = gridSize * gridSize;
  
  // Subscribe to store state
  const selectedCell = useChessGameStore(state => state.selectedCell);
  const hoveredCell = useChessGameStore(state => state.hoveredCell);
  const draggedPiece = useChessGameStore(state => state.draggedPiece);
  const isCapturePossible = useChessGameStore(state => state.isCapturePossible);
  
  // Debug logging
  React.useEffect(() => {
    if (draggedPiece) {
      console.log('🔥 [OVERLAY] draggedPiece:', draggedPiece.color, draggedPiece.type);
    }
    if (hoveredCell) {
      console.log('🎯 [OVERLAY] hoveredCell:', hoveredCell);
      if (isCapturePossible(hoveredCell)) {
        console.log('🎯 [OVERLAY] capture possible on:', hoveredCell);
      }
    }
  }, [draggedPiece, hoveredCell, isCapturePossible]);
  
  // Use the existing grid generator in overlay mode
  const overlayCells = generateChessGridCells(numCells, undefined, undefined, {
    overlayMode: true,
    showCoordinates: false
  });

  // Simple capture detection using store helper
  const isCaptureHover = (cellId: string) => {
    return isCapturePossible(cellId);
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'grid',
        gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
        gridTemplateRows: `repeat(${gridSize}, 1fr)`,
        gap: '0px',
        pointerEvents: 'none', // Don't interfere with chess interactions
        zIndex: 1, // Above board, below pieces
        transform: isFlipped ? 'rotate(180deg)' : undefined,
      }}
    >
      {overlayCells.map((cell) => {
        const isSelected = selectedCell === cell.id;
        const isHovered = hoveredCell === cell.id && hoveredCell !== selectedCell;
        const isCapture = isCaptureHover(cell.id);
        
        const elementProps = cell.element.props as { className?: string; style?: React.CSSProperties };
        const selectedClass = isSelected ? 'selected' : '';
        const hoveredClass = isHovered ? 'hovered' : '';
        const captureClass = isCapture ? 'capture' : '';
        
        // Debug CSS classes for capture
        if (isCapture) {
          console.log('🎨 [OVERLAY] Applying capture class to cell:', cell.id, {
            baseClasses: elementProps.className,
            finalClasses: `${elementProps.className || ''} ${selectedClass} ${hoveredClass} ${captureClass}`.trim()
          });
        }
        
        return React.cloneElement(cell.element as React.ReactElement<{ 
          className?: string;
          style?: React.CSSProperties;
        }>, {
          key: cell.id,
          className: `${elementProps.className || ''} ${selectedClass} ${hoveredClass} ${captureClass}`.trim(),
          style: {
            ...elementProps.style,
            // Ensure overlay positioning
            position: 'relative',
            zIndex: isSelected || isHovered || isCapture ? 10 : 1,
          }
        });
      })}
    </div>
  );
};