// Wrapper-based animation system for MobileChessBoard
import React from "react";
import { useWrapperChessBoard } from "../../hooks/chess/useWrapperChessBoard";
import { useChessGameStore } from "../../stores/chessGameStore";
import { useChessSettings } from "../../stores/appStore";
import { ChessGrid } from "./ChessGrid";
import { ChessOverlay } from "./ChessOverlay";
import { PieceWrapper } from "./PieceWrapper";
import type { MobileChessGameState } from "../../types";

interface MobileChessBoardProps {
  gridSize?: number;
  pieceConfig?: 'drag-test' | 'mobile-test' | 'standard-chess' | 'puzzle';
  onGameStateChange?: (gameState: MobileChessGameState) => void;
}

// Helper function to get size multiplier based on setting
const getPieceSizeMultiplier = (size: 'small' | 'medium' | 'large'): number => {
  switch (size) {
    case 'small': return 0.55;   // Reduced by 15% (from 0.65)
    case 'medium': return 0.63;  // Reduced by 30% (from 0.9)
    case 'large': return 0.81;   // Reduced by 30% (from 1.15)
    default: return 0.63;
  }
};

export const MobileChessBoard: React.FC<MobileChessBoardProps> = ({ gridSize = 8, pieceConfig, onGameStateChange: _onGameStateChange }) => {
  // Get piece size setting from store
  const { pieceSize } = useChessSettings();
  
  // Centralized responsive piece sizing based on grid size and user setting
  const GRID_SIZE = gridSize;
  const sizeMultiplier = getPieceSizeMultiplier(pieceSize);
  const PIECE_SIZE = `min(${100 / GRID_SIZE * sizeMultiplier}vw, ${100 / GRID_SIZE * sizeMultiplier}vh)`;
  
  // Use hook for chess board state
  const { wrapperPieces, handleCellClick, handlePieceClick, handleDragStart, handleDrop, isFlipped, isDragging, setDraggedPiece } = useWrapperChessBoard(GRID_SIZE, pieceConfig);
  
  // Get store state directly
  const setHoveredCell = useChessGameStore(state => state.setHoveredCell);
  
  // Debug dragging state
  React.useEffect(() => {
    console.log('📱 [MOBILE] isDragging changed to:', isDragging);
  }, [isDragging]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        aspectRatio: "1",
        position: "relative",
      }}
    >
      {/* Chess Grid */}
      <ChessGrid 
        gridSize={GRID_SIZE}
        selectedCell={useChessGameStore(state => state.selectedCell)}
        onCellClick={handleCellClick}
        onCellDrop={handleDrop}
        onHoverChange={setHoveredCell}
        isFlipped={isFlipped}
        isDragging={isDragging}
      />

      {/* Chess Overlay - Glassmorphism effects */}
      <ChessOverlay
        gridSize={GRID_SIZE}
        isFlipped={isFlipped}
      />

      {/* Piece Pool - All pieces in wrappers with CSS transforms */}
      <div className="piece-pool" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 2 }}>
        {wrapperPieces.map(piece => (
          <PieceWrapper
            key={piece.id}
            piece={piece}
            size={PIECE_SIZE}
            gridSize={GRID_SIZE}
            onDragStart={handleDragStart}
            onPieceClick={handlePieceClick}
            onDrop={handleDrop}
            setDraggedPiece={setDraggedPiece}
          />
        ))}
      </div>
    </div>
  );
};