import { useState, useEffect } from 'react';
import { ProfilesAPIClient } from '../../clients/ProfilesAPIClient';

/**
 * Query hooks for profiles GET operations
 * Available GET methods: getProfile
 */
export const useProfilesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new ProfilesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching profiles data using getProfile`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getProfile as any)(params);
      setData(result);
      console.log('profiles query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useProfilesQueries query error:`, err);
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