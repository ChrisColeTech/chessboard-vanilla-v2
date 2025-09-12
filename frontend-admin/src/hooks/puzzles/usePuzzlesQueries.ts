import { useState, useEffect } from 'react';
import { PuzzlesAPIClient } from '../../clients/PuzzlesAPIClient';

/**
 * Query hooks for puzzles GET operations
 * Available GET methods: getNextPuzzle, getPuzzleHint, getPuzzleCategories, getPuzzleHistory, getCustomPuzzles
 */
export const usePuzzlesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new PuzzlesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching puzzles data using getNextPuzzle`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getNextPuzzle as any)(params);
      setData(result);
      console.log('puzzles query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$usePuzzlesQueries query error:`, err);
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