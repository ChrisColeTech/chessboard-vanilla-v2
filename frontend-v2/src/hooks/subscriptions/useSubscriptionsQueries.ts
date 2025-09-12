import { useState, useEffect } from 'react';
import { SubscriptionsAPIClient } from '../../clients/SubscriptionsAPIClient';

/**
 * Query hooks for subscriptions GET operations
 * Available GET methods: getUserSubscription
 */
export const useSubscriptionsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new SubscriptionsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching subscriptions data using getUserSubscription`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getUserSubscription as any)(params);
      setData(result);
      console.log('subscriptions query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useSubscriptionsQueries query error:`, err);
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