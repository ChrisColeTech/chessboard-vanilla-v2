// FenService.ts - FEN parsing and validation
import { Chess } from 'chess.js';
import type { ChessGameState, ChessPiece, PieceType } from '../../types';
import { squareToPosition } from '../../utils';

export class FenService {
  public static validateFen(fen: string): boolean {
    try {
      const chess = new Chess();
      chess.load(fen);
      return true;
    } catch {
      return false;
    }
  }

  public static parseFenToPieces(fen: string): Map<string, ChessPiece> {
    if (!this.validateFen(fen)) {
      throw new Error('Invalid FEN string');
    }

    const chess = new Chess(fen);
    const board = chess.board();
    const position = new Map<string, ChessPiece>();

    board.forEach((row, rankIndex) => {
      row.forEach((piece, fileIndex) => {
        if (piece) {
          const file = String.fromCharCode('a'.charCodeAt(0) + fileIndex);
          const rank = 8 - rankIndex;
          const square = `${file}${rank}`;
          const chessPosition = squareToPosition(square);
          
          const chessPiece: ChessPiece = {
            id: `${piece.color}${piece.type}${square}`,
            type: this.convertPieceType(piece.type),
            color: piece.color === 'w' ? 'white' : 'black',
            position: chessPosition
          };
          
          position.set(square, chessPiece);
        }
      });
    });

    return position;
  }

  public static generateFen(gameState: ChessGameState): string {
    // In practice, we rely on chess.js for FEN generation
    // This is a placeholder for the interface
    return gameState.fen;
  }

  public static getFenInfo(fen: string) {
    const parts = fen.split(' ');
    
    if (parts.length !== 6) {
      throw new Error('Invalid FEN format');
    }

    return {
      piecePlacement: parts[0],
      activeColor: parts[1] === 'w' ? 'white' as const : 'black' as const,
      castlingRights: parts[2],
      enPassantTarget: parts[3] === '-' ? null : parts[3],
      halfmoveClock: parseInt(parts[4]),
      fullmoveNumber: parseInt(parts[5])
    };
  }

  private static convertPieceType(piece: string): PieceType {
    const typeMap: Record<string, PieceType> = {
      'k': 'king',
      'q': 'queen',
      'r': 'rook',
      'b': 'bishop',
      'n': 'knight',
      'p': 'pawn'
    };
    return typeMap[piece.toLowerCase()] as PieceType || 'pawn';
  }

  public static isStartingPosition(fen: string): boolean {
    const startingFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
    return fen === startingFen;
  }

  public static getGamePhase(fen: string): 'opening' | 'middlegame' | 'endgame' {
    const pieces = this.parseFenToPieces(fen);
    let materialCount = 0;

    pieces.forEach(piece => {
      switch (piece.type) {
        case 'queen': materialCount += 9; break;
        case 'rook': materialCount += 5; break;
        case 'bishop': case 'knight': materialCount += 3; break;
        case 'pawn': materialCount += 1; break;
      }
    });

    if (materialCount > 60) return 'opening';
    if (materialCount > 20) return 'middlegame';
    return 'endgame';
  }
}