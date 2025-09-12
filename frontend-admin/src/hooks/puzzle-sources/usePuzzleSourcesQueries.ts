import { useState, useEffect } from 'react';
import { PuzzleSourcesAPIClient } from '../../clients/PuzzleSourcesAPIClient';

/**
 * Query hooks for puzzle-sources GET operations
 * Available GET methods: getAllSources, getSourceById
 */
export const usePuzzleSourcesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new PuzzleSourcesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching puzzle-sources data using getAllSources`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllSources as any)(params);
      setData(result);
      console.log('puzzle-sources query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$usePuzzleSourcesQueries query error:`, err);
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