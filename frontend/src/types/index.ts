// index.ts - Type exports barrel
export type {
  // Chess types
  PieceColor,
  PieceType,
  File,
  Rank,
  ChessPosition,
  ChessPositionObject,
  ChessPiece,
  ChessMove,
  CastlingRights,
  ChessGameState,
  ChessMoveInput,
  ChessMoveResult,
  GameResult
} from './chess/chess.types';

export type {
  // Component types
  ChessboardProps,
  BoardProps,
  SquareProps,
  PieceProps,
  DraggedPieceProps,
  PlayChessboardProps
} from './core/component.types';

// Phase 1: Computer opponent types
export type {
  ComputerDifficulty,
  ComputerMoveRequest,
  ComputerMoveResult,
  ComputerOpponentConfig,
  ComputerThinkingState,
  ComputerOpponentStatus,
  ComputerMoveAnalysis
} from './chess/computer-opponent.types';

// Phase 1: Play game types
export type {
  PlayGameMode,
  PlayGameState,
  PlayGameActions,
  GameResultType,
  PlayGameResult,
  GameSettings,
  PlayerInfo,
  GameSession,
  GameMoveRecord
} from './chess/play-game.types';

// Phase 1: Mobile chess types
export type {
  MobileChessConfig,
  MobileChessInteraction,
  MobileBoardState,
  MobileChessGameState,
  MobileSquareState,
  MobileTouchEvent,
  MobileChessMoveResult,
  MobileBoardDimensions,
  MobilePieceAnimation
} from './chess/mobile-chess.types';

// Mobile chess constants
export {
  DEFAULT_MOBILE_CHESS_CONFIG,
  MOBILE_BOARD_SIZE_PRESETS,
  MOBILE_TOUCH_THRESHOLDS
} from './chess/mobile-chess.types';

// Phase 1: Play UI component types
export type {
  PlayerStatusProps,
  GameControlsProps,
  DifficultyLevelProps,
  ComputerThinkingProps,
  GameStatusBarProps,
  PlaySettingsProps,
  MoveHistoryProps,
  GameResultModalProps,
  BasePlayComponentProps,
  PlayComponentTheme,
  PlayComponentSize,
  PlayComponentAnimation
} from './ui/play-components.types';

// Phase 2: UI Audio types
export type {
  UIInteractionType,
  UISoundType,
  UIInteractionConfig,
  UIElementSelector,
  UIExclusionConfig
} from './audio/ui-audio.types';

// Phase 2: Global Audio Service types
export type {
  GlobalUIAudioConfig,
  GlobalUIAudioConfigUpdate,
  GlobalUIAudioService,
  GlobalClickHandler,
  ElementDetectionResult
} from './audio/global-audio.types';

// Phase 3: UI Tests types
export type {
  UITestRoute,
  UITestNavigationState,
  UITestNavigationActions,
  UITestNavigationHook,
  AudioDemoConfiguration,
  DemoSection,
  DemoButtonExample,
  ExclusionExample,
  CodeSnippet,
  AudioDemoState,
  AudioDemoActions,
  AudioDemoHook,
  DragTestConfiguration,
  DragTestState,
  DragTestActions,
  MoveHandler,
  DragTestingHook
} from './ui';

// Phase 4: Chess Board Audio types
export type {
  ChessBoardAudioEvents,
  MoveAudioContext,
  ChessBoardInteractionType,
  ChessBoardAudioConfig
} from './audio/chess-board-audio.types';

export {
  DEFAULT_CHESS_BOARD_AUDIO_CONFIG,
  CHESS_BOARD_AUDIO_PROFILES
} from './audio/chess-board-audio.types';

// Phase 4: Audio Feedback types
export type {
  AudioFeedbackTiming,
  AudioFeedbackIntensity,
  AudioFeedbackPattern,
  AudioFeedbackContext,
  AudioFeedbackDecision,
  ComponentAudioConfig
} from './audio/audio-feedback.types';

export {
  DEFAULT_AUDIO_TIMING,
  AUDIO_FEEDBACK_PATTERNS
} from './audio/audio-feedback.types';

// Authentication types
export type {
  User,
  UserProgress,
  LoginRequest,
  RegisterRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  ChangePasswordRequest,
  UpdateProfileRequest,
  VerifyTokenRequest,
  AuthResponse,
  LoginResponse,
  MeResponse,
  TokenVerificationResponse,
  AuthState,
  AuthActions,
  UseAuthReturn,
  UseLoginReturn,
  UseRegisterReturn,
  UseForgotPasswordReturn,
  FormValidationError,
  AuthFormState,
  TokenInfo,
  AuthConfig,
  ProtectedRouteProps,
  AuthGuardProps,
  AuthContextValue,
  AuthErrorType,
  AuthError,
  AuthStorage,
  AuthApiClient
} from './auth/auth.types';