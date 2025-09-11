import { useState, useEffect } from 'react';
import { TutorialsAPIClient } from '../../clients/TutorialsAPIClient';

/**
 * Query hooks for tutorials GET operations
 * Available GET methods: getTutorials, getTutorialById
 */
export const useTutorialsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new TutorialsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching tutorials data using getTutorials`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getTutorials as any)(params);
      setData(result);
      console.log('tutorials query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useTutorialsQueries query error:`, err);
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