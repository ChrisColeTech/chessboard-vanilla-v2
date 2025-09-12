import { useState } from 'react';
import { StatsAPIClient } from '../../clients/StatsAPIClient';

/**
 * Stats domain hook for stats operations
 * Uses real backend endpoints: stats
 */
export const useStats = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new StatsAPIClient();

  // Real API methods from backend config
  const getOverviewStats = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getOverviewStats as any)(...args);
      console.log('getOverviewStats result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getOverviewStats failed';
      setError(errorMessage);
      console.error('getOverviewStats error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getPuzzleStats = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getPuzzleStats as any)(...args);
      console.log('getPuzzleStats result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getPuzzleStats failed';
      setError(errorMessage);
      console.error('getPuzzleStats error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getGameStats = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getGameStats as any)(...args);
      console.log('getGameStats result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getGameStats failed';
      setError(errorMessage);
      console.error('getGameStats error:', err);
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
    getOverviewStats, getPuzzleStats, getGameStats
  };
};