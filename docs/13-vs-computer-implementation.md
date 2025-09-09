# VS Computer Page Implementation

## Overview

This document outlines the implementation of a dedicated VS Computer demo page featuring human vs computer gameplay using Stockfish.js integration. This creates a sophisticated standalone chess application that showcases the chessboard-vanilla-v2 library's capabilities with AI opponent functionality, requiring no backend infrastructure.

## Executive Summary

**Goal**: Create a dedicated VS Computer demo page that demonstrates:

- Human vs Computer gameplay with Stockfish.js AI
- Multiple difficulty levels (10 levels from Beginner to Master)
- Professional computer opponent with realistic thinking behavior
- Clean UI focused on AI gameplay experience
- Complete chessboard-vanilla-v2 library integration with AI

**Key Technologies**:

- **chess.js**: Game logic and move validation
- **Stockfish.js**: World-class computer opponent
- **chessboard-vanilla-v2**: Core chessboard component
- **React + TypeScript**: Modern component architecture

## Architecture Overview

### ASCII Page Mockup (Large Chessboard with Minimal UI)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Responsive Chessboard Examples                              [@demo] ▼    │
├──┬──────────────────────────────────────────────────────────────────────┤
│▼ │                      VS Computer Chess Demo                          │
│🏠│                                                                       │
│♟️│  ┌─ CONTROLS ────────────────────────────────────────────────────┐   │
│🎮│  │ [≡] New | Reset | Play As: White ▼ | AI Level: 5 ▼ | 🤖 Ready │   │
│🎯│  └─────────────────────────────────────────────────────────────────┘   │
│  │                                                                       │
│  │                                                                       │
│  │  🤖 Stockfish Level 5  ⚫ Black  ⏱️ 02:15  🧠 Thinking...              │
│  │                                                                       │
│  │              ┌─────────────────────────────────────────┐               │
│  │              │                                         │               │
│  │              │                                         │               │
│  │              │              CHESSBOARD                 │               │
│  │              │            (HERO ELEMENT)               │               │
│  │              │          (DOMINATES PAGE)               │               │
│  │              │                                         │               │
│  │              │      ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜                  │               │
│  │              │      ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟                  │               │
│  │              │      ░ ■ ░ ■ ░ ■ ░ ■                  │               │
│  │              │      ■ ░ ■ ░ ■ ░ ■ ░                  │               │
│  │              │      ░ ■ ░ ■ ░ ■ ░ ■                  │               │
│  │              │      ■ ░ ■ ░ ■ ░ ■ ░                  │               │
│  │              │      ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙                  │               │
│  │              │      ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖                  │               │
│  │              │          a b c d e f g h               │               │
│  │              │                                         │               │
│  │              └─────────────────────────────────────────┘               │
│  │                                                                       │
│  │  👤 You (Human)  ⚪ White  ⏱️ 03:45  🎯 Your Turn                       │
│  │                                                                       │
│  │  Move 5 • Opening: Ruy Lopez • 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6...     │
│  │                                                                       │
└──┴───────────────────────────────────────────────────────────────────────────┘
```

### Layout Principles (Chessboard-Dominant Design)

**🎯 Massive Chessboard Focus:**

- **Chessboard takes 80%+ of screen space**: True hero element that dominates the page
- **Central positioning**: Board centered with generous margins around it
- **Perfect square aspect**: Maintains proper chess proportions at large size

**📱 Minimal UI Approach:**

- **Compact top toolbar**: Essential controls in single row (New, Reset, Color, AI Level)
- **Streamlined player info**: Simple status lines above/below board (not bulky cards)
- **Single info strip**: Move history and game status in one compact line

**⏰ Essential Chess Elements:**

- **Computer status line** (above board): AI level, color, timer, thinking indicator
- **Human status line** (below board): Your color, timer, turn indicator
- **Game info strip** (bottom): Move number, opening, recent moves in single line

**🎮 Progressive Disclosure:**

- **Collapsed by default**: Only essential info visible during gameplay
- **[≡] Expand when needed**: Click to reveal advanced settings panel
- **Focus on chess**: UI gets out of the way to let you focus on the game

**🎨 Clean Professional Design:**

- **Minimal visual competition**: Nothing competes with the chessboard for attention
- **Information hierarchy**: Board > Player status > Game info > Controls
- **Smooth animations**: Subtle transitions for thinking states and turn changes
- **Responsive scaling**: Board scales appropriately for different screen sizes

### Component Hierarchy

```
VSComputerPage.tsx                   # Main VS Computer page container
├── PlayerCard.tsx                   # Human/Computer player information cards
│   ├── HumanPlayerCard.tsx          # Your color, turn status, interaction hints
│   └── ComputerPlayerCard.tsx       # AI level, thinking status, search depth
├── ChessboardDemo.tsx               # Central chessboard with AI game state
├── GameControls.tsx                 # Essential game actions (top-right)
├── DifficultySelector.tsx           # AI strength selection (center-right)
├── MoveHistory.tsx                  # Notation with export (bottom-right)
├── GameStatusBar.tsx                # Full-width status information (bottom)
└── ComputerThinking.tsx             # Animated thinking indicator overlay
```

### State Management Architecture

```typescript
// VS Computer game state
interface VSComputerGameState {
  // Core game state
  chess: Chess; // chess.js instance
  playerColor: "white" | "black"; // Human player color (computer plays opposite)

  // Computer opponent
  computerDifficulty: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
  isComputerThinking: boolean;
  computerThinkingTime: number; // ms for realistic thinking delay

  // Game status
  gameStatus: "playing" | "checkmate" | "stalemate" | "draw" | "resigned";
  currentPlayer: "white" | "black";
  isGameOver: boolean;
  gameResult?: string;
  winner?: "human" | "computer" | "draw";

  // UI state
  selectedSquare: string | null;
  validMoves: string[];
  lastMove: { from: string; to: string } | null;
  moveHistory: string[];
}
```

## Architecture-Compliant Implementation

Following the established architecture guide, we'll properly separate concerns:

### Installation and Setup

```bash
cd /mnt/c/Projects/chessboard-vanilla-v2/example-v2
npm install stockfish
```

### Layer 1: Types (Domain Organized)

```typescript
// src/types/chess/computer-opponent.types.ts
export type ComputerDifficulty = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

export interface ComputerMoveRequest {
  readonly fen: string;
  readonly difficulty: ComputerDifficulty;
  readonly timeLimit: number;
}

export interface ComputerMoveResult {
  readonly success: boolean;
  readonly move?: string;
  readonly error?: string;
  readonly thinkingTime: number;
}

export interface ComputerOpponentConfig {
  readonly difficulty: ComputerDifficulty;
  readonly thinkingDelay: number;
  readonly depth: number;
}
```

```typescript
// src/types/demo/vs-computer.types.ts
export interface VSComputerGameState {
  readonly chess: Chess;
  readonly playerColor: "white" | "black";
  readonly computerDifficulty: ComputerDifficulty;
  readonly isComputerThinking: boolean;
  readonly gameStatus:
    | "playing"
    | "checkmate"
    | "stalemate"
    | "draw"
    | "resigned";
  readonly currentPlayer: "white" | "black";
  readonly isGameOver: boolean;
  readonly winner?: "human" | "computer" | "draw";
  readonly selectedSquare: string | null;
  readonly validMoves: string[];
  readonly lastMove: { from: string; to: string } | null;
  readonly moveHistory: string[];
}
```

### Layer 2: Services & Clients (Business Logic Separated)

#### Computer Chess Service (Business Logic)

```typescript
// src/services/chess/ComputerChessService.ts
import type {
  ComputerOpponentConfig,
  ComputerDifficulty,
} from "../../types/chess/computer-opponent.types";

export class ComputerChessService {
  /**
   * Calculate search depth for difficulty level
   * Pure business logic - no external dependencies
   */
  static getDifficultyConfig(
    difficulty: ComputerDifficulty
  ): ComputerOpponentConfig {
    const configs: Record<ComputerDifficulty, ComputerOpponentConfig> = {
      1: { difficulty: 1, thinkingDelay: 500, depth: 1 }, // Beginner
      2: { difficulty: 2, thinkingDelay: 700, depth: 2 }, // Beginner
      3: { difficulty: 3, thinkingDelay: 900, depth: 3 }, // Easy
      4: { difficulty: 4, thinkingDelay: 1100, depth: 4 }, // Easy-Medium
      5: { difficulty: 5, thinkingDelay: 1300, depth: 6 }, // Medium
      6: { difficulty: 6, thinkingDelay: 1500, depth: 8 }, // Medium-Hard
      7: { difficulty: 7, thinkingDelay: 1700, depth: 10 }, // Hard
      8: { difficulty: 8, thinkingDelay: 1900, depth: 12 }, // Hard
      9: { difficulty: 9, thinkingDelay: 2100, depth: 15 }, // Expert
      10: { difficulty: 10, thinkingDelay: 2300, depth: 18 }, // Master
    };

    return configs[difficulty];
  }

  /**
   * Validate computer move format
   */
  static validateMoveFormat(move: string): boolean {
    // e2e4, a7a8q format validation
    const moveRegex = /^[a-h][1-8][a-h][1-8][qrbn]?$/;
    return moveRegex.test(move);
  }

  /**
   * Parse engine move to from/to format
   */
  static parseEngineMove(engineMove: string): {
    from: string;
    to: string;
    promotion?: string;
  } {
    if (!this.validateMoveFormat(engineMove)) {
      throw new Error(`Invalid move format: ${engineMove}`);
    }

    const from = engineMove.substring(0, 2);
    const to = engineMove.substring(2, 4);
    const promotion =
      engineMove.length > 4 ? engineMove.substring(4) : undefined;

    return { from, to, promotion };
  }
}
```

#### Stockfish Client (External Communication)

```typescript
// src/services/clients/StockfishClient.ts
import type {
  ComputerMoveRequest,
  ComputerMoveResult,
} from "../../types/chess/computer-opponent.types";

export class StockfishClient {
  private stockfish: Worker | null = null;
  private isReady: boolean = false;
  private isInitialized: boolean = false;

  /**
   * Initialize Stockfish engine worker
   * Handles external resource (Worker) creation
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    return new Promise((resolve, reject) => {
      try {
        this.stockfish = new Worker("/stockfish/stockfish.js");

        this.stockfish.onmessage = (event) => {
          if (event.data === "uciok") {
            this.isReady = true;
            this.isInitialized = true;
            resolve();
          }
        };

        this.stockfish.postMessage("uci");
      } catch (error) {
        reject(new Error(`Stockfish initialization failed: ${error}`));
      }
    });
  }

  /**
   * Request best move from Stockfish engine
   * Pure external communication - no business logic
   */
  async getBestMove(request: ComputerMoveRequest): Promise<ComputerMoveResult> {
    const startTime = Date.now();

    if (!this.stockfish || !this.isReady) {
      return {
        success: false,
        error: "Stockfish engine not ready",
        thinkingTime: 0,
      };
    }

    return new Promise((resolve) => {
      let bestMove = "";
      let resolved = false;

      const messageHandler = (event: MessageEvent) => {
        const message = event.data;

        if (message.startsWith("bestmove") && !resolved) {
          resolved = true;
          bestMove = message.split(" ")[1];
          this.stockfish!.removeEventListener("message", messageHandler);

          const thinkingTime = Date.now() - startTime;

          if (bestMove && bestMove !== "(none)") {
            resolve({
              success: true,
              move: bestMove,
              thinkingTime,
            });
          } else {
            resolve({
              success: false,
              error: "No valid move found",
              thinkingTime,
            });
          }
        }
      };

      this.stockfish.addEventListener("message", messageHandler);

      // Send position and search command
      this.stockfish.postMessage(`position fen ${request.fen}`);
      this.stockfish.postMessage(
        `go depth ${this.calculateDepth(request.difficulty)}`
      );

      // Timeout fallback
      setTimeout(() => {
        if (!resolved) {
          resolved = true;
          this.stockfish!.removeEventListener("message", messageHandler);
          resolve({
            success: false,
            error: "Engine timeout",
            thinkingTime: Date.now() - startTime,
          });
        }
      }, request.timeLimit);
    });
  }

  /**
   * Calculate search depth based on difficulty
   * Simple mapping logic for client layer
   */
  private calculateDepth(difficulty: number): number {
    return Math.min(Math.max(difficulty * 2, 1), 18);
  }

  /**
   * Cleanup external resources
   */
  destroy(): void {
    if (this.stockfish) {
      this.stockfish.terminate();
      this.stockfish = null;
    }
    this.isReady = false;
    this.isInitialized = false;
  }
}
```

## Enhanced Hooks Architecture

### Layer 3: Hooks (Architecture Compliant)

#### useVSComputerState Hook

```typescript
// src/hooks/demo/useVSComputerState.ts
import { useState, useCallback, useEffect, useRef } from "react";
import { Chess } from "chess.js";
import { ChessGameService } from "../../services/chess/ChessGameService";
import { ComputerChessService } from "../../services/chess/ComputerChessService";
import { StockfishClient } from "../../services/clients/StockfishClient";
import type { VSComputerGameState } from "../../types/demo/vs-computer.types";
import type {
  ComputerDifficulty,
  ComputerMoveRequest,
} from "../../types/chess/computer-opponent.types";
import type { ChessMoveInput } from "../../types/chess/chess.types";

/**
 * VS Computer game state management hook
 * Architecture compliant: Uses services for business logic, clients for external communication
 */
export const useVSComputerState = () => {
  // Service and client references (proper architecture)
  const chessServiceRef = useRef<ChessGameService>();
  const stockfishClientRef = useRef(new StockfishClient());

  // Game state (React state only)
  const [gameState, setGameState] = useState<VSComputerGameState>({
    chess: new Chess(),
    playerColor: "white",
    computerDifficulty: 5,
    isComputerThinking: false,
    gameStatus: "playing",
    currentPlayer: "white",
    isGameOver: false,
    selectedSquare: null,
    validMoves: [],
    lastMove: null,
    moveHistory: [],
  });

  // Loading and error states
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize services and clients
  useEffect(() => {
    const initializeServices = async () => {
      try {
        // Initialize chess service (business logic)
        chessServiceRef.current = new ChessGameService();

        // Initialize Stockfish client (external communication)
        await stockfishClientRef.current.initialize();

        // Set initial game state using service
        const initialState = chessServiceRef.current.getCurrentState();
        setGameState((prev) => ({
          ...prev,
          chess: chessServiceRef.current!.getChessInstance(),
        }));

        setIsLoading(false);
      } catch (error) {
        setError(
          error instanceof Error ? error.message : "Initialization failed"
        );
        setIsLoading(false);
      }
    };

    initializeServices();

    // Cleanup
    return () => {
      stockfishClientRef.current.destroy();
    };
  }, []);

  /**
   * Make a move on the board
   */
  const makeMove = useCallback(
    async (from: string, to: string) => {
      try {
        // Attempt the move
        const move = chess.move({ from, to, promotion: "q" });
        if (!move) return false;

        // Update game state
        const newState = {
          ...gameState,
          currentPlayer: chess.turn() === "w" ? "white" : "black",
          lastMove: { from, to },
          moveHistory: chess.history(),
          selectedSquare: null,
          validMoves: [],
          isGameOver: chess.isGameOver(),
          gameStatus: getGameStatus(chess),
        };

        setGameState(newState);

        // If computer's turn and game not over
        if (
          !newState.isGameOver &&
          ((newState.playerColor === "white" &&
            newState.currentPlayer === "black") ||
            (newState.playerColor === "black" &&
              newState.currentPlayer === "white"))
        ) {
          await makeComputerMove(newState);
        }

        return true;
      } catch (error) {
        console.error("Move error:", error);
        return false;
      }
    },
    [chess, gameState, stockfish]
  );

  /**
   * Make computer move
   */
  const makeComputerMove = useCallback(
    async (currentState: VSComputerGameState) => {
      setGameState((prev) => ({ ...prev, isComputerThinking: true }));

      try {
        // Add realistic thinking delay
        const thinkingDelay = stockfish.getThinkingDelay(
          currentState.computerDifficulty
        );
        await new Promise((resolve) => setTimeout(resolve, thinkingDelay));

        // Get best move from Stockfish
        const bestMove = await stockfish.getBestMove(
          chess.fen(),
          currentState.computerDifficulty,
          3000
        );

        if (bestMove && bestMove !== "(none)") {
          // Parse move (e.g., "e2e4" -> from: "e2", to: "e4")
          const from = bestMove.substring(0, 2);
          const to = bestMove.substring(2, 4);
          const promotion =
            bestMove.length > 4 ? bestMove.substring(4) : undefined;

          // Make computer move
          const move = chess.move({ from, to, promotion: promotion || "q" });

          if (move) {
            setGameState((prev) => ({
              ...prev,
              currentPlayer: chess.turn() === "w" ? "white" : "black",
              lastMove: { from, to },
              moveHistory: chess.history(),
              isGameOver: chess.isGameOver(),
              gameStatus: getGameStatus(chess),
              isComputerThinking: false,
            }));
          }
        }
      } catch (error) {
        console.error("Computer move error:", error);
        setGameState((prev) => ({ ...prev, isComputerThinking: false }));
      }
    },
    [chess, stockfish]
  );

  /**
   * Start new game
   */
  const newGame = useCallback(
    (playerColor: "white" | "black" = "white") => {
      chess.reset();

      setGameState({
        ...gameState,
        chess,
        playerColor,
        currentPlayer: "white",
        isGameOver: false,
        gameStatus: "playing",
        selectedSquare: null,
        validMoves: [],
        lastMove: null,
        moveHistory: [],
        isComputerThinking: false,
      });

      // If computer plays white (human chose black), make first move
      if (playerColor === "black") {
        setTimeout(() => {
          makeComputerMove({
            ...gameState,
            playerColor,
            currentPlayer: "white",
          });
        }, 500);
      }
    },
    [gameState, chess, makeComputerMove]
  );

  /**
   * Set computer difficulty
   */
  const setDifficulty = useCallback((difficulty: ComputerDifficulty) => {
    setGameState((prev) => ({
      ...prev,
      computerDifficulty: difficulty,
    }));
  }, []);

  /**
   * Select square and get valid moves
   */
  const selectSquare = useCallback(
    (square: string) => {
      if (gameState.isComputerThinking || gameState.isGameOver) return;

      // If clicking same square, deselect
      if (gameState.selectedSquare === square) {
        setGameState((prev) => ({
          ...prev,
          selectedSquare: null,
          validMoves: [],
        }));
        return;
      }

      // If square selected and clicking different square, try to move
      if (gameState.selectedSquare) {
        makeMove(gameState.selectedSquare, square);
        return;
      }

      // Select new square and show valid moves (only human player's pieces)
      const piece = chess.get(square as any);
      if (
        piece &&
        piece.color === (gameState.playerColor === "white" ? "w" : "b")
      ) {
        const moves = chess.moves({ square: square as any, verbose: true });
        const validMoves = moves.map((move) => move.to);

        setGameState((prev) => ({
          ...prev,
          selectedSquare: square,
          validMoves,
        }));
      }
    },
    [chess, gameState, makeMove]
  );

  return {
    gameState,
    makeMove,
    newGame,
    setDifficulty,
    selectSquare,
    // Derived state
    currentFen: chess.fen(),
    isPlayerTurn: gameState.currentPlayer === gameState.playerColor,
    canMakeMove:
      !gameState.isComputerThinking &&
      !gameState.isGameOver &&
      gameState.currentPlayer === gameState.playerColor,
  };
};

/**
 * Determine game status from chess instance
 */
function getGameStatus(chess: Chess): VSComputerGameState["gameStatus"] {
  if (chess.isCheckmate()) return "checkmate";
  if (chess.isStalemate()) return "stalemate";
  if (chess.isDraw()) return "draw";
  return "playing";
}
```

## UI Components Implementation

### Player Color Selector

```typescript
// src/components/demo/PlayerColorSelector.tsx
import React from "react";
import { Button } from "../ui/Button";
import { Circle, CircleDot } from "lucide-react";

interface PlayerColorSelectorProps {
  playerColor: "white" | "black";
  onColorChange: (color: "white" | "black") => void;
  disabled?: boolean;
}

export const PlayerColorSelector: React.FC<PlayerColorSelectorProps> = ({
  playerColor,
  onColorChange,
  disabled = false,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-stone-700 dark:text-stone-300">
        Play as
      </label>
      <div className="flex space-x-2">
        <Button
          variant={playerColor === "white" ? "default" : "secondary"}
          onClick={() => onColorChange("white")}
          disabled={disabled}
          className="flex items-center space-x-2"
        >
          <Circle className="w-4 h-4 fill-white stroke-stone-600" />
          <span>White</span>
        </Button>

        <Button
          variant={playerColor === "black" ? "default" : "secondary"}
          onClick={() => onColorChange("black")}
          disabled={disabled}
          className="flex items-center space-x-2"
        >
          <CircleDot className="w-4 h-4 fill-stone-800 stroke-stone-800" />
          <span>Black</span>
        </Button>
      </div>
    </div>
  );
};
```

### Difficulty Selector

```typescript
// src/components/demo/DifficultySelector.tsx
import React from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/Select";
import type { ComputerDifficulty } from "../../types/demo/freeplay.types";

interface DifficultySelectorProps {
  difficulty: ComputerDifficulty;
  onDifficultyChange: (difficulty: ComputerDifficulty) => void;
  disabled?: boolean;
}

const DIFFICULTY_LABELS = {
  1: "Beginner (Depth 1)",
  2: "Beginner (Depth 2)",
  3: "Easy (Depth 3)",
  4: "Easy-Medium (Depth 4)",
  5: "Medium (Depth 6)",
  6: "Medium-Hard (Depth 8)",
  7: "Hard (Depth 10)",
  8: "Hard (Depth 12)",
  9: "Expert (Depth 15)",
  10: "Master (Depth 18)",
} as const;

export const DifficultySelector: React.FC<DifficultySelectorProps> = ({
  difficulty,
  onDifficultyChange,
  disabled = false,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-stone-700 dark:text-stone-300">
        Computer Difficulty
      </label>
      <Select
        value={difficulty.toString()}
        onValueChange={(value) =>
          onDifficultyChange(Number(value) as ComputerDifficulty)
        }
        disabled={disabled}
      >
        <SelectTrigger className="w-full">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {Object.entries(DIFFICULTY_LABELS).map(([level, label]) => (
            <SelectItem key={level} value={level}>
              {label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};
```

### VS Computer Page

```typescript
// src/pages/demo/VSComputerPage.tsx
import React from "react";
import { Chessboard } from "chessboard-vanilla-v2";
import "chessboard-vanilla-v2/styles";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { PlayerColorSelector } from "../../components/demo/PlayerColorSelector";
import { DifficultySelector } from "../../components/demo/DifficultySelector";
import { GameStatus } from "../../components/demo/GameStatus";
import { MoveHistory } from "../../components/demo/MoveHistory";
import { useVSComputerState } from "../../hooks/demo/useVSComputerState";
import { RotateCcw, Play, Flag, Lightbulb } from "lucide-react";

export const VSComputerPage: React.FC = () => {
  const {
    gameState,
    makeMove,
    newGame,
    setDifficulty,
    selectSquare,
    currentFen,
    isPlayerTurn,
    canMakeMove,
  } = useVSComputerState();

  const handleSquareClick = (square: string) => {
    if (canMakeMove && isPlayerTurn) {
      selectSquare(square);
    }
  };

  const handleMove = (from: string, to: string) => {
    if (canMakeMove && isPlayerTurn) {
      return makeMove(from, to);
    }
    return false;
  };

  const handleNewGame = () => {
    newGame(gameState.playerColor);
  };

  const handleColorChange = (color: "white" | "black") => {
    newGame(color);
  };

  return (
    <div className="flex-1 overflow-y-auto">
      {/* Page Header */}
      <div className="border-b border-stone-200 dark:border-stone-800 bg-stone-50/80 dark:bg-stone-900/80 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold text-stone-900 dark:text-stone-100 mb-2">
            VS Computer Chess Demo
          </h1>
          <p className="text-stone-600 dark:text-stone-400">
            Challenge a world-class computer opponent powered by Stockfish.js
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Chessboard - Main Focus (3 columns on large screens) */}
            <div className="lg:col-span-3">
              <Card className="overflow-hidden">
                <CardContent className="p-6">
                  <div className="aspect-square max-w-2xl mx-auto">
                    <Chessboard
                      initialFen={currentFen}
                      onMove={handleMove}
                      onSquareClick={handleSquareClick}
                      pieceSet="modern"
                      boardTheme="brown"
                      showCoordinates={true}
                      animationsEnabled={true}
                      allowDragAndDrop={canMakeMove && isPlayerTurn}
                      selectedSquare={gameState.selectedSquare}
                      validMoves={gameState.validMoves}
                      lastMove={gameState.lastMove}
                      className="w-full h-full"
                    />
                  </div>

                  {/* Computer Thinking Indicator */}
                  {gameState.isComputerThinking && (
                    <div className="mt-4 text-center">
                      <div className="inline-flex items-center space-x-2 text-chess-royal">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-chess-royal"></div>
                        <span className="text-sm font-medium">
                          Computer is thinking...
                        </span>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Control Panel (1 column on large screens) */}
            <div className="space-y-4">
              {/* Game Controls */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Game Controls</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Player Color Selection */}
                  <PlayerColorSelector
                    playerColor={gameState.playerColor}
                    onColorChange={handleColorChange}
                    disabled={
                      !gameState.isGameOver && gameState.moveHistory.length > 0
                    }
                  />

                  {/* Computer Difficulty */}
                  <DifficultySelector
                    difficulty={gameState.computerDifficulty}
                    onDifficultyChange={setDifficulty}
                    disabled={gameState.isComputerThinking}
                  />

                  {/* Action Buttons */}
                  <div className="space-y-2">
                    <Button
                      onClick={handleNewGame}
                      className="w-full"
                      variant="default"
                    >
                      <Play className="w-4 h-4 mr-2" />
                      New Game
                    </Button>

                    <Button
                      onClick={() => {
                        /* TODO: Implement resign */
                      }}
                      className="w-full"
                      variant="secondary"
                      disabled={gameState.isGameOver}
                    >
                      <Flag className="w-4 h-4 mr-2" />
                      Resign
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Game Status */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Game Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <GameStatus
                    currentPlayer={gameState.currentPlayer}
                    gameStatus={gameState.gameStatus}
                    isComputerThinking={gameState.isComputerThinking}
                    playerColor={gameState.playerColor}
                    winner={gameState.winner}
                  />
                </CardContent>
              </Card>

              {/* Move History */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Move History</CardTitle>
                </CardHeader>
                <CardContent>
                  <MoveHistory
                    moves={gameState.moveHistory}
                    currentMoveIndex={gameState.moveHistory.length - 1}
                  />
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VSComputerPage;
```

## Implementation Timeline (Architecture Compliant)

Following the **Priority 1-5 Architecture Pattern** from the guide:

### Priority 1: Foundation Layer (1 hour)

1. **Types**: Create domain-organized types in `types/chess/` and `types/demo/`
   - `computer-opponent.types.ts` - Computer opponent interfaces
   - `vs-computer.types.ts` - VS Computer game state types
2. **Utils**: Create chess utility functions in `utils/chess/`
   - `computer-chess.utils.ts` - Move parsing and validation utilities
3. **Constants**: Create domain constants in `constants/chess/`
   - `computer-difficulty.constants.ts` - Difficulty level configurations

**Why First**: Everything depends on these foundations. No circular dependencies.

### Priority 2: Infrastructure Layer (2 hours)

1. **Services**: Business logic in `services/chess/`
   - `ComputerChessService.ts` - Computer opponent business logic
2. **Clients**: External communication in `services/clients/`
   - `StockfishClient.ts` - Stockfish Worker communication
3. **Add Stockfish.js dependency** and configure asset loading

**Why Second**: Provides business logic and external communication. Hooks will consume these.

### Priority 3: Data Layer (1 hour)

1. **Hooks**: State management in `hooks/demo/`
   - `useVSComputerState.ts` - Computer opponent game state
2. **Integration**: Connect services and clients through hooks
3. **Error handling**: Proper error boundaries and fallbacks

**Why Third**: Bridges services to components. Must exist before presentation layer.

### Priority 4: Presentation Layer (2 hours)

1. **Components**: UI components in `components/demo/`
   - `PlayerColorSelector.tsx` - Choose White/Black
   - `DifficultySelector.tsx` - 10 difficulty levels
   - `ComputerThinking.tsx` - Thinking indicator
   - `VSComputerStatus.tsx` - Game status with computer info
2. **Professional styling**: Apply golden standard style guide

**Why Fourth**: Pure presentation consuming data from hooks.

### Priority 5: Feature Layer (1 hour)

1. **Page**: Complete page in `pages/demo/`
   - `VSComputerPage.tsx` - Orchestrate all components
2. **Integration testing**: Verify complete flow works
3. **Mobile optimization**: Responsive layout refinements

**Why Last**: Features combine all lower layers.

## Success Criteria

### Functional Requirements

- ✅ **Human vs Human gameplay** - Complete chess game with move validation
- ✅ **Human vs Computer gameplay** - Stockfish opponent with 10 difficulty levels
- ✅ **Professional UI** - Clean, elegant interface following style guide
- ✅ **Responsive design** - Works perfectly on mobile, tablet, and desktop
- ✅ **Error handling** - Graceful fallbacks for all failure scenarios

### Technical Requirements

- ✅ **No backend dependency** - Completely standalone application
- ✅ **Performance** - Smooth animations and responsive interactions
- ✅ **Accessibility** - Keyboard navigation and screen reader support
- ✅ **Code quality** - Clean architecture following established patterns
- ✅ **Documentation** - Implementation examples for developers

### Demo Quality Requirements

- ✅ **Professional appearance** - Showcases chessboard-vanilla-v2 library professionally
- ✅ **Feature completeness** - Demonstrates all major library capabilities
- ✅ **User experience** - Intuitive, enjoyable chess playing experience
- ✅ **Developer appeal** - Clear code examples and implementation guidance

## Architecture-Compliant File Structure

```
src/
├── types/                               # Priority 1: Foundation
│   ├── chess/
│   │   └── computer-opponent.types.ts   # NEW: Computer opponent interfaces
│   └── demo/
│       └── vs-computer.types.ts         # NEW: VS Computer game state types
├── utils/                               # Priority 1: Foundation
│   └── chess/
│       └── computer-chess.utils.ts      # NEW: Move parsing utilities
├── constants/                           # Priority 1: Foundation
│   └── chess/
│       └── computer-difficulty.constants.ts  # NEW: Difficulty configs
├── services/                            # Priority 2: Infrastructure
│   ├── chess/
│   │   └── ComputerChessService.ts      # NEW: Business logic
│   └── clients/
│       └── StockfishClient.ts           # NEW: External communication
├── hooks/                               # Priority 3: Data Layer
│   └── demo/
│       └── useVSComputerState.ts        # NEW: State management
├── components/                          # Priority 4: Presentation
│   └── demo/
│       ├── PlayerColorSelector.tsx      # NEW: Choose White/Black
│       ├── DifficultySelector.tsx       # NEW: 10 difficulty levels
│       ├── ComputerThinking.tsx         # NEW: Thinking indicator
│       └── VSComputerStatus.tsx         # NEW: Game status display
└── pages/                               # Priority 5: Features
    └── demo/
        └── VSComputerPage.tsx           # NEW: Complete VS Computer demo
```

This implementation creates a world-class chess demo that showcases the chessboard-vanilla-v2 library with a complete standalone experience featuring professional computer opponent gameplay.
