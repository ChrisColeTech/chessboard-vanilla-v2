import { useState } from 'react';
import { SessionsAPIClient } from '../../clients/SessionsAPIClient';

/**
 * Sessions domain hook for sessions operations
 * Uses real backend endpoints: sessions
 */
export const useSessions = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new SessionsAPIClient();

  // Real API methods from backend config
  const createSession = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.createSession as any)(...args);
      console.log('createSession result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'createSession failed';
      setError(errorMessage);
      console.error('createSession error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const validateSession = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.validateSession as any)(...args);
      console.log('validateSession result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'validateSession failed';
      setError(errorMessage);
      console.error('validateSession error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const expireSession = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.expireSession as any)(...args);
      console.log('expireSession result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'expireSession failed';
      setError(errorMessage);
      console.error('expireSession error:', err);
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
    createSession, validateSession, expireSession
  };
};