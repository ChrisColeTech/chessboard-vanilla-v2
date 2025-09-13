import { create } from 'zustand';
import type { ChessPiece } from '../types';
import type { WrapperPiece } from '../types/chess/wrapper-piece.types';

interface ChessGameState {
  // Piece data
  pieces: WrapperPiece[];
  squareMap: Record<string, { color: string; type: string } | null>;
  capturedPieces: ChessPiece[];
  
  // Game state
  selectedCell: string | null;
  hoveredCell: string | null;
  isFlipped: boolean;
  
  // Drag state
  draggedPiece: WrapperPiece | null;
  isDragging: boolean;
  
  // Actions
  setPieces: (pieces: WrapperPiece[]) => void;
  setSelectedCell: (cell: string | null) => void;
  setHoveredCell: (cell: string | null) => void;
  setDraggedPiece: (piece: WrapperPiece | null) => void;
  setCapturedPieces: (pieces: ChessPiece[]) => void;
  addCapturedPiece: (piece: ChessPiece) => void;
  flipBoard: () => void;
  
  // Helper methods
  isCapturePossible: (cellId: string) => boolean;
  getPieceAt: (position: string) => { color: string; type: string } | null;
}

export const useChessGameStore = create<ChessGameState>((set, get) => ({
  // Initial state
  pieces: [],
  squareMap: {},
  capturedPieces: [],
  selectedCell: null,
  hoveredCell: null,
  isFlipped: false,
  draggedPiece: null,
  isDragging: false,
  
  // Actions
  setPieces: (pieces) => {
    // Update pieces and rebuild squareMap
    const squareMap: Record<string, { color: string; type: string } | null> = {};
    pieces.forEach(piece => {
      squareMap[piece.boardPosition] = { color: piece.color, type: piece.type };
    });
    
    set({ pieces, squareMap });
  },
  
  setSelectedCell: (cell) => set({ selectedCell: cell }),
  
  setHoveredCell: (cell) => set({ hoveredCell: cell }),
  
  setDraggedPiece: (piece) => set({ 
    draggedPiece: piece, 
    isDragging: !!piece 
  }),
  
  setCapturedPieces: (pieces) => set({ capturedPieces: pieces }),
  
  addCapturedPiece: (piece) => set((state) => ({ 
    capturedPieces: [...state.capturedPieces, piece] 
  })),
  
  flipBoard: () => set((state) => ({ isFlipped: !state.isFlipped })),
  
  // Helper methods (non-reactive)
  isCapturePossible: (cellId: string) => {
    const state = get();
    if (!state.draggedPiece || !state.hoveredCell || cellId !== state.hoveredCell) {
      return false;
    }
    
    const pieceOnSquare = state.squareMap[cellId];
    return !!(pieceOnSquare && pieceOnSquare.color !== state.draggedPiece.color);
  },
  
  getPieceAt: (position) => {
    return get().squareMap[position] || null;
  },
}));