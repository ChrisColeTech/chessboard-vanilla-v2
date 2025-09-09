# Component Architecture - Presentation Layer

## Principles

Components are **pure presentation layer** with **zero business logic**. Each component has a single UI responsibility and communicates only through props and callbacks.

### Core Rules
- **No business logic** in components
- **No direct service calls** - use hooks only
- **No inline types** - import from types files
- **Single UI responsibility** per component
- **Props-based communication** only
- **Memoization** for performance
- **Accessibility first** design

---

## Component Hierarchy

```
Chessboard (Container Component)
├── Board (Layout Component)
│   ├── Square (Interactive Component) × 64
│   │   ├── Piece (Display Component)
│   │   └── SquareHighlight (Visual Component)
│   ├── CoordinateLabels (Display Component)
│   └── BoardOverlay (Visual Component)
│       ├── MoveArrows (Visual Component)
│       └── LastMoveHighlight (Visual Component)
└── GameControls (Interactive Component)
    ├── MoveHistory (Display Component)
    ├── GameStatus (Display Component)
    └── ActionButtons (Interactive Component)
```

---

## Container Components

### 1. Chessboard (Main Container)

```typescript
// components/chessboard/Chessboard/Chessboard.tsx
import React from 'react';
import { cn } from '@/utils/ui.utils';
import { Board } from '../Board';
import { useChessMaster } from '@/hooks';
import type { ChessboardProps } from '@/types';
import './Chessboard.styles.css';

/**
 * Main chessboard container component
 * Responsibility: Coordinate all chess-related hooks and pass data to child components
 */
export const Chessboard: React.FC<ChessboardProps> = ({
  gameState: externalGameState,
  onMove,
  onSquareClick,
  onPieceSelect,
  orientation = 'white',
  pieceSet = 'classic',
  boardWidth,
  showCoordinates = true,
  allowDragAndDrop = true,
  animationDuration = 300,
  customSquareStyles = {},
  theme,
  disabled = false,
  autoResize = true,
  className,
  style,
  testId,
  ...rest
}) => {
  const {
    gameState,
    isLoading,
    error,
    makeMove,
    dimensions,
    containerRef,
    orientation: currentOrientation,
    setOrientation,
    dragState,
    handleDragStart,
    handleDragEnd,
    handleDrop,
    animatedPieces,
    isAnimating,
    getValidMoves,
    isValidMove
  } = useChessMaster({
    initialGameState: externalGameState,
    boardWidth,
    orientation,
    animationDuration,
    disabled
  });

  // Use external move handler if provided, otherwise use internal
  const handleMoveInternal = React.useCallback(async (move: ChessMoveInput): Promise<boolean> => {
    if (onMove) {
      return await Promise.resolve(onMove(move));
    }
    return makeMove(move);
  }, [onMove, makeMove]);

  const handleSquareClickInternal = React.useCallback((position: ChessPosition) => {
    onSquareClick?.(position);
  }, [onSquareClick]);

  const handlePieceSelectInternal = React.useCallback((piece: ChessPiece, position: ChessPosition) => {
    onPieceSelect?.(piece, position);
  }, [onPieceSelect]);

  if (isLoading) {
    return (
      <div 
        className={cn('chessboard chessboard--loading', className)}
        style={style}
        data-testid={testId}
      >
        <div className="chessboard__loading-indicator">
          Loading chess game...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div 
        className={cn('chessboard chessboard--error', className)}
        style={style}
        data-testid={testId}
      >
        <div className="chessboard__error-message">
          Error: {error}
        </div>
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      className={cn(
        'chessboard',
        `chessboard--${currentOrientation}`,
        `chessboard--${pieceSet}`,
        {
          'chessboard--disabled': disabled,
          'chessboard--animating': isAnimating
        },
        className
      )}
      style={{
        width: dimensions.width,
        height: dimensions.height,
        ...style
      }}
      data-testid={testId}
      {...rest}
    >
      <Board
        gameState={gameState}
        orientation={currentOrientation}
        pieceSet={pieceSet}
        dimensions={dimensions}
        onSquareClick={handleSquareClickInternal}
        onPieceSelect={handlePieceSelectInternal}
        onMove={handleMoveInternal}
        dragState={dragState}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
        onDrop={handleDrop}
        animatedPieces={animatedPieces}
        isAnimating={isAnimating}
        showCoordinates={showCoordinates}
        customSquareStyles={customSquareStyles}
        theme={theme}
        disabled={disabled}
        allowDragAndDrop={allowDragAndDrop}
        getValidMoves={getValidMoves}
        isValidMove={isValidMove}
      />
    </div>
  );
};

Chessboard.displayName = 'Chessboard';
```

---

## Layout Components

### 1. Board Component

```typescript
// components/chessboard/Board/Board.tsx
import React, { useMemo } from 'react';
import { cn } from '@/utils/ui.utils';
import { Square } from '../Square';
import { CoordinateLabels } from '../CoordinateLabels';
import { BoardOverlay } from '../BoardOverlay';
import { generateSquares, getSquareColor } from '@/utils/chess.utils';
import type { BoardProps, SquareNotation } from '@/types';
import './Board.styles.css';

/**
 * Chess board layout component
 * Responsibility: Render 8x8 grid of squares with coordinates and overlays
 */
export const Board = React.memo<BoardProps>(({
  gameState,
  orientation,
  pieceSet,
  dimensions,
  onSquareClick,
  onPieceSelect,
  onMove,
  dragState,
  onDragStart,
  onDragEnd,
  onDrop,
  animatedPieces,
  isAnimating,
  showCoordinates,
  customSquareStyles,
  theme,
  disabled,
  allowDragAndDrop,
  getValidMoves,
  isValidMove,
  className,
  style,
  testId
}) => {
  // Memoize square generation to prevent unnecessary recalculations
  const squares = useMemo(() => 
    generateSquares(orientation), 
    [orientation]
  );

  // Memoize rendered squares
  const renderedSquares = useMemo(() => 
    squares.map((square) => {
      const piece = gameState?.position.get(square);
      const isLight = getSquareColor(square) === 'light';
      const customStyle = customSquareStyles?.[square];
      
      return (
        <Square
          key={square}
          position={square}
          piece={piece}
          isLight={isLight}
          size={dimensions.squareSize}
          pieceSet={pieceSet}
          onSquareClick={onSquareClick}
          onPieceSelect={onPieceSelect}
          onMove={onMove}
          dragState={dragState}
          onDragStart={onDragStart}
          onDragEnd={onDragEnd}
          onDrop={onDrop}
          animatedPieces={animatedPieces}
          isAnimating={isAnimating}
          customStyle={customStyle}
          theme={theme}
          disabled={disabled}
          allowDragAndDrop={allowDragAndDrop}
          getValidMoves={getValidMoves}
          isValidMove={isValidMove}
        />
      );
    }), 
    [
      squares, gameState?.position, dimensions.squareSize, pieceSet,
      onSquareClick, onPieceSelect, onMove, dragState, onDragStart,
      onDragEnd, onDrop, animatedPieces, isAnimating, customSquareStyles,
      theme, disabled, allowDragAndDrop, getValidMoves, isValidMove
    ]
  );

  return (
    <div 
      className={cn(
        'chess-board',
        `chess-board--${orientation}`,
        {
          'chess-board--disabled': disabled,
          'chess-board--animating': isAnimating
        },
        className
      )}
      style={{
        width: dimensions.width,
        height: dimensions.height,
        ...style
      }}
      data-testid={testId}
      role="grid"
      aria-label={`Chess board, ${orientation} perspective`}
      aria-describedby="chess-board-instructions"
    >
      {/* Hidden instructions for screen readers */}
      <div 
        id="chess-board-instructions" 
        className="sr-only"
      >
        Use arrow keys to navigate squares, Enter to select pieces, and Tab for game controls.
      </div>

      {/* Board squares */}
      <div 
        className="chess-board__squares"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(8, 1fr)',
          gridTemplateRows: 'repeat(8, 1fr)',
          width: '100%',
          height: '100%'
        }}
      >
        {renderedSquares}
      </div>

      {/* Coordinate labels */}
      {showCoordinates && (
        <CoordinateLabels
          orientation={orientation}
          dimensions={dimensions}
          theme={theme}
        />
      )}

      {/* Board overlays (arrows, highlights, etc.) */}
      <BoardOverlay
        gameState={gameState}
        orientation={orientation}
        dimensions={dimensions}
        theme={theme}
        lastMove={gameState?.lastMove}
        dragState={dragState}
      />
    </div>
  );
});

Board.displayName = 'Board';
```

---

## Interactive Components

### 1. Square Component

```typescript
// components/chessboard/Square/Square.tsx
import React, { useMemo, useCallback } from 'react';
import { cn } from '@/utils/ui.utils';
import { Piece } from '../Piece';
import { SquareHighlight } from '../SquareHighlight';
import { squareNotationToPosition, positionToSquareNotation } from '@/utils/chess.utils';
import type { SquareProps, ChessMoveInput } from '@/types';
import './Square.styles.css';

/**
 * Individual chess board square component
 * Responsibility: Handle square interactions and render piece if present
 */
export const Square = React.memo<SquareProps>(({
  position,
  piece,
  isLight,
  size,
  pieceSet,
  onSquareClick,
  onPieceSelect,
  onMove,
  dragState,
  onDragStart,
  onDragEnd,
  onDrop,
  animatedPieces,
  isAnimating,
  customStyle,
  theme,
  disabled,
  allowDragAndDrop,
  getValidMoves,
  isValidMove,
  className,
  style,
  testId
}) => {
  const chessPosition = useMemo(() => 
    squareNotationToPosition(position), 
    [position]
  );

  // Check if this square is a valid drop target
  const isValidDropTarget = useMemo(() => {
    if (!dragState.isDragging || !dragState.draggedFrom) return false;
    
    const fromSquare = positionToSquareNotation(dragState.draggedFrom);
    return isValidMove(fromSquare, position);
  }, [dragState, position, isValidMove]);

  // Check if this square should be highlighted
  const isHighlighted = useMemo(() => {
    // Highlight if it's the last move square
    // Highlight if it's a valid move target
    // etc.
    return false; // Simplified for example
  }, []);

  const handleClick = useCallback(() => {
    if (disabled) return;
    
    onSquareClick(chessPosition);
    
    if (piece) {
      onPieceSelect(piece, chessPosition);
    }
  }, [disabled, onSquareClick, onPieceSelect, piece, chessPosition]);

  const handleKeyDown = useCallback((event: React.KeyboardEvent) => {
    if (disabled) return;

    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick();
    }
  }, [disabled, handleClick]);

  const handleDragStart = useCallback((event: React.DragEvent) => {
    if (!allowDragAndDrop || disabled || !piece) {
      event.preventDefault();
      return;
    }

    onDragStart?.(piece, chessPosition);
  }, [allowDragAndDrop, disabled, piece, onDragStart, chessPosition]);

  const handleDragOver = useCallback((event: React.DragEvent) => {
    if (isValidDropTarget) {
      event.preventDefault(); // Allow drop
    }
  }, [isValidDropTarget]);

  const handleDrop = useCallback(async (event: React.DragEvent) => {
    event.preventDefault();
    
    if (!dragState.draggedFrom || !isValidDropTarget) return;

    const move: ChessMoveInput = {
      from: positionToSquareNotation(dragState.draggedFrom),
      to: position
    };

    try {
      await onMove(move);
    } finally {
      onDragEnd?.();
    }
  }, [dragState.draggedFrom, isValidDropTarget, position, onMove, onDragEnd]);

  const squareStyles = useMemo(() => ({
    width: size,
    height: size,
    backgroundColor: isLight ? theme.lightSquareColor : theme.darkSquareColor,
    ...customStyle,
    ...style
  }), [size, isLight, theme, customStyle, style]);

  return (
    <div
      className={cn(
        'chess-square',
        {
          'chess-square--light': isLight,
          'chess-square--dark': !isLight,
          'chess-square--highlighted': isHighlighted,
          'chess-square--valid-drop': isValidDropTarget,
          'chess-square--disabled': disabled,
          'chess-square--has-piece': !!piece
        },
        className
      )}
      style={squareStyles}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      data-testid={testId}
      data-square={position}
      tabIndex={0}
      role="gridcell"
      aria-label={`Square ${position}${piece ? `, ${piece.color} ${piece.type}` : ', empty'}`}
      aria-describedby={piece ? `piece-${piece.id}` : undefined}
    >
      {/* Square highlights */}
      <SquareHighlight
        isHighlighted={isHighlighted}
        isValidDropTarget={isValidDropTarget}
        theme={theme}
      />

      {/* Piece on this square */}
      {piece && (
        <Piece
          piece={piece}
          position={chessPosition}
          size={size}
          pieceSet={pieceSet}
          isDragging={dragState.isDragging && dragState.draggedPiece?.id === piece.id}
          animatedPieces={animatedPieces}
          onDragStart={handleDragStart}
          disabled={disabled}
          allowDragAndDrop={allowDragAndDrop}
        />
      )}
    </div>
  );
});

Square.displayName = 'Square';
```

---

## Display Components

### 1. Piece Component

```typescript
// components/chessboard/Piece/Piece.tsx
import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/utils/ui.utils';
import { getPieceSvgPath } from '@/utils/piece.utils';
import type { PieceProps } from '@/types';
import './Piece.styles.css';

/**
 * Chess piece display component
 * Responsibility: Render piece SVG with animations
 */
export const Piece = React.memo<PieceProps>(({
  piece,
  position,
  size,
  pieceSet,
  isDragging = false,
  animatedPieces,
  onDragStart,
  disabled,
  allowDragAndDrop,
  className,
  style,
  testId
}) => {
  // Find animation for this piece
  const pieceAnimation = useMemo(() => 
    animatedPieces?.find(anim => anim.pieceId === piece.id),
    [animatedPieces, piece.id]
  );

  const svgPath = useMemo(() => 
    getPieceSvgPath(piece.type, piece.color, pieceSet),
    [piece.type, piece.color, pieceSet]
  );

  const handleDragStart = useMemo(() => 
    allowDragAndDrop && !disabled ? onDragStart : undefined,
    [allowDragAndDrop, disabled, onDragStart]
  );

  const pieceStyles = useMemo(() => ({
    width: size,
    height: size,
    cursor: handleDragStart ? 'grab' : 'default',
    opacity: isDragging ? 0.5 : 1,
    ...style
  }), [size, handleDragStart, isDragging, style]);

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={`${piece.id}-${position.file}${position.rank}`}
        className={cn(
          'chess-piece',
          `chess-piece--${piece.color}`,
          `chess-piece--${piece.type}`,
          {
            'chess-piece--dragging': isDragging,
            'chess-piece--disabled': disabled,
            'chess-piece--draggable': !!handleDragStart
          },
          className
        )}
        style={pieceStyles}
        data-testid={testId}
        data-piece-id={piece.id}
        data-piece-type={piece.type}
        data-piece-color={piece.color}
        draggable={!!handleDragStart}
        onDragStart={handleDragStart}
        // Animation props
        layout
        initial={{ scale: 0, opacity: 0 }}
        animate={{ 
          scale: 1, 
          opacity: isDragging ? 0.5 : 1,
          x: pieceAnimation?.isAnimating ? 
            `${(pieceAnimation.to.file.charCodeAt(0) - position.file.charCodeAt(0)) * size}px` : 0,
          y: pieceAnimation?.isAnimating ? 
            `${(position.rank - pieceAnimation.to.rank) * size}px` : 0
        }}
        exit={{ scale: 0, opacity: 0 }}
        transition={{
          type: "spring",
          stiffness: 500,
          damping: 30,
          layout: {
            duration: 0.3
          }
        }}
        // Accessibility
        role="img"
        aria-label={`${piece.color} ${piece.type}`}
        aria-describedby={`piece-${piece.id}`}
      >
        {/* SVG piece image */}
        <img
          src={svgPath}
          alt={`${piece.color} ${piece.type}`}
          className="chess-piece__image"
          draggable={false}
          onError={(e) => {
            console.warn(`Failed to load piece image: ${svgPath}`);
            e.currentTarget.src = '/assets/pieces/fallback.svg';
          }}
        />

        {/* Hidden description for screen readers */}
        <div id={`piece-${piece.id}`} className="sr-only">
          {piece.color} {piece.type} on square {position.file}{position.rank}
        </div>
      </motion.div>
    </AnimatePresence>
  );
});

Piece.displayName = 'Piece';
```

---

## Visual Components

### 1. Square Highlight Component

```typescript
// components/chessboard/SquareHighlight/SquareHighlight.tsx
import React from 'react';
import { cn } from '@/utils/ui.utils';
import type { SquareHighlightProps } from '@/types';
import './SquareHighlight.styles.css';

/**
 * Square highlighting visual component
 * Responsibility: Render visual highlights for squares
 */
export const SquareHighlight = React.memo<SquareHighlightProps>(({
  isHighlighted,
  highlightType = 'selected',
  isValidDropTarget,
  theme,
  className,
  style
}) => {
  if (!isHighlighted && !isValidDropTarget) return null;

  const highlightColor = theme.highlightColors[highlightType] || theme.highlightColors.selected;

  return (
    <div
      className={cn(
        'square-highlight',
        `square-highlight--${highlightType}`,
        {
          'square-highlight--drop-target': isValidDropTarget
        },
        className
      )}
      style={{
        backgroundColor: isValidDropTarget 
          ? theme.highlightColors['valid-move']
          : highlightColor,
        ...style
      }}
      aria-hidden="true"
    />
  );
});

SquareHighlight.displayName = 'SquareHighlight';
```

### 2. Coordinate Labels Component

```typescript
// components/chessboard/CoordinateLabels/CoordinateLabels.tsx
import React, { useMemo } from 'react';
import { cn } from '@/utils/ui.utils';
import type { CoordinateLabelsProps } from '@/types';
import './CoordinateLabels.styles.css';

/**
 * Board coordinate labels component
 * Responsibility: Render file and rank labels around the board
 */
export const CoordinateLabels = React.memo<CoordinateLabelsProps>(({
  orientation,
  dimensions,
  theme,
  className,
  style
}) => {
  const files = useMemo(() => 
    orientation === 'white' 
      ? ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
      : ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'],
    [orientation]
  );

  const ranks = useMemo(() => 
    orientation === 'white' 
      ? [8, 7, 6, 5, 4, 3, 2, 1]
      : [1, 2, 3, 4, 5, 6, 7, 8],
    [orientation]
  );

  return (
    <div 
      className={cn('coordinate-labels', className)}
      style={style}
      aria-hidden="true"
    >
      {/* File labels (bottom) */}
      <div className="coordinate-labels__files">
        {files.map((file, index) => (
          <div
            key={file}
            className="coordinate-labels__file"
            style={{
              left: (index * dimensions.squareSize) + (dimensions.squareSize / 2),
              color: theme.coordinateColor,
              fontSize: dimensions.squareSize * 0.15
            }}
          >
            {file}
          </div>
        ))}
      </div>

      {/* Rank labels (left) */}
      <div className="coordinate-labels__ranks">
        {ranks.map((rank, index) => (
          <div
            key={rank}
            className="coordinate-labels__rank"
            style={{
              top: (index * dimensions.squareSize) + (dimensions.squareSize / 2),
              color: theme.coordinateColor,
              fontSize: dimensions.squareSize * 0.15
            }}
          >
            {rank}
          </div>
        ))}
      </div>
    </div>
  );
});

CoordinateLabels.displayName = 'CoordinateLabels';
```

---

## Component Testing

```typescript
// components/chessboard/Piece/__tests__/Piece.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { Piece } from '../Piece';
import type { ChessPiece, ChessPosition } from '@/types';

const mockPiece: ChessPiece = {
  id: 'test-piece-1',
  type: 'king',
  color: 'white',
  hasMoved: false
};

const mockPosition: ChessPosition = {
  file: 'e',
  rank: 1
};

describe('Piece Component', () => {
  it('renders piece with correct attributes', () => {
    render(
      <Piece
        piece={mockPiece}
        position={mockPosition}
        size={64}
        pieceSet="classic"
      />
    );

    const pieceElement = screen.getByRole('img');
    expect(pieceElement).toBeInTheDocument();
    expect(pieceElement).toHaveAttribute('aria-label', 'white king');
  });

  it('applies draggable attributes when drag is allowed', () => {
    const mockDragStart = jest.fn();
    
    render(
      <Piece
        piece={mockPiece}
        position={mockPosition}
        size={64}
        pieceSet="classic"
        allowDragAndDrop
        onDragStart={mockDragStart}
      />
    );

    const pieceElement = screen.getByTestId('chess-piece');
    expect(pieceElement).toHaveAttribute('draggable', 'true');
  });

  it('does not allow drag when disabled', () => {
    render(
      <Piece
        piece={mockPiece}
        position={mockPosition}
        size={64}
        pieceSet="classic"
        disabled
        allowDragAndDrop
      />
    );

    const pieceElement = screen.getByTestId('chess-piece');
    expect(pieceElement).toHaveAttribute('draggable', 'false');
  });
});
```

This component architecture ensures clean separation of concerns, comprehensive accessibility, and optimal performance through proper memoization and React patterns.