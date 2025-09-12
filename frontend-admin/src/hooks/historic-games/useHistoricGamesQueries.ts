import { useState, useEffect } from 'react';
import { HistoricGamesAPIClient } from '../../clients/HistoricGamesAPIClient';

/**
 * Query hooks for historic-games GET operations
 * Available GET methods: getAllHistoricGames, getGameById, searchGames, getGamesByPlayer
 */
export const useHistoricGamesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new HistoricGamesAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching historic-games data using getAllHistoricGames`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllHistoricGames as any)(params);
      setData(result);
      console.log('historic-games query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useHistoricGamesQueries query error:`, err);
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