// Zustand store for authentication state management
import { create } from 'zustand';
import { devtools, persist, subscribeWithSelector } from 'zustand/middleware';
import type {
  User,
  UserProgress,
  AuthState,
  AuthActions,
  LoginRequest,
  RegisterRequest,
  ResetPasswordRequest,
  ChangePasswordRequest,
  UpdateProfileRequest,
  AuthError
} from '../types';

import { authService } from '../services';
import { 
  authStorage, 
  sessionUtils, 
  tokenUtils, 
  AuthErrorUtils 
} from '../utils';

// Define the complete auth store interface
interface AuthStoreInterface extends AuthState, AuthActions {
  // Additional store-specific methods
  initialize: () => Promise<void>;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setProgress: (progress: UserProgress | null) => void;
}

// Create the auth store
export const useAuthStore = create<AuthStoreInterface>()(
  devtools(
    persist(
      subscribeWithSelector((set, get) => ({
        // Initial state
        user: null,
        token: null,
        isLoading: false,
        isAuthenticated: false,
        error: null,
        progress: null,

        // State setters
        setLoading: (isLoading: boolean) => {
          set({ isLoading }, false, 'auth/setLoading');
        },

        setError: (error: string | null) => {
          set({ error }, false, 'auth/setError');
        },

        setUser: (user: User | null) => {
          set({ 
            user,
            isAuthenticated: !!user 
          }, false, 'auth/setUser');
        },

        setToken: (token: string | null) => {
          set({ token }, false, 'auth/setToken');
        },

        setProgress: (progress: UserProgress | null) => {
          set({ progress }, false, 'auth/setProgress');
        },

        // Initialize auth state from storage
        initialize: async () => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/initialize/start');

            const session = sessionUtils.initializeSession();
            
            if (session.isAuthenticated && session.user && session.token) {
              // Verify token with backend
              try {
                const response = await authService.verifyToken(session.token);
                
                if (response.success && response.data?.tokenValid) {
                  // Token is valid, fetch fresh user data
                  const userResponse = await authService.getCurrentUser();
                  
                  if (userResponse.success && userResponse.data) {
                    set({
                      user: userResponse.data.user,
                      token: session.token,
                      progress: userResponse.data.progress,
                      isAuthenticated: true,
                      isLoading: false,
                      error: null
                    }, false, 'auth/initialize/success');
                    
                    // Update storage with fresh data
                    authStorage.setUser(userResponse.data.user);
                    return;
                  }
                }
              } catch (error) {
                console.warn('Token verification failed during initialization:', error);
              }
            }

            // Clear invalid session
            sessionUtils.clearSession();
            set({
              user: null,
              token: null,
              progress: null,
              isAuthenticated: false,
              isLoading: false,
              error: null
            }, false, 'auth/initialize/cleared');

          } catch (error: any) {
            console.error('Auth initialization failed:', error);
            set({
              user: null,
              token: null,
              progress: null,
              isAuthenticated: false,
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(error)
            }, false, 'auth/initialize/error');
          }
        },

        // Auth actions
        login: async (credentials: LoginRequest) => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/login/start');

            const response = await authService.login(credentials);
            
            if (response.success && response.data) {
              const { user, token } = response.data;
              
              // Store auth data
              sessionUtils.setSession(user, token);
              
              // Fetch user progress
              let progress = null;
              try {
                const progressResponse = await authService.getCurrentUser();
                if (progressResponse.success && progressResponse.data) {
                  progress = progressResponse.data.progress;
                }
              } catch (error) {
                console.warn('Failed to fetch user progress:', error);
              }

              set({
                user,
                token,
                progress,
                isAuthenticated: true,
                isLoading: false,
                error: null
              }, false, 'auth/login/success');

            } else {
              throw AuthErrorUtils.createAuthError(
                'INVALID_CREDENTIALS',
                response.error || 'Login failed'
              );
            }
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/login/error');
            throw authError;
          }
        },

        register: async (userData: RegisterRequest) => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/register/start');

            const response = await authService.register(userData);
            
            if (response.success && response.data) {
              // Auto-login after registration
              await get().login({
                email: userData.email,
                password: userData.password
              });
            } else {
              throw AuthErrorUtils.createAuthError(
                'SERVER_ERROR',
                response.error || 'Registration failed'
              );
            }
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/register/error');
            throw authError;
          }
        },

        logout: () => {
          // Call logout endpoint (fire and forget)
          authService.logout().catch(console.warn);
          
          // Clear local state and storage
          sessionUtils.clearSession();
          set({
            user: null,
            token: null,
            progress: null,
            isAuthenticated: false,
            isLoading: false,
            error: null
          }, false, 'auth/logout');
        },

        forgotPassword: async (email: string) => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/forgotPassword/start');

            const response = await authService.forgotPassword(email);
            
            if (!response.success) {
              throw AuthErrorUtils.createAuthError(
                'SERVER_ERROR',
                response.error || 'Failed to send password reset email'
              );
            }

            set({ isLoading: false }, false, 'auth/forgotPassword/success');
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/forgotPassword/error');
            throw authError;
          }
        },

        resetPassword: async (data: ResetPasswordRequest) => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/resetPassword/start');

            const response = await authService.resetPassword(data);
            
            if (!response.success) {
              throw AuthErrorUtils.createAuthError(
                'SERVER_ERROR',
                response.error || 'Failed to reset password'
              );
            }

            set({ isLoading: false }, false, 'auth/resetPassword/success');
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/resetPassword/error');
            throw authError;
          }
        },

        changePassword: async (data: ChangePasswordRequest) => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/changePassword/start');

            const response = await authService.changePassword(data);
            
            if (!response.success) {
              throw AuthErrorUtils.createAuthError(
                'SERVER_ERROR',
                response.error || 'Failed to change password'
              );
            }

            set({ isLoading: false }, false, 'auth/changePassword/success');
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/changePassword/error');
            throw authError;
          }
        },

        updateProfile: async (data: UpdateProfileRequest) => {
          try {
            set({ isLoading: true, error: null }, false, 'auth/updateProfile/start');

            const response = await authService.updateProfile(data);
            
            if (response.success && response.data) {
              const updatedUser = response.data;
              
              // Update storage
              authStorage.setUser(updatedUser);
              
              set({
                user: updatedUser,
                isLoading: false,
                error: null
              }, false, 'auth/updateProfile/success');
            } else {
              throw AuthErrorUtils.createAuthError(
                'SERVER_ERROR',
                response.error || 'Failed to update profile'
              );
            }
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/updateProfile/error');
            throw authError;
          }
        },

        verifyToken: async (token: string): Promise<boolean> => {
          try {
            const response = await authService.verifyToken(token);
            return response.success && response.data?.tokenValid === true;
          } catch (error) {
            return false;
          }
        },

        refreshUser: async () => {
          try {
            set({ isLoading: true }, false, 'auth/refreshUser/start');

            const response = await authService.getCurrentUser();
            
            if (response.success && response.data) {
              const { user, progress } = response.data;
              
              // Update storage
              authStorage.setUser(user);
              
              set({
                user,
                progress,
                isLoading: false,
                error: null
              }, false, 'auth/refreshUser/success');
            } else {
              throw AuthErrorUtils.createAuthError(
                'SERVER_ERROR',
                'Failed to refresh user data'
              );
            }
          } catch (error: any) {
            const authError = error instanceof Error ? error as AuthError : AuthErrorUtils.parseApiError(error);
            set({
              isLoading: false,
              error: AuthErrorUtils.getUserFriendlyMessage(authError)
            }, false, 'auth/refreshUser/error');
            throw authError;
          }
        },

        clearError: () => {
          set({ error: null }, false, 'auth/clearError');
        }
      })),
      {
        name: 'chess-auth-storage',
        // Only persist non-sensitive data
        partialize: (state) => ({
          user: state.user,
          isAuthenticated: state.isAuthenticated
        }),
        // Custom storage to use our auth storage utilities
        storage: {
          getItem: (name: string) => {
            try {
              const item = localStorage.getItem(name);
              return item ? JSON.parse(item) : null;
            } catch {
              return null;
            }
          },
          setItem: (name: string, value: any) => {
            try {
              localStorage.setItem(name, JSON.stringify(value));
            } catch {
              // Storage failed, continue without persistence
            }
          },
          removeItem: (name: string) => {
            try {
              localStorage.removeItem(name);
            } catch {
              // Storage removal failed, continue
            }
          }
        }
      }
    ),
    {
      name: 'AuthStore'
    }
  )
);

// Subscribe to auth changes for side effects
useAuthStore.subscribe(
  (state) => state.token,
  (token) => {
    // Update token in storage when it changes
    if (token) {
      tokenUtils.setStoredToken(token);
    } else {
      tokenUtils.removeStoredToken();
    }
  }
);

useAuthStore.subscribe(
  (state) => state.user,
  (user) => {
    // Update user in storage when it changes
    if (user) {
      authStorage.setUser(user);
    } else {
      authStorage.removeUser();
    }
  }
);

// Export selectors for convenient access
export const authSelectors = {
  user: (state: AuthStoreInterface) => state.user,
  token: (state: AuthStoreInterface) => state.token,
  isAuthenticated: (state: AuthStoreInterface) => state.isAuthenticated,
  isLoading: (state: AuthStoreInterface) => state.isLoading,
  error: (state: AuthStoreInterface) => state.error,
  progress: (state: AuthStoreInterface) => state.progress,
};

// Export the store type for use in components
export type AuthStore = AuthStoreInterface;

export default useAuthStore;