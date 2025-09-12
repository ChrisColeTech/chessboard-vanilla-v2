import { useState } from 'react';
import { SubscriptionsAPIClient } from '../../clients/SubscriptionsAPIClient';

/**
 * Subscriptions domain hook for subscriptions operations
 * Uses real backend endpoints: subscriptions
 */
export const useSubscriptions = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new SubscriptionsAPIClient();

  // Real API methods from backend config
  const getUserSubscription = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserSubscription as any)(...args);
      console.log('getUserSubscription result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserSubscription failed';
      setError(errorMessage);
      console.error('getUserSubscription error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const createSubscription = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.createSubscription as any)(...args);
      console.log('createSubscription result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'createSubscription failed';
      setError(errorMessage);
      console.error('createSubscription error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const updateSubscription = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.updateSubscription as any)(...args);
      console.log('updateSubscription result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'updateSubscription failed';
      setError(errorMessage);
      console.error('updateSubscription error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    clearError: () => setError(null),
    client,
    // Available methods
    getUserSubscription, createSubscription, updateSubscription
  };
};