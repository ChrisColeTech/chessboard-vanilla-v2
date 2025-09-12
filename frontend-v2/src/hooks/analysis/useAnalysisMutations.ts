import { useState } from 'react';
import { AnalysisAPIClient } from '../../clients/AnalysisAPIClient';

/**
 * Mutation hooks for analysis POST/PUT/DELETE operations
 * Available mutation methods: analyzePosition
 */
export const useAnalysisMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AnalysisAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating analysis data using analyzePosition:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.analyzePosition as any)(id || data, data);
      console.log('analysis mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useAnalysisMutations mutation error:`, err);
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