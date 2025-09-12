import { useState, useEffect } from 'react';
import { EndgamesAPIClient } from '../../clients/EndgamesAPIClient';

/**
 * Query hooks for endgames GET operations
 * Available GET methods: getAllEndgames, getEndgameById, getEndgamesByCategory
 */
export const useEndgamesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new EndgamesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching endgames data using getAllEndgames`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllEndgames as any)(params);
      setData(result);
      console.log('endgames query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useEndgamesQueries query error:`, err);
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