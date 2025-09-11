export * from './users';
export * from './puzzles';
export * from './games';
export * from './stats';
export * from './learning';
export * from './tutorials';
export * from './auth';
export * from './sessions';
export * from './achievements';
export * from './progress';
export * from './openings';
export * from './analysis';
export * from './ai-opponents';
export * from './analytics';
export * from './profiles';
export * from './endgames';
export * from './game-reviews';
export * from './historic-games';
export * from './puzzle-attempts';
export * from './puzzle-sources';
export * from './learning-modules';
export * from './tutorial-steps';
export * from './study-plans';
export * from './help';
export * from './subscriptions';
// index.ts - Hooks exports barrel

// Audio hooks
export { useGlobalUIAudio } from './audio/useGlobalUIAudio';

// Stockfish hooks
export { useStockfish } from './chess/useStockfish';

// Menu hooks
export { useMenuDropdown } from './core/useMenuDropdown';

// Action Sheet hooks
export { useActionSheet } from './core/useActionSheet';

// Page Action hooks
export { usePlayActions } from './chess/usePlayActions';
export { useSlotsActions } from './casino/useSlotsActions';
export { useWorkerActions } from './chess/useWorkerActions';
export { useUITestsActions } from './uitests/useUITestsActions';
export { useLayoutActions } from './core/useLayoutActions';
export { useDragTestActions } from './uitests/useDragTestActions';
export { useUIAudioTestActions } from './uitests/useUIAudioTestActions';

// Authentication hooks
export {
  useAuth,
  useLogin,
  useRegister,
  useForgotPassword,
  useProfile,
  useAuthStatus,
  useUser,
  useLogout,
  useAuthError,
  useAuthInitialization,
  useProtectedRoute,
  useTokenVerification
} from './useAuth';

export { useDemoLogin, DEMO_USER_CREDENTIALS } from './useDemoLogin';