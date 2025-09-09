import React from 'react';
import { getPieceImagePath } from '../../constants/pieces.constants';
import { useAppStore } from '../../stores/appStore';
import { useChessGameStore } from '../../stores/chessGameStore';
import type { WrapperPiece } from '../../types/chess/wrapper-piece.types';

interface PieceWrapperProps {
  piece: WrapperPiece;
  size: string; // CSS size value like "min(12vw, 12vh)"
  gridSize?: number; // Grid size for coordinate conversion
  onDragStart?: (piece: WrapperPiece) => void;
  onPieceClick?: (piece: WrapperPiece) => void;
  onDrop?: (targetSquare: string, dragData: { pieceId: string; fromPosition: string }) => void;
  setDraggedPiece?: (piece: WrapperPiece | null) => void;
}

export const PieceWrapper: React.FC<PieceWrapperProps> = ({ piece, size, gridSize = 6, onDragStart, onPieceClick, onDrop, setDraggedPiece }) => {
  const selectedPieceSet = useAppStore((state) => state.selectedPieceSet);
  const [isDragging, setIsDragging] = React.useState(false);
  
  // Check if ANY piece is being dragged (from store)
  const isAnyPieceDragging = useChessGameStore(state => state.isDragging);
  const [dragPosition, setDragPosition] = React.useState({ x: piece.x, y: piece.y });
  const [hasDragged, setHasDragged] = React.useState(false);
  const dragStartTimeRef = React.useRef<number>(0);

  // Sync drag position when piece position changes (from animations)
  React.useEffect(() => {
    if (!isDragging) {
      setDragPosition({ x: piece.x, y: piece.y });
    }
  }, [piece.x, piece.y, isDragging]);

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    dragStartTimeRef.current = Date.now();
    setHasDragged(false);
    
    const startX = e.clientX;
    const startY = e.clientY;
    let actuallyDragging = false;
    
    let lastMoveTime = 0;
    const handleMouseMove = (e: MouseEvent) => {
      // Throttle mouse move events to ~60fps
      const now = Date.now();
      if (now - lastMoveTime < 16) return;
      lastMoveTime = now;
      
      // Only start dragging after moving more than 5 pixels
      const deltaX = Math.abs(e.clientX - startX);
      const deltaY = Math.abs(e.clientY - startY);
      
      if (!actuallyDragging && (deltaX > 5 || deltaY > 5)) {
        actuallyDragging = true;
        setIsDragging(true);
        setHasDragged(true);
        setDraggedPiece?.(piece); // Set the global drag state
        onDragStart?.(piece);
        console.log('🔥 [PIECE] Actually started dragging, actuallyDragging =', actuallyDragging);
      }
      
      if (actuallyDragging) {
        console.log('🖱️ [PIECE] Mouse move during drag');
        // Get container for coordinate conversion
        const container = document.querySelector('.piece-pool')?.parentElement as HTMLElement;
        if (!container) return;
        
        const rect = container.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        
        setDragPosition({ x, y });
      }
    };
    
    const handleMouseUp = (e: MouseEvent) => {
      console.log('🔚 [PIECE] Mouse up, actuallyDragging =', actuallyDragging);
      setIsDragging(false);
      setDragPosition({ x: piece.x, y: piece.y }); // Reset position
      
      // Only handle drop if we actually dragged
      if (actuallyDragging) {
        // Find target square using the chess grid conversion
        const container = document.querySelector('.piece-pool')?.parentElement as HTMLElement;
        if (container && onDrop) {
          const rect = container.getBoundingClientRect();
          // Convert mouse position to percentage
          const x = ((e.clientX - rect.left) / rect.width) * 100;
          const y = ((e.clientY - rect.top) / rect.height) * 100;
          
          // Calculate grid position using the passed gridSize
          let col = Math.floor((x / 100) * gridSize);
          let row = Math.floor((y / 100) * gridSize);
          
          // Bounds check
          if (col >= 0 && col < gridSize && row >= 0 && row < gridSize) {
            // Convert to chess notation with dynamic file generation
            const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
            const file = files[col];
            const rank = gridSize - row;
            const targetSquare = `${file}${rank}`;
            
            // Call drop handler directly
            const dropData = {
              pieceId: piece.id,
              fromPosition: piece.boardPosition
            };
            
            onDrop(targetSquare, dropData);
          }
        }
      }
      
      // Clear the global drag state when mouse is released
      setDraggedPiece?.(null);
      
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleClick = (_e: React.MouseEvent) => {
    // Only trigger click if we didn't drag and it was a quick click
    const clickDuration = Date.now() - dragStartTimeRef.current;
    if (!hasDragged && clickDuration < 300) {
      onPieceClick?.(piece);
    }
  };

  return (
    <div
      className="piece-wrapper"
      style={{
        position: 'absolute',
        left: `${dragPosition.x}%`,
        top: `${dragPosition.y}%`,
        transform: `translate(-50%, -50%) scale(${piece.scale})`,
        width: size,
        height: size,
        opacity: isDragging ? 0.8 : piece.opacity,
        transition: piece.isAnimating && !isDragging ? 'all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.18s ease-out' : 'none',
        zIndex: isDragging ? 20 : 10,
        pointerEvents: isAnyPieceDragging ? 'none' : 'auto',
        userSelect: 'none',
        cursor: isDragging ? 'grabbing' : 'grab',
      }}
      onMouseDown={handleMouseDown}
      onClick={handleClick}
    >
      <img
        className={`chess-piece ${piece.color === "white" ? "chess-piece-white chess-piece-white-shadow" : "chess-piece-black chess-piece-black-shadow"}`}
        src={getPieceImagePath(
          piece.color as 'white' | 'black',
          piece.type as 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn',
          selectedPieceSet,
          piece.boardPosition
        )}
        alt={`${piece.color} ${piece.type}`}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
          pointerEvents: isAnyPieceDragging ? 'none' : 'auto',
        }}
      />
    </div>
  );
};