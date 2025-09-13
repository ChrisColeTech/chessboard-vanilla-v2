import { useState } from 'react';
import { HistoricGamesAPIClient } from '../../clients/HistoricGamesAPIClient';

/**
 * Mutation hooks for historic-games POST/PUT/DELETE operations
 * Available mutation methods: searchGames
 */
export const useHistoricGamesMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new HistoricGamesAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating historic-games data using searchGames:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.searchGames as any)(id || data, data);
      console.log('historic-games mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useHistoricGamesMutations mutation error:`, err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    mutate
  };
};