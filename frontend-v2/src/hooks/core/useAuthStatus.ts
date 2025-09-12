import { useState, useEffect } from "react";

export const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    // Simulate auth check
    setTimeout(() => {
      setIsAuthenticated(true);
      setUser({ name: 'Demo User', email: 'demo@example.com' });
      setIsLoading(false);
    }, 500);
  }, []);

  return {
    isAuthenticated,
    isLoading,
    user
  };
};