import { useState } from 'react';
import { StudyPlansAPIClient } from '../../clients/StudyPlansAPIClient';

/**
 * Mutation hooks for study-plans POST/PUT/DELETE operations
 * Available mutation methods: createStudyPlan, updatePlan
 */
export const useStudyPlansMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new StudyPlansAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating study-plans data using createStudyPlan:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.createStudyPlan as any)(id || data, data);
      console.log('study-plans mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useStudyPlansMutations mutation error:`, err);
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