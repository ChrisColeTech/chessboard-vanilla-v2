// index.ts - Utils exports barrel
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
} from './chess.utils';

export {
  squareToCoordinates,
  coordinatesToSquare,
  isValidSquare,
  getSquareDistance,
  getAdjacentSquares
} from './coordinate.utils';

export type {
  BoardCoordinates
} from './coordinate.utils';

// Phase 2: UI Tests utilities
export {
  generateDemoButtons,
  generateExclusionExamples,
  generateCodeSnippets,
  formatCodeSnippet,
  getDemoButtonById,
  getExclusionExampleById,
  generateInteractiveSelectors,
  generateExclusionSelectors,
  mapInteractionToSound,
  generateSelectorFromExample,
  matchesExclusionPattern,
  validateDemoConfiguration,
  generateImplementationTip,
  extractElementTypeFromSelector,
  isInteractiveSelector,
  groupExamplesByCategory,
  formatSelectorForDisplay
} from './ui-tests';

// Phase 3: Mobile chess utilities
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
} from './chess';

// Authentication utilities
export {
  DEFAULT_AUTH_CONFIG,
  TokenUtils,
  AuthStorageService,
  ValidationUtils,
  AuthErrorUtils,
  ApiUtils,
  SessionUtils,
  authStorage,
  tokenUtils,
  validationUtils,
  authErrorUtils,
  apiUtils,
  sessionUtils
} from './auth.utils';