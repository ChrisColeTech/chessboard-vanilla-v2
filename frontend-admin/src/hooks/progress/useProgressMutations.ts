import { useState } from 'react';
import { ProgressAPIClient } from '../../clients/ProgressAPIClient';

/**
 * Mutation hooks for progress POST/PUT/DELETE operations
 * Available mutation methods: updateProgress
 */
export const useProgressMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new ProgressAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating progress data using updateProgress:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.updateProgress as any)(id || data, data);
      console.log('progress mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useProgressMutations mutation error:`, err);
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