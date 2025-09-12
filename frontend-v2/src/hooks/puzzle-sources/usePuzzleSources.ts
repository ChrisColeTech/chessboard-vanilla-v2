import { useState } from 'react';
import { PuzzleSourcesAPIClient } from '../../clients/PuzzleSourcesAPIClient';

/**
 * PuzzleSources domain hook for puzzle-sources operations
 * Uses real backend endpoints: puzzle-sources
 */
export const usePuzzleSources = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzleSourcesAPIClient();

  // Real API methods from backend config
  const getAllSources = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllSources as any)(...args);
      console.log('getAllSources result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllSources failed';
      setError(errorMessage);
      console.error('getAllSources error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getSourceById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getSourceById as any)(...args);
      console.log('getSourceById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getSourceById failed';
      setError(errorMessage);
      console.error('getSourceById error:', err);
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
    getAllSources, getSourceById
  };
};