# TypeScript Type Definitions

## Core Chess Types

### Basic Chess Entities

```typescript
// types/chess.types.ts

/**
 * Chess piece types following standard chess notation
 */
export type PieceType = 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn';

/**
 * Chess piece colors
 */
export type PieceColor = 'white' | 'black';

/**
 * Chess files (columns) from a-h
 */
export type File = 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h';

/**
 * Chess ranks (rows) from 1-8
 */
export type Rank = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;

/**
 * Board orientation
 */
export type BoardOrientation = 'white' | 'black';

/**
 * Standard chess square notation (e.g., 'e4', 'a1')
 */
export type SquareNotation = `${File}${Rank}`;

/**
 * Chess position on the board
 */
export interface ChessPosition {
  readonly rank: Rank;
  readonly file: File;
}

/**
 * Chess piece with unique identifier
 */
export interface ChessPiece {
  readonly id: string;
  readonly type: PieceType;
  readonly color: PieceColor;
  readonly hasMoved: boolean;
}

/**
 * Castling rights for both sides
 */
export interface CastlingRights {
  readonly whiteKingside: boolean;
  readonly whiteQueenside: boolean;
  readonly blackKingside: boolean;
  readonly blackQueenside: boolean;
}

/**
 * Chess move representation
 */
export interface ChessMove {
  readonly id: string;
  readonly from: ChessPosition;
  readonly to: ChessPosition;
  readonly piece: ChessPiece;
  readonly capturedPiece?: ChessPiece;
  readonly isPromotion: boolean;
  readonly promotionPiece?: PieceType;
  readonly isCastling: boolean;
  readonly isEnPassant: boolean;
  readonly san: string; // Standard algebraic notation
  readonly fen: string; // Position after move
  readonly timestamp: Date;
}

/**
 * Chess move input for making moves
 */
export interface ChessMoveInput {
  readonly from: SquareNotation;
  readonly to: SquareNotation;
  readonly promotion?: PieceType;
}

/**
 * Result of a move attempt
 */
export interface ChessMoveResult {
  readonly success: boolean;
  readonly move?: ChessMove;
  readonly gameState: ChessGameState;
  readonly error?: string;
}

/**
 * Complete chess game state
 */
export interface ChessGameState {
  readonly id: string;
  readonly position: ReadonlyMap<SquareNotation, ChessPiece>;
  readonly activeColor: PieceColor;
  readonly castlingRights: CastlingRights;
  readonly enPassantTarget?: ChessPosition;
  readonly halfmoveClock: number;
  readonly fullmoveNumber: number;
  readonly isCheck: boolean;
  readonly isCheckmate: boolean;
  readonly isStalemate: boolean;
  readonly isDraw: boolean;
  readonly fen: string;
  readonly moveHistory: readonly ChessMove[];
  readonly lastMove?: ChessMove;
}

/**
 * Chess game configuration options
 */
export interface ChessGameConfig {
  readonly initialFen?: string;
  readonly validateMoves?: boolean;
  readonly trackHistory?: boolean;
  readonly enableUndo?: boolean;
}
```

## UI and Component Types

```typescript
// types/ui.types.ts

/**
 * Available piece sets
 */
export type PieceSet = 'classic' | 'modern' | 'tournament' | 'executive' | 'conqueror';

/**
 * Animation timing configurations
 */
export interface AnimationConfig {
  readonly duration: number;
  readonly easing: string;
  readonly stiffness?: number;
  readonly damping?: number;
}

/**
 * Square highlighting types
 */
export type HighlightType = 'selected' | 'valid-move' | 'last-move' | 'check' | 'capture';

/**
 * Square style configuration
 */
export interface SquareStyle {
  readonly backgroundColor?: string;
  readonly borderColor?: string;
  readonly borderWidth?: string;
  readonly highlightColor?: string;
}

/**
 * Custom square styles mapping
 */
export type CustomSquareStyles = Partial<Record<SquareNotation, SquareStyle>>;

/**
 * Board theme configuration
 */
export interface BoardTheme {
  readonly lightSquareColor: string;
  readonly darkSquareColor: string;
  readonly coordinateColor: string;
  readonly borderColor: string;
  readonly highlightColors: Record<HighlightType, string>;
}

/**
 * Responsive board dimensions
 */
export interface BoardDimensions {
  readonly width: number;
  readonly height: number;
  readonly squareSize: number;
}

/**
 * Drag and drop state
 */
export interface DragState {
  readonly isDragging: boolean;
  readonly draggedPiece?: ChessPiece;
  readonly draggedFrom?: ChessPosition;
  readonly dropTarget?: ChessPosition;
}

/**
 * Animation state for pieces
 */
export interface PieceAnimation {
  readonly pieceId: string;
  readonly from: ChessPosition;
  readonly to: ChessPosition;
  readonly isAnimating: boolean;
  readonly progress: number;
}
```

## Component Props Types

```typescript
// types/component.types.ts

/**
 * Base component props
 */
export interface BaseComponentProps {
  readonly className?: string;
  readonly style?: React.CSSProperties;
  readonly testId?: string;
}

/**
 * Chessboard component props
 */
export interface ChessboardProps extends BaseComponentProps {
  readonly gameState?: ChessGameState;
  readonly onMove?: (move: ChessMoveInput) => Promise<boolean> | boolean;
  readonly onSquareClick?: (position: ChessPosition) => void;
  readonly onPieceSelect?: (piece: ChessPiece, position: ChessPosition) => void;
  readonly orientation?: BoardOrientation;
  readonly pieceSet?: PieceSet;
  readonly boardWidth?: number;
  readonly showCoordinates?: boolean;
  readonly allowDragAndDrop?: boolean;
  readonly animationDuration?: number;
  readonly customSquareStyles?: CustomSquareStyles;
  readonly theme?: Partial<BoardTheme>;
  readonly disabled?: boolean;
  readonly autoResize?: boolean;
}

/**
 * Board component props
 */
export interface BoardProps extends BaseComponentProps {
  readonly gameState: ChessGameState;
  readonly orientation: BoardOrientation;
  readonly onSquareClick: (position: ChessPosition) => void;
  readonly onDragStart?: (piece: ChessPiece, position: ChessPosition) => void;
  readonly onDragEnd?: () => void;
  readonly onDrop?: (from: ChessPosition, to: ChessPosition) => void;
  readonly animatedPieces: readonly PieceAnimation[];
  readonly isAnimating: boolean;
  readonly showCoordinates: boolean;
  readonly pieceSet: PieceSet;
  readonly customSquareStyles?: CustomSquareStyles;
  readonly theme: BoardTheme;
  readonly dimensions: BoardDimensions;
}

/**
 * Square component props
 */
export interface SquareProps extends BaseComponentProps {
  readonly position: ChessPosition;
  readonly piece?: ChessPiece;
  readonly isLight: boolean;
  readonly isHighlighted: boolean;
  readonly highlightType?: HighlightType;
  readonly onClick: (position: ChessPosition) => void;
  readonly onDragStart?: (piece: ChessPiece, position: ChessPosition) => void;
  readonly onDragEnd?: () => void;
  readonly onDrop?: (position: ChessPosition) => void;
  readonly onDragOver?: (position: ChessPosition) => void;
  readonly customStyle?: SquareStyle;
  readonly theme: BoardTheme;
  readonly size: number;
  readonly showCoordinate?: boolean;
  readonly coordinatePosition?: 'top-left' | 'bottom-right';
}

/**
 * Piece component props
 */
export interface PieceProps extends BaseComponentProps {
  readonly piece: ChessPiece;
  readonly position: ChessPosition;
  readonly size: number;
  readonly pieceSet: PieceSet;
  readonly isDragging?: boolean;
  readonly isAnimating?: boolean;
  readonly animationProgress?: number;
  readonly onDragStart?: (piece: ChessPiece, position: ChessPosition) => void;
  readonly onDragEnd?: () => void;
}
```

## Hook Types

```typescript
// types/hooks.types.ts

/**
 * Chess game hook return type
 */
export interface ChessGameHook {
  readonly gameState: ChessGameState | null;
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly makeMove: (move: ChessMoveInput) => Promise<boolean>;
  readonly undoMove: () => boolean;
  readonly resetGame: (fen?: string) => void;
  readonly loadGame: (gameState: ChessGameState) => void;
  readonly isGameOver: boolean;
  readonly canUndo: boolean;
}

/**
 * Drag and drop hook configuration
 */
export interface DragAndDropConfig {
  readonly onMove: (move: ChessMoveInput) => Promise<boolean> | boolean;
  readonly gameState: ChessGameState | null;
  readonly disabled?: boolean;
  readonly allowInvalidMoves?: boolean;
}

/**
 * Drag and drop hook return type
 */
export interface DragAndDropHook {
  readonly dragState: DragState;
  readonly handleDragStart: (piece: ChessPiece, position: ChessPosition) => void;
  readonly handleDragEnd: () => void;
  readonly handleDrop: (from: ChessPosition, to: ChessPosition) => Promise<void>;
  readonly handleDragOver: (position: ChessPosition) => void;
  readonly isValidDropTarget: (position: ChessPosition) => boolean;
}

/**
 * Chess animation hook configuration
 */
export interface ChessAnimationConfig {
  readonly pieces?: ReadonlyMap<SquareNotation, ChessPiece>;
  readonly lastMove?: ChessMove;
  readonly animationConfig?: AnimationConfig;
  readonly disabled?: boolean;
}

/**
 * Chess animation hook return type
 */
export interface ChessAnimationHook {
  readonly animatedPieces: readonly PieceAnimation[];
  readonly isAnimating: boolean;
  readonly animateMove: (move: ChessMove) => Promise<void>;
  readonly cancelAnimations: () => void;
}

/**
 * Responsive board hook return type
 */
export interface ResponsiveBoardHook {
  readonly dimensions: BoardDimensions;
  readonly containerRef: React.RefObject<HTMLDivElement>;
  readonly isResizing: boolean;
  readonly orientation: BoardOrientation;
  readonly setOrientation: (orientation: BoardOrientation) => void;
}
```

## Service Types

```typescript
// types/services.types.ts

/**
 * Chess game service interface
 */
export interface IChessGameService {
  getCurrentState(): ChessGameState;
  makeMove(move: ChessMoveInput): ChessMoveResult;
  undoMove(): ChessMoveResult;
  resetGame(fen?: string): void;
  loadGame(gameState: ChessGameState): void;
  validateMove(move: ChessMoveInput): boolean;
  getValidMoves(square?: SquareNotation): ChessMove[];
  isGameOver(): boolean;
}

/**
 * FEN service interface
 */
export interface IFenService {
  parseFen(fen: string): ChessGameState;
  generateFen(gameState: ChessGameState): string;
  validateFen(fen: string): FenValidationResult;
  getDefaultFen(): string;
}

/**
 * FEN validation result
 */
export interface FenValidationResult {
  readonly isValid: boolean;
  readonly errors: readonly string[];
  readonly warnings: readonly string[];
}

/**
 * Move validation service interface
 */
export interface IMoveValidationService {
  validateMove(move: ChessMoveInput, gameState: ChessGameState): MoveValidationResult;
  getValidMoves(square: SquareNotation, gameState: ChessGameState): ChessMove[];
  isSquareAttacked(square: SquareNotation, byColor: PieceColor, gameState: ChessGameState): boolean;
}

/**
 * Move validation result
 */
export interface MoveValidationResult {
  readonly isValid: boolean;
  readonly reason?: string;
  readonly suggestedMoves?: readonly ChessMove[];
}

/**
 * Animation service interface
 */
export interface IAnimationService {
  createAnimation(move: ChessMove, config: AnimationConfig): Promise<void>;
  cancelAnimation(animationId: string): void;
  cancelAllAnimations(): void;
  isAnimating(): boolean;
}

/**
 * Game storage service interface
 */
export interface IGameStorageService {
  saveGame(gameState: ChessGameState): Promise<void>;
  loadGame(gameId: string): Promise<ChessGameState | null>;
  deleteGame(gameId: string): Promise<void>;
  listSavedGames(): Promise<readonly SavedGameInfo[]>;
}

/**
 * Saved game information
 */
export interface SavedGameInfo {
  readonly id: string;
  readonly name: string;
  readonly createdAt: Date;
  readonly updatedAt: Date;
  readonly moveCount: number;
  readonly currentPosition: string; // FEN
}
```

## Event Types

```typescript
// types/events.types.ts

/**
 * Chess game events
 */
export type ChessGameEvent = 
  | 'move'
  | 'capture'
  | 'check'
  | 'checkmate'
  | 'stalemate'
  | 'draw'
  | 'promotion'
  | 'castling'
  | 'en-passant';

/**
 * Event payload for chess moves
 */
export interface ChessMoveEvent {
  readonly type: 'move';
  readonly move: ChessMove;
  readonly gameState: ChessGameState;
}

/**
 * Event payload for game end
 */
export interface ChessGameEndEvent {
  readonly type: 'checkmate' | 'stalemate' | 'draw';
  readonly winner?: PieceColor;
  readonly reason: string;
  readonly gameState: ChessGameState;
}

/**
 * Event payload for piece capture
 */
export interface ChessCaptureEvent {
  readonly type: 'capture';
  readonly capturedPiece: ChessPiece;
  readonly capturingPiece: ChessPiece;
  readonly position: ChessPosition;
  readonly move: ChessMove;
}

/**
 * Union type for all chess events
 */
export type ChessEvent = 
  | ChessMoveEvent 
  | ChessGameEndEvent 
  | ChessCaptureEvent;

/**
 * Event handler types
 */
export type ChessEventHandler<T extends ChessEvent = ChessEvent> = (event: T) => void;

/**
 * Event emitter interface
 */
export interface IChessEventEmitter {
  on<T extends ChessEvent>(eventType: T['type'], handler: ChessEventHandler<T>): void;
  off<T extends ChessEvent>(eventType: T['type'], handler: ChessEventHandler<T>): void;
  emit<T extends ChessEvent>(event: T): void;
  removeAllListeners(): void;
}
```

## Utility Types

```typescript
// types/utility.types.ts

/**
 * Make all properties of T optional except for K
 */
export type PartialExcept<T, K extends keyof T> = Partial<T> & Pick<T, K>;

/**
 * Make all properties of T required except for K
 */
export type RequiredExcept<T, K extends keyof T> = Required<T> & Partial<Pick<T, K>>;

/**
 * Extract function type from hook return
 */
export type ExtractHookFunction<T, K extends keyof T> = T[K] extends (...args: any[]) => any ? T[K] : never;

/**
 * Deep readonly for nested objects
 */
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

/**
 * Configuration object with defaults
 */
export type WithDefaults<T, D> = T & { readonly [K in keyof D]: K extends keyof T ? T[K] : D[K] };
```