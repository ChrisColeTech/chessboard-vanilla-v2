import { useState, useEffect } from 'react';
import { ProgressAPIClient } from '../../clients/ProgressAPIClient';

/**
 * Query hooks for progress GET operations
 * Available GET methods: getUserProgress, getProgressStats
 */
export const useProgressQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new ProgressAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching progress data using getUserProgress`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getUserProgress as any)(params);
      setData(result);
      console.log('progress query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useProgressQueries query error:`, err);
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