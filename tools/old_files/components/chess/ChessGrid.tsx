import React from 'react';
import { useChessGrid } from '../../hooks/chess/useChessGrid';
import type { GridCell } from "../../utils/grid-generator.utils";

interface ChessGridProps {
  gridSize: number;
  selectedCell: string | null;
  onCellClick: (cellId: string) => void;
  onCellDrop?: (cellId: string, dragData: { pieceId: string; fromPosition: string }) => void;
  onHoverChange?: (cellId: string | null) => void;
  isFlipped?: boolean;
  isDragging?: boolean;
}

export const ChessGrid: React.FC<ChessGridProps> = ({ 
  gridSize, 
  selectedCell, 
  onCellClick,
  onCellDrop,
  onHoverChange,
  isFlipped = false,
  isDragging = false
}) => {
  const { gridCells } = useChessGrid(gridSize);

  // Clear hover state when dragging stops
  React.useEffect(() => {
    if (!isDragging && onHoverChange) {
      onHoverChange(null);
    }
  }, [isDragging, onHoverChange]);

  const getCellStyle = (_cell: GridCell, _isSelected: boolean, _isHovered: boolean) => {
    return {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      cursor: "pointer",
      fontSize: "24px",
      fontWeight: "bold",
    };
  };

  const handleDrop = (cellId: string) => (e: React.DragEvent) => {
    e.preventDefault();
    
    try {
      const dragData = JSON.parse(e.dataTransfer.getData('application/json'));
      onCellDrop?.(cellId, dragData);
    } catch (error) {
      console.warn('Failed to parse drag data:', error);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault(); // Allow drop
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "grid",
        gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
        gridTemplateRows: `repeat(${gridSize}, 1fr)`,
        gap: "0px",
        transform: isFlipped ? "rotate(180deg)" : undefined,
      }}
    >
      {gridCells.map((cell) => {
        const elementProps = cell.element.props as { style?: React.CSSProperties; className?: string };
        const isSelected = selectedCell === cell.id;
        
        return React.cloneElement(cell.element as React.ReactElement<{ 
          onClick?: () => void; 
          onDrop?: (e: React.DragEvent) => void;
          onDragOver?: (e: React.DragEvent) => void;
          onMouseEnter?: () => void;
          onMouseLeave?: () => void;
          style?: React.CSSProperties;
          className?: string;
        }>, {
          key: cell.id,
          onClick: () => onCellClick(cell.id),
          onDrop: handleDrop(cell.id),
          onDragOver: handleDragOver,
          onMouseEnter: () => {
            console.log('🎯 Mouse enter cell:', cell.id, 'isDragging:', isDragging);
            if (isDragging && onHoverChange) {
              console.log('✅ Setting hovered cell:', cell.id);
              onHoverChange(cell.id);
            }
          },
          onMouseLeave: () => {
            console.log('👋 Mouse leave cell:', cell.id, 'isDragging:', isDragging);
            if (isDragging && onHoverChange) {
              console.log('❌ Clearing hovered cell');
              onHoverChange(null);
            }
          },
          className: `${elementProps.className || ''} chess-square`.trim(),
          style: {
            ...elementProps.style,
            ...getCellStyle(cell, isSelected, false),
          },
        });
      })}
    </div>
  );
};