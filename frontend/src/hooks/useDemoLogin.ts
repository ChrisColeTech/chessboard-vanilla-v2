import { useState } from 'react';
import { useLogin } from './useAuth';

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
 */
export const useDemoLogin = (): UseDemoLoginReturn => {
  const { login, isLoading: loginLoading, error: loginError } = useLogin();
  const [isDemo, setIsDemo] = useState(false);

  const loginWithDemo = async (): Promise<void> => {
    try {
      setIsDemo(true);
      await login({
        email: DEMO_USER_CREDENTIALS.email,
        password: DEMO_USER_CREDENTIALS.password,
      });
    } catch (error) {
      // Error handling is managed by the login hook
      setIsDemo(false);
      throw error;
    }
  };

  return {
    loginWithDemo,
    isLoading: loginLoading,
    error: loginError,
    isDemo,
  };
};