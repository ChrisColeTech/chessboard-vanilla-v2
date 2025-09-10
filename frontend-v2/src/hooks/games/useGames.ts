import { useState } from 'react';
import { GamesAPIClient } from '../../clients/GamesAPIClient';

/**
 * Games domain hook for games operations
 * Uses real backend endpoints: games
 */
export const useGames = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new GamesAPIClient();

  // Real API methods from backend config
  const getGames = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getGames as any)(...args);
      console.log('getGames result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getGames failed';
      setError(errorMessage);
      console.error('getGames error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getGameById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getGameById as any)(...args);
      console.log('getGameById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getGameById failed';
      setError(errorMessage);
      console.error('getGameById error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const createGame = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.createGame as any)(...args);
      console.log('createGame result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'createGame failed';
      setError(errorMessage);
      console.error('createGame error:', err);
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
    getGames, getGameById, createGame
  };
};