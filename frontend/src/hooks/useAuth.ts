// React hooks for authentication functionality
import { useCallback, useEffect } from 'react';
import { useShallow } from 'zustand/react/shallow';
import type {
  UseAuthReturn,
  UseLoginReturn,
  UseRegisterReturn,
  UseForgotPasswordReturn,
  LoginRequest,
  RegisterRequest,
  ResetPasswordRequest,
  ChangePasswordRequest,
  UpdateProfileRequest
} from '../types';

import { useAuthStore } from '../store/auth.store';

/**
 * Main authentication hook
 * Provides access to auth state and all auth actions
 */
export const useAuth = (): UseAuthReturn => {
  const store = useAuthStore(
    useShallow((state) => ({
      // State
      user: state.user,
      token: state.token,
      isLoading: state.isLoading,
      isAuthenticated: state.isAuthenticated,
      error: state.error,
      progress: state.progress,
      
      // Actions
      login: state.login,
      register: state.register,
      logout: state.logout,
      forgotPassword: state.forgotPassword,
      resetPassword: state.resetPassword,
      changePassword: state.changePassword,
      updateProfile: state.updateProfile,
      verifyToken: state.verifyToken,
      refreshUser: state.refreshUser,
      clearError: state.clearError,
      initialize: state.initialize
    }))
  );

  // Initialize auth state on mount
  useEffect(() => {
    store.initialize();
  }, []);

  return store;
};

/**
 * Login-specific hook
 * Focused on login functionality with isolated loading state
 */
export const useLogin = (): UseLoginReturn => {
  const { login, isLoading, error, clearError } = useAuthStore(
    useShallow((state) => ({
      login: state.login,
      isLoading: state.isLoading,
      error: state.error,
      clearError: state.clearError
    }))
  );

  const handleLogin = useCallback(async (credentials: LoginRequest) => {
    await login(credentials);
  }, [login]);

  return {
    login: handleLogin,
    isLoading,
    error,
    clearError
  };
};

/**
 * Registration-specific hook
 * Focused on registration functionality with isolated state
 */
export const useRegister = (): UseRegisterReturn => {
  const { register, isLoading, error, clearError } = useAuthStore(
    useShallow((state) => ({
      register: state.register,
      isLoading: state.isLoading,
      error: state.error,
      clearError: state.clearError
    }))
  );

  const handleRegister = useCallback(async (userData: RegisterRequest) => {
    await register(userData);
  }, [register]);

  return {
    register: handleRegister,
    isLoading,
    error,
    clearError
  };
};

/**
 * Password reset hook
 * Handles both forgot password and reset password flows
 */
export const useForgotPassword = (): UseForgotPasswordReturn => {
  const { 
    forgotPassword, 
    resetPassword, 
    isLoading, 
    error, 
    clearError 
  } = useAuthStore(
    useShallow((state) => ({
      forgotPassword: state.forgotPassword,
      resetPassword: state.resetPassword,
      isLoading: state.isLoading,
      error: state.error,
      clearError: state.clearError
    }))
  );

  const handleForgotPassword = useCallback(async (email: string) => {
    await forgotPassword(email);
  }, [forgotPassword]);

  const handleResetPassword = useCallback(async (data: ResetPasswordRequest) => {
    await resetPassword(data);
  }, [resetPassword]);

  // Track success state (no error and not loading after an action)
  const success = !error && !isLoading;

  const clearSuccess = useCallback(() => {
    // Success is derived state, so clearing error effectively clears success
    clearError();
  }, [clearError]);

  return {
    forgotPassword: handleForgotPassword,
    resetPassword: handleResetPassword,
    isLoading,
    error,
    success,
    clearError,
    clearSuccess
  };
};

/**
 * Profile management hook
 * Handles profile updates and password changes
 */
export const useProfile = () => {
  const { 
    user,
    updateProfile, 
    changePassword,
    refreshUser,
    isLoading, 
    error, 
    clearError 
  } = useAuthStore(
    useShallow((state) => ({
      user: state.user,
      updateProfile: state.updateProfile,
      changePassword: state.changePassword,
      refreshUser: state.refreshUser,
      isLoading: state.isLoading,
      error: state.error,
      clearError: state.clearError
    }))
  );

  const handleUpdateProfile = useCallback(async (data: UpdateProfileRequest) => {
    await updateProfile(data);
  }, [updateProfile]);

  const handleChangePassword = useCallback(async (data: ChangePasswordRequest) => {
    await changePassword(data);
  }, [changePassword]);

  const handleRefreshUser = useCallback(async () => {
    await refreshUser();
  }, [refreshUser]);

  return {
    user,
    updateProfile: handleUpdateProfile,
    changePassword: handleChangePassword,
    refreshUser: handleRefreshUser,
    isLoading,
    error,
    clearError
  };
};

/**
 * Authentication status hook
 * Provides only authentication status without actions
 */
export const useAuthStatus = () => {
  return useAuthStore(
    useShallow((state) => ({
      isAuthenticated: state.isAuthenticated,
      user: state.user,
      isLoading: state.isLoading
    }))
  );
};

/**
 * User data hook
 * Provides access to current user and progress data
 */
export const useUser = () => {
  return useAuthStore(
    useShallow((state) => ({
      user: state.user,
      progress: state.progress,
      isAuthenticated: state.isAuthenticated
    }))
  );
};

/**
 * Logout hook
 * Simple hook for logout functionality
 */
export const useLogout = () => {
  const logout = useAuthStore((state) => state.logout);
  
  return useCallback(() => {
    logout();
  }, [logout]);
};

/**
 * Auth error hook
 * Provides access to auth errors and clearing functionality
 */
export const useAuthError = () => {
  return useAuthStore(
    useShallow((state) => ({
      error: state.error,
      clearError: state.clearError
    }))
  );
};

/**
 * Auth initialization hook
 * Handles auth state initialization
 */
export const useAuthInitialization = () => {
  const { initialize, isLoading } = useAuthStore(
    useShallow((state) => ({
      initialize: state.initialize,
      isLoading: state.isLoading
    }))
  );

  useEffect(() => {
    initialize();
  }, [initialize]);

  return { isLoading };
};

/**
 * Protected route hook
 * Checks authentication status and provides redirect logic
 */
export const useProtectedRoute = (redirectPath?: string) => {
  const { isAuthenticated, isLoading, user } = useAuthStatus();

  return {
    isAuthenticated,
    isLoading,
    user,
    shouldRedirect: !isLoading && !isAuthenticated,
    redirectPath: redirectPath || '/login'
  };
};

/**
 * Token verification hook
 * Provides token verification functionality
 */
export const useTokenVerification = () => {
  const { verifyToken, token } = useAuthStore(
    useShallow((state) => ({
      verifyToken: state.verifyToken,
      token: state.token
    }))
  );

  const verifyCurrentToken = useCallback(async () => {
    if (!token) return false;
    return verifyToken(token);
  }, [verifyToken, token]);

  return {
    verifyToken,
    verifyCurrentToken,
    hasToken: !!token
  };
};