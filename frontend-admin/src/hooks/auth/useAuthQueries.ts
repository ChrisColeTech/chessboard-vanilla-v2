import { useState, useEffect } from 'react';
import { AuthAPIClient } from '../../clients/AuthAPIClient';

/**
 * Query hooks for auth GET operations
 * Available GET methods: getCurrentUser, healthCheck
 */
export const useAuthQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new AuthAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching auth data using getCurrentUser`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getCurrentUser as any)(params);
      setData(result);
      console.log('auth query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useAuthQueries query error:`, err);
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