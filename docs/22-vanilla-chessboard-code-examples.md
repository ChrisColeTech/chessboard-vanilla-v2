# Vanilla Chessboard Code Examples - Document 22

## Overview

This document contains detailed code implementations for the vanilla chessboard project outlined in Document 21. All code examples follow the Architecture Guide (Document 02) principles with accurate chess.js v1.4.0 and Stockfish.js v17.1 APIs.

---

## Phase 1: Foundation Layer Code Examples

### Type Definitions (`/src/types/chess.types.ts`)

```typescript
// chess.types.ts - Core chess domain types
export type PieceColor = 'white' | 'black';
export type PieceType = 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn';
export type File = 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h';
export type Rank = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;

// ChessPosition as string type for compatibility with chess.js and string methods
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
```

### Component Types (`/src/types/component.types.ts`)

```typescript
// component.types.ts - React component prop types
import { ChessGameState, ChessPiece, ChessPosition, ChessMove, PieceColor, GameResult } from './chess.types';

export interface ChessboardProps {
  pieceSet?: keyof typeof PIECE_SETS;
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
```

### Utility Functions (`/src/utils/chess.utils.ts`)

```typescript
// chess.utils.ts - Core chess utilities
import { ChessPosition, ChessPositionObject, File, Rank } from '../types';

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

export const isValidPosition = (position: ChessPosition): boolean => {
  return isValidFile(position.file) && isValidRank(position.rank);
};

export const getSquareColor = (position: ChessPosition): 'light' | 'dark' => {
  const fileIndex = fileToIndex(position.file);
  const rankIndex = rankToIndex(position.rank);
  return (fileIndex + rankIndex) % 2 === 0 ? 'dark' : 'light';
};

export const isValidFile = (file: string): file is File => {
  return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].includes(file);
};

export const isValidRank = (rank: number): rank is Rank => {
  return rank >= 1 && rank <= 8;
};

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

export const generateSquareList = (orientation: PieceColor = 'white') => {
  const squares = [];
  const ranks = orientation === 'white' ? [8, 7, 6, 5, 4, 3, 2, 1] : [1, 2, 3, 4, 5, 6, 7, 8];
  const files: File[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  
  for (const rank of ranks) {
    for (const file of files) {
      squares.push({
        file,
        rank: rank as Rank,
        position: { file, rank: rank as Rank }
      });
    }
  }
  
  return squares;
};
```

### Constants (`/src/constants/chess.constants.ts`)

```typescript
// chess.constants.ts - Chess game constants
export const STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

export const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;
export const RANKS = [1, 2, 3, 4, 5, 6, 7, 8] as const;

export const PIECE_TYPES = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn'] as const;
export const PIECE_COLORS = ['white', 'black'] as const;

export const PIECE_SETS = {
  classic: 'classic',
  modern: 'modern',
  tournament: 'tournament',
  executive: 'executive',
  conqueror: 'conqueror'
} as const;

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
```

---

## Phase 2: Chess Engine Services Code Examples

### Chess Game Service (`/src/services/ChessGameService.ts`)

```typescript
// ChessGameService.ts - Core chess game logic using chess.js v1.4.0
import { Chess } from 'chess.js';
import { 
  ChessGameState, 
  ChessMove, 
  ChessMoveInput, 
  ChessMoveResult, 
  ChessPiece, 
  ChessPosition 
} from '../types';
import { squareToPosition, positionToSquare } from '../utils';

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
      });

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
    
    // Parse chess.js board() output
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

    return {
      position,
      activeColor: this.gameEngine.turn() === 'w' ? 'white' : 'black',
      castlingRights: this.getCastlingRights(),
      enPassantTarget: this.getEnPassantTarget(),
      halfmoveClock: this.gameEngine.halfmoveClock || 0,
      fullmoveNumber: this.gameEngine.fullmoveNumber || 1,
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
      return this.gameEngine.moves({ square, verbose: false });
    }
    return this.gameEngine.moves({ verbose: false });
  }

  public getValidMovesVerbose(square?: string) {
    return this.gameEngine.moves({ square, verbose: true });
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
    } catch (error) {
      return false;
    }
  }

  private convertMove(move: any): ChessMove {
    return {
      from: squareToPosition(move.from),
      to: squareToPosition(move.to),
      piece: {
        id: `${move.color}${move.piece}${move.from}`,
        type: this.convertPieceType(move.piece),
        color: move.color === 'w' ? 'white' : 'black',
        position: squareToPosition(move.from)
      },
      capturedPiece: move.captured ? {
        id: `${move.color === 'w' ? 'b' : 'w'}${move.captured}${move.to}`,
        type: this.convertPieceType(move.captured),
        color: move.color === 'w' ? 'black' : 'white',
        position: squareToPosition(move.to)
      } : undefined,
      promotion: move.promotion ? this.convertPieceType(move.promotion) : undefined,
      isCheck: this.gameEngine.isCheck(),
      isCheckmate: this.gameEngine.isCheckmate(),
      notation: move.san,
      san: move.san,
      uci: `${move.from}${move.to}${move.promotion || ''}`
    };
  }

  private convertPieceType(piece: string) {
    const typeMap = {
      'k': 'king',
      'q': 'queen',
      'r': 'rook',
      'b': 'bishop',
      'n': 'knight',
      'p': 'pawn'
    };
    return typeMap[piece.toLowerCase()] || 'pawn';
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
    
    return squareToPosition(enPassantSquare);
  }
}
```

### Stockfish Service (`/src/services/StockfishService.ts`)

```typescript
// StockfishService.ts - Stockfish.js v17.1 Web Worker integration
export class StockfishService {
  private stockfish: Worker | null = null;
  private isReady: boolean = false;
  private pendingCommands: Map<string, (response: string) => void> = new Map();
  private commandId = 0;

  constructor() {
    this.initializeEngine();
  }

  private initializeEngine(): void {
    try {
      // Check WebAssembly support (accurate implementation from docs)
      const wasmSupported = typeof WebAssembly === 'object' && 
        WebAssembly.validate(Uint8Array.of(0x0, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00));

      // Use appropriate Stockfish version based on WASM support
      const stockfishPath = wasmSupported ? 
        '/stockfish/stockfish-17.1-lite-single-03e3232.js' : 
        '/stockfish/stockfish-17.1-asm-341ff22.js';

      this.stockfish = new Worker(stockfishPath);
      
      this.stockfish.addEventListener('message', this.handleMessage.bind(this));
      this.stockfish.addEventListener('error', this.handleError.bind(this));

      // Initialize UCI protocol
      this.sendCommand('uci');
      
      // Wait for readiness
      this.sendCommand('isready').then(() => {
        this.isReady = true;
        console.log('Stockfish engine ready');
      });

    } catch (error) {
      console.error('Failed to initialize Stockfish:', error);
      this.isReady = false;
    }
  }

  private handleMessage(event: MessageEvent): void {
    const message = event.data as string;
    console.log('Stockfish:', message);

    // Handle UCI protocol responses
    if (message === 'uciok') {
      console.log('UCI protocol initialized');
      return;
    }

    if (message === 'readyok') {
      const readyCommand = this.pendingCommands.get('isready');
      if (readyCommand) {
        readyCommand(message);
        this.pendingCommands.delete('isready');
      }
      return;
    }

    // Handle bestmove responses
    if (message.startsWith('bestmove')) {
      const bestMoveCommand = this.pendingCommands.get('bestmove');
      if (bestMoveCommand) {
        bestMoveCommand(message);
        this.pendingCommands.delete('bestmove');
      }
      return;
    }

    // Handle evaluation responses
    if (message.includes('cp ')) {
      const evalCommand = this.pendingCommands.get('evaluation');
      if (evalCommand) {
        evalCommand(message);
        this.pendingCommands.delete('evaluation');
      }
    }
  }

  private handleError(error: ErrorEvent): void {
    console.error('Stockfish Worker error:', error);
    this.isReady = false;
  }

  private sendCommand(command: string): Promise<string> {
    return new Promise((resolve, reject) => {
      if (!this.stockfish) {
        reject(new Error('Stockfish not initialized'));
        return;
      }

      const commandType = command.split(' ')[0];
      this.pendingCommands.set(commandType, resolve);

      this.stockfish.postMessage(command);

      // Set timeout for commands
      setTimeout(() => {
        if (this.pendingCommands.has(commandType)) {
          this.pendingCommands.delete(commandType);
          reject(new Error(`Command timeout: ${command}`));
        }
      }, 10000); // 10 second timeout
    });
  }

  public async getBestMove(fen: string, skillLevel: number = 8, timeLimit: number = 1000): Promise<string | null> {
    if (!this.isReady || !this.stockfish) {
      console.warn('Stockfish not ready');
      return null;
    }

    try {
      // Set skill level (0-20, where 20 is strongest)
      await this.sendCommand(`setoption name Skill Level value ${Math.max(0, Math.min(20, skillLevel))}`);
      
      // Set position
      await this.sendCommand(`position fen ${fen}`);
      
      // Request best move with time limit
      const response = await this.sendCommand(`go movetime ${timeLimit}`);
      
      // Parse bestmove response: "bestmove e2e4 ponder e7e5"
      const match = response.match(/bestmove\s+([a-h][1-8][a-h][1-8][qrbn]?)/);
      if (match) {
        return match[1];
      }
      
      return null;
    } catch (error) {
      console.error('Error getting best move:', error);
      return null;
    }
  }

  public async evaluatePosition(fen: string, depth: number = 15): Promise<number> {
    if (!this.isReady || !this.stockfish) {
      console.warn('Stockfish not ready');
      return 0;
    }

    try {
      // Set position
      await this.sendCommand(`position fen ${fen}`);
      
      // Request evaluation
      const response = await this.sendCommand(`go depth ${depth}`);
      
      // Parse evaluation from info messages
      // Look for "info depth X score cp Y" pattern
      const cpMatch = response.match(/score cp (-?\d+)/);
      if (cpMatch) {
        return parseInt(cpMatch[1]) / 100; // Convert centipawns to pawns
      }

      // Look for mate scores "info depth X score mate Y"
      const mateMatch = response.match(/score mate (-?\d+)/);
      if (mateMatch) {
        const mateIn = parseInt(mateMatch[1]);
        return mateIn > 0 ? 999 : -999; // Large positive/negative for mate
      }
      
      return 0;
    } catch (error) {
      console.error('Error evaluating position:', error);
      return 0;
    }
  }

  public async setSkillLevel(level: number): Promise<void> {
    if (!this.isReady) {
      return;
    }

    const clampedLevel = Math.max(0, Math.min(20, level));
    await this.sendCommand(`setoption name Skill Level value ${clampedLevel}`);
  }

  public async setDepth(depth: number): Promise<void> {
    if (!this.isReady) {
      return;
    }

    const clampedDepth = Math.max(1, Math.min(20, depth));
    await this.sendCommand(`setoption name Depth value ${clampedDepth}`);
  }

  public destroy(): void {
    if (this.stockfish) {
      this.stockfish.terminate();
      this.stockfish = null;
    }
    this.isReady = false;
    this.pendingCommands.clear();
  }

  public isEngineReady(): boolean {
    return this.isReady;
  }
}
```

### FEN Service (`/src/services/FenService.ts`)

```typescript
// FenService.ts - FEN parsing and validation
import { Chess } from 'chess.js';
import { ChessGameState, ChessPiece, ChessPosition } from '../types';
import { squareToPosition } from '../utils';

export class FenService {
  public static validateFen(fen: string): boolean {
    try {
      const chess = new Chess();
      chess.load(fen);
      return true;
    } catch (error) {
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

  private static convertPieceType(piece: string) {
    const typeMap = {
      'k': 'king',
      'q': 'queen', 
      'r': 'rook',
      'b': 'bishop',
      'n': 'knight',
      'p': 'pawn'
    };
    return typeMap[piece.toLowerCase()] || 'pawn';
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
```

---

## Phase 3: React Hooks Code Examples

### Core Chess Game Hook (`/src/hooks/useChessGame.ts`)

```typescript
// useChessGame.ts - Main chess game state management
import { useState, useEffect, useRef, useCallback } from 'react';
import { ChessGameService } from '../services/ChessGameService';
import { ChessGameState, ChessMove, ChessMoveInput, PieceType } from '../types';

export interface UseChessGameHook {
  gameState: ChessGameState | null;
  isLoading: boolean;
  makeMove: (from: string, to: string, promotion?: PieceType) => Promise<boolean>;
  undoMove: () => boolean;
  resetGame: (fen?: string) => void;
  getValidMoves: (square?: string) => string[];
  isGameOver: boolean;
  error: string | null;
}

export const useChessGame = (initialFen?: string): UseChessGameHook => {
  const [gameState, setGameState] = useState<ChessGameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const gameServiceRef = useRef<ChessGameService>();

  // Initialize game service
  useEffect(() => {
    try {
      gameServiceRef.current = new ChessGameService(initialFen);
      setGameState(gameServiceRef.current.getCurrentState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize game');
    } finally {
      setIsLoading(false);
    }
  }, [initialFen]);

  const makeMove = useCallback(async (
    from: string, 
    to: string, 
    promotion?: PieceType
  ): Promise<boolean> => {
    if (!gameServiceRef.current) {
      setError('Game not initialized');
      return false;
    }

    try {
      setError(null);
      const moveInput: ChessMoveInput = { from, to, promotion };
      const result = gameServiceRef.current.makeMove(moveInput);
      
      if (result.success) {
        setGameState(result.gameState);
        return true;
      } else {
        setError(result.error || 'Invalid move');
        return false;
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Move failed';
      setError(errorMessage);
      return false;
    }
  }, []);

  const undoMove = useCallback((): boolean => {
    if (!gameServiceRef.current) {
      setError('Game not initialized');
      return false;
    }

    try {
      setError(null);
      const success = gameServiceRef.current.undoLastMove();
      
      if (success) {
        setGameState(gameServiceRef.current.getCurrentState());
        return true;
      }
      
      return false;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Undo failed');
      return false;
    }
  }, []);

  const resetGame = useCallback((fen?: string): void => {
    if (!gameServiceRef.current) {
      return;
    }

    try {
      setError(null);
      gameServiceRef.current.resetGame(fen);
      setGameState(gameServiceRef.current.getCurrentState());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Reset failed');
    }
  }, []);

  const getValidMoves = useCallback((square?: string): string[] => {
    if (!gameServiceRef.current) {
      return [];
    }

    try {
      return gameServiceRef.current.getValidMoves(square);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get valid moves');
      return [];
    }
  }, []);

  return {
    gameState,
    isLoading,
    makeMove,
    undoMove,
    resetGame,
    getValidMoves,
    isGameOver: gameState?.isGameOver || false,
    error
  };
};
```

### Stockfish Hook (`/src/hooks/useStockfish.ts`)

```typescript
// useStockfish.ts - Computer opponent integration
import { useState, useEffect, useRef, useCallback } from 'react';
import { StockfishService } from '../services/StockfishService';

export interface UseStockfishHook {
  isReady: boolean;
  isThinking: boolean;
  skillLevel: number;
  setSkillLevel: (level: number) => void;
  requestMove: (fen: string, timeLimit?: number) => Promise<string | null>;
  evaluatePosition: (fen: string) => Promise<number>;
  error: string | null;
}

export const useStockfish = (): UseStockfishHook => {
  const [isReady, setIsReady] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [skillLevel, setSkillLevelState] = useState(8);
  const [error, setError] = useState<string | null>(null);
  const stockfishRef = useRef<StockfishService>();

  // Initialize Stockfish service
  useEffect(() => {
    try {
      stockfishRef.current = new StockfishService();
      
      // Poll for readiness (Stockfish initialization is async)
      const checkReady = setInterval(() => {
        if (stockfishRef.current?.isEngineReady()) {
          setIsReady(true);
          clearInterval(checkReady);
        }
      }, 100);

      // Cleanup timeout
      setTimeout(() => {
        clearInterval(checkReady);
        if (!isReady) {
          setError('Stockfish initialization timeout');
        }
      }, 5000);

      return () => {
        clearInterval(checkReady);
      };
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize Stockfish');
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (stockfishRef.current) {
        stockfishRef.current.destroy();
      }
    };
  }, []);

  const setSkillLevel = useCallback(async (level: number): Promise<void> => {
    if (!stockfishRef.current || !isReady) {
      setError('Stockfish not ready');
      return;
    }

    try {
      setError(null);
      await stockfishRef.current.setSkillLevel(level);
      setSkillLevelState(level);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to set skill level');
    }
  }, [isReady]);

  const requestMove = useCallback(async (
    fen: string, 
    timeLimit: number = 1000
  ): Promise<string | null> => {
    if (!stockfishRef.current || !isReady) {
      setError('Stockfish not ready');
      return null;
    }

    try {
      setError(null);
      setIsThinking(true);
      
      const move = await stockfishRef.current.getBestMove(fen, skillLevel, timeLimit);
      
      return move;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get computer move');
      return null;
    } finally {
      setIsThinking(false);
    }
  }, [isReady, skillLevel]);

  const evaluatePosition = useCallback(async (fen: string): Promise<number> => {
    if (!stockfishRef.current || !isReady) {
      setError('Stockfish not ready');
      return 0;
    }

    try {
      setError(null);
      return await stockfishRef.current.evaluatePosition(fen);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to evaluate position');
      return 0;
    }
  }, [isReady]);

  return {
    isReady,
    isThinking,
    skillLevel,
    setSkillLevel,
    requestMove,
    evaluatePosition,
    error
  };
};
```

### Responsive Board Hook (`/src/hooks/useResponsiveBoard.ts`)

```typescript
// useResponsiveBoard.ts - Responsive board sizing
import { useState, useEffect, useRef, useCallback } from 'react';

export interface UseResponsiveBoardHook {
  boardSize: { width: number; height: number };
  squareSize: number;
  containerRef: React.RefObject<HTMLDivElement>;
  isResizing: boolean;
}

export const useResponsiveBoard = (maxWidth?: number): UseResponsiveBoardHook => {
  const [boardSize, setBoardSize] = useState({ width: 0, height: 0 });
  const [isResizing, setIsResizing] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const resizeTimeoutRef = useRef<NodeJS.Timeout>();

  const calculateBoardSize = useCallback(() => {
    if (!containerRef.current) {
      return { width: 400, height: 400 };
    }

    const container = containerRef.current;
    const containerRect = container.getBoundingClientRect();
    const containerSize = Math.min(containerRect.width, containerRect.height);

    // Apply constraints
    const minSize = 200;
    const maxSize = maxWidth || 800;
    const size = Math.max(minSize, Math.min(maxSize, containerSize * 0.9));

    return { width: size, height: size };
  }, [maxWidth]);

  const updateBoardSize = useCallback(() => {
    setIsResizing(true);
    
    // Debounce resize updates
    if (resizeTimeoutRef.current) {
      clearTimeout(resizeTimeoutRef.current);
    }

    resizeTimeoutRef.current = setTimeout(() => {
      const newSize = calculateBoardSize();
      setBoardSize(newSize);
      setIsResizing(false);
    }, 100);
  }, [calculateBoardSize]);

  // Initial size calculation
  useEffect(() => {
    if (containerRef.current) {
      const initialSize = calculateBoardSize();
      setBoardSize(initialSize);
    }
  }, [calculateBoardSize]);

  // ResizeObserver for responsive updates
  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    const resizeObserver = new ResizeObserver(() => {
      updateBoardSize();
    });

    resizeObserver.observe(containerRef.current);

    // Fallback window resize listener
    const handleWindowResize = () => updateBoardSize();
    window.addEventListener('resize', handleWindowResize);

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', handleWindowResize);
      if (resizeTimeoutRef.current) {
        clearTimeout(resizeTimeoutRef.current);
      }
    };
  }, [updateBoardSize]);

  const squareSize = boardSize.width / 8;

  return {
    boardSize,
    squareSize,
    containerRef,
    isResizing
  };
};
```

### Drag and Drop Hook (`/src/hooks/useDragAndDrop.ts`)

```typescript
// useDragAndDrop.ts - Drag and drop interaction
import { useState, useCallback, useRef } from 'react';
import { ChessPiece, ChessPosition, ChessGameState } from '../types';
import { positionToSquare } from '../utils';

export interface UseDragAndDropHook {
  draggedPiece: ChessPiece | null;
  isDragging: boolean;
  dragSource: ChessPosition | null;
  validDropTargets: ChessPosition[];
  handleDragStart: (piece: ChessPiece, position: ChessPosition) => void;
  handleDragEnd: () => void;
  handleDrop: (targetPosition: ChessPosition) => Promise<boolean>;
  handleSquareClick: (position: ChessPosition) => void;
}

export const useDragAndDrop = (
  gameState: ChessGameState | null,
  onMove: (from: string, to: string) => Promise<boolean>,
  getValidMoves: (square?: string) => string[]
): UseDragAndDropHook => {
  const [draggedPiece, setDraggedPiece] = useState<ChessPiece | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragSource, setDragSource] = useState<ChessPosition | null>(null);
  const [validDropTargets, setValidDropTargets] = useState<ChessPosition[]>([]);
  const [selectedSquare, setSelectedSquare] = useState<ChessPosition | null>(null);
  const dragDataRef = useRef<{ piece: ChessPiece; source: ChessPosition } | null>(null);

  const clearDragState = useCallback(() => {
    setDraggedPiece(null);
    setIsDragging(false);
    setDragSource(null);
    setValidDropTargets([]);
    dragDataRef.current = null;
  }, []);

  const handleDragStart = useCallback((piece: ChessPiece, position: ChessPosition) => {
    if (!gameState || gameState.isGameOver) {
      return;
    }

    // Check if it's the current player's turn
    if (piece.color !== gameState.activeColor) {
      return;
    }

    setDraggedPiece(piece);
    setIsDragging(true);
    setDragSource(position);
    dragDataRef.current = { piece, source: position };

    // Get valid moves for this piece
    const sourceSquare = positionToSquare(position);
    const validMoves = getValidMoves(sourceSquare);
    const targets = validMoves.map(move => {
      // Parse UCI move format (e.g., "e2e4")
      const to = move.length >= 4 ? move.substring(2, 4) : move;
      try {
        return squareToPosition(to);
      } catch {
        return null;
      }
    }).filter((pos): pos is ChessPosition => pos !== null);

    setValidDropTargets(targets);
  }, [gameState, getValidMoves]);

  const handleDragEnd = useCallback(() => {
    // Small delay to allow drop event to process first
    setTimeout(() => {
      setIsDragging(false);
      // Don't clear other state immediately in case drop is processing
    }, 50);
  }, []);

  const handleDrop = useCallback(async (targetPosition: ChessPosition): Promise<boolean> => {
    if (!dragDataRef.current || !gameState) {
      clearDragState();
      return false;
    }

    const { source } = dragDataRef.current;
    const fromSquare = positionToSquare(source);
    const toSquare = positionToSquare(targetPosition);

    // Check if this is a valid drop target
    const isValidTarget = validDropTargets.some(
      target => target.file === targetPosition.file && target.rank === targetPosition.rank
    );

    if (!isValidTarget) {
      clearDragState();
      return false;
    }

    try {
      const success = await onMove(fromSquare, toSquare);
      clearDragState();
      setSelectedSquare(null);
      return success;
    } catch (error) {
      console.error('Drop move failed:', error);
      clearDragState();
      return false;
    }
  }, [validDropTargets, gameState, onMove, clearDragState]);

  const handleSquareClick = useCallback((position: ChessPosition) => {
    if (!gameState || gameState.isGameOver) {
      return;
    }

    const clickedSquare = positionToSquare(position);
    const piece = gameState.position.get(clickedSquare);

    // If no piece is selected, select this square (if it has a piece)
    if (!selectedSquare) {
      if (piece && piece.color === gameState.activeColor) {
        setSelectedSquare(position);
        
        // Show valid moves for click-to-move
        const validMoves = getValidMoves(clickedSquare);
        const targets = validMoves.map(move => {
          const to = move.length >= 4 ? move.substring(2, 4) : move;
          try {
            return squareToPosition(to);
          } catch {
            return null;
          }
        }).filter((pos): pos is ChessPosition => pos !== null);
        
        setValidDropTargets(targets);
      }
      return;
    }

    // If same square clicked, deselect
    if (selectedSquare.file === position.file && selectedSquare.rank === position.rank) {
      setSelectedSquare(null);
      setValidDropTargets([]);
      return;
    }

    // If different piece of same color clicked, select new piece
    if (piece && piece.color === gameState.activeColor) {
      setSelectedSquare(position);
      
      const validMoves = getValidMoves(clickedSquare);
      const targets = validMoves.map(move => {
        const to = move.length >= 4 ? move.substring(2, 4) : move;
        try {
          return squareToPosition(to);
        } catch {
          return null;
        }
      }).filter((pos): pos is ChessPosition => pos !== null);
      
      setValidDropTargets(targets);
      return;
    }

    // Try to make a move from selected square to clicked square
    const fromSquare = positionToSquare(selectedSquare);
    const toSquare = clickedSquare;

    // Check if this is a valid move
    const isValidMove = validDropTargets.some(
      target => target.file === position.file && target.rank === position.rank
    );

    if (isValidMove) {
      onMove(fromSquare, toSquare).then(() => {
        setSelectedSquare(null);
        setValidDropTargets([]);
      }).catch(error => {
        console.error('Click move failed:', error);
      });
    } else {
      // Invalid move, clear selection
      setSelectedSquare(null);
      setValidDropTargets([]);
    }
  }, [gameState, selectedSquare, validDropTargets, getValidMoves, onMove]);

  return {
    draggedPiece,
    isDragging,
    dragSource,
    validDropTargets,
    handleDragStart,
    handleDragEnd,
    handleDrop,
    handleSquareClick
  };
};
```

---

## Phase 4: Vanilla CSS Code Examples

### Core Chessboard Styles (`/src/styles/chessboard.css`)

```css
/* chessboard.css - Core chessboard styling */

/* CSS Custom Properties for theming */
:root {
  --chessboard-light-square: #F0D9B5;
  --chessboard-dark-square: #B58863;
  --chessboard-border: #8B4513;
  --chessboard-highlight: rgba(255, 255, 0, 0.5);
  --chessboard-valid-move: rgba(0, 255, 0, 0.6);
  --chessboard-capture: rgba(255, 0, 0, 0.8);
  --chessboard-selected: rgba(0, 100, 200, 0.3);
  --coordinate-color: #8B4513;
  --coordinate-size: 0.75rem;
}

/* Main chessboard container */
.chessboard {
  --board-size: min(90vw, 90vh, 600px);
  --square-size: calc(var(--board-size) / 8);
  
  width: var(--board-size);
  height: var(--board-size);
  aspect-ratio: 1;
  
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  grid-template-rows: repeat(8, 1fr);
  
  border: 3px solid var(--chessboard-border);
  border-radius: 4px;
  position: relative;
  user-select: none;
  background: var(--chessboard-light-square);
  
  /* Prevent layout shift during loading */
  min-width: 200px;
  min-height: 200px;
}

/* Individual squares */
.chessboard-square {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

/* Alternating square colors - using CSS Grid positioning */
.chessboard-square:nth-child(odd) {
  background-color: var(--chessboard-light-square);
}

.chessboard-square:nth-child(even) {
  background-color: var(--chessboard-dark-square);
}

/* Correct alternating pattern for 8x8 grid */
.chessboard-square:nth-child(8n+1),
.chessboard-square:nth-child(8n+3),
.chessboard-square:nth-child(8n+5),
.chessboard-square:nth-child(8n+7) {
  background-color: var(--chessboard-dark-square);
}

.chessboard-square:nth-child(8n+2),
.chessboard-square:nth-child(8n+4),
.chessboard-square:nth-child(8n+6),
.chessboard-square:nth-child(8n+8) {
  background-color: var(--chessboard-light-square);
}

/* Second row offset for proper checkerboard */
.chessboard-square:nth-child(n+9):nth-child(-n+16):nth-child(odd),
.chessboard-square:nth-child(n+25):nth-child(-n+32):nth-child(odd),
.chessboard-square:nth-child(n+41):nth-child(-n+48):nth-child(odd),
.chessboard-square:nth-child(n+57):nth-child(-n+64):nth-child(odd) {
  background-color: var(--chessboard-light-square);
}

.chessboard-square:nth-child(n+9):nth-child(-n+16):nth-child(even),
.chessboard-square:nth-child(n+25):nth-child(-n+32):nth-child(even),
.chessboard-square:nth-child(n+41):nth-child(-n+48):nth-child(even),
.chessboard-square:nth-child(n+57):nth-child(-n+64):nth-child(even) {
  background-color: var(--chessboard-dark-square);
}

/* Square hover effects */
.chessboard-square:hover {
  background-color: var(--chessboard-highlight);
}

/* Selected square highlighting */
.chessboard-square.selected {
  background-color: var(--chessboard-selected) !important;
  box-shadow: inset 0 0 0 3px rgba(0, 100, 200, 0.8);
}

/* Valid move indicators */
.chessboard-square.valid-move::after {
  content: '';
  position: absolute;
  width: 35%;
  height: 35%;
  border-radius: 50%;
  background: var(--chessboard-valid-move);
  pointer-events: none;
  z-index: 1;
}

/* Capture move indicators */
.chessboard-square.valid-move.capture-target::after {
  width: 90%;
  height: 90%;
  border: 4px solid var(--chessboard-capture);
  background: transparent;
  border-radius: 8px;
}

/* Chess pieces */
.chessboard-piece {
  width: 85%;
  height: 85%;
  cursor: pointer;
  transition: transform 0.2s ease;
  z-index: 2;
  pointer-events: auto;
  
  /* Ensure pieces are crisp */
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
}

.chessboard-piece:hover {
  transform: scale(1.05);
}

.chessboard-piece.dragging {
  opacity: 0.7;
  transform: scale(1.1) rotate(5deg);
  z-index: 1000;
  pointer-events: none;
}

/* Smooth piece movement animations */
.chessboard-piece.moving {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 10;
}

/* Coordinate labels */
.chessboard-coordinates {
  position: absolute;
  font-size: var(--coordinate-size);
  font-weight: bold;
  font-family: 'Arial', sans-serif;
  color: var(--coordinate-color);
  pointer-events: none;
  z-index: 3;
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.8);
}

.coordinate-rank {
  top: 2px;
  left: 2px;
}

.coordinate-file {
  bottom: 2px;
  right: 2px;
}

/* Drag preview (for HTML5 drag API) */
.drag-preview {
  position: fixed;
  top: -1000px;
  left: -1000px;
  width: 60px;
  height: 60px;
  opacity: 0.8;
  pointer-events: none;
  z-index: 9999;
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  .chessboard {
    --board-size: min(95vw, 95vh);
    border-width: 2px;
  }
  
  .chessboard-coordinates {
    --coordinate-size: 0.65rem;
  }
  
  .chessboard-piece {
    width: 90%;
    height: 90%;
  }
}

@media (max-width: 480px) {
  .chessboard {
    --board-size: min(98vw, 98vh);
    border-width: 1px;
  }
  
  .chessboard-coordinates {
    --coordinate-size: 0.6rem;
  }
}

@media (min-width: 1200px) {
  .chessboard {
    --board-size: min(70vw, 70vh, 800px);
  }
  
  .chessboard-coordinates {
    --coordinate-size: 0.9rem;
  }
}

/* High DPI display optimizations */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
  .chessboard-piece {
    image-rendering: -webkit-optimize-contrast;
    image-rendering: optimize-contrast;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .chessboard-piece,
  .chessboard-piece.moving,
  .chessboard-square {
    transition: none !important;
    animation: none !important;
  }
}

/* Focus indicators for keyboard navigation */
.chessboard-square:focus {
  outline: 3px solid #4A90E2;
  outline-offset: -3px;
}

.chessboard-piece:focus {
  outline: 2px solid #4A90E2;
  outline-offset: 2px;
}

/* Loading state */
.chessboard.loading {
  opacity: 0.6;
  pointer-events: none;
}

.chessboard.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  margin: -20px 0 0 -20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: chess-loading 1s linear infinite;
}

@keyframes chess-loading {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Theme variations */
.chessboard.theme-wood {
  --chessboard-light-square: #F7E8A4;
  --chessboard-dark-square: #C5833A;
  --chessboard-border: #8B4513;
}

.chessboard.theme-green {
  --chessboard-light-square: #FFFFDD;
  --chessboard-dark-square: #86A666;
  --chessboard-border: #5F5F5F;
}

.chessboard.theme-blue {
  --chessboard-light-square: #E8F4FD;
  --chessboard-dark-square: #4A90E2;
  --chessboard-border: #2C5985;
}
```

### App Layout Styles (`/src/styles/app.css`)

```css
/* app.css - Application layout and components */

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #333;
}

.app-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.app-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 2rem;
}

.chessboard-container {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.game-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.game-status {
  background: rgba(255, 255, 255, 0.9);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  color: #333;
  text-align: center;
  min-width: 200px;
}

.game-status.thinking {
  background: rgba(255, 165, 0, 0.9);
  color: white;
}

.game-status.thinking::before {
  content: '🤔 ';
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn:active {
  transform: translateY(0);
}

.btn-primary {
  background: #4A90E2;
  color: white;
}

.btn-primary:hover {
  background: #357ABD;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 1);
}

.btn-danger {
  background: #E74C3C;
  color: white;
}

.btn-danger:hover {
  background: #C0392B;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Responsive layout */
@media (max-width: 768px) {
  .app-main {
    padding: 1rem;
    gap: 1.5rem;
  }
  
  .app-header {
    padding: 0.75rem 1rem;
  }
  
  .app-header h1 {
    font-size: 1.5rem;
  }
  
  .chessboard-container {
    padding: 1rem;
    border-radius: 8px;
  }
  
  .game-controls {
    flex-direction: column;
    width: 100%;
  }
  
  .btn {
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .app-main {
    padding: 0.5rem;
  }
  
  .chessboard-container {
    padding: 0.5rem;
    margin: 0;
    background: transparent;
    backdrop-filter: none;
    box-shadow: none;
    border: none;
  }
}
```

### Global Styles (`/src/styles/global.css`)

```css
/* global.css - Global styles and resets */

/* Modern CSS Reset */
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
}

body {
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}

p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}

/* Focus management */
:focus {
  outline: 2px solid #4A90E2;
  outline-offset: 2px;
}

/* Remove focus outline for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Reduced motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
  
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --chessboard-light-square: #FFFFFF;
    --chessboard-dark-square: #000000;
    --chessboard-border: #000000;
    --chessboard-valid-move: rgba(0, 255, 0, 0.9);
    --chessboard-capture: rgba(255, 0, 0, 0.9);
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .app {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  }
  
  .app-header {
    background: rgba(0, 0, 0, 0.3);
  }
  
  .chessboard-container {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}

/* Utility classes */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.loading {
  opacity: 0.6;
  pointer-events: none;
}

.error {
  color: #E74C3C;
  background: rgba(231, 76, 60, 0.1);
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.success {
  color: #27AE60;
  background: rgba(39, 174, 96, 0.1);
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid rgba(39, 174, 96, 0.3);
}

.warning {
  color: #F39C12;
  background: rgba(243, 156, 18, 0.1);
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid rgba(243, 156, 18, 0.3);
}
```

This document provides comprehensive, production-ready code examples for all phases of the vanilla chessboard implementation. Each code block follows the architecture principles and includes accurate API usage for chess.js v1.4.0 and Stockfish.js v17.1.