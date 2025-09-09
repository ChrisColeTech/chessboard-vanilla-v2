# Hooks Architecture - Single Responsibility Design

## Principles

Each hook follows **Single Responsibility Principle (SRP)** with clearly defined purposes:
- **State Management Hooks**: Manage React state only
- **Business Logic Hooks**: Bridge services and components  
- **UI Interaction Hooks**: Handle user interactions
- **Performance Hooks**: Optimize rendering and calculations

No hook contains business logic, API calls, or inline type definitions.

---

## Core Chess Hooks

### 1. Game State Management Hook

```typescript
// hooks/useChessGame.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { ChessGameService } from '@/services/chess';
import type { 
  ChessGameHook, 
  ChessGameState, 
  ChessMoveInput,
  ChessGameConfig 
} from '@/types';

/**
 * Primary hook for chess game state management
 * Responsibility: Bridge between ChessGameService and React components
 */
export const useChessGame = (config: ChessGameConfig = {}): ChessGameHook => {
  const [gameState, setGameState] = useState<ChessGameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const gameServiceRef = useRef<ChessGameService>();

  // Initialize game service
  useEffect(() => {
    try {
      gameServiceRef.current = new ChessGameService(config);
      setGameState(gameServiceRef.current.getCurrentState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize game');
    } finally {
      setIsLoading(false);
    }
  }, [config.initialFen, config.validateMoves]);

  const makeMove = useCallback(async (move: ChessMoveInput): Promise<boolean> => {
    if (!gameServiceRef.current) return false;

    try {
      setError(null);
      const result = gameServiceRef.current.makeMove(move);
      
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

  const undoMove = useCallback(): boolean => {
    if (!gameServiceRef.current) return false;

    try {
      const result = gameServiceRef.current.undoMove();
      if (result.success) {
        setGameState(result.gameState);
        setError(null);
        return true;
      }
      return false;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Undo failed');
      return false;
    }
  }, []);

  const resetGame = useCallback((fen?: string) => {
    if (!gameServiceRef.current) return;

    try {
      gameServiceRef.current.resetGame(fen);
      setGameState(gameServiceRef.current.getCurrentState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Reset failed');
    }
  }, []);

  const loadGame = useCallback((newGameState: ChessGameState) => {
    if (!gameServiceRef.current) return;

    try {
      gameServiceRef.current.loadGame(newGameState);
      setGameState(gameServiceRef.current.getCurrentState());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Load game failed');
    }
  }, []);

  return {
    gameState,
    isLoading,
    error,
    makeMove,
    undoMove,
    resetGame,
    loadGame,
    isGameOver: gameState?.isCheckmate || gameState?.isStalemate || gameState?.isDraw || false,
    canUndo: (gameState?.moveHistory.length || 0) > 0
  };
};
```

### 2. Drag and Drop Hook

```typescript
// hooks/useDragAndDrop.ts
import { useState, useCallback, useRef } from 'react';
import type { 
  DragAndDropHook, 
  DragAndDropConfig, 
  DragState, 
  ChessPiece, 
  ChessPosition,
  ChessMoveInput,
  SquareNotation 
} from '@/types';
import { positionToSquareNotation } from '@/utils';

/**
 * Hook for drag and drop interactions
 * Responsibility: Manage drag state and coordinate with move validation
 */
export const useDragAndDrop = (config: DragAndDropConfig): DragAndDropHook => {
  const [dragState, setDragState] = useState<DragState>({
    isDragging: false
  });

  const dragStartPositionRef = useRef<ChessPosition | null>(null);

  const handleDragStart = useCallback((piece: ChessPiece, position: ChessPosition) => {
    if (config.disabled) return;

    dragStartPositionRef.current = position;
    setDragState({
      isDragging: true,
      draggedPiece: piece,
      draggedFrom: position
    });
  }, [config.disabled]);

  const handleDragEnd = useCallback(() => {
    setDragState({
      isDragging: false
    });
    dragStartPositionRef.current = null;
  }, []);

  const handleDrop = useCallback(async (from: ChessPosition, to: ChessPosition) => {
    if (!dragStartPositionRef.current || config.disabled) {
      handleDragEnd();
      return;
    }

    const move: ChessMoveInput = {
      from: positionToSquareNotation(from),
      to: positionToSquareNotation(to)
    };

    try {
      const success = await Promise.resolve(config.onMove(move));
      
      if (!success && !config.allowInvalidMoves) {
        // Visual feedback for invalid move could be added here
      }
    } catch (error) {
      console.warn('Move failed:', error);
    }

    handleDragEnd();
  }, [config.onMove, config.disabled, config.allowInvalidMoves, handleDragEnd]);

  const handleDragOver = useCallback((position: ChessPosition) => {
    if (!dragState.isDragging) return;

    setDragState(prev => ({
      ...prev,
      dropTarget: position
    }));
  }, [dragState.isDragging]);

  const isValidDropTarget = useCallback((position: ChessPosition): boolean => {
    if (!config.gameState || !dragStartPositionRef.current) return false;

    const from = positionToSquareNotation(dragStartPositionRef.current);
    const to = positionToSquareNotation(position);
    
    // This would typically call a validation service
    // For now, just check if it's a different square
    return from !== to;
  }, [config.gameState]);

  return {
    dragState,
    handleDragStart,
    handleDragEnd,
    handleDrop,
    handleDragOver,
    isValidDropTarget
  };
};
```

### 3. Chess Animation Hook

```typescript
// hooks/useChessAnimation.ts
import { useState, useCallback, useEffect, useRef } from 'react';
import type { 
  ChessAnimationHook, 
  ChessAnimationConfig, 
  PieceAnimation, 
  ChessMove,
  AnimationConfig 
} from '@/types';
import { AnimationService } from '@/services/animation';

/**
 * Hook for managing chess piece animations
 * Responsibility: Coordinate animations with React state changes
 */
export const useChessAnimation = (config: ChessAnimationConfig): ChessAnimationHook => {
  const [animatedPieces, setAnimatedPieces] = useState<readonly PieceAnimation[]>([]);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const animationServiceRef = useRef<AnimationService>();
  const activeAnimationsRef = useRef<Set<string>>(new Set());

  // Initialize animation service
  useEffect(() => {
    animationServiceRef.current = new AnimationService();
    
    return () => {
      animationServiceRef.current?.cancelAllAnimations();
    };
  }, []);

  // Detect moves and trigger animations
  useEffect(() => {
    if (config.disabled || !config.lastMove || !animationServiceRef.current) return;

    animateMove(config.lastMove);
  }, [config.lastMove, config.disabled]);

  const animateMove = useCallback(async (move: ChessMove): Promise<void> => {
    if (!animationServiceRef.current || config.disabled) return;

    const animationId = `${move.id}-${Date.now()}`;
    activeAnimationsRef.current.add(animationId);

    const animation: PieceAnimation = {
      pieceId: move.piece.id,
      from: move.from,
      to: move.to,
      isAnimating: true,
      progress: 0
    };

    setAnimatedPieces(prev => [...prev, animation]);
    setIsAnimating(true);

    try {
      await animationServiceRef.current.createAnimation(
        move, 
        config.animationConfig || { duration: 300, easing: 'ease-out' }
      );

      // Update animation progress during animation
      // This would be handled by the animation service
      
    } catch (error) {
      console.warn('Animation failed:', error);
    } finally {
      // Clean up completed animation
      setAnimatedPieces(prev => 
        prev.filter(anim => anim.pieceId !== move.piece.id)
      );
      
      activeAnimationsRef.current.delete(animationId);
      
      if (activeAnimationsRef.current.size === 0) {
        setIsAnimating(false);
      }
    }
  }, [config.disabled, config.animationConfig]);

  const cancelAnimations = useCallback(() => {
    if (!animationServiceRef.current) return;

    animationServiceRef.current.cancelAllAnimations();
    setAnimatedPieces([]);
    setIsAnimating(false);
    activeAnimationsRef.current.clear();
  }, []);

  return {
    animatedPieces,
    isAnimating,
    animateMove,
    cancelAnimations
  };
};
```

### 4. Responsive Board Hook

```typescript
// hooks/useResponsiveBoard.ts
import { useState, useEffect, useRef, useCallback } from 'react';
import type { 
  ResponsiveBoardHook, 
  BoardDimensions, 
  BoardOrientation 
} from '@/types';

/**
 * Hook for responsive board sizing and orientation
 * Responsibility: Manage board dimensions and responsive behavior
 */
export const useResponsiveBoard = (initialWidth?: number): ResponsiveBoardHook => {
  const [dimensions, setDimensions] = useState<BoardDimensions>({
    width: initialWidth || 400,
    height: initialWidth || 400,
    squareSize: (initialWidth || 400) / 8
  });
  
  const [isResizing, setIsResizing] = useState(false);
  const [orientation, setOrientation] = useState<BoardOrientation>('white');
  
  const containerRef = useRef<HTMLDivElement>(null);
  const resizeTimeoutRef = useRef<NodeJS.Timeout>();

  // ResizeObserver for responsive behavior
  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (!entry) return;

      setIsResizing(true);
      
      // Clear previous timeout
      if (resizeTimeoutRef.current) {
        clearTimeout(resizeTimeoutRef.current);
      }

      // Debounce resize updates
      resizeTimeoutRef.current = setTimeout(() => {
        const { width, height } = entry.contentRect;
        const size = Math.min(width, height);
        
        setDimensions({
          width: size,
          height: size,
          squareSize: size / 8
        });
        
        setIsResizing(false);
      }, 16); // ~60fps
    });

    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
      if (resizeTimeoutRef.current) {
        clearTimeout(resizeTimeoutRef.current);
      }
    };
  }, []);

  const setOrientationCallback = useCallback((newOrientation: BoardOrientation) => {
    setOrientation(newOrientation);
  }, []);

  return {
    dimensions,
    containerRef,
    isResizing,
    orientation,
    setOrientation: setOrientationCallback
  };
};
```

---

## Utility Hooks

### 1. Chess Validation Hook

```typescript
// hooks/useChessValidation.ts
import { useMemo, useCallback } from 'react';
import type { ChessGameState, SquareNotation, ChessMove } from '@/types';
import { MoveValidationService } from '@/services/chess';

/**
 * Hook for move validation and legal moves calculation
 * Responsibility: Provide validation utilities to components
 */
export const useChessValidation = (gameState: ChessGameState | null) => {
  const validationService = useMemo(
    () => new MoveValidationService(), 
    []
  );

  const getValidMoves = useCallback((square: SquareNotation): ChessMove[] => {
    if (!gameState) return [];
    
    return validationService.getValidMoves(square, gameState);
  }, [gameState, validationService]);

  const isValidMove = useCallback((from: SquareNotation, to: SquareNotation): boolean => {
    if (!gameState) return false;

    const result = validationService.validateMove({ from, to }, gameState);
    return result.isValid;
  }, [gameState, validationService]);

  const getValidMovesForPiece = useCallback((square: SquareNotation): SquareNotation[] => {
    return getValidMoves(square).map(move => 
      `${move.to.file}${move.to.rank}` as SquareNotation
    );
  }, [getValidMoves]);

  return {
    getValidMoves,
    isValidMove,
    getValidMovesForPiece,
    hasValidMoves: gameState ? getValidMoves.length > 0 : false
  };
};
```

### 2. Chess Event Hook

```typescript
// hooks/useChessEvents.ts
import { useEffect, useCallback } from 'react';
import type { 
  ChessEvent, 
  ChessEventHandler, 
  ChessGameState,
  IChessEventEmitter 
} from '@/types';

/**
 * Hook for chess game event handling
 * Responsibility: Manage event subscriptions and cleanup
 */
export const useChessEvents = (
  eventEmitter: IChessEventEmitter | null,
  gameState: ChessGameState | null
) => {
  const onMove = useCallback<ChessEventHandler<ChessMoveEvent>>((event) => {
    // Handle move events
    console.log('Move made:', event.move.san);
  }, []);

  const onCapture = useCallback<ChessEventHandler<ChessCaptureEvent>>((event) => {
    // Handle capture events
    console.log('Piece captured:', event.capturedPiece.type);
  }, []);

  const onGameEnd = useCallback<ChessEventHandler<ChessGameEndEvent>>((event) => {
    // Handle game end events
    console.log('Game ended:', event.type, event.winner);
  }, []);

  // Subscribe to events
  useEffect(() => {
    if (!eventEmitter) return;

    eventEmitter.on('move', onMove);
    eventEmitter.on('capture', onCapture);
    eventEmitter.on('checkmate', onGameEnd);
    eventEmitter.on('stalemate', onGameEnd);
    eventEmitter.on('draw', onGameEnd);

    return () => {
      eventEmitter.off('move', onMove);
      eventEmitter.off('capture', onCapture);
      eventEmitter.off('checkmate', onGameEnd);
      eventEmitter.off('stalemate', onGameEnd);
      eventEmitter.off('draw', onGameEnd);
    };
  }, [eventEmitter, onMove, onCapture, onGameEnd]);

  // Emit events based on game state changes
  useEffect(() => {
    if (!eventEmitter || !gameState) return;

    if (gameState.isCheckmate) {
      eventEmitter.emit({
        type: 'checkmate',
        winner: gameState.activeColor === 'white' ? 'black' : 'white',
        reason: 'Checkmate',
        gameState
      });
    } else if (gameState.isStalemate) {
      eventEmitter.emit({
        type: 'stalemate',
        reason: 'Stalemate',
        gameState
      });
    } else if (gameState.isDraw) {
      eventEmitter.emit({
        type: 'draw',
        reason: 'Draw',
        gameState
      });
    }
  }, [eventEmitter, gameState]);
};
```

---

## Hook Composition Patterns

### 1. Master Chess Hook

```typescript
// hooks/useChessMaster.ts
import type { ChessGameConfig } from '@/types';

/**
 * Composed hook that combines multiple chess hooks
 * Responsibility: Provide a single interface for complete chess functionality
 */
export const useChessMaster = (config: ChessGameConfig = {}) => {
  const gameHook = useChessGame(config);
  const responsiveHook = useResponsiveBoard(config.boardWidth);
  const validationHook = useChessValidation(gameHook.gameState);
  
  const dragDropHook = useDragAndDrop({
    onMove: gameHook.makeMove,
    gameState: gameHook.gameState,
    disabled: gameHook.isGameOver
  });

  const animationHook = useChessAnimation({
    pieces: gameHook.gameState?.position,
    lastMove: gameHook.gameState?.lastMove,
    disabled: config.disableAnimations
  });

  return {
    // Game state
    ...gameHook,
    
    // Board dimensions
    ...responsiveHook,
    
    // Drag and drop
    ...dragDropHook,
    
    // Animations
    ...animationHook,
    
    // Validation
    ...validationHook
  };
};
```

---

## Testing Hooks

```typescript
// hooks/__tests__/useChessGame.test.ts
import { renderHook, act } from '@testing-library/react';
import { useChessGame } from '../useChessGame';

describe('useChessGame', () => {
  it('should initialize with default game state', () => {
    const { result } = renderHook(() => useChessGame());
    
    expect(result.current.isLoading).toBe(false);
    expect(result.current.gameState).not.toBeNull();
    expect(result.current.error).toBeNull();
  });

  it('should make valid moves', async () => {
    const { result } = renderHook(() => useChessGame());
    
    await act(async () => {
      const success = await result.current.makeMove({
        from: 'e2',
        to: 'e4'
      });
      
      expect(success).toBe(true);
      expect(result.current.gameState?.moveHistory).toHaveLength(1);
    });
  });

  it('should reject invalid moves', async () => {
    const { result } = renderHook(() => useChessGame());
    
    await act(async () => {
      const success = await result.current.makeMove({
        from: 'e2',
        to: 'e5' // Invalid move
      });
      
      expect(success).toBe(false);
      expect(result.current.error).toBeTruthy();
    });
  });
});
```

This hooks architecture ensures clean separation of concerns, testability, and reusability while strictly following SRP principles.