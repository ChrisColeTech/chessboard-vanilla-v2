// index.ts - Chess utilities barrel export

// Core chess utilities (re-exported from parent)
export {
  positionToSquare,
  squareToPosition,
  isValidPosition,
  getSquareColor,
  isValidFile,
  isValidRank,
  fileToIndex,
  rankToIndex,
  indexToFile,
  indexToRank,
  generateSquareList
} from '../chess.utils';

// Mobile chess utilities
export {
  calculateMobileBoardSize,
  getTouchTargetSize,
  screenCoordsToChessSquare,
  chessSquareToScreenCoords,
  detectTouchGesture,
  isValidTouchTarget,
  normalizeTouchEvent,
  calculateTouchDistance,
  exceedsDragThreshold,
  getMobileSquareColor,
  generateMobileBoardSquares,
  debounceTouchEvent,
  supportsHapticFeedback,
  triggerHapticFeedback,
  isLandscapeOrientation,
  getSafeAreaInsets
} from './mobile-chess.utils';