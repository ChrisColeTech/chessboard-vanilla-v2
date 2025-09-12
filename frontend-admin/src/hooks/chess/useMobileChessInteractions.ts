// useMobileChessInteractions.ts - Mobile chess touch and interaction handling
// Phase 4: Mobile Chess Interaction Hooks - Touch gesture recognition and mobile interactions

import { useState, useCallback, useRef, useEffect } from 'react';
import type { 
  ChessPosition,
  MobileChessInteraction,
  MobileTouchEvent,
  MobileBoardDimensions,
  MobileChessConfig,
  MobileChessMoveResult
} from '../../types';
import {
  normalizeTouchEvent,
  isValidTouchTarget,
  exceedsDragThreshold,
  triggerHapticFeedback,
  debounceTouchEvent
} from '../../utils/chess';

export interface UseMobileChessInteractionsHook {
  // Touch state
  activeTouches: Map<number, MobileTouchEvent>;
  isDragging: boolean;
  dragSource: ChessPosition | null;
  dragTarget: ChessPosition | null;
  selectedSquare: ChessPosition | null;
  
  // Interaction handlers
  handleTouchStart: (event: TouchEvent | MouseEvent) => void;
  handleTouchMove: (event: TouchEvent | MouseEvent) => void;
  handleTouchEnd: (event: TouchEvent | MouseEvent) => void;
  handleSquareTap: (position: ChessPosition) => void;
  
  // Gesture detection
  lastGestureType: MobileChessInteraction['type'] | null;
  gestureHistory: MobileChessInteraction[];
  
  // Configuration
  updateConfig: (config: Partial<MobileChessConfig>) => void;
  
  // State management
  clearInteractionState: () => void;
}

export const useMobileChessInteractions = (
  boardElement: HTMLElement | null,
  boardDimensions: MobileBoardDimensions | null,
  mobileConfig: MobileChessConfig,
  onMove: (from: ChessPosition, to: ChessPosition) => Promise<MobileChessMoveResult>,
  onSquareSelect: (position: ChessPosition) => void,
  recordInteraction: (interaction: MobileChessInteraction) => void
): UseMobileChessInteractionsHook => {
  
  // Touch state management
  const [activeTouches, setActiveTouches] = useState<Map<number, MobileTouchEvent>>(new Map());
  const [isDragging, setIsDragging] = useState(false);
  const [dragSource, setDragSource] = useState<ChessPosition | null>(null);
  const [dragTarget, setDragTarget] = useState<ChessPosition | null>(null);
  const [selectedSquare, setSelectedSquare] = useState<ChessPosition | null>(null);
  const [lastGestureType, setLastGestureType] = useState<MobileChessInteraction['type'] | null>(null);
  const [gestureHistory, setGestureHistory] = useState<MobileChessInteraction[]>([]);
  const [config, setConfig] = useState<MobileChessConfig>(mobileConfig);

  // Refs for tracking interaction state
  const touchStartTime = useRef<number>(0);
  const touchStartPosition = useRef<{ x: number; y: number } | null>(null);
  const longPressTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const doubleTapTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastTapTime = useRef<number>(0);
  const lastTapPosition = useRef<ChessPosition | null>(null);

  // Debounced handlers to improve performance
  const debouncedHandleTouchMove = useCallback(
    debounceTouchEvent((event: TouchEvent | MouseEvent) => {
      handleTouchMoveInternal(event);
    }, 16), // ~60fps
    [boardElement, boardDimensions, config]
  );

  // Clear interaction state
  const clearInteractionState = useCallback(() => {
    setActiveTouches(new Map());
    setIsDragging(false);
    setDragSource(null);
    setDragTarget(null);
    setSelectedSquare(null);
    touchStartTime.current = 0;
    touchStartPosition.current = null;
    
    // Clear timers
    if (longPressTimer.current) {
      clearTimeout(longPressTimer.current);
      longPressTimer.current = null;
    }
    if (doubleTapTimer.current) {
      clearTimeout(doubleTapTimer.current);
      doubleTapTimer.current = null;
    }
  }, []);

  // Update mobile configuration
  const updateConfig = useCallback((newConfig: Partial<MobileChessConfig>) => {
    setConfig(prev => ({ ...prev, ...newConfig }));
  }, []);

  // Handle touch start
  const handleTouchStart = useCallback((event: TouchEvent | MouseEvent) => {
    if (!boardElement || !boardDimensions) return;

    const normalizedEvent = normalizeTouchEvent(event, boardElement);
    if (!normalizedEvent) return;

    const currentTime = Date.now();
    touchStartTime.current = currentTime;
    touchStartPosition.current = normalizedEvent.boardCoords;

    // Update active touches
    setActiveTouches(prev => new Map(prev.set(normalizedEvent.touchId, normalizedEvent)));

    // Check for valid touch target
    const target = event.target as HTMLElement;
    if (!isValidTouchTarget(target, normalizedEvent.boardCoords, boardElement.getBoundingClientRect())) {
      return;
    }

    // Handle square selection if touching a square
    if (normalizedEvent.square) {
      // Check for double tap
      const timeSinceLastTap = currentTime - lastTapTime.current;
      const isDoubleTap = timeSinceLastTap < 300 && 
                         lastTapPosition.current === normalizedEvent.square;

      if (isDoubleTap) {
        // Clear double tap timer
        if (doubleTapTimer.current) {
          clearTimeout(doubleTapTimer.current);
          doubleTapTimer.current = null;
        }
        
        // Handle double tap gesture
        handleDoubleTap(normalizedEvent.square, currentTime);
      } else {
        // Set up potential single tap
        lastTapTime.current = currentTime;
        lastTapPosition.current = normalizedEvent.square;
        
        // Set up double tap detection window
        doubleTapTimer.current = setTimeout(() => {
          handleSingleTap(normalizedEvent.square!, currentTime);
        }, 300);
      }

      // Set up long press detection
      if (config.tapToMoveEnabled) {
        longPressTimer.current = setTimeout(() => {
          handleLongPress(normalizedEvent.square!, currentTime);
        }, 500);
      }

      // Enable drag if configured
      if (config.enableDragAndDrop) {
        setDragSource(normalizedEvent.square);
      }
    }

    event.preventDefault();
  }, [boardElement, boardDimensions, config, onSquareSelect]);

  // Internal touch move handler
  const handleTouchMoveInternal = useCallback((event: TouchEvent | MouseEvent) => {
    if (!boardElement || !boardDimensions || !touchStartPosition.current) return;

    const normalizedEvent = normalizeTouchEvent(event, boardElement);
    if (!normalizedEvent) return;

    // Update active touches
    setActiveTouches(prev => new Map(prev.set(normalizedEvent.touchId, normalizedEvent)));

    // Check if movement exceeds drag threshold
    const hasExceededThreshold = exceedsDragThreshold(
      touchStartPosition.current,
      normalizedEvent.boardCoords,
      config.enableDragAndDrop ? 10 : 20
    );

    if (hasExceededThreshold) {
      // Clear long press timer since we're dragging
      if (longPressTimer.current) {
        clearTimeout(longPressTimer.current);
        longPressTimer.current = null;
      }

      // Clear double tap timer
      if (doubleTapTimer.current) {
        clearTimeout(doubleTapTimer.current);
        doubleTapTimer.current = null;
      }

      // Enable drag mode
      if (config.enableDragAndDrop && dragSource && !isDragging) {
        setIsDragging(true);
        if (config.enableHapticFeedback) {
          triggerHapticFeedback('light');
        }
      }

      // Update drag target
      if (isDragging && normalizedEvent.square) {
        setDragTarget(normalizedEvent.square);
      }
    }

    event.preventDefault();
  }, [boardElement, boardDimensions, config, dragSource, isDragging]);

  // Handle touch move (debounced)
  const handleTouchMove = useCallback((event: TouchEvent | MouseEvent) => {
    debouncedHandleTouchMove(event);
  }, [debouncedHandleTouchMove]);

  // Handle touch end
  const handleTouchEnd = useCallback((event: TouchEvent | MouseEvent) => {
    if (!boardElement || !boardDimensions) return;

    const normalizedEvent = normalizeTouchEvent(event, boardElement);
    if (!normalizedEvent) return;

    const currentTime = Date.now();
    const touchDuration = currentTime - touchStartTime.current;

    // Clear timers
    if (longPressTimer.current) {
      clearTimeout(longPressTimer.current);
      longPressTimer.current = null;
    }

    // Remove from active touches
    setActiveTouches(prev => {
      const newMap = new Map(prev);
      newMap.delete(normalizedEvent.touchId);
      return newMap;
    });

    // Handle drag end
    if (isDragging && dragSource && dragTarget) {
      handleDragEnd(dragSource, dragTarget, currentTime);
    } else if (dragSource && !isDragging && touchDuration < 200) {
      // Quick tap - treat as square selection
      handleSquareTap(dragSource);
    }

    // Reset drag state
    setIsDragging(false);
    setDragSource(null);
    setDragTarget(null);
    touchStartPosition.current = null;

    event.preventDefault();
  }, [boardElement, boardDimensions, isDragging, dragSource, dragTarget, onMove, onSquareSelect]);

  // Handle single tap
  const handleSingleTap = useCallback((square: ChessPosition, timestamp: number) => {
    const interaction: MobileChessInteraction = {
      type: 'tap',
      square,
      timestamp,
      coords: { x: 0, y: 0 }, // Will be updated by calling component
      duration: 0
    };

    recordInteraction(interaction);
    setLastGestureType('tap');
    setGestureHistory(prev => [...prev.slice(-9), interaction]);

    onSquareSelect(square);
    setSelectedSquare(square);

    if (config.enableHapticFeedback) {
      triggerHapticFeedback('light');
    }
  }, [config, recordInteraction, onSquareSelect]);

  // Handle double tap
  const handleDoubleTap = useCallback((square: ChessPosition, timestamp: number) => {
    const interaction: MobileChessInteraction = {
      type: 'double-tap',
      square,
      timestamp,
      coords: { x: 0, y: 0 }, // Will be updated by calling component
      duration: 0
    };

    recordInteraction(interaction);
    setLastGestureType('double-tap');
    setGestureHistory(prev => [...prev.slice(-9), interaction]);

    // Double tap could trigger special actions (like auto-move best move)
    onSquareSelect(square);

    if (config.enableHapticFeedback) {
      triggerHapticFeedback('medium');
    }
  }, [config, recordInteraction, onSquareSelect]);

  // Handle long press
  const handleLongPress = useCallback((square: ChessPosition, timestamp: number) => {
    const interaction: MobileChessInteraction = {
      type: 'long-press',
      square,
      timestamp,
      coords: { x: 0, y: 0 }, // Will be updated by calling component
      duration: 500
    };

    recordInteraction(interaction);
    setLastGestureType('long-press');
    setGestureHistory(prev => [...prev.slice(-9), interaction]);

    // Long press could show move hints or piece info
    onSquareSelect(square);

    if (config.enableHapticFeedback) {
      triggerHapticFeedback('heavy');
    }
  }, [config, recordInteraction, onSquareSelect]);

  // Handle drag end
  const handleDragEnd = useCallback(async (from: ChessPosition, to: ChessPosition, timestamp: number) => {
    const interaction: MobileChessInteraction = {
      type: 'drag',
      square: from,
      timestamp,
      coords: { x: 0, y: 0 }, // Will be updated by calling component
      duration: timestamp - touchStartTime.current
    };

    recordInteraction(interaction);
    setLastGestureType('drag');
    setGestureHistory(prev => [...prev.slice(-9), interaction]);

    // Attempt to make the move
    try {
      const result = await onMove(from, to);
      
      if (result.isValid && config.enableHapticFeedback) {
        triggerHapticFeedback(result.feedback.triggerHaptic ? 'medium' : 'light');
      } else if (!result.isValid && config.enableHapticFeedback) {
        triggerHapticFeedback('heavy');
      }
    } catch (error) {
      console.warn('Error making drag move:', error);
      if (config.enableHapticFeedback) {
        triggerHapticFeedback('heavy');
      }
    }
  }, [config, recordInteraction, onMove]);

  // Handle square tap
  const handleSquareTap = useCallback((position: ChessPosition) => {
    onSquareSelect(position);
    setSelectedSquare(position);
  }, [onSquareSelect]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      clearInteractionState();
    };
  }, [clearInteractionState]);

  return {
    activeTouches,
    isDragging,
    dragSource,
    dragTarget,
    selectedSquare,
    handleTouchStart,
    handleTouchMove,
    handleTouchEnd,
    handleSquareTap,
    lastGestureType,
    gestureHistory,
    updateConfig,
    clearInteractionState
  };
};