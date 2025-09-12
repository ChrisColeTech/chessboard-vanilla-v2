import { useState, useEffect } from 'react';
import { OpeningsAPIClient } from '../../clients/OpeningsAPIClient';

/**
 * Query hooks for openings GET operations
 * Available GET methods: getAllOpenings, getOpeningByEco, searchOpenings
 */
export const useOpeningsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new OpeningsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching openings data using getAllOpenings`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllOpenings as any)(params);
      setData(result);
      console.log('openings query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useOpeningsQueries query error:`, err);
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