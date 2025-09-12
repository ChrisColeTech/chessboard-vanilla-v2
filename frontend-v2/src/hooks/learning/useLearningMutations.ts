import { useState } from 'react';
import { LearningAPIClient } from '../../clients/LearningAPIClient';

/**
 * Mutation hooks for learning POST/PUT/DELETE operations
 * Available mutation methods: enrollInPath, updateProgress
 */
export const useLearningMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new LearningAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating learning data using enrollInPath:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.enrollInPath as any)(id || data, data);
      console.log('learning mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useLearningMutations mutation error:`, err);
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