import { useState } from 'react';
import { AuthAPIClient } from '../../clients/AuthAPIClient';

/**
 * Auth domain hook for auth operations
 * Uses real backend endpoints: auth
 */
export const useAuth = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AuthAPIClient();

  // Real API methods from backend config
  const register = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.register as any)(...args);
      console.log('register result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'register failed';
      setError(errorMessage);
      console.error('register error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const login = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.login as any)(...args);
      console.log('login result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'login failed';
      setError(errorMessage);
      console.error('login error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getCurrentUser = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getCurrentUser as any)(...args);
      console.log('getCurrentUser result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getCurrentUser failed';
      setError(errorMessage);
      console.error('getCurrentUser error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    clearError: () => setError(null),
    client,
    // Available methods
    register, login, getCurrentUser
  };
};