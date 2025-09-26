// chess.types.ts - Core chess domain types
export type PieceColor = 'white' | 'black';
export type PieceType = 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn';
export type File = 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h';
export type Rank = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;

// ChessPosition as string type for compatibility with string methods
export type ChessPosition = string;

// Helper interface for position object form when needed
export interface ChessPositionObject {
  readonly file: File;
  readonly rank: Rank;
}

export interface ChessPiece {
  readonly id: string;
  readonly type: PieceType;
  readonly color: PieceColor;
  readonly position: ChessPositionObject;
}

export interface ChessMove {
  readonly from: ChessPosition;
  readonly to: ChessPosition;
  readonly piece: ChessPiece;
  readonly capturedPiece?: ChessPiece;
  readonly captured?: ChessPiece; // Alternative property name for compatibility
  readonly promotion?: PieceType;
  readonly isCheck: boolean;
  readonly isCheckmate: boolean;
  readonly notation: string;
  readonly san: string;
  readonly uci: string;
}

export interface CastlingRights {
  readonly white: {
    readonly kingSide: boolean;
    readonly queenSide: boolean;
  };
  readonly black: {
    readonly kingSide: boolean;
    readonly queenSide: boolean;
  };
}

export interface ChessGameState {
  readonly position: Map<string, ChessPiece>;
  readonly board: Record<string, ChessPiece | null>; // Board representation for position lookup
  readonly activeColor: PieceColor;
  readonly castlingRights: CastlingRights;
  readonly enPassantTarget?: ChessPosition;
  readonly halfmoveClock: number;
  readonly fullmoveNumber: number;
  readonly isCheck: boolean;
  readonly isCheckmate: boolean;
  readonly isStalemate: boolean;
  readonly isDraw: boolean;
  readonly isGameOver: boolean;
  readonly fen: string;
  readonly history: readonly ChessMove[];
  readonly lastMove?: { from: string; to: string };
}

// Service interfaces
export interface ChessMoveInput {
  readonly from: string;
  readonly to: string;
  readonly promotion?: PieceType;
}

export interface ChessMoveResult {
  readonly success: boolean;
  readonly move?: ChessMove;
  readonly gameState: ChessGameState;
  readonly error?: string;
}

export interface GameResult {
  readonly winner?: PieceColor;
  readonly reason: 'checkmate' | 'stalemate' | 'draw' | 'resignation' | 'timeout';
  readonly moves: readonly ChessMove[];
  readonly pgn: string;
}