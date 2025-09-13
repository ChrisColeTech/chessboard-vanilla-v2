import { useState } from 'react';
import { useLogin } from './useAuth';
import { useAuthStore } from '../stores/authStore';
import { sessionUtils } from '../utils';

export interface DemoLoginCredentials {
  email: string;
  password: string;
  name: string;
}

// Demo user credentials from the project plan
export const DEMO_USER_CREDENTIALS: DemoLoginCredentials = {
  email: 'chessdemo@example.com',
  password: 'ChessDemo2024',
  name: 'Demo User'
};

export interface UseDemoLoginReturn {
  loginWithDemo: () => Promise<void>;
  isLoading: boolean;
  error: string | null;
  isDemo: boolean;
}

/**
 * Hook for demo user auto-login functionality
 * Provides easy access to login with pre-configured demo credentials
 * Bypasses API when running on ngrok for development
 */
export const useDemoLogin = (): UseDemoLoginReturn => {
  const { login, isLoading: loginLoading, error: loginError } = useLogin();
  const [isDemo, setIsDemo] = useState(false);
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  
  // Get auth store methods for bypass
  const setUser = useAuthStore((state) => state.setUser);
  const setToken = useAuthStore((state) => state.setToken);
  const setProgress = useAuthStore((state) => state.setProgress);
  const setLoading = useAuthStore((state) => state.setLoading);
  const setError = useAuthStore((state) => state.setError);

  // Check if running on ngrok
  const isNgrok = window.location.hostname.includes('ngrok') || 
                  window.location.hostname.includes('ngrok-free.app');

  const loginWithDemo = async (): Promise<void> => {
    try {
      setIsDemo(true);
      setLocalError(null);

      if (isNgrok) {
        // Bypass API call for ngrok - simulate successful login
        setLocalLoading(true);
        setLoading(true);
        setError(null);

        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Create mock user data matching auth types
        const mockUser = {
          id: 'demo-user-1',
          username: 'demo_user',
          email: DEMO_USER_CREDENTIALS.email,
          chess_elo: 1200,
          puzzle_rating: 1100,
          preferences: JSON.stringify({
            theme: 'system',
            language: 'en',
            notifications: {
              email: true,
              push: true
            }
          }),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };

        const mockToken = 'demo-token-ngrok-bypass';
        const mockProgress = {
          id: 'demo-progress-1',
          user_id: 'demo-user-1',
          puzzles_solved: 42,
          puzzles_correct: 35,
          current_streak: 3,
          best_streak: 8,
          total_time_spent: 1337,
          achievements_unlocked: JSON.stringify(['first_win', 'streak_3']),
          last_puzzle_date: new Date().toISOString(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };

        // Store auth data
        sessionUtils.setSession(mockUser, mockToken);
        
        // Update store
        setUser(mockUser);
        setToken(mockToken);
        setProgress(mockProgress);
        setLoading(false);
        setLocalLoading(false);

        console.log('🚀 Demo login bypassed API (ngrok detected)');
      } else {
        // Use normal API login
        await login({
          email: DEMO_USER_CREDENTIALS.email,
          password: DEMO_USER_CREDENTIALS.password,
        });
      }
    } catch (error) {
      setIsDemo(false);
      setLocalLoading(false);
      if (isNgrok) {
        const errorMessage = 'Demo login bypass failed';
        setLocalError(errorMessage);
        setError(errorMessage);
        setLoading(false);
      }
      throw error;
    }
  };

  return {
    loginWithDemo,
    isLoading: isNgrok ? localLoading : loginLoading,
    error: isNgrok ? localError : loginError,
    isDemo,
  };
};