import { useState, useEffect } from 'react';
import { SessionsAPIClient } from '../../clients/SessionsAPIClient';

/**
 * Query hooks for sessions GET operations
 * Available GET methods: validateSession
 */
export const useSessionsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new SessionsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching sessions data using validateSession`);
      // Call the GET method with type casting for flexibility
      const result = await (client.validateSession as any)(params);
      setData(result);
      console.log('sessions query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useSessionsQueries query error:`, err);
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