// useDragTesting.ts - Hook for managing drag testing functionality

import { useState, useCallback, useMemo, useRef } from 'react';
import type {
  DragTestingHook,
  DragTestConfiguration,
  DragTestState,
  DragTestActions,
  ChessPosition,
  MoveHandler
} from '../../types';
import { UIDemoService } from '../../services';
import { DEFAULT_DRAG_TEST_CONFIG } from '../../constants';

/**
 * Hook for managing drag testing state and functionality
 */
export const useDragTesting = (
  initialConfig?: Partial<DragTestConfiguration>,
  moveHandler?: MoveHandler
): DragTestingHook => {
  const demoService = useMemo(() => UIDemoService.getInstance(), []);
  
  // Configuration state
  const [config, setConfig] = useState<DragTestConfiguration>(() => {
    return demoService.validateDragTestConfig(initialConfig || {});
  });

  // Drag testing state
  const [selectedSquare, setSelectedSquare] = useState<ChessPosition | null>(null);
  const [validMoves, setValidMoves] = useState<readonly ChessPosition[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  // Additional testing state
  const [dragStartPosition, setDragStartPosition] = useState<ChessPosition | null>(null);
  const [dragEndPosition, setDragEndPosition] = useState<ChessPosition | null>(null);
  const [lastMoveAttempt, setLastMoveAttempt] = useState<{
    from: ChessPosition;
    to: ChessPosition;
    success: boolean;
    timestamp: number;
  } | null>(null);

  // Refs for drag tracking
  const dragStartTime = useRef<number>(0);
  const dragElement = useRef<HTMLElement | null>(null);

  // Configuration actions
  const updateConfig = useCallback((updates: Partial<DragTestConfiguration>) => {
    const newConfig = demoService.validateDragTestConfig({ ...config, ...updates });
    setConfig(newConfig);
  }, [config, demoService]);

  const resetConfig = useCallback(() => {
    setConfig(DEFAULT_DRAG_TEST_CONFIG);
  }, []);

  const toggleVisualFeedback = useCallback(() => {
    updateConfig({ enableVisualFeedback: !config.enableVisualFeedback });
  }, [config.enableVisualFeedback, updateConfig]);

  const toggleValidMoves = useCallback(() => {
    updateConfig({ showValidMoves: !config.showValidMoves });
  }, [config.showValidMoves, updateConfig]);

  const toggleCapture = useCallback(() => {
    updateConfig({ captureEnabled: !config.captureEnabled });
  }, [config.captureEnabled, updateConfig]);

  // Drag testing actions
  const setSelectedSquareWithMoves = useCallback((square: ChessPosition | null, moves: readonly ChessPosition[] = []) => {
    setSelectedSquare(square);
    setValidMoves(moves);
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedSquare(null);
    setValidMoves([]);
    setIsDragging(false);
    setDragStartPosition(null);
    setDragEndPosition(null);
  }, []);

  const startDrag = useCallback((fromSquare: ChessPosition, element?: HTMLElement) => {
    setIsDragging(true);
    setDragStartPosition(fromSquare);
    setSelectedSquare(fromSquare);
    dragStartTime.current = Date.now();
    
    if (element) {
      dragElement.current = element;
    }
  }, []);

  const endDrag = useCallback(async (toSquare: ChessPosition) => {
    if (!dragStartPosition) {
      console.warn('Drag ended without start position');
      setIsDragging(false);
      return false;
    }

    setDragEndPosition(toSquare);
    
    let moveSuccess = false;
    
    if (moveHandler && dragStartPosition !== toSquare) {
      try {
        moveSuccess = await moveHandler(dragStartPosition, toSquare);
        
        // Record move attempt for analysis
        setLastMoveAttempt({
          from: dragStartPosition,
          to: toSquare,
          success: moveSuccess,
          timestamp: Date.now()
        });
      } catch (error) {
        console.error('Move handler error:', error);
        moveSuccess = false;
      }
    }

    // Clean up drag state
    setIsDragging(false);
    
    if (moveSuccess) {
      // Successful move - clear selection
      clearSelection();
    } else {
      // Failed move - keep selection for retry
      setDragStartPosition(null);
      setDragEndPosition(null);
    }

    dragElement.current = null;
    
    return moveSuccess;
  }, [dragStartPosition, moveHandler, clearSelection]);

  const cancelDrag = useCallback(() => {
    setIsDragging(false);
    setDragStartPosition(null);
    setDragEndPosition(null);
    dragElement.current = null;
    
    // Keep selected square for potential retry
  }, []);

  // Reset testing
  const resetTest = useCallback(() => {
    setSelectedSquare(null);
    setValidMoves([]);
    setIsDragging(false);
    setDragStartPosition(null);
    setDragEndPosition(null);
    setLastMoveAttempt(null);
    dragStartTime.current = 0;
    dragElement.current = null;
  }, []);

  // Utility methods
  const isValidMove = useCallback((toSquare: ChessPosition): boolean => {
    return validMoves.includes(toSquare);
  }, [validMoves]);

  const isSquareSelected = useCallback((square: ChessPosition): boolean => {
    return selectedSquare === square;
  }, [selectedSquare]);


  const getLastMoveStats = useCallback(() => {
    return lastMoveAttempt;
  }, [lastMoveAttempt]);

  const canDropOnSquare = useCallback((square: ChessPosition): boolean => {
    if (!config.showValidMoves) return true; // Allow drops everywhere when validation is off
    return isValidMove(square);
  }, [config.showValidMoves, isValidMove]);

  // State object
  const state: DragTestState = {
    selectedSquare,
    validMoves,
    isDragging
  };

  // Enhanced state with testing utilities
  const enhancedState = {
    ...state,
    dragStartPosition,
    dragEndPosition,
    lastMoveAttempt
  };

  // Actions object
  const actions: DragTestActions = {
    updateConfig,
    resetTest,
    setSelectedSquare: setSelectedSquareWithMoves,
    setValidMoves
  };

  // Enhanced actions with testing utilities
  const enhancedActions = {
    ...actions,
    resetConfig,
    toggleVisualFeedback,
    toggleValidMoves,
    toggleCapture,
    clearSelection,
    startDrag,
    endDrag,
    cancelDrag,
    isValidMove,
    isSquareSelected,
    canDropOnSquare,
    getLastMoveStats
  };

  // Return hook interface
  return {
    config,
    ...enhancedState,
    ...enhancedActions
  };
};