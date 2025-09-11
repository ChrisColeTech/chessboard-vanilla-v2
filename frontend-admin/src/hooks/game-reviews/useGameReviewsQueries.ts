import { useState, useEffect } from 'react';
import { GameReviewsAPIClient } from '../../clients/GameReviewsAPIClient';

/**
 * Query hooks for game-reviews GET operations
 * Available GET methods: getGameReviews, getReviewById
 */
export const useGameReviewsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new GameReviewsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching game-reviews data using getGameReviews`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getGameReviews as any)(params);
      setData(result);
      console.log('game-reviews query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useGameReviewsQueries query error:`, err);
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