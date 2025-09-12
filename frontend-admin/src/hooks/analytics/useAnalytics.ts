import { useState } from 'react';
import { AnalyticsAPIClient } from '../../clients/AnalyticsAPIClient';

/**
 * Analytics domain hook for analytics operations
 * Uses real backend endpoints: analytics
 */
export const useAnalytics = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AnalyticsAPIClient();

  // Real API methods from backend config
  const trackEvent = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.trackEvent as any)(...args);
      console.log('trackEvent result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'trackEvent failed';
      setError(errorMessage);
      console.error('trackEvent error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getUserAnalytics = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserAnalytics as any)(...args);
      console.log('getUserAnalytics result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserAnalytics failed';
      setError(errorMessage);
      console.error('getUserAnalytics error:', err);
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
    trackEvent, getUserAnalytics
  };
};