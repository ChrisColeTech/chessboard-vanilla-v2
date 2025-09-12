import { useState, useEffect } from 'react';
import { LearningAPIClient } from '../../clients/LearningAPIClient';

/**
 * Query hooks for learning GET operations
 * Available GET methods: getLearningPaths, getLearningPathById
 */
export const useLearningQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new LearningAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching learning data using getLearningPaths`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getLearningPaths as any)(params);
      setData(result);
      console.log('learning query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useLearningQueries query error:`, err);
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