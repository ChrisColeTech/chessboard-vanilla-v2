import React from 'react';

interface DraggedPieceProps {
  piece: string;
  position: { x: number; y: number };
  size: number;
}

export const DraggedPiece: React.FC<DraggedPieceProps> = ({ piece, position, size }) => {
  return (
    <div
      className="fixed pointer-events-none z-50 select-none"
      style={{
        left: position.x - size / 2,
        top: position.y - size / 2,
        width: size,
        height: size,
        fontSize: size * 0.8,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      {piece}
    </div>
  );
};
