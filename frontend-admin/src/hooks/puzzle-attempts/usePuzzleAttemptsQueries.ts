import { useState, useEffect } from 'react';
import { PuzzleAttemptsAPIClient } from '../../clients/PuzzleAttemptsAPIClient';

/**
 * Query hooks for puzzle-attempts GET operations
 * Available GET methods: getUserAttempts, getPuzzleAttempts
 */
export const usePuzzleAttemptsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new PuzzleAttemptsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching puzzle-attempts data using getUserAttempts`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getUserAttempts as any)(params);
      setData(result);
      console.log('puzzle-attempts query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$usePuzzleAttemptsQueries query error:`, err);
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