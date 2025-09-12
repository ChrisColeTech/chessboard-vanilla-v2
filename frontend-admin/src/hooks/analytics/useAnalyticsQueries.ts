import { useState, useEffect } from 'react';
import { AnalyticsAPIClient } from '../../clients/AnalyticsAPIClient';

/**
 * Query hooks for analytics GET operations
 * Available GET methods: getUserAnalytics
 */
export const useAnalyticsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new AnalyticsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching analytics data using getUserAnalytics`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getUserAnalytics as any)(params);
      setData(result);
      console.log('analytics query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useAnalyticsQueries query error:`, err);
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