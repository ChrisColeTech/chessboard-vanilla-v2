// ChessGameService.ts - Core chess game logic using chess.js v1.4.0
import { Chess } from 'chess.js';
import type { 
  ChessGameState, 
  ChessMove, 
  ChessMoveInput, 
  ChessMoveResult, 
  ChessPiece, 
  ChessPosition,
  PieceColor,
  PieceType 
} from '../../types';
import { squareToPosition } from '../../utils';

export class ChessGameService {
  private gameEngine: Chess;
  private moveHistory: ChessMove[] = [];

  constructor(initialFen?: string) {
    this.gameEngine = new Chess(initialFen);
  }

  public makeMove(moveInput: ChessMoveInput): ChessMoveResult {
    try {
      // Use chess.js v1.4.0 API
      const move = this.gameEngine.move({
        from: moveInput.from,
        to: moveInput.to,
        promotion: moveInput.promotion ? moveInput.promotion[0] : undefined
      }) as any;

      if (!move) {
        return {
          success: false,
          error: 'Invalid move',
          gameState: this.getCurrentState()
        };
      }

      // Convert chess.js move to our format
      const chessMove = this.convertMove(move);
      this.moveHistory.push(chessMove);

      return {
        success: true,
        move: chessMove,
        gameState: this.getCurrentState()
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        gameState: this.getCurrentState()
      };
    }
  }

  public getCurrentState(): ChessGameState {
    const board = this.gameEngine.board();
    const position = new Map<string, ChessPiece>();
    const boardRecord: Record<string, ChessPiece | null> = {};
    
    // Initialize all squares to null
    for (let rank = 1; rank <= 8; rank++) {
      for (let file = 0; file < 8; file++) {
        const square = `${String.fromCharCode('a'.charCodeAt(0) + file)}${rank}` as ChessPosition;
        boardRecord[square] = null;
      }
    }
    
    // Parse chess.js board() output
    board.forEach((row, rankIndex) => {
      row.forEach((piece, fileIndex) => {
        if (piece) {
          const file = String.fromCharCode('a'.charCodeAt(0) + fileIndex);
          const rank = 8 - rankIndex;
          const square = `${file}${rank}` as ChessPosition;
          const chessPosition = squareToPosition(square);
          
          const chessPiece: ChessPiece = {
            id: `${piece.color}${piece.type}${square}`,
            type: this.convertPieceType(piece.type),
            color: piece.color === 'w' ? 'white' : 'black',
            position: chessPosition
          };
          
          position.set(square, chessPiece);
          boardRecord[square] = chessPiece;
        }
      });
    });

    return {
      position,
      board: boardRecord,
      activeColor: this.gameEngine.turn() === 'w' ? 'white' : 'black',
      castlingRights: this.getCastlingRights(),
      enPassantTarget: this.getEnPassantTarget(),
      halfmoveClock: this.getHalfmoveClock(),
      fullmoveNumber: this.getFullmoveNumber(),
      isCheck: this.gameEngine.isCheck(),
      isCheckmate: this.gameEngine.isCheckmate(),
      isStalemate: this.gameEngine.isStalemate(),
      isDraw: this.gameEngine.isDraw(),
      isGameOver: this.gameEngine.isGameOver(),
      fen: this.gameEngine.fen(),
      history: [...this.moveHistory]
    };
  }

  public getValidMoves(square?: string): string[] {
    if (square) {
      // Cast to chess.js Square type - we know our squares are valid
      return this.gameEngine.moves({ square: square as any, verbose: false });
    }
    return this.gameEngine.moves({ verbose: false });
  }

  public getValidMovesVerbose(square?: string) {
    if (square) {
      return this.gameEngine.moves({ square: square as any, verbose: true });
    }
    return this.gameEngine.moves({ verbose: true });
  }

  public getValidTargetSquares(square: string): string[] {
    const verboseMoves = this.gameEngine.moves({ square: square as any, verbose: true }) as any[];
    return verboseMoves.map((move: any) => move.to);
  }

  public undoLastMove(): boolean {
    const undoMove = this.gameEngine.undo();
    if (undoMove) {
      this.moveHistory.pop();
      return true;
    }
    return false;
  }

  public resetGame(fen?: string): void {
    this.gameEngine = new Chess(fen);
    this.moveHistory = [];
  }

  public getFen(): string {
    return this.gameEngine.fen();
  }

  public getPgn(): string {
    return this.gameEngine.pgn();
  }

  public loadFen(fen: string): boolean {
    try {
      this.gameEngine.load(fen);
      this.moveHistory = [];
      return true;
    } catch {
      return false;
    }
  }

  private convertMove(move: any): ChessMove {
    const capturedPiece = move.captured ? {
      id: `${move.color === 'w' ? 'b' : 'w'}${move.captured}${move.to}`,
      type: this.convertPieceType(move.captured),
      color: (move.color === 'w' ? 'black' : 'white') as PieceColor,
      position: squareToPosition(move.to)
    } : undefined;
    
    return {
      from: move.from as ChessPosition,
      to: move.to as ChessPosition,
      piece: {
        id: `${move.color}${move.piece}${move.from}`,
        type: this.convertPieceType(move.piece),
        color: move.color === 'w' ? 'white' : 'black',
        position: squareToPosition(move.from)
      },
      capturedPiece,
      captured: capturedPiece,
      promotion: move.promotion ? this.convertPieceType(move.promotion) : undefined,
      isCheck: this.gameEngine.isCheck(),
      isCheckmate: this.gameEngine.isCheckmate(),
      notation: move.san,
      san: move.san,
      uci: `${move.from}${move.to}${move.promotion || ''}`
    };
  }

  private convertPieceType(piece: string): PieceType {
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

  private getHalfmoveClock(): number {
    const fen = this.gameEngine.fen();
    const parts = fen.split(' ');
    return parseInt(parts[4]) || 0;
  }

  private getFullmoveNumber(): number {
    const fen = this.gameEngine.fen();
    const parts = fen.split(' ');
    return parseInt(parts[5]) || 1;
  }

  private getCastlingRights() {
    // Parse castling rights from FEN
    const fen = this.gameEngine.fen();
    const castlingPart = fen.split(' ')[2];
    
    return {
      white: {
        kingSide: castlingPart.includes('K'),
        queenSide: castlingPart.includes('Q')
      },
      black: {
        kingSide: castlingPart.includes('k'),
        queenSide: castlingPart.includes('q')
      }
    };
  }

  private getEnPassantTarget(): ChessPosition | undefined {
    const fen = this.gameEngine.fen();
    const enPassantSquare = fen.split(' ')[3];
    
    if (enPassantSquare === '-') {
      return undefined;
    }
    
    return enPassantSquare as ChessPosition;
  }
}