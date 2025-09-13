// chess.constants.ts - Chess game constants
export const STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

export const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;
export const RANKS = [1, 2, 3, 4, 5, 6, 7, 8] as const;

export const PIECE_TYPES = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn'] as const;
export const PIECE_COLORS = ['white', 'black'] as const;

export const PIECE_UNICODE = {
  wK: '♔', wQ: '♕', wR: '♖', wB: '♗', wN: '♘', wP: '♙',
  bK: '♚', bQ: '♛', bR: '♜', bB: '♝', bN: '♞', bP: '♟'
} as const;

export const PIECE_NAMES = {
  king: 'King',
  queen: 'Queen', 
  rook: 'Rook',
  bishop: 'Bishop',
  knight: 'Knight',
  pawn: 'Pawn'
} as const;

export const DEFAULT_BOARD_SIZE = 600;
export const MIN_BOARD_SIZE = 200;
export const MAX_BOARD_SIZE = 800;

// Standard 8x8 chess starting position
export const INITIAL_CHESS_PIECES = {
  // White pieces (ranks 1-2)
  a1: { id: 'white-rook-a1', type: 'rook', color: 'white', position: { file: 'a', rank: 1 } },
  b1: { id: 'white-knight-b1', type: 'knight', color: 'white', position: { file: 'b', rank: 1 } },
  c1: { id: 'white-bishop-c1', type: 'bishop', color: 'white', position: { file: 'c', rank: 1 } },
  d1: { id: 'white-queen-d1', type: 'queen', color: 'white', position: { file: 'd', rank: 1 } },
  e1: { id: 'white-king-e1', type: 'king', color: 'white', position: { file: 'e', rank: 1 } },
  f1: { id: 'white-bishop-f1', type: 'bishop', color: 'white', position: { file: 'f', rank: 1 } },
  g1: { id: 'white-knight-g1', type: 'knight', color: 'white', position: { file: 'g', rank: 1 } },
  h1: { id: 'white-rook-h1', type: 'rook', color: 'white', position: { file: 'h', rank: 1 } },
  a2: { id: 'white-pawn-a2', type: 'pawn', color: 'white', position: { file: 'a', rank: 2 } },
  b2: { id: 'white-pawn-b2', type: 'pawn', color: 'white', position: { file: 'b', rank: 2 } },
  c2: { id: 'white-pawn-c2', type: 'pawn', color: 'white', position: { file: 'c', rank: 2 } },
  d2: { id: 'white-pawn-d2', type: 'pawn', color: 'white', position: { file: 'd', rank: 2 } },
  e2: { id: 'white-pawn-e2', type: 'pawn', color: 'white', position: { file: 'e', rank: 2 } },
  f2: { id: 'white-pawn-f2', type: 'pawn', color: 'white', position: { file: 'f', rank: 2 } },
  g2: { id: 'white-pawn-g2', type: 'pawn', color: 'white', position: { file: 'g', rank: 2 } },
  h2: { id: 'white-pawn-h2', type: 'pawn', color: 'white', position: { file: 'h', rank: 2 } },
  
  // Black pieces (ranks 7-8)
  a8: { id: 'black-rook-a8', type: 'rook', color: 'black', position: { file: 'a', rank: 8 } },
  b8: { id: 'black-knight-b8', type: 'knight', color: 'black', position: { file: 'b', rank: 8 } },
  c8: { id: 'black-bishop-c8', type: 'bishop', color: 'black', position: { file: 'c', rank: 8 } },
  d8: { id: 'black-queen-d8', type: 'queen', color: 'black', position: { file: 'd', rank: 8 } },
  e8: { id: 'black-king-e8', type: 'king', color: 'black', position: { file: 'e', rank: 8 } },
  f8: { id: 'black-bishop-f8', type: 'bishop', color: 'black', position: { file: 'f', rank: 8 } },
  g8: { id: 'black-knight-g8', type: 'knight', color: 'black', position: { file: 'g', rank: 8 } },
  h8: { id: 'black-rook-h8', type: 'rook', color: 'black', position: { file: 'h', rank: 8 } },
  a7: { id: 'black-pawn-a7', type: 'pawn', color: 'black', position: { file: 'a', rank: 7 } },
  b7: { id: 'black-pawn-b7', type: 'pawn', color: 'black', position: { file: 'b', rank: 7 } },
  c7: { id: 'black-pawn-c7', type: 'pawn', color: 'black', position: { file: 'c', rank: 7 } },
  d7: { id: 'black-pawn-d7', type: 'pawn', color: 'black', position: { file: 'd', rank: 7 } },
  e7: { id: 'black-pawn-e7', type: 'pawn', color: 'black', position: { file: 'e', rank: 7 } },
  f7: { id: 'black-pawn-f7', type: 'pawn', color: 'black', position: { file: 'f', rank: 7 } },
  g7: { id: 'black-pawn-g7', type: 'pawn', color: 'black', position: { file: 'g', rank: 7 } },
  h7: { id: 'black-pawn-h7', type: 'pawn', color: 'black', position: { file: 'h', rank: 7 } },
} as const;

// 8x8 squares arranged in grid (top to bottom, left to right)
export const CHESS_SQUARES = [
  'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
  'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
  'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
  'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
  'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
  'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
  'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
  'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
] as const;