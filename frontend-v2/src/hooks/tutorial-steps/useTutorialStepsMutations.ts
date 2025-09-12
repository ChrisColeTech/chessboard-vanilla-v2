import { useState } from 'react';
import { TutorialStepsAPIClient } from '../../clients/TutorialStepsAPIClient';

/**
 * Mutation hooks for tutorial-steps POST/PUT/DELETE operations
 * Available mutation methods: completeStep
 */
export const useTutorialStepsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new TutorialStepsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating tutorial-steps data using completeStep:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.completeStep as any)(id || data, data);
      console.log('tutorial-steps mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useTutorialStepsMutations mutation error:`, err);
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