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

// Auth hooks
import { useState, useEffect } from "react";

export const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate auth check
    const checkAuth = async () => {
      setIsLoading(true);
      // Placeholder: Always authenticated for now
      setTimeout(() => {
        setIsAuthenticated(true);
        setIsLoading(false);
      }, 100);
    };

    checkAuth();
  }, []);

  return {
    isAuthenticated,
    isLoading,
    login: () => setIsAuthenticated(true),
    logout: () => setIsAuthenticated(false)
  };
};
