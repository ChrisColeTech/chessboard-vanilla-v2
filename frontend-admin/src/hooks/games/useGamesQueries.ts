import { useState, useEffect } from 'react';
import { GamesAPIClient } from '../../clients/GamesAPIClient';

/**
 * Query hooks for games GET operations
 * Available GET methods: getGames, getGameById, getGameAnalysis, getGameReviews
 */
export const useGamesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new GamesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching games data using getGames`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getGames as any)(params);
      setData(result);
      console.log('games query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useGamesQueries query error:`, err);
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