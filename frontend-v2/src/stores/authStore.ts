import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AuthState, LoginCredentials, UserInfo } from '../types/auth';
import { AuthAPIClient } from '../clients/AuthAPIClient';

interface AuthStore extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  updateUser: (user: Partial<UserInfo>) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      status: 'idle',
      user: null,
      token: null,
      error: null,
      
      login: async (credentials) => {
        set({ status: 'loading', error: null });
        
        try {
          const authClient = new AuthAPIClient();
          const response = await authClient.login(credentials);
          const { user, token } = response.data;
          
          localStorage.setItem('auth_token', token);
          set({ 
            status: 'authenticated', 
            user, 
            token, 
            error: null 
          });
        } catch (error: any) {
          set({ 
            status: 'error', 
            error: error.message 
          });
          throw error;
        }
      },
      
      logout: () => {
        localStorage.removeItem('auth_token');
        set({ 
          status: 'unauthenticated', 
          user: null, 
          token: null, 
          error: null 
        });
      },
      
      refreshToken: async () => {
        try {
          const token = get().token;
          if (!token) return false;
          
          const authClient = new AuthAPIClient();
          const response = await authClient.verifyToken({ token });
          const { user } = response.data;
          
          set({ user });
          return true;
        } catch {
          get().logout();
          return false;
        }
      },
      
      updateUser: (userData) => {
        const currentUser = get().user;
        if (currentUser) {
          set({ user: { ...currentUser, ...userData } });
        }
      },
      
      clearError: () => {
        set({ error: null });
      }
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        status: state.status 
      }),
    }
  )
);
