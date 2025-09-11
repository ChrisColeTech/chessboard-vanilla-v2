import { useState } from 'react';
import { ProgressAPIClient } from '../../clients/ProgressAPIClient';

/**
 * Progress domain hook for progress operations
 * Uses real backend endpoints: progress
 */
export const useProgress = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new ProgressAPIClient();

  // Real API methods from backend config
  const getUserProgress = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserProgress as any)(...args);
      console.log('getUserProgress result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserProgress failed';
      setError(errorMessage);
      console.error('getUserProgress error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const updateProgress = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.updateProgress as any)(...args);
      console.log('updateProgress result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'updateProgress failed';
      setError(errorMessage);
      console.error('updateProgress error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getProgressStats = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getProgressStats as any)(...args);
      console.log('getProgressStats result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getProgressStats failed';
      setError(errorMessage);
      console.error('getProgressStats error:', err);
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
    getUserProgress, updateProgress, getProgressStats
  };
};