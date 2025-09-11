import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';

interface DragContextType {
  draggedPiece: string | null;
  cursorPosition: { x: number; y: number };
  draggedPieceSize: number;
  startDrag: (piece: string, position: { x: number; y: number }, size?: number) => void;
  endDrag: () => void;
  updateCursor: (position: { x: number; y: number }) => void;
}

const DragContext = createContext<DragContextType | undefined>(undefined);

export const useDrag = () => {
  const context = useContext(DragContext);
  if (!context) {
    throw new Error('useDrag must be used within a DragProvider');
  }
  return context;
};

interface DragProviderProps {
  children: ReactNode;
}

export const DragProvider: React.FC<DragProviderProps> = ({ children }) => {
  const [draggedPiece, setDraggedPiece] = useState<string | null>(null);
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  const [draggedPieceSize, setDraggedPieceSize] = useState(40);

  const startDrag = (piece: string, position: { x: number; y: number }, size = 40) => {
    setDraggedPiece(piece);
    setCursorPosition(position);
    setDraggedPieceSize(size);
  };

  const endDrag = () => {
    setDraggedPiece(null);
  };

  const updateCursor = (position: { x: number; y: number }) => {
    setCursorPosition(position);
  };

  return (
    <DragContext.Provider value={{
      draggedPiece,
      cursorPosition,
      draggedPieceSize,
      startDrag,
      endDrag,
      updateCursor
    }}>
      {children}
    </DragContext.Provider>
  );
};
