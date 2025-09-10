import { useState } from 'react';
import { GameReviewsAPIClient } from '../../clients/GameReviewsAPIClient';

/**
 * Mutation hooks for game-reviews POST/PUT/DELETE operations
 * Available mutation methods: createReview
 */
export const useGameReviewsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new GameReviewsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating game-reviews data using createReview:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.createReview as any)(id || data, data);
      console.log('game-reviews mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useGameReviewsMutations mutation error:`, err);
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