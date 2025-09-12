import { useState } from 'react';
import { AnalyticsAPIClient } from '../../clients/AnalyticsAPIClient';

/**
 * Mutation hooks for analytics POST/PUT/DELETE operations
 * Available mutation methods: trackEvent
 */
export const useAnalyticsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AnalyticsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating analytics data using trackEvent:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.trackEvent as any)(id || data, data);
      console.log('analytics mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useAnalyticsMutations mutation error:`, err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    mutate
  };
};