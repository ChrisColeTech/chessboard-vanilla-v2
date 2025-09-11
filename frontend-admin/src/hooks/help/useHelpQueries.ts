import { useState, useEffect } from 'react';
import { HelpAPIClient } from '../../clients/HelpAPIClient';

/**
 * Query hooks for help GET operations
 * Available GET methods: getAllHelp, getHelpByCategory, searchHelp
 */
export const useHelpQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new HelpAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching help data using getAllHelp`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllHelp as any)(params);
      setData(result);
      console.log('help query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useHelpQueries query error:`, err);
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