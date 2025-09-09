# Play Page Code Examples
## Source Code Reference for Implementation

This document contains all the source code examples extracted from the Play Page Implementation Plan (doc 41) for easy reference during development.

---

## Phase 1: Foundation Types

### Computer Opponent Types
```typescript
// /src/types/chess/computer-opponent.types.ts
export type ComputerDifficulty = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

export interface ComputerMoveRequest {
  fen: string;
  difficulty: ComputerDifficulty;
  timeLimit?: number;
}

export interface ComputerMoveResult {
  move: string; // UCI format: "e2e4"
  success: boolean;
  error?: string;
}

export interface ComputerOpponentConfig {
  difficulty: ComputerDifficulty;
  timeLimit: number;
  skillLevel: number; // Internal Stockfish 0-20 scale
}

export interface ComputerThinkingState {
  isThinking: boolean;
  startTime?: number;
  expectedDuration?: number;
}
```

### Play Game State Types
```typescript
// /src/types/chess/play-game.types.ts
export interface PlayGameState {
  gameState: ChessGameState;
  currentPlayer: 'white' | 'black';
  playerColor: 'white' | 'black';
  computerColor: 'white' | 'black';
  gameMode: 'human-vs-computer';
  difficulty: ComputerDifficulty;
  isComputerTurn: boolean;
  thinkingState: ComputerThinkingState;
}

export interface PlayGameActions {
  makePlayerMove: (from: string, to: string, promotion?: PieceType) => Promise<boolean>;
  requestComputerMove: () => Promise<void>;
  updateDifficulty: (level: ComputerDifficulty) => Promise<void>;
  resetGame: (playerColor?: 'white' | 'black') => void;
}

export interface GameResult {
  type: 'checkmate' | 'stalemate' | 'draw' | 'resignation' | 'ongoing';
  winner?: 'white' | 'black';
  message: string;
}

export interface GameSettings {
  playerColor: 'white' | 'black';
  difficulty: ComputerDifficulty;
  timeLimit: number;
  audioEnabled: boolean;
}
```

### UI Component Types
```typescript
// /src/types/ui/play-components.types.ts
export interface PlayerStatusProps {
  isHuman: boolean;
  color: 'white' | 'black';
  isCurrentTurn: boolean;
  isThinking?: boolean;
  capturedPieces: ChessPiece[];
}

export interface GameControlsProps {
  onNewGame: () => void;
  onResign: () => void;
  onFlipBoard: () => void;
  isGameActive: boolean;
}

export interface DifficultyLevelProps {
  currentLevel: ComputerDifficulty;
  onLevelChange: (level: ComputerDifficulty) => void;
  disabled?: boolean;
}
```

---

## Phase 2: Utilities & Constants

### Computer Chess Utils
```typescript
// /src/utils/chess/computer-chess.utils.ts
export const parseEngineMove = (move: string): { from: string; to: string; promotion?: string } => {
  if (move.length < 4) throw new Error('Invalid move format');
  
  return {
    from: move.substring(0, 2),
    to: move.substring(2, 4),
    promotion: move.length > 4 ? move[4] : undefined
  };
};

export const validateMoveFormat = (move: string): boolean => {
  const uciPattern = /^[a-h][1-8][a-h][1-8][qrbn]?$/;
  return uciPattern.test(move);
};

export const calculateThinkingTime = (difficulty: number): number => {
  // More time for higher difficulties for realism
  const baseTime = 500;
  const multiplier = 1 + (difficulty - 1) * 0.3;
  return Math.floor(baseTime * multiplier);
};

export const formatGameTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};
```

### Play Game Utils
```typescript
// /src/utils/chess/play-game.utils.ts
export const getGameResultMessage = (result: GameResult): string => {
  switch (result.type) {
    case 'checkmate':
      return result.winner === 'white' ? 'White wins by checkmate!' : 'Black wins by checkmate!';
    case 'stalemate':
      return 'Game drawn by stalemate';
    case 'draw':
      return 'Game drawn';
    case 'resignation':
      return result.winner === 'white' ? 'Black resigned - White wins!' : 'White resigned - Black wins!';
    default:
      return 'Game in progress';
  }
};

export const isPlayerTurn = (gameState: PlayGameState): boolean => {
  return gameState.currentPlayer === gameState.playerColor;
};

export const canMakeMove = (gameState: PlayGameState): boolean => {
  return !gameState.gameState.isGameOver && 
         isPlayerTurn(gameState) && 
         !gameState.thinkingState.isThinking;
};
```

### Computer Difficulty Constants
```typescript
// /src/constants/chess/computer-difficulty.constants.ts
export const DIFFICULTY_CONFIGS: Record<ComputerDifficulty, ComputerOpponentConfig> = {
  1: { difficulty: 1, timeLimit: 500, skillLevel: 0 },
  2: { difficulty: 2, timeLimit: 600, skillLevel: 2 },
  3: { difficulty: 3, timeLimit: 700, skillLevel: 4 },
  4: { difficulty: 4, timeLimit: 800, skillLevel: 6 },
  5: { difficulty: 5, timeLimit: 1000, skillLevel: 8 },
  6: { difficulty: 6, timeLimit: 1200, skillLevel: 10 },
  7: { difficulty: 7, timeLimit: 1400, skillLevel: 12 },
  8: { difficulty: 8, timeLimit: 1600, skillLevel: 14 },
  9: { difficulty: 9, timeLimit: 1800, skillLevel: 16 },
  10: { difficulty: 10, timeLimit: 2000, skillLevel: 18 }
};

export const getDifficultyDescription = (level: ComputerDifficulty): string => {
  if (level <= 2) return "Beginner (learning the rules)";
  if (level <= 4) return "Casual player (plays for fun)";  
  if (level <= 6) return "Club player (plays regularly)";
  if (level <= 8) return "Strong club player (quite good)";
  return "Expert level (very strong)";
};
```

---

## Phase 3: Business Logic Services

### Play Game Service
```typescript
// /src/services/chess/PlayGameService.ts
export class PlayGameService {
  private chessGameService: ChessGameService;
  private currentPlayer: 'white' | 'black' = 'white';
  private playerColor: 'white' | 'black' = 'white';
  private gameMode: 'human-vs-computer' | 'human-vs-human' = 'human-vs-computer';

  constructor(playerColor: 'white' | 'black' = 'white') {
    this.chessGameService = new ChessGameService();
    this.playerColor = playerColor;
  }

  // Pure business logic methods
  public makePlayerMove(from: string, to: string, promotion?: PieceType): ChessMoveResult {
    if (!this.isPlayerTurn()) {
      return { success: false, error: 'Not player turn', gameState: this.getCurrentState() };
    }
    
    return this.chessGameService.makeMove({ from, to, promotion });
  }

  public isPlayerTurn(): boolean {
    return this.currentPlayer === this.playerColor;
  }

  public isComputerTurn(): boolean {
    return this.currentPlayer !== this.playerColor && this.gameMode === 'human-vs-computer';
  }

  public switchTurn(): void {
    this.currentPlayer = this.currentPlayer === 'white' ? 'black' : 'white';
  }

  public getCurrentState(): ChessGameState {
    return this.chessGameService.getCurrentState();
  }

  public getValidMoves(square?: string): string[] {
    return this.chessGameService.getValidMoves(square);
  }

  public resetGame(fen?: string): void {
    this.chessGameService.resetGame(fen);
    this.currentPlayer = 'white';
  }
}
```

### Computer Opponent Service
```typescript
// /src/services/chess/ComputerOpponentService.ts
export class ComputerOpponentService {
  public getDifficultyConfig(level: ComputerDifficulty): ComputerOpponentConfig {
    return DIFFICULTY_CONFIGS[level];
  }

  public calculateSearchDepth(difficulty: number): number {
    // Map difficulty 1-10 to search depth
    return Math.min(3 + Math.floor(difficulty / 2), 8);
  }

  public generateThinkingDelay(difficulty: number): number {
    const config = this.getDifficultyConfig(difficulty as ComputerDifficulty);
    const baseDelay = config.timeLimit;
    const randomFactor = 0.8 + Math.random() * 0.4; // ±20% variation
    return Math.floor(baseDelay * randomFactor);
  }

  public formatComputerStatus(isThinking: boolean, level: number): string {
    if (!isThinking) return 'Ready';
    
    const description = getDifficultyDescription(level as ComputerDifficulty);
    return `Thinking... (${description})`;
  }
}
```

---

## Phase 4: External Communication

### Stockfish Engine Client
```typescript
// /src/services/clients/StockfishEngineClient.ts
export class StockfishEngineClient {
  private stockfishService: StockfishService;

  constructor() {
    this.stockfishService = getStockfishService();
  }

  public async isReady(): Promise<boolean> {
    return this.stockfishService.isEngineReady();
  }

  public async requestMove(fen: string, skillLevel: number, timeLimit: number = 1000): Promise<string | null> {
    return await this.stockfishService.getBestMoveWithPosition(fen, skillLevel, timeLimit);
  }

  public async setSkillLevel(level: number): Promise<void> {
    return await this.stockfishService.setSkillLevel(level);
  }

  public getStats() {
    return this.stockfishService.getStats();
  }
}
```

---

## Phase 5: State Management Hooks

### usePlayGame Hook
```typescript
// /src/hooks/chess/usePlayGame.ts
export const usePlayGame = (playerColor: 'white' | 'black' = 'white') => {
  const [playGameService] = useState(() => new PlayGameService(playerColor));
  const [computerClient] = useState(() => new ComputerOpponentClient());
  
  // UI state only
  const [gameState, setGameState] = useState<ChessGameState | null>(null);
  const [isComputerThinking, setIsComputerThinking] = useState(false);
  const [skillLevel, setSkillLevel] = useState(5);
  const [error, setError] = useState<string | null>(null);

  // Initialize game state
  useEffect(() => {
    setGameState(playGameService.getCurrentState());
  }, [playGameService]);

  const makeMove = useCallback(async (from: string, to: string, promotion?: PieceType): Promise<boolean> => {
    try {
      setError(null);
      
      // Use service for business logic
      const result = playGameService.makePlayerMove(from, to, promotion);
      if (!result.success) {
        setError(result.error || 'Invalid move');
        return false;
      }

      // Update UI state
      setGameState(result.gameState);
      playGameService.switchTurn();

      // Handle computer turn if needed
      if (playGameService.isComputerTurn() && !result.gameState.isGameOver) {
        await handleComputerTurn();
      }

      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Move failed');
      return false;
    }
  }, [playGameService]);

  const handleComputerTurn = useCallback(async () => {
    setIsComputerThinking(true);
    try {
      const currentState = playGameService.getCurrentState();
      const computerMove = await computerClient.requestMove(currentState.fen, skillLevel);
      
      if (computerMove) {
        // Parse UCI format and execute through service
        const from = computerMove.substring(0, 2);
        const to = computerMove.substring(2, 4);
        const promotion = computerMove.length > 4 ? computerMove[4] as PieceType : undefined;
        
        const result = playGameService.makePlayerMove(from, to, promotion);
        if (result.success) {
          setGameState(result.gameState);
          playGameService.switchTurn();
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Computer move failed');
    } finally {
      setIsComputerThinking(false);
    }
  }, [playGameService, computerClient, skillLevel]);

  const updateSkillLevel = useCallback(async (level: number) => {
    setSkillLevel(level);
    await computerClient.setSkillLevel(level);
  }, [computerClient]);

  const resetGame = useCallback((fen?: string) => {
    playGameService.resetGame(fen);
    setGameState(playGameService.getCurrentState());
    setIsComputerThinking(false);
    setError(null);
  }, [playGameService]);

  // Return UI state and actions only
  return {
    gameState,
    isComputerThinking,
    isPlayerTurn: playGameService.isPlayerTurn(),
    skillLevel,
    error,
    makeMove,
    updateSkillLevel,
    resetGame,
    getValidMoves: playGameService.getValidMoves.bind(playGameService)
  };
};
```

---

## Phase 6: UI Components

### Player Status Component
```typescript
// /src/components/play/PlayerStatus.tsx
export const PlayerStatus: React.FC<PlayerStatusProps> = ({
  isHuman,
  color,
  isCurrentTurn,
  isThinking = false,
  capturedPieces
}) => {
  return (
    <div className={`card-gaming p-4 ${isCurrentTurn ? 'ring-2 ring-blue-400' : ''}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`w-4 h-4 rounded-full ${color === 'white' ? 'bg-white' : 'bg-gray-800'} border-2`} />
          <span className="font-semibold">
            {isHuman ? 'You' : 'Computer'} ({color})
          </span>
          {isThinking && (
            <div className="flex items-center gap-2 text-blue-400">
              <Brain className="w-4 h-4 animate-pulse" />
              <span className="text-sm">Thinking...</span>
            </div>
          )}
        </div>
        <CapturedPieces pieces={capturedPieces} />
      </div>
    </div>
  );
};
```

### Game Controls Component
```typescript
// /src/components/play/GameControls.tsx
export const GameControls: React.FC<GameControlsProps> = ({
  onNewGame,
  onResign,
  onFlipBoard,
  isGameActive
}) => {
  return (
    <div className="card-gaming p-4">
      <h3 className="text-lg font-semibold mb-4">Game Controls</h3>
      <div className="flex gap-2">
        <button
          onClick={onNewGame}
          className="flex-1 glass-layout p-3 rounded-lg hover:bg-white/10 transition-colors"
        >
          <RotateCcw className="w-4 h-4 mx-auto mb-1" />
          <span className="text-sm">New Game</span>
        </button>
        
        <button
          onClick={onResign}
          disabled={!isGameActive}
          className="flex-1 glass-layout p-3 rounded-lg hover:bg-red-500/20 transition-colors disabled:opacity-50"
        >
          <Flag className="w-4 h-4 mx-auto mb-1" />
          <span className="text-sm">Resign</span>
        </button>
        
        <button
          onClick={onFlipBoard}
          className="flex-1 glass-layout p-3 rounded-lg hover:bg-white/10 transition-colors"
        >
          <RefreshCw className="w-4 h-4 mx-auto mb-1" />
          <span className="text-sm">Flip</span>
        </button>
      </div>
    </div>
  );
};
```

### Difficulty Selector Component
```typescript
// /src/components/play/DifficultySelector.tsx
export const DifficultySelector: React.FC<DifficultyLevelProps> = ({
  currentLevel,
  onLevelChange,
  disabled = false
}) => {
  return (
    <div className="card-gaming p-4">
      <h3 className="text-lg font-semibold mb-4">Difficulty Level</h3>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">Level {currentLevel}</span>
          <span className="text-xs text-gray-400">
            {getDifficultyDescription(currentLevel)}
          </span>
        </div>
        
        <div className="flex gap-1">
          {Array.from({ length: 10 }, (_, i) => i + 1).map(level => (
            <button
              key={level}
              onClick={() => onLevelChange(level as ComputerDifficulty)}
              disabled={disabled}
              className={`w-8 h-8 rounded text-xs font-bold transition-colors
                ${level <= currentLevel 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-300 text-gray-600 hover:bg-gray-200'
                }
                ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105'}
              `}
            >
              {level}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
```

---

## Phase 7: Board Integration

### Play Chessboard Component Structure
```typescript
// /src/components/play/PlayChessboard.tsx
export const PlayChessboard: React.FC = () => {
  const { gameState, makeMove, getValidMoves, isComputerThinking } = usePlayGame();
  const { boardSize, squareSize, containerRef } = useResponsiveBoard();
  const { draggedPiece, validDropTargets, handleDragStart, handleDrop } = useDragAndDrop(
    gameState, 
    makeMove, 
    getValidMoves
  );

  // 8x8 board rendering with drag & drop integration
  const renderSquare = (square: ChessPosition, piece: ChessPiece | null) => {
    const isValidTarget = validDropTargets.includes(square);
    const squareColor = getSquareColor(square);
    
    return (
      <div
        key={square}
        data-square={square}
        className={`
          relative flex items-center justify-center
          ${squareColor === 'light' ? 'bg-amber-100' : 'bg-amber-800'}
          ${isValidTarget ? 'ring-2 ring-green-400' : ''}
          ${isComputerThinking ? 'pointer-events-none' : ''}
        `}
        style={{ width: squareSize, height: squareSize }}
      >
        {piece && (
          <img
            src={getPieceImagePath(piece.color, piece.type)}
            alt={`${piece.color} ${piece.type}`}
            draggable={false}
            onMouseDown={(e) => !isComputerThinking && handleDragStart(e, piece, square)}
            className="w-4/5 h-4/5 cursor-grab"
          />
        )}
        {isValidTarget && (
          <div className="absolute inset-2 rounded-full bg-green-400/30" />
        )}
      </div>
    );
  };

  return (
    <div ref={containerRef} className="relative">
      <div 
        className="grid grid-cols-8 border-2 border-amber-900"
        style={{ width: boardSize.width, height: boardSize.height }}
      >
        {generateSquareList('white').map(square => {
          const piece = gameState?.pieces[square] || null;
          return renderSquare(square as ChessPosition, piece);
        })}
      </div>
    </div>
  );
};
```

---

## Phase 8: Play Page Assembly

### Complete Play Page Structure
```typescript
// /src/pages/PlayPage.tsx
export const PlayPage: React.FC = () => {
  const { 
    gameState, 
    isComputerThinking, 
    skillLevel, 
    updateSkillLevel, 
    resetGame, 
    error 
  } = usePlayGame('white');
  
  const { setInstructions } = useInstructions();
  const { playMove, playCheck, playGameStart } = useChessAudio();

  // Initialize instructions
  useEffect(() => {
    setInstructions("Play Chess vs Computer", [
      "Drag pieces or click to move against the computer opponent",
      "Adjust difficulty level from 1 (beginner) to 10 (expert)",
      "Use game controls to start new games or resign",
      "Listen for audio feedback on moves and game events"
    ]);
  }, [setInstructions]);

  // Game event handlers
  const handleNewGame = useCallback(() => {
    resetGame();
    playGameStart();
  }, [resetGame, playGameStart]);

  const handleDifficultyChange = useCallback(async (level: ComputerDifficulty) => {
    await updateSkillLevel(level);
  }, [updateSkillLevel]);

  // Extract captured pieces
  const computerCaptured = gameState?.capturedPieces.filter(p => p.color === 'white') || [];
  const playerCaptured = gameState?.capturedPieces.filter(p => p.color === 'black') || [];

  return (
    <div className="space-y-6">
      {/* Computer status */}
      <PlayerStatus
        isHuman={false}
        color="black"
        isCurrentTurn={gameState?.activeColor === 'black'}
        isThinking={isComputerThinking}
        capturedPieces={computerCaptured}
      />

      {/* Main chessboard */}
      <div className="flex justify-center">
        <PlayChessboard />
      </div>

      {/* Player status */}
      <PlayerStatus
        isHuman={true}
        color="white"
        isCurrentTurn={gameState?.activeColor === 'white'}
        capturedPieces={playerCaptured}
      />

      {/* Controls sidebar */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <GameControls
          onNewGame={handleNewGame}
          onResign={() => resetGame()}
          onFlipBoard={() => {}} // TODO: Board orientation
          isGameActive={!gameState?.isGameOver}
        />
        
        <DifficultySelector
          currentLevel={skillLevel}
          onLevelChange={handleDifficultyChange}
          disabled={isComputerThinking}
        />
      </div>

      {/* Error display */}
      {error && (
        <div className="card-gaming p-4 bg-red-500/20 border border-red-500/50">
          <p className="text-red-300">{error}</p>
        </div>
      )}
    </div>
  );
};
```

---

## Integration Patterns

### Hook Combination Pattern
```typescript
// Complete hook integration for Play page
const { gameState, makeMove, getValidMoves, resetGame, error } = useChessGame();
const { isReady, isThinking, requestMove, setSkillLevel } = useStockfish();
const { boardSize, squareSize, containerRef } = useResponsiveBoard();
const { draggedPiece, validDropTargets, handleDragStart, handleDrop } = useDragAndDrop(
  gameState, 
  makeMove, 
  getValidMoves
);
```

### Audio Integration Pattern
```typescript
// Audio integration in move handlers
if (result.newGameState.gameStatus === 'checkmate') {
  playGameStart(); // Using game start as "game over" sound
} else if (result.newGameState.gameStatus === 'check') {
  playCheck();
} else {
  playMove(!!result.capturedPiece);  // Boolean for capture sound
}
```

## Phase 3: Navigation Integration

### Placeholder PlayPage (Phase 3 Only)
```typescript
// /src/pages/PlayPage.tsx - SIMPLE PLACEHOLDER FOR PHASE 3
import React, { useEffect } from 'react';
import { useInstructions } from '../contexts/InstructionsContext';

export const PlayPage: React.FC = () => {
  const { setInstructions } = useInstructions();

  useEffect(() => {
    setInstructions("Play Chess vs Computer - Coming Soon", [
      "This page will feature human vs computer chess gameplay",
      "Computer opponent with 10 difficulty levels (1-10)",
      "Full drag & drop chessboard interface",
      "Audio feedback and professional game controls",
      "Currently under development..."
    ]);
  }, [setInstructions]);

  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="card-gaming p-8 text-center max-w-md">
        <h1 className="text-2xl font-bold mb-4">Play vs Computer</h1>
        <p className="text-muted-foreground mb-6">
          Professional chess gameplay with AI opponent coming soon!
        </p>
        <div className="space-y-2 text-sm text-muted-foreground">
          <p>🎯 10 difficulty levels</p>
          <p>🎵 Audio feedback</p>
          <p>🎮 Drag & drop interface</p>
          <p>🤖 Stockfish AI engine</p>
        </div>
      </div>
    </div>
  );
};
```

### Navigation Integration
```typescript
// Add to components/layout/types.ts
export type TabId = 'layout' | 'worker' | 'drag' | 'slots' | 'play'

// Add to App.tsx routing
{selectedTab === 'play' && <PlayPage />}

// Add to TabBar.tsx tabs array
{ 
  id: 'play', 
  label: 'Play', 
  icon: Target, // Or chess piece icon when available
  description: 'vs Computer'
}

// Add to pages/index.ts
export { PlayPage } from './PlayPage'
```

**⚠️ Note**: This is the Phase 3 placeholder implementation only. The full PlayPage with game logic is implemented in Phase 10.

---

This code reference provides all the implementation patterns needed to build the Play page following the architectural guidelines established in the existing codebase.