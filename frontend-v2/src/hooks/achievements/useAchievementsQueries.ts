import { useState, useEffect } from 'react';
import { AchievementsAPIClient } from '../../clients/AchievementsAPIClient';

/**
 * Query hooks for achievements GET operations
 * Available GET methods: getAllAchievements, getUserAchievements
 */
export const useAchievementsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new AchievementsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching achievements data using getAllAchievements`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllAchievements as any)(params);
      setData(result);
      console.log('achievements query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useAchievementsQueries query error:`, err);
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