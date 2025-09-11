import { useState } from 'react';
import { AiOpponentsAPIClient } from '../../clients/AiOpponentsAPIClient';

/**
 * AiOpponents domain hook for ai-opponents operations
 * Uses real backend endpoints: ai-opponents
 */
export const useAiOpponents = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AiOpponentsAPIClient();

  // Real API methods from backend config
  const getAllOpponents = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllOpponents as any)(...args);
      console.log('getAllOpponents result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllOpponents failed';
      setError(errorMessage);
      console.error('getAllOpponents error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getOpponentById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getOpponentById as any)(...args);
      console.log('getOpponentById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getOpponentById failed';
      setError(errorMessage);
      console.error('getOpponentById error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getOpponentsByDifficulty = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getOpponentsByDifficulty as any)(...args);
      console.log('getOpponentsByDifficulty result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getOpponentsByDifficulty failed';
      setError(errorMessage);
      console.error('getOpponentsByDifficulty error:', err);
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
    getAllOpponents, getOpponentById, getOpponentsByDifficulty
  };
};