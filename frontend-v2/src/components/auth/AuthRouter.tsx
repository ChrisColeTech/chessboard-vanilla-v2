import React, { useEffect } from 'react';
import { LoginPage } from '../../pages/user/LoginPage';
import { useAppStore } from '../../stores/appStore';

export type AuthPage = 'login' | 'register' | 'forgotPassword';

interface AuthRouterProps {
  initialPage?: AuthPage;
}

export const AuthRouter: React.FC<AuthRouterProps> = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);

  // Initialize to login state on mount
  useEffect(() => {
    setCurrentChildPage(null); // Always start with login (main page)
  }, [setCurrentChildPage]);

  // Only render LoginPage - it handles all child navigation internally
  return <LoginPage />;
};

export default AuthRouter;