// pieces.constants.ts - Piece set definitions
export const PIECE_SETS = {
  classic: 'classic',
  modern: 'modern',
  tournament: 'tournament',
  executive: 'executive',
  conqueror: 'conqueror'
} as const;

export const PIECE_SET_NAMES = {
  classic: 'Classic',
  modern: 'Modern',
  tournament: 'Tournament',
  executive: 'Executive',
  conqueror: 'Conqueror'
} as const;

export const DEFAULT_PIECE_SET = 'classic' as const;

// SVG piece file naming convention
export const getPieceFileName = (
  color: 'white' | 'black',
  type: 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn',
  pieceSet: keyof typeof PIECE_SETS = DEFAULT_PIECE_SET,
  position?: string
): string => {
  const colorPrefix = color === 'white' ? 'w' : 'b';
  const typeMap = {
    king: 'K',
    queen: 'Q',
    rook: 'R',
    bishop: 'B',
    knight: 'N',
    pawn: 'P'
  };
  
  const typeCode = typeMap[type];
  
  // Handle knight orientation for sets with -left/-right versions
  if (type === 'knight' && pieceSet !== 'classic' && position) {
    const file = position[0]; // Extract file (a-h)
    // Queenside knights (a-file, b-file) face left, Kingside knights (g-file, h-file) face right
    const orientation = (file === 'a' || file === 'b') ? 'left' : 'right';
    return `${colorPrefix}${typeCode}-${orientation}.svg`;
  }
  
  return `${colorPrefix}${typeCode}.svg`;
};

export const getPieceImagePath = (
  color: 'white' | 'black',
  type: 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn',
  pieceSet: keyof typeof PIECE_SETS = DEFAULT_PIECE_SET,
  position?: string
): string => {
  const fileName = getPieceFileName(color, type, pieceSet, position);
  return `/pieces/${pieceSet}/${fileName}`;
};

// Piece values for evaluation (in centipawns)
export const PIECE_VALUES = {
  pawn: 100,
  knight: 300,
  bishop: 300,
  rook: 500,
  queen: 900,
  king: 0 // King is invaluable
} as const;

// Material balance thresholds for game phase detection
export const GAME_PHASE_THRESHOLDS = {
  OPENING_MATERIAL: 6000, // Above this is opening
  ENDGAME_MATERIAL: 1500  // Below this is endgame
} as const;