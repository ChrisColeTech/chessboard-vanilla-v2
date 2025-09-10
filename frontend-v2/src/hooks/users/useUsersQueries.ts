import { useState, useEffect } from 'react';
import { UsersAPIClient } from '../../clients/UsersAPIClient';

/**
 * Query hooks for users GET operations
 * Available GET methods: getUserProfile, getUserPreferences, getUserSettings
 */
export const useUsersQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new UsersAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching users data using getUserProfile`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getUserProfile as any)(params);
      setData(result);
      console.log('users query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useUsersQueries query error:`, err);
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