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