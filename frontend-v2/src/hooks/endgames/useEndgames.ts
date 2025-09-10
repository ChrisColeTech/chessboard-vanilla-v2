import { useState } from 'react';
import { EndgamesAPIClient } from '../../clients/EndgamesAPIClient';

/**
 * Endgames domain hook for endgames operations
 * Uses real backend endpoints: endgames
 */
export const useEndgames = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new EndgamesAPIClient();

  // Real API methods from backend config
  const getAllEndgames = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllEndgames as any)(...args);
      console.log('getAllEndgames result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllEndgames failed';
      setError(errorMessage);
      console.error('getAllEndgames error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getEndgameById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getEndgameById as any)(...args);
      console.log('getEndgameById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getEndgameById failed';
      setError(errorMessage);
      console.error('getEndgameById error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getEndgamesByCategory = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getEndgamesByCategory as any)(...args);
      console.log('getEndgamesByCategory result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getEndgamesByCategory failed';
      setError(errorMessage);
      console.error('getEndgamesByCategory error:', err);
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
    getAllEndgames, getEndgameById, getEndgamesByCategory
  };
};