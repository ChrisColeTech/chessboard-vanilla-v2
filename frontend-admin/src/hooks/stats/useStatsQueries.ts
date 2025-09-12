import { useState, useEffect } from 'react';
import { StatsAPIClient } from '../../clients/StatsAPIClient';

/**
 * Query hooks for stats GET operations
 * Available GET methods: getOverviewStats, getPuzzleStats, getGameStats, getProgressStats, getPerformanceStats, getRatingStats
 */
export const useStatsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new StatsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching stats data using getOverviewStats`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getOverviewStats as any)(params);
      setData(result);
      console.log('stats query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useStatsQueries query error:`, err);
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