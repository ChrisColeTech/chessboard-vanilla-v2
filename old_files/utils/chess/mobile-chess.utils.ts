// mobile-chess.utils.ts - Mobile-optimized chess utilities
// Phase 3: Mobile-Optimized Utilities - Mobile chess helper functions

import type {
  ChessPosition,
  MobileBoardDimensions,
  MobileChessInteraction,
  MobileTouchEvent,
  MobileChessConfig
} from '../../types';
import {
  MOBILE_BOARD_SIZE_PRESETS,
  MOBILE_TOUCH_THRESHOLDS
} from '../../types';

/**
 * Calculate optimal board dimensions for mobile display
 * Ensures the chessboard fits properly within mobile container constraints
 */
export function calculateMobileBoardSize(
  containerWidth: number, 
  containerHeight: number,
  config?: Partial<MobileChessConfig>
): MobileBoardDimensions {
  // Account for padding and UI elements
  const padding = 16; // Standard mobile padding
  const availableWidth = containerWidth - (padding * 2);
  const availableHeight = containerHeight - (padding * 2);
  
  // Use smaller dimension to ensure square board fits
  const maxSize = Math.min(availableWidth, availableHeight);
  
  // Apply size preset if specified
  let boardSize: number;
  if (config?.boardSize && config.boardSize !== 'auto') {
    boardSize = Math.min(MOBILE_BOARD_SIZE_PRESETS[config.boardSize], maxSize);
  } else {
    boardSize = maxSize;
  }
  
  // Ensure board size is divisible by 8 for clean squares
  boardSize = Math.floor(boardSize / 8) * 8;
  
  // Calculate square dimensions
  const squareSize = boardSize / 8;
  
  // Ensure touch targets meet minimum size requirements
  const minTouchTarget = config?.touchTargetSize || 44;
  const touchTargetSize = Math.max(squareSize, minTouchTarget);
  
  // Check if board fits comfortably (with some breathing room)
  const fitsComfortably = (boardSize + padding * 2) <= Math.min(containerWidth, containerHeight) * 0.9;
  
  return {
    containerWidth,
    containerHeight,
    boardSize,
    squareSize,
    touchTargetSize,
    padding,
    fitsComfortably
  };
}

/**
 * Get optimal touch target size for mobile squares
 * Ensures touch targets meet accessibility guidelines
 */
export function getTouchTargetSize(squareSize: number, minSize: number = 44): number {
  // iOS and Android recommend minimum 44px touch targets
  return Math.max(squareSize, minSize);
}

/**
 * Convert screen coordinates to chess square position
 * Handles board orientation and responsive sizing
 */
export function screenCoordsToChessSquare(
  screenX: number,
  screenY: number,
  boardDimensions: MobileBoardDimensions,
  boardElement: HTMLElement,
  isBoardFlipped: boolean = false
): ChessPosition | null {
  // Get board's bounding rectangle
  const rect = boardElement.getBoundingClientRect();
  
  // Calculate relative position within the board
  const relativeX = screenX - rect.left;
  const relativeY = screenY - rect.top;
  
  // Check if coordinates are within board bounds
  if (relativeX < 0 || relativeX > boardDimensions.boardSize ||
      relativeY < 0 || relativeY > boardDimensions.boardSize) {
    return null;
  }
  
  // Calculate file and rank indices
  let fileIndex = Math.floor(relativeX / boardDimensions.squareSize);
  let rankIndex = Math.floor(relativeY / boardDimensions.squareSize);
  
  // Handle board flipping
  if (isBoardFlipped) {
    fileIndex = 7 - fileIndex;
    rankIndex = 7 - rankIndex;
  }
  
  // Convert to chess notation
  if (fileIndex < 0 || fileIndex > 7 || rankIndex < 0 || rankIndex > 7) {
    return null;
  }
  
  const file = String.fromCharCode('a'.charCodeAt(0) + fileIndex);
  const rank = 8 - rankIndex; // Ranks go from 8 at top to 1 at bottom
  
  return `${file}${rank}` as ChessPosition;
}

/**
 * Convert chess square to screen coordinates
 * Useful for positioning UI elements relative to squares
 */
export function chessSquareToScreenCoords(
  position: ChessPosition,
  boardDimensions: MobileBoardDimensions,
  boardElement: HTMLElement,
  isBoardFlipped: boolean = false
): { x: number; y: number } {
  const rect = boardElement.getBoundingClientRect();
  
  // Parse chess position
  const file = position[0];
  const rank = parseInt(position[1]);
  
  // Calculate indices
  let fileIndex = file.charCodeAt(0) - 'a'.charCodeAt(0);
  let rankIndex = 8 - rank;
  
  // Handle board flipping
  if (isBoardFlipped) {
    fileIndex = 7 - fileIndex;
    rankIndex = 7 - rankIndex;
  }
  
  // Calculate screen coordinates (center of square)
  const x = rect.left + (fileIndex * boardDimensions.squareSize) + (boardDimensions.squareSize / 2);
  const y = rect.top + (rankIndex * boardDimensions.squareSize) + (boardDimensions.squareSize / 2);
  
  return { x, y };
}

/**
 * Detect touch gesture type based on interaction data
 * Recognizes tap, long-press, drag, and double-tap gestures
 */
export function detectTouchGesture(
  interaction: MobileChessInteraction,
  previousInteractions: MobileChessInteraction[] = []
): MobileChessInteraction['type'] {
  const duration = interaction.duration || 0;
  const { tapMaxDuration, longPressMinDuration, doubleTapWindow } = MOBILE_TOUCH_THRESHOLDS;
  
  // Long press detection
  if (duration >= longPressMinDuration) {
    return 'long-press';
  }
  
  // Quick tap detection
  if (duration <= tapMaxDuration) {
    // Check for double tap
    const recentTaps = previousInteractions.filter(
      prev => prev.type === 'tap' &&
              prev.square === interaction.square &&
              (interaction.timestamp - prev.timestamp) <= doubleTapWindow
    );
    
    if (recentTaps.length > 0) {
      return 'double-tap';
    }
    
    return 'tap';
  }
  
  // Default to drag for longer interactions
  return 'drag';
}

/**
 * Check if a touch event is a valid target for chess interaction
 * Validates touch coordinates and element types
 */
export function isValidTouchTarget(
  element: HTMLElement | null,
  touchCoords: { x: number; y: number },
  boardBounds: DOMRect
): boolean {
  if (!element) return false;
  
  // Check if touch is within board bounds
  if (touchCoords.x < boardBounds.left || touchCoords.x > boardBounds.right ||
      touchCoords.y < boardBounds.top || touchCoords.y > boardBounds.bottom) {
    return false;
  }
  
  // Check if element has chess square data attribute
  const hasSquareData = element.hasAttribute('data-square') ||
                       element.closest('[data-square]') !== null;
  
  return hasSquareData;
}

/**
 * Normalize touch event data for consistent handling
 * Handles differences between touch and mouse events
 */
export function normalizeTouchEvent(
  event: TouchEvent | MouseEvent,
  boardElement: HTMLElement
): MobileTouchEvent | null {
  let clientX: number, clientY: number, touchId: number;
  
  if (event.type.startsWith('touch')) {
    const touchEvent = event as TouchEvent;
    if (touchEvent.touches.length === 0 && touchEvent.changedTouches.length === 0) {
      return null;
    }
    
    const touch = touchEvent.touches[0] || touchEvent.changedTouches[0];
    clientX = touch.clientX;
    clientY = touch.clientY;
    touchId = touch.identifier;
  } else {
    const mouseEvent = event as MouseEvent;
    clientX = mouseEvent.clientX;
    clientY = mouseEvent.clientY;
    touchId = 0; // Mouse events use a consistent ID
  }
  
  const rect = boardElement.getBoundingClientRect();
  const boardCoords = {
    x: clientX - rect.left,
    y: clientY - rect.top
  };
  
  // Determine chess square if within bounds
  let square: ChessPosition | null = null;
  if (boardCoords.x >= 0 && boardCoords.x <= rect.width &&
      boardCoords.y >= 0 && boardCoords.y <= rect.height) {
    const fileIndex = Math.floor(boardCoords.x / (rect.width / 8));
    const rankIndex = Math.floor(boardCoords.y / (rect.height / 8));
    
    if (fileIndex >= 0 && fileIndex < 8 && rankIndex >= 0 && rankIndex < 8) {
      const file = String.fromCharCode('a'.charCodeAt(0) + fileIndex);
      const rank = 8 - rankIndex;
      square = `${file}${rank}` as ChessPosition;
    }
  }
  
  // Determine gesture type
  let gesture: MobileTouchEvent['gesture'];
  if (event.type.endsWith('start') || event.type === 'mousedown') {
    gesture = 'start';
  } else if (event.type.endsWith('move') || event.type === 'mousemove') {
    gesture = 'move';
  } else if (event.type.endsWith('end') || event.type === 'mouseup') {
    gesture = 'end';
  } else {
    gesture = 'cancel';
  }
  
  return {
    originalEvent: event as TouchEvent, // Type assertion for consistency
    boardCoords,
    square,
    gesture,
    touchId
  };
}

/**
 * Calculate distance between two touch points
 * Useful for drag threshold detection
 */
export function calculateTouchDistance(
  point1: { x: number; y: number },
  point2: { x: number; y: number }
): number {
  const deltaX = point2.x - point1.x;
  const deltaY = point2.y - point1.y;
  return Math.sqrt(deltaX * deltaX + deltaY * deltaY);
}

/**
 * Check if a touch movement exceeds the drag threshold
 * Helps distinguish between taps and drags
 */
export function exceedsDragThreshold(
  startCoords: { x: number; y: number },
  currentCoords: { x: number; y: number },
  threshold: number = MOBILE_TOUCH_THRESHOLDS.dragMinMovement
): boolean {
  const distance = calculateTouchDistance(startCoords, currentCoords);
  return distance > threshold;
}

/**
 * Get mobile-optimized square colors for better visibility
 * Adjusts contrast for mobile screens
 */
export function getMobileSquareColor(
  position: ChessPosition,
  theme: 'light' | 'dark' = 'light'
): { background: string; border: string; text: string } {
  const file = position[0];
  const rank = parseInt(position[1]);
  const fileIndex = file.charCodeAt(0) - 'a'.charCodeAt(0);
  const isLightSquare = (fileIndex + rank) % 2 === 0;
  
  if (theme === 'dark') {
    return isLightSquare 
      ? { background: '#393939', border: '#2a2a2a', text: '#e0e0e0' }
      : { background: '#2a2a2a', border: '#1a1a1a', text: '#ffffff' };
  } else {
    return isLightSquare
      ? { background: '#f0d9b5', border: '#d4c4a8', text: '#654321' }
      : { background: '#b58863', border: '#9b7653', text: '#ffffff' };
  }
}

/**
 * Generate mobile-optimized board squares data
 * Creates square configuration optimized for mobile rendering
 */
export function generateMobileBoardSquares(
  orientation: 'white' | 'black' = 'white',
  boardDimensions: MobileBoardDimensions
): Array<{
  position: ChessPosition;
  coords: { x: number; y: number };
  size: { width: number; height: number };
  colors: { background: string; border: string; text: string };
  touchTarget: { width: number; height: number };
}> {
  const squares = [];
  const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  const ranks = orientation === 'white' ? [8, 7, 6, 5, 4, 3, 2, 1] : [1, 2, 3, 4, 5, 6, 7, 8];
  
  for (let rankIndex = 0; rankIndex < 8; rankIndex++) {
    for (let fileIndex = 0; fileIndex < 8; fileIndex++) {
      const rank = ranks[rankIndex];
      const file = files[fileIndex];
      const position = `${file}${rank}` as ChessPosition;
      
      const coords = {
        x: fileIndex * boardDimensions.squareSize,
        y: rankIndex * boardDimensions.squareSize
      };
      
      const size = {
        width: boardDimensions.squareSize,
        height: boardDimensions.squareSize
      };
      
      const touchTarget = {
        width: boardDimensions.touchTargetSize,
        height: boardDimensions.touchTargetSize
      };
      
      const colors = getMobileSquareColor(position);
      
      squares.push({
        position,
        coords,
        size,
        colors,
        touchTarget
      });
    }
  }
  
  return squares;
}

/**
 * Debounce touch events to prevent excessive firing
 * Improves performance on mobile devices
 */
export function debounceTouchEvent<T extends any[]>(
  func: (...args: T) => void,
  delay: number = 16 // ~60fps
): (...args: T) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  
  return (...args: T) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

/**
 * Check if device supports haptic feedback
 * Feature detection for mobile haptics
 */
export function supportsHapticFeedback(): boolean {
  return 'vibrate' in navigator || 
         ('hapticFeedback' in navigator) ||
         // @ts-ignore - Check for iOS haptic feedback
         ('tapticEngine' in navigator);
}

/**
 * Trigger haptic feedback if supported
 * Provides tactile feedback for mobile chess interactions
 */
export function triggerHapticFeedback(
  pattern: 'light' | 'medium' | 'heavy' = 'light'
): void {
  if (!supportsHapticFeedback()) return;
  
  try {
    if ('vibrate' in navigator) {
      const vibrationPattern = {
        light: [10],
        medium: [20],
        heavy: [30]
      };
      navigator.vibrate(vibrationPattern[pattern]);
    }
    
    // @ts-ignore - iOS haptic feedback (if available)
    if ('tapticEngine' in navigator && (navigator as any).tapticEngine) {
      const intensity = {
        light: 0.3,
        medium: 0.6,
        heavy: 1.0
      };
      (navigator as any).tapticEngine.impact(intensity[pattern]);
    }
  } catch (error) {
    // Silently fail if haptic feedback is not available
    console.debug('Haptic feedback not available:', error);
  }
}

/**
 * Check if device is in landscape orientation
 * Useful for adjusting mobile chess board layout
 */
export function isLandscapeOrientation(): boolean {
  return window.innerWidth > window.innerHeight;
}

/**
 * Get safe area insets for mobile devices
 * Accounts for notches, home indicators, etc.
 */
export function getSafeAreaInsets(): {
  top: number;
  right: number;
  bottom: number;
  left: number;
} {
  const computedStyle = getComputedStyle(document.documentElement);
  
  return {
    top: parseInt(computedStyle.getPropertyValue('--safe-area-inset-top') || '0'),
    right: parseInt(computedStyle.getPropertyValue('--safe-area-inset-right') || '0'),
    bottom: parseInt(computedStyle.getPropertyValue('--safe-area-inset-bottom') || '0'),
    left: parseInt(computedStyle.getPropertyValue('--safe-area-inset-left') || '0')
  };
}