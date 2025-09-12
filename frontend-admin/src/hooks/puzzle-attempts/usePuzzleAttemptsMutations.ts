import { useState } from 'react';
import { PuzzleAttemptsAPIClient } from '../../clients/PuzzleAttemptsAPIClient';

/**
 * Mutation hooks for puzzle-attempts POST/PUT/DELETE operations
 * Available mutation methods: recordAttempt
 */
export const usePuzzleAttemptsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzleAttemptsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating puzzle-attempts data using recordAttempt:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.recordAttempt as any)(id || data, data);
      console.log('puzzle-attempts mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$usePuzzleAttemptsMutations mutation error:`, err);
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