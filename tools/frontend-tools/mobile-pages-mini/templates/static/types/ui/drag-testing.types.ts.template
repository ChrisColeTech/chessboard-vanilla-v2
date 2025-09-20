// drag-testing.types.ts - Drag testing type definitions

import type { ChessPosition } from '../chess/chess.types';

/**
 * Configuration for drag test behavior
 */
export interface DragTestConfiguration {
  readonly enableVisualFeedback: boolean;
  readonly showValidMoves: boolean;
  readonly captureEnabled: boolean;
}

/**
 * Current state of drag testing
 */
export interface DragTestState {
  readonly selectedSquare: ChessPosition | null;
  readonly validMoves: readonly ChessPosition[];
  readonly isDragging: boolean;
}

/**
 * Drag test actions interface
 */
export interface DragTestActions {
  readonly updateConfig: (updates: Partial<DragTestConfiguration>) => void;
  readonly resetTest: () => void;
  readonly setSelectedSquare: (square: ChessPosition | null) => void;
  readonly setValidMoves: (moves: readonly ChessPosition[]) => void;
}

/**
 * Move handler function type
 */
export type MoveHandler = (from: ChessPosition, to: ChessPosition) => Promise<boolean>;

/**
 * Complete drag testing hook return type
 */
export interface DragTestingHook extends DragTestState, DragTestActions {
  readonly config: DragTestConfiguration;
}