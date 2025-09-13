// coordinate.utils.ts - Board coordinate system utilities (SIMPLIFIED FOR STOCKFISH TEST)
import type { ChessPosition, PieceColor, File, Rank } from '../types';
import { fileToIndex, rankToIndex, indexToFile, indexToRank } from './chess.utils';

export interface BoardCoordinates {
  x: number;
  y: number;
}

export const squareToCoordinates = (
  square: ChessPosition,
  squareSize: number,
  orientation: PieceColor = 'white'
): BoardCoordinates => {
  if (square.length !== 2) {
    throw new Error(`Invalid square: ${square}`);
  }
  
  const file = square[0];
  const rank = parseInt(square[1]);
  
  const fileIndex = fileToIndex(file as File);
  const rankIndex = rankToIndex(rank as Rank);
  
  if (orientation === 'white') {
    return {
      x: fileIndex * squareSize,
      y: (7 - rankIndex) * squareSize
    };
  } else {
    return {
      x: (7 - fileIndex) * squareSize,
      y: rankIndex * squareSize
    };
  }
};

export const coordinatesToSquare = (
  x: number,
  y: number,
  squareSize: number,
  orientation: PieceColor = 'white'
): ChessPosition => {
  const fileIndex = Math.floor(x / squareSize);
  const rankIndex = Math.floor(y / squareSize);
  
  if (fileIndex < 0 || fileIndex > 7 || rankIndex < 0 || rankIndex > 7) {
    throw new Error(`Coordinates out of bounds: ${x}, ${y}`);
  }
  
  let file, rank;
  
  if (orientation === 'white') {
    file = indexToFile(fileIndex);
    rank = indexToRank(7 - rankIndex);
  } else {
    file = indexToFile(7 - fileIndex);
    rank = indexToRank(rankIndex);
  }
  
  return `${file}${rank}` as ChessPosition;
};

export const isValidSquare = (square: string): square is ChessPosition => {
  if (square.length !== 2) return false;
  const file = square[0];
  const rank = parseInt(square[1]);
  return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].includes(file) && rank >= 1 && rank <= 8;
};

export const getSquareDistance = (square1: ChessPosition, square2: ChessPosition): number => {
  if (!isValidSquare(square1) || !isValidSquare(square2)) {
    throw new Error('Invalid square format');
  }
  
  const file1Index = fileToIndex(square1[0] as File);
  const rank1Index = rankToIndex(parseInt(square1[1]) as Rank);
  const file2Index = fileToIndex(square2[0] as File);
  const rank2Index = rankToIndex(parseInt(square2[1]) as Rank);
  
  return Math.max(
    Math.abs(file1Index - file2Index),
    Math.abs(rank1Index - rank2Index)
  );
};

export const getAdjacentSquares = (square: ChessPosition): ChessPosition[] => {
  if (!isValidSquare(square)) {
    throw new Error('Invalid square format');
  }
  
  const adjacent: ChessPosition[] = [];
  const fileIndex = fileToIndex(square[0] as File);
  const rankIndex = rankToIndex(parseInt(square[1]) as Rank);
  
  for (let df = -1; df <= 1; df++) {
    for (let dr = -1; dr <= 1; dr++) {
      if (df === 0 && dr === 0) continue;
      
      const newFileIndex = fileIndex + df;
      const newRankIndex = rankIndex + dr;
      
      if (newFileIndex >= 0 && newFileIndex <= 7 && newRankIndex >= 0 && newRankIndex <= 7) {
        const newFile = indexToFile(newFileIndex);
        const newRank = indexToRank(newRankIndex);
        adjacent.push(`${newFile}${newRank}` as ChessPosition);
      }
    }
  }
  
  return adjacent;
};