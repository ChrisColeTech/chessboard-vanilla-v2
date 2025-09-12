import { useState } from 'react';
import { GamesAPIClient } from '../../clients/GamesAPIClient';

/**
 * Mutation hooks for games POST/PUT/DELETE operations
 * Available mutation methods: createGame, updateGame, analyzeGame
 */
export const useGamesMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new GamesAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating games data using createGame:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.createGame as any)(id || data, data);
      console.log('games mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useGamesMutations mutation error:`, err);
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