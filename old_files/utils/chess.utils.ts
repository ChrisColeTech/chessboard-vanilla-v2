// chess.utils.ts - Core chess utilities
import type { ChessPosition, ChessPositionObject, File, Rank, PieceColor } from '../types/chess/chess.types';

export const fileToIndex = (file: File): number => {
  return file.charCodeAt(0) - 'a'.charCodeAt(0);
};

export const rankToIndex = (rank: Rank): number => {
  return rank - 1;
};

export const indexToFile = (index: number): File => {
  if (index < 0 || index > 7) {
    throw new Error(`Invalid file index: ${index}`);
  }
  return String.fromCharCode('a'.charCodeAt(0) + index) as File;
};

export const indexToRank = (index: number): Rank => {
  if (index < 0 || index > 7) {
    throw new Error(`Invalid rank index: ${index}`);
  }
  return (index + 1) as Rank;
};

export const positionToSquare = (position: ChessPositionObject): string => {
  return `${position.file}${position.rank}`;
};

export const squareToPosition = (square: string): ChessPositionObject => {
  if (square.length !== 2) {
    throw new Error(`Invalid square format: ${square}`);
  }
  
  const file = square[0] as File;
  const rank = parseInt(square[1]) as Rank;
  
  if (!isValidFile(file) || !isValidRank(rank)) {
    throw new Error(`Invalid square: ${square}`);
  }
  
  return { file, rank };
};

// Utility function to extract file and rank from ChessPosition (string)
export const positionToFileRank = (position: ChessPosition): { file: File; rank: Rank } => {
  if (position.length !== 2) {
    throw new Error(`Invalid position format: ${position}`);
  }
  
  const file = position[0] as File;
  const rank = parseInt(position[1]) as Rank;
  
  if (!isValidFile(file) || !isValidRank(rank)) {
    throw new Error(`Invalid position: ${position}`);
  }
  
  return { file, rank };
};

export const isValidPosition = (position: ChessPositionObject | ChessPosition): boolean => {
  if (typeof position === 'string') {
    if (position.length !== 2) return false;
    const file = position[0];
    const rank = parseInt(position[1]);
    return isValidFile(file) && isValidRank(rank);
  } else {
    return isValidFile(position.file) && isValidRank(position.rank);
  }
};

export const getSquareColor = (position: ChessPositionObject | ChessPosition): 'light' | 'dark' => {
  let file: File, rank: Rank;
  
  if (typeof position === 'string') {
    const fileRank = positionToFileRank(position);
    file = fileRank.file;
    rank = fileRank.rank;
  } else {
    file = position.file;
    rank = position.rank;
  }
  
  const fileIndex = fileToIndex(file);
  const rankIndex = rankToIndex(rank);
  return (fileIndex + rankIndex) % 2 === 0 ? 'dark' : 'light';
};

export const isValidFile = (file: string): file is File => {
  return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].includes(file);
};

export const isValidRank = (rank: number): rank is Rank => {
  return rank >= 1 && rank <= 8;
};


export const generateSquareList = (orientation: PieceColor = 'white') => {
  const squares = [];
  const ranks = orientation === 'white' ? [8, 7, 6, 5, 4, 3, 2, 1] : [1, 2, 3, 4, 5, 6, 7, 8];
  const files: File[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  
  for (const rank of ranks) {
    for (const file of files) {
      squares.push({
        file,
        rank: rank as Rank,
        square: `${file}${rank}` as ChessPosition,
        position: { file, rank: rank as Rank }
      });
    }
  }
  
  return squares;
};