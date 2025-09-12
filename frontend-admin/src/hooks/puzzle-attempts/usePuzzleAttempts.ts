import { useState } from 'react';
import { PuzzleAttemptsAPIClient } from '../../clients/PuzzleAttemptsAPIClient';

/**
 * PuzzleAttempts domain hook for puzzle-attempts operations
 * Uses real backend endpoints: puzzle-attempts
 */
export const usePuzzleAttempts = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzleAttemptsAPIClient();

  // Real API methods from backend config
  const recordAttempt = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.recordAttempt as any)(...args);
      console.log('recordAttempt result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'recordAttempt failed';
      setError(errorMessage);
      console.error('recordAttempt error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getUserAttempts = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserAttempts as any)(...args);
      console.log('getUserAttempts result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserAttempts failed';
      setError(errorMessage);
      console.error('getUserAttempts error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getPuzzleAttempts = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getPuzzleAttempts as any)(...args);
      console.log('getPuzzleAttempts result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getPuzzleAttempts failed';
      setError(errorMessage);
      console.error('getPuzzleAttempts error:', err);
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
    recordAttempt, getUserAttempts, getPuzzleAttempts
  };
};