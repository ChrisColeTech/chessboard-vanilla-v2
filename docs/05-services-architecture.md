# Services Architecture - Business Logic Layer

## Principles

Services contain **pure business logic** with **zero React dependencies**. Each service follows SRP and can be tested independently. Services are injected into hooks and never called directly by components.

### Core Rules
- **No React imports** or dependencies
- **Pure functions** and classes only
- **Single responsibility** per service
- **Interface-based design** for testability
- **Dependency injection** support
- **No side effects** unless explicitly designed for them

---

## Chess Game Services

### 1. Chess Game Service

```typescript
// services/chess/ChessGameService.ts
import { Chess } from 'chess.js';
import type { 
  IChessGameService,
  ChessGameState,
  ChessMoveInput,
  ChessMoveResult,
  ChessMove,
  ChessGameConfig,
  SquareNotation 
} from '@/types';
import { FenService } from './FenService';
import { MoveValidationService } from './MoveValidationService';
import { createChessGameState, createChessMove } from '@/utils/chess.utils';

/**
 * Core chess game logic service
 * Responsibility: Manage game state, moves, and rules validation
 */
export class ChessGameService implements IChessGameService {
  private readonly chess: Chess;
  private readonly fenService: FenService;
  private readonly validationService: MoveValidationService;
  private readonly config: Required<ChessGameConfig>;

  constructor(
    config: ChessGameConfig = {},
    fenService = new FenService(),
    validationService = new MoveValidationService()
  ) {
    this.config = {
      initialFen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
      validateMoves: true,
      trackHistory: true,
      enableUndo: true,
      ...config
    };

    this.fenService = fenService;
    this.validationService = validationService;
    this.chess = new Chess(this.config.initialFen);

    // Validate initial FEN if provided
    if (config.initialFen) {
      const validation = this.fenService.validateFen(config.initialFen);
      if (!validation.isValid) {
        throw new Error(`Invalid initial FEN: ${validation.errors.join(', ')}`);
      }
    }
  }

  public getCurrentState(): ChessGameState {
    return createChessGameState({
      chess: this.chess,
      fenService: this.fenService,
      includeHistory: this.config.trackHistory
    });
  }

  public makeMove(move: ChessMoveInput): ChessMoveResult {
    try {
      // Pre-move validation if enabled
      if (this.config.validateMoves) {
        const validation = this.validationService.validateMove(
          move, 
          this.getCurrentState()
        );
        
        if (!validation.isValid) {
          return {
            success: false,
            error: validation.reason || 'Invalid move',
            gameState: this.getCurrentState()
          };
        }
      }

      // Attempt the move
      const chessMove = this.chess.move({
        from: move.from,
        to: move.to,
        promotion: move.promotion || 'q'
      });

      if (!chessMove) {
        return {
          success: false,
          error: 'Move rejected by chess engine',
          gameState: this.getCurrentState()
        };
      }

      // Create our move representation
      const move = createChessMove(chessMove, this.chess);
      const newState = this.getCurrentState();

      return {
        success: true,
        move,
        gameState: newState
      };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown move error',
        gameState: this.getCurrentState()
      };
    }
  }

  public undoMove(): ChessMoveResult {
    if (!this.config.enableUndo) {
      return {
        success: false,
        error: 'Undo is disabled',
        gameState: this.getCurrentState()
      };
    }

    try {
      const undoneMove = this.chess.undo();
      
      if (!undoneMove) {
        return {
          success: false,
          error: 'No moves to undo',
          gameState: this.getCurrentState()
        };
      }

      return {
        success: true,
        gameState: this.getCurrentState()
      };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Undo failed',
        gameState: this.getCurrentState()
      };
    }
  }

  public resetGame(fen?: string): void {
    const resetFen = fen || this.config.initialFen;
    
    // Validate new FEN if provided
    if (fen) {
      const validation = this.fenService.validateFen(fen);
      if (!validation.isValid) {
        throw new Error(`Invalid FEN for reset: ${validation.errors.join(', ')}`);
      }
    }

    this.chess.load(resetFen);
  }

  public loadGame(gameState: ChessGameState): void {
    const validation = this.fenService.validateFen(gameState.fen);
    if (!validation.isValid) {
      throw new Error(`Cannot load invalid game state: ${validation.errors.join(', ')}`);
    }

    this.chess.load(gameState.fen);
  }

  public validateMove(move: ChessMoveInput): boolean {
    if (!this.config.validateMoves) return true;

    const result = this.validationService.validateMove(move, this.getCurrentState());
    return result.isValid;
  }

  public getValidMoves(square?: SquareNotation): ChessMove[] {
    const currentState = this.getCurrentState();
    
    if (square) {
      return this.validationService.getValidMoves(square, currentState);
    }

    // Return all valid moves for current player
    const moves = this.chess.moves({ verbose: true });
    return moves.map(move => createChessMove(move, this.chess));
  }

  public isGameOver(): boolean {
    return this.chess.isGameOver();
  }

  public getGameStatus(): string {
    if (this.chess.isCheckmate()) {
      return `Checkmate - ${this.chess.turn() === 'w' ? 'Black' : 'White'} wins`;
    }
    
    if (this.chess.isStalemate()) {
      return 'Stalemate - Draw';
    }
    
    if (this.chess.isDraw()) {
      return 'Draw';
    }
    
    if (this.chess.inCheck()) {
      return `${this.chess.turn() === 'w' ? 'White' : 'Black'} in check`;
    }
    
    return `${this.chess.turn() === 'w' ? 'White' : 'Black'} to move`;
  }
}
```

### 2. FEN Service

```typescript
// services/chess/FenService.ts
import { Chess } from 'chess.js';
import type { 
  IFenService,
  ChessGameState,
  FenValidationResult,
  ChessPosition,
  ChessPiece,
  PieceColor,
  PieceType 
} from '@/types';

/**
 * FEN (Forsyth-Edwards Notation) processing service
 * Responsibility: Parse, generate, and validate FEN strings
 */
export class FenService implements IFenService {
  private static readonly DEFAULT_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  
  private static readonly PIECE_MAP: Record<string, { type: PieceType; color: PieceColor }> = {
    'K': { type: 'king', color: 'white' },
    'Q': { type: 'queen', color: 'white' },
    'R': { type: 'rook', color: 'white' },
    'B': { type: 'bishop', color: 'white' },
    'N': { type: 'knight', color: 'white' },
    'P': { type: 'pawn', color: 'white' },
    'k': { type: 'king', color: 'black' },
    'q': { type: 'queen', color: 'black' },
    'r': { type: 'rook', color: 'black' },
    'b': { type: 'bishop', color: 'black' },
    'n': { type: 'knight', color: 'black' },
    'p': { type: 'pawn', color: 'black' }
  };

  public parseFen(fen: string): ChessGameState {
    const validation = this.validateFen(fen);
    if (!validation.isValid) {
      throw new Error(`Invalid FEN: ${validation.errors.join(', ')}`);
    }

    // Use chess.js to parse the FEN
    const chess = new Chess(fen);
    const [position, activeColor, castling, enPassant, halfmove, fullmove] = fen.split(' ');

    return {
      id: this.generateGameId(),
      position: this.parsePosition(position),
      activeColor: activeColor === 'w' ? 'white' : 'black',
      castlingRights: this.parseCastlingRights(castling),
      enPassantTarget: enPassant === '-' ? undefined : this.parseSquare(enPassant),
      halfmoveClock: parseInt(halfmove, 10),
      fullmoveNumber: parseInt(fullmove, 10),
      isCheck: chess.inCheck(),
      isCheckmate: chess.isCheckmate(),
      isStalemate: chess.isStalemate(),
      isDraw: chess.isDraw(),
      fen,
      moveHistory: [], // Would be populated from game history if available
      lastMove: undefined
    };
  }

  public generateFen(gameState: ChessGameState): string {
    const position = this.generatePositionString(gameState.position);
    const activeColor = gameState.activeColor === 'white' ? 'w' : 'b';
    const castling = this.generateCastlingString(gameState.castlingRights);
    const enPassant = gameState.enPassantTarget 
      ? `${gameState.enPassantTarget.file}${gameState.enPassantTarget.rank}`
      : '-';
    const halfmove = gameState.halfmoveClock.toString();
    const fullmove = gameState.fullmoveNumber.toString();

    return `${position} ${activeColor} ${castling} ${enPassant} ${halfmove} ${fullmove}`;
  }

  public validateFen(fen: string): FenValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    if (!fen || typeof fen !== 'string') {
      errors.push('FEN must be a non-empty string');
      return { isValid: false, errors, warnings };
    }

    const parts = fen.trim().split(/\s+/);
    if (parts.length !== 6) {
      errors.push('FEN must contain exactly 6 space-separated fields');
      return { isValid: false, errors, warnings };
    }

    const [position, activeColor, castling, enPassant, halfmove, fullmove] = parts;

    // Validate using chess.js
    try {
      const chess = new Chess(fen);
      
      // Additional custom validations
      this.validatePosition(position, errors, warnings);
      this.validateActiveColor(activeColor, errors);
      this.validateCastling(castling, errors);
      this.validateEnPassant(enPassant, errors);
      this.validateHalfmove(halfmove, errors);
      this.validateFullmove(fullmove, errors);

    } catch (error) {
      errors.push(error instanceof Error ? error.message : 'Invalid FEN format');
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  public getDefaultFen(): string {
    return FenService.DEFAULT_FEN;
  }

  private parsePosition(positionString: string): ReadonlyMap<SquareNotation, ChessPiece> {
    const pieces = new Map<SquareNotation, ChessPiece>();
    const ranks = positionString.split('/');

    for (let rankIndex = 0; rankIndex < 8; rankIndex++) {
      const rank = ranks[rankIndex];
      let fileIndex = 0;

      for (let i = 0; i < rank.length; i++) {
        const char = rank[i];
        
        if (/\d/.test(char)) {
          // Skip empty squares
          fileIndex += parseInt(char, 10);
        } else if (FenService.PIECE_MAP[char]) {
          const { type, color } = FenService.PIECE_MAP[char];
          const file = String.fromCharCode(97 + fileIndex) as File; // 'a' + fileIndex
          const rankNum = (8 - rankIndex) as Rank;
          
          pieces.set(`${file}${rankNum}` as SquareNotation, {
            id: `${color}-${type}-${file}${rankNum}`,
            type,
            color,
            hasMoved: false // This would need to be determined from game history
          });

          fileIndex++;
        }
      }
    }

    return pieces;
  }

  private parseCastlingRights(castlingString: string): CastlingRights {
    return {
      whiteKingside: castlingString.includes('K'),
      whiteQueenside: castlingString.includes('Q'),
      blackKingside: castlingString.includes('k'),
      blackQueenside: castlingString.includes('q')
    };
  }

  private parseSquare(squareString: string): ChessPosition {
    const file = squareString[0] as File;
    const rank = parseInt(squareString[1], 10) as Rank;
    return { file, rank };
  }

  private generatePositionString(position: ReadonlyMap<SquareNotation, ChessPiece>): string {
    const ranks: string[] = [];

    for (let rankNum = 8; rankNum >= 1; rankNum--) {
      let rankString = '';
      let emptySquares = 0;

      for (let fileNum = 0; fileNum < 8; fileNum++) {
        const file = String.fromCharCode(97 + fileNum) as File;
        const square = `${file}${rankNum}` as SquareNotation;
        const piece = position.get(square);

        if (piece) {
          if (emptySquares > 0) {
            rankString += emptySquares.toString();
            emptySquares = 0;
          }
          
          const pieceChar = this.getPieceCharacter(piece);
          rankString += pieceChar;
        } else {
          emptySquares++;
        }
      }

      if (emptySquares > 0) {
        rankString += emptySquares.toString();
      }

      ranks.push(rankString);
    }

    return ranks.join('/');
  }

  private generateCastlingString(rights: CastlingRights): string {
    let castling = '';
    if (rights.whiteKingside) castling += 'K';
    if (rights.whiteQueenside) castling += 'Q';
    if (rights.blackKingside) castling += 'k';
    if (rights.blackQueenside) castling += 'q';
    return castling || '-';
  }

  private getPieceCharacter(piece: ChessPiece): string {
    const charMap: Record<string, string> = {
      'white-king': 'K', 'white-queen': 'Q', 'white-rook': 'R',
      'white-bishop': 'B', 'white-knight': 'N', 'white-pawn': 'P',
      'black-king': 'k', 'black-queen': 'q', 'black-rook': 'r',
      'black-bishop': 'b', 'black-knight': 'n', 'black-pawn': 'p'
    };
    
    return charMap[`${piece.color}-${piece.type}`] || '?';
  }

  private generateGameId(): string {
    return `game-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private validatePosition(position: string, errors: string[], warnings: string[]): void {
    const ranks = position.split('/');
    if (ranks.length !== 8) {
      errors.push('Position must contain exactly 8 ranks separated by /');
      return;
    }

    let whiteKings = 0;
    let blackKings = 0;

    for (const rank of ranks) {
      let fileCount = 0;
      
      for (const char of rank) {
        if (/\d/.test(char)) {
          fileCount += parseInt(char, 10);
        } else if (FenService.PIECE_MAP[char]) {
          fileCount++;
          
          if (char === 'K') whiteKings++;
          if (char === 'k') blackKings++;
        } else {
          errors.push(`Invalid character in position: ${char}`);
        }
      }
      
      if (fileCount !== 8) {
        errors.push(`Rank must contain exactly 8 squares: ${rank}`);
      }
    }

    if (whiteKings !== 1) errors.push('Must have exactly one white king');
    if (blackKings !== 1) errors.push('Must have exactly one black king');
  }

  private validateActiveColor(activeColor: string, errors: string[]): void {
    if (activeColor !== 'w' && activeColor !== 'b') {
      errors.push('Active color must be "w" or "b"');
    }
  }

  private validateCastling(castling: string, errors: string[]): void {
    if (castling !== '-' && !/^[KQkq]*$/.test(castling)) {
      errors.push('Castling availability must contain only K, Q, k, q, or be "-"');
    }
  }

  private validateEnPassant(enPassant: string, errors: string[]): void {
    if (enPassant !== '-' && !/^[a-h][36]$/.test(enPassant)) {
      errors.push('En passant target must be a valid square on rank 3 or 6, or "-"');
    }
  }

  private validateHalfmove(halfmove: string, errors: string[]): void {
    const num = parseInt(halfmove, 10);
    if (isNaN(num) || num < 0) {
      errors.push('Halfmove clock must be a non-negative integer');
    }
  }

  private validateFullmove(fullmove: string, errors: string[]): void {
    const num = parseInt(fullmove, 10);
    if (isNaN(num) || num < 1) {
      errors.push('Fullmove number must be a positive integer');
    }
  }
}
```

### 3. Move Validation Service

```typescript
// services/chess/MoveValidationService.ts
import { Chess } from 'chess.js';
import type { 
  IMoveValidationService,
  ChessMoveInput,
  ChessGameState,
  MoveValidationResult,
  SquareNotation,
  ChessMove,
  PieceColor 
} from '@/types';
import { createChessMove } from '@/utils/chess.utils';

/**
 * Chess move validation service
 * Responsibility: Validate moves and calculate legal moves
 */
export class MoveValidationService implements IMoveValidationService {
  
  public validateMove(
    move: ChessMoveInput, 
    gameState: ChessGameState
  ): MoveValidationResult {
    try {
      // Create a temporary chess instance to test the move
      const chess = new Chess(gameState.fen);
      
      const testMove = chess.move({
        from: move.from,
        to: move.to,
        promotion: move.promotion || 'q'
      });

      if (!testMove) {
        // Move was rejected, try to determine why
        const reason = this.determineMoveRejectionReason(move, gameState);
        const suggestedMoves = this.getValidMoves(move.from, gameState);
        
        return {
          isValid: false,
          reason,
          suggestedMoves
        };
      }

      // Move is valid
      return {
        isValid: true
      };

    } catch (error) {
      return {
        isValid: false,
        reason: error instanceof Error ? error.message : 'Move validation failed'
      };
    }
  }

  public getValidMoves(square: SquareNotation, gameState: ChessGameState): ChessMove[] {
    try {
      const chess = new Chess(gameState.fen);
      const moves = chess.moves({ 
        square: square,
        verbose: true 
      });

      return moves.map(move => createChessMove(move, chess));
    } catch (error) {
      console.warn('Failed to get valid moves:', error);
      return [];
    }
  }

  public isSquareAttacked(
    square: SquareNotation, 
    byColor: PieceColor, 
    gameState: ChessGameState
  ): boolean {
    try {
      const chess = new Chess(gameState.fen);
      
      // Get all moves for the attacking color
      const allMoves = chess.moves({ 
        verbose: true,
        color: byColor === 'white' ? 'w' : 'b'
      });

      return allMoves.some(move => move.to === square);
    } catch (error) {
      console.warn('Failed to check square attack:', error);
      return false;
    }
  }

  private determineMoveRejectionReason(
    move: ChessMoveInput, 
    gameState: ChessGameState
  ): string {
    const piece = gameState.position.get(move.from);
    
    if (!piece) {
      return 'No piece on source square';
    }

    if (piece.color !== gameState.activeColor) {
      return `It's ${gameState.activeColor}'s turn`;
    }

    const targetPiece = gameState.position.get(move.to);
    if (targetPiece && targetPiece.color === piece.color) {
      return 'Cannot capture your own piece';
    }

    // Check if move would leave king in check
    if (this.wouldLeaveKingInCheck(move, gameState)) {
      return 'Move would leave king in check';
    }

    // More specific piece movement validation
    switch (piece.type) {
      case 'pawn':
        return this.validatePawnMove(move, gameState);
      case 'king':
        return this.validateKingMove(move, gameState);
      default:
        return 'Invalid move for piece type';
    }
  }

  private wouldLeaveKingInCheck(move: ChessMoveInput, gameState: ChessGameState): boolean {
    try {
      const chess = new Chess(gameState.fen);
      const testMove = chess.move({
        from: move.from,
        to: move.to,
        promotion: move.promotion
      });

      if (!testMove) return false;

      // If the move was legal, check if the king is in check after the move
      return chess.inCheck();
    } catch {
      return false;
    }
  }

  private validatePawnMove(move: ChessMoveInput, gameState: ChessGameState): string {
    // Implement specific pawn move validation logic
    return 'Invalid pawn move';
  }

  private validateKingMove(move: ChessMoveInput, gameState: ChessGameState): string {
    // Implement specific king move validation logic
    return 'Invalid king move';
  }
}
```

---

## Animation Service

```typescript
// services/animation/AnimationService.ts
import type { 
  IAnimationService,
  ChessMove,
  AnimationConfig 
} from '@/types';

/**
 * Chess piece animation service
 * Responsibility: Handle piece movement animations
 */
export class AnimationService implements IAnimationService {
  private activeAnimations = new Map<string, Animation>();
  private animationIdCounter = 0;

  public async createAnimation(
    move: ChessMove, 
    config: AnimationConfig
  ): Promise<void> {
    const animationId = this.generateAnimationId();
    
    return new Promise((resolve, reject) => {
      try {
        // Create animation using Web Animations API
        const element = document.querySelector(`[data-piece-id="${move.piece.id}"]`);
        
        if (!element) {
          resolve(); // Element not found, skip animation
          return;
        }

        const fromRect = this.getSquareRect(move.from);
        const toRect = this.getSquareRect(move.to);
        
        if (!fromRect || !toRect) {
          resolve(); // Couldn't find squares, skip animation
          return;
        }

        const deltaX = toRect.left - fromRect.left;
        const deltaY = toRect.top - fromRect.top;

        const animation = element.animate([
          { transform: 'translate(0, 0)' },
          { transform: `translate(${deltaX}px, ${deltaY}px)` }
        ], {
          duration: config.duration,
          easing: config.easing,
          fill: 'forwards'
        });

        this.activeAnimations.set(animationId, animation);

        animation.addEventListener('finish', () => {
          this.activeAnimations.delete(animationId);
          resolve();
        });

        animation.addEventListener('cancel', () => {
          this.activeAnimations.delete(animationId);
          reject(new Error('Animation cancelled'));
        });

      } catch (error) {
        reject(error);
      }
    });
  }

  public cancelAnimation(animationId: string): void {
    const animation = this.activeAnimations.get(animationId);
    if (animation) {
      animation.cancel();
      this.activeAnimations.delete(animationId);
    }
  }

  public cancelAllAnimations(): void {
    for (const [id, animation] of this.activeAnimations) {
      animation.cancel();
    }
    this.activeAnimations.clear();
  }

  public isAnimating(): boolean {
    return this.activeAnimations.size > 0;
  }

  private generateAnimationId(): string {
    return `animation-${++this.animationIdCounter}`;
  }

  private getSquareRect(position: ChessPosition): DOMRect | null {
    const square = document.querySelector(
      `[data-square="${position.file}${position.rank}"]`
    );
    return square?.getBoundingClientRect() || null;
  }
}
```

---

## Storage Service

```typescript
// services/storage/GameStorageService.ts
import type { 
  IGameStorageService,
  ChessGameState,
  SavedGameInfo 
} from '@/types';

/**
 * Game persistence service
 * Responsibility: Save, load, and manage game storage
 */
export class GameStorageService implements IGameStorageService {
  private readonly storageKey = 'chess-games';

  public async saveGame(gameState: ChessGameState): Promise<void> {
    try {
      const savedGames = await this.getSavedGames();
      
      const gameInfo: SavedGameInfo = {
        id: gameState.id,
        name: this.generateGameName(gameState),
        createdAt: new Date(),
        updatedAt: new Date(),
        moveCount: gameState.moveHistory.length,
        currentPosition: gameState.fen
      };

      // Update existing or add new
      const existingIndex = savedGames.findIndex(game => game.id === gameState.id);
      if (existingIndex >= 0) {
        savedGames[existingIndex] = {
          ...savedGames[existingIndex],
          ...gameInfo,
          updatedAt: new Date()
        };
      } else {
        savedGames.push(gameInfo);
      }

      // Save game data
      localStorage.setItem(`${this.storageKey}-${gameState.id}`, JSON.stringify(gameState));
      
      // Update games index
      localStorage.setItem(this.storageKey, JSON.stringify(savedGames));

    } catch (error) {
      throw new Error(`Failed to save game: ${error}`);
    }
  }

  public async loadGame(gameId: string): Promise<ChessGameState | null> {
    try {
      const gameData = localStorage.getItem(`${this.storageKey}-${gameId}`);
      
      if (!gameData) {
        return null;
      }

      return JSON.parse(gameData) as ChessGameState;
    } catch (error) {
      throw new Error(`Failed to load game: ${error}`);
    }
  }

  public async deleteGame(gameId: string): Promise<void> {
    try {
      // Remove game data
      localStorage.removeItem(`${this.storageKey}-${gameId}`);
      
      // Update games index
      const savedGames = await this.getSavedGames();
      const filteredGames = savedGames.filter(game => game.id !== gameId);
      localStorage.setItem(this.storageKey, JSON.stringify(filteredGames));

    } catch (error) {
      throw new Error(`Failed to delete game: ${error}`);
    }
  }

  public async listSavedGames(): Promise<readonly SavedGameInfo[]> {
    return this.getSavedGames();
  }

  private async getSavedGames(): Promise<SavedGameInfo[]> {
    try {
      const gamesData = localStorage.getItem(this.storageKey);
      return gamesData ? JSON.parse(gamesData) : [];
    } catch {
      return [];
    }
  }

  private generateGameName(gameState: ChessGameState): string {
    const moveCount = gameState.moveHistory.length;
    const status = gameState.isCheckmate ? 'Checkmate' 
      : gameState.isStalemate ? 'Stalemate'
      : gameState.isDraw ? 'Draw'
      : 'In Progress';
    
    return `Game ${moveCount} moves - ${status}`;
  }
}
```

---

## Service Factory and Dependency Injection

```typescript
// services/ServiceFactory.ts
import type { 
  IChessGameService,
  IFenService,
  IMoveValidationService,
  IAnimationService,
  IGameStorageService 
} from '@/types';

import { ChessGameService } from './chess/ChessGameService';
import { FenService } from './chess/FenService';
import { MoveValidationService } from './chess/MoveValidationService';
import { AnimationService } from './animation/AnimationService';
import { GameStorageService } from './storage/GameStorageService';

/**
 * Service factory for dependency injection
 * Responsibility: Create and manage service instances
 */
export class ServiceFactory {
  private static fenService: IFenService;
  private static validationService: IMoveValidationService;
  private static animationService: IAnimationService;
  private static storageService: IGameStorageService;

  public static createChessGameService(config: ChessGameConfig = {}): IChessGameService {
    return new ChessGameService(
      config,
      this.getFenService(),
      this.getValidationService()
    );
  }

  public static getFenService(): IFenService {
    if (!this.fenService) {
      this.fenService = new FenService();
    }
    return this.fenService;
  }

  public static getValidationService(): IMoveValidationService {
    if (!this.validationService) {
      this.validationService = new MoveValidationService();
    }
    return this.validationService;
  }

  public static getAnimationService(): IAnimationService {
    if (!this.animationService) {
      this.animationService = new AnimationService();
    }
    return this.animationService;
  }

  public static getStorageService(): IGameStorageService {
    if (!this.storageService) {
      this.storageService = new GameStorageService();
    }
    return this.storageService;
  }

  // For testing - inject mock services
  public static setServices(services: Partial<{
    fenService: IFenService;
    validationService: IMoveValidationService;
    animationService: IAnimationService;
    storageService: IGameStorageService;
  }>): void {
    if (services.fenService) this.fenService = services.fenService;
    if (services.validationService) this.validationService = services.validationService;
    if (services.animationService) this.animationService = services.animationService;
    if (services.storageService) this.storageService = services.storageService;
  }
}
```

This services architecture provides clean separation of business logic, comprehensive error handling, and full testability while maintaining zero React dependencies.