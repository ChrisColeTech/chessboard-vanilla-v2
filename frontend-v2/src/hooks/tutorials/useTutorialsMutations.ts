import { useState } from 'react';
import { TutorialsAPIClient } from '../../clients/TutorialsAPIClient';

/**
 * Mutation hooks for tutorials POST/PUT/DELETE operations
 * Available mutation methods: completeTutorial
 */
export const useTutorialsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new TutorialsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating tutorials data using completeTutorial:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.completeTutorial as any)(id || data, data);
      console.log('tutorials mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useTutorialsMutations mutation error:`, err);
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