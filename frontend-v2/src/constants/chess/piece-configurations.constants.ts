// Simple chess piece configuration system

export interface PieceConfig {
  id: string;
  color: 'white' | 'black';
  type: 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn';
  boardPosition: string;
}

// Simple piece configurations with relative positions
const PIECE_CONFIGS = {
  'drag-test': {
    'black-king': { color: 'black', type: 'king', file: 0, rank: 1 },
    'black-queen': { color: 'black', type: 'queen', file: 1, rank: 1 },
    'white-pawn1': { color: 'white', type: 'pawn', file: 0, rank: 0 },
    'white-pawn2': { color: 'white', type: 'pawn', file: 1, rank: 0 }
  },
  'mobile-test': {
    'black-king': { color: 'black', type: 'king', file: 0, rank: 1 },
    'black-queen': { color: 'black', type: 'queen', file: 0.33, rank: 1 },
    'white-queen': { color: 'white', type: 'queen', file: 0.67, rank: 0 },
    'white-king': { color: 'white', type: 'king', file: 1, rank: 0 }
  },
  'standard-chess': {
    // White pieces (rank 0 and 1/7 = 0.143)
    'white-rook1': { color: 'white', type: 'rook', file: 0, rank: 0 },
    'white-knight1': { color: 'white', type: 'knight', file: 1/7, rank: 0 },
    'white-bishop1': { color: 'white', type: 'bishop', file: 2/7, rank: 0 },
    'white-queen': { color: 'white', type: 'queen', file: 3/7, rank: 0 },
    'white-king': { color: 'white', type: 'king', file: 4/7, rank: 0 },
    'white-bishop2': { color: 'white', type: 'bishop', file: 5/7, rank: 0 },
    'white-knight2': { color: 'white', type: 'knight', file: 6/7, rank: 0 },
    'white-rook2': { color: 'white', type: 'rook', file: 1, rank: 0 },
    'white-pawn1': { color: 'white', type: 'pawn', file: 0, rank: 1/7 },
    'white-pawn2': { color: 'white', type: 'pawn', file: 1/7, rank: 1/7 },
    'white-pawn3': { color: 'white', type: 'pawn', file: 2/7, rank: 1/7 },
    'white-pawn4': { color: 'white', type: 'pawn', file: 3/7, rank: 1/7 },
    'white-pawn5': { color: 'white', type: 'pawn', file: 4/7, rank: 1/7 },
    'white-pawn6': { color: 'white', type: 'pawn', file: 5/7, rank: 1/7 },
    'white-pawn7': { color: 'white', type: 'pawn', file: 6/7, rank: 1/7 },
    'white-pawn8': { color: 'white', type: 'pawn', file: 1, rank: 1/7 },
    
    // Black pieces (rank 6/7 = 0.857 and 1)
    'black-pawn1': { color: 'black', type: 'pawn', file: 0, rank: 6/7 },
    'black-pawn2': { color: 'black', type: 'pawn', file: 1/7, rank: 6/7 },
    'black-pawn3': { color: 'black', type: 'pawn', file: 2/7, rank: 6/7 },
    'black-pawn4': { color: 'black', type: 'pawn', file: 3/7, rank: 6/7 },
    'black-pawn5': { color: 'black', type: 'pawn', file: 4/7, rank: 6/7 },
    'black-pawn6': { color: 'black', type: 'pawn', file: 5/7, rank: 6/7 },
    'black-pawn7': { color: 'black', type: 'pawn', file: 6/7, rank: 6/7 },
    'black-pawn8': { color: 'black', type: 'pawn', file: 1, rank: 6/7 },
    'black-rook1': { color: 'black', type: 'rook', file: 0, rank: 1 },
    'black-knight1': { color: 'black', type: 'knight', file: 1/7, rank: 1 },
    'black-bishop1': { color: 'black', type: 'bishop', file: 2/7, rank: 1 },
    'black-queen': { color: 'black', type: 'queen', file: 3/7, rank: 1 },
    'black-king': { color: 'black', type: 'king', file: 4/7, rank: 1 },
    'black-bishop2': { color: 'black', type: 'bishop', file: 5/7, rank: 1 },
    'black-knight2': { color: 'black', type: 'knight', file: 6/7, rank: 1 },
    'black-rook2': { color: 'black', type: 'rook', file: 1, rank: 1 }
  }
} as const;

// Generate piece configuration for any grid size
export function generatePieceConfiguration(
  configKey: keyof typeof PIECE_CONFIGS,
  gridSize: number
): PieceConfig[] {
  const config = PIECE_CONFIGS[configKey];
  
  return Object.entries(config).map(([id, piece]) => {
    const fileIndex = Math.round(piece.file * (gridSize - 1));
    const rankIndex = Math.round(piece.rank * (gridSize - 1));
    
    const file = String.fromCharCode('a'.charCodeAt(0) + fileIndex);
    const rank = (rankIndex + 1).toString();
    
    return {
      id,
      color: piece.color as 'white' | 'black',
      type: piece.type as any,
      boardPosition: `${file}${rank}`
    };
  });
}

// Static configurations for backward compatibility and puzzle support
export const PIECE_CONFIGURATIONS = {
  'drag-test': generatePieceConfiguration('drag-test', 3),
  'mobile-test': generatePieceConfiguration('mobile-test', 4),
  'standard-chess': generatePieceConfiguration('standard-chess', 8),
  'puzzle': [] as PieceConfig[] // Dynamic puzzle configuration, updated at runtime
} as const;