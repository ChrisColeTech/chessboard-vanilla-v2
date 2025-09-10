import { useState } from 'react';
import { SubscriptionsAPIClient } from '../../clients/SubscriptionsAPIClient';

/**
 * Mutation hooks for subscriptions POST/PUT/DELETE operations
 * Available mutation methods: createSubscription, updateSubscription
 */
export const useSubscriptionsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new SubscriptionsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating subscriptions data using createSubscription:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.createSubscription as any)(id || data, data);
      console.log('subscriptions mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useSubscriptionsMutations mutation error:`, err);
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