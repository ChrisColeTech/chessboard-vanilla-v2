// DraggedPiece.tsx - Cursor-following piece component using fixed positioning
import React from 'react';
import type { ChessPiece } from '../../types';
import { getPieceImagePath, DEFAULT_PIECE_SET } from '../../constants/pieces.constants';

interface DraggedPieceProps {
  piece: ChessPiece;
  position: { x: number; y: number };
  size?: number;
  pieceSet?: string;
}

export const DraggedPiece: React.FC<DraggedPieceProps> = ({ 
  piece, 
  position, 
  size = 60, 
  pieceSet = DEFAULT_PIECE_SET 
}) => {
  if (!piece || position.x === 0 || position.y === 0) {
    return null;
  }

  return (
    <div
      style={{
        position: 'fixed',
        top: position.y - size / 2,
        left: position.x - size / 2,
        width: size,
        height: size,
        zIndex: 1000,
        pointerEvents: 'none', // Don't interfere with drop detection
        transition: 'none' // No animations during drag
      }}
    >
      <img
        src={getPieceImagePath(piece.color, piece.type, pieceSet as any)}
        alt={`${piece.color} ${piece.type}`}
        style={{
          width: '100%',
          height: '100%',
          opacity: 1, // Fully opaque dragged piece
          userSelect: 'none'
        }}
        draggable={false}
      />
    </div>
  );
};