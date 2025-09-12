import { useState } from 'react';
import { HistoricGamesAPIClient } from '../../clients/HistoricGamesAPIClient';

/**
 * HistoricGames domain hook for historic-games operations
 * Uses real backend endpoints: historic-games
 */
export const useHistoricGames = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new HistoricGamesAPIClient();

  // Real API methods from backend config
  const getAllHistoricGames = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllHistoricGames as any)(...args);
      console.log('getAllHistoricGames result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllHistoricGames failed';
      setError(errorMessage);
      console.error('getAllHistoricGames error:', err);
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
  const searchGames = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.searchGames as any)(...args);
      console.log('searchGames result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'searchGames failed';
      setError(errorMessage);
      console.error('searchGames error:', err);
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
    getAllHistoricGames, getGameById, searchGames
  };
};