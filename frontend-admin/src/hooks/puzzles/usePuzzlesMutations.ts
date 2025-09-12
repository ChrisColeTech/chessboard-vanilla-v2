import { useState } from 'react';
import { PuzzlesAPIClient } from '../../clients/PuzzlesAPIClient';

/**
 * Mutation hooks for puzzles POST/PUT/DELETE operations
 * Available mutation methods: solvePuzzle, createCustomPuzzle
 */
export const usePuzzlesMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzlesAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating puzzles data using solvePuzzle:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.solvePuzzle as any)(id || data, data);
      console.log('puzzles mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$usePuzzlesMutations mutation error:`, err);
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