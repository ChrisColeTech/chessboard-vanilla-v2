import { useState, useEffect } from 'react';
import { LearningModulesAPIClient } from '../../clients/LearningModulesAPIClient';

/**
 * Query hooks for learning-modules GET operations
 * Available GET methods: getModulesByPath, getModuleById
 */
export const useLearningModulesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new LearningModulesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching learning-modules data using getModulesByPath`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getModulesByPath as any)(params);
      setData(result);
      console.log('learning-modules query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useLearningModulesQueries query error:`, err);
    } finally {
      setLoading(false);
    }
  };

  // Auto-fetch on mount
  useEffect(() => {
    refetch();
  }, []);
  
  return {
    data,
    loading,
    error,
    refetch
  };
};