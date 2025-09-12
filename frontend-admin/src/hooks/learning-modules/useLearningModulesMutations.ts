import { useState } from 'react';
import { LearningModulesAPIClient } from '../../clients/LearningModulesAPIClient';

/**
 * Mutation hooks for learning-modules POST/PUT/DELETE operations
 * Available mutation methods: completeModule
 */
export const useLearningModulesMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new LearningModulesAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating learning-modules data using completeModule:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.completeModule as any)(id || data, data);
      console.log('learning-modules mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useLearningModulesMutations mutation error:`, err);
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