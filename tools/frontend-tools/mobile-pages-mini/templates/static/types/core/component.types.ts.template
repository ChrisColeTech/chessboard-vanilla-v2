// component.types.ts - React component prop types
import type { ChessGameState, ChessPiece, ChessPosition, ChessMove, PieceColor, GameResult } from '../chess/chess.types';

export interface ChessboardProps {
  pieceSet?: 'classic' | 'modern' | 'tournament' | 'executive' | 'conqueror';
  showCoordinates?: boolean;
  allowDragAndDrop?: boolean;
  orientation?: PieceColor;
  onMove?: (move: ChessMove) => void;
  onGameEnd?: (result: GameResult) => void;
  maxWidth?: number;
  className?: string;
  style?: React.CSSProperties;
}

export interface BoardProps {
  gameState: ChessGameState | null;
  orientation: PieceColor;
  pieceSet: string;
  showCoordinates: boolean;
  validDropTargets: readonly ChessPosition[];
  onSquareClick?: (position: ChessPosition) => void;
  onDragStart?: (piece: ChessPiece, position: ChessPosition) => void;
  onDragEnd?: () => void;
  onDrop?: (targetPosition: ChessPosition) => Promise<boolean>;
}

export interface SquareProps {
  position: ChessPosition;
  piece?: ChessPiece;
  isValidDropTarget: boolean;
  showCoordinates: boolean;
  pieceSet: string;
  onClick?: (position: ChessPosition) => void;
  onDragStart?: (piece: ChessPiece, position: ChessPosition) => void;
  onDragEnd?: () => void;
  onDrop?: (position: ChessPosition) => Promise<boolean>;
}

export interface PieceProps {
  piece: ChessPiece;
  pieceSet: string;
  onDragStart?: (piece: ChessPiece, position: ChessPosition) => void;
  onDragEnd?: () => void;
}

export interface DraggedPieceProps {
  piece: ChessPiece;
  pieceSet: string;
}

export interface PlayChessboardProps {
  playerColor?: PieceColor;
  showCoordinates?: boolean;
  highlightLastMove?: boolean;
  showValidMoves?: boolean;
  disabled?: boolean;
  className?: string;
}

