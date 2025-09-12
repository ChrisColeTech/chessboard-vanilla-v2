import { useState } from 'react';
import { GameReviewsAPIClient } from '../../clients/GameReviewsAPIClient';

/**
 * GameReviews domain hook for game-reviews operations
 * Uses real backend endpoints: game-reviews
 */
export const useGameReviews = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new GameReviewsAPIClient();

  // Real API methods from backend config
  const createReview = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.createReview as any)(...args);
      console.log('createReview result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'createReview failed';
      setError(errorMessage);
      console.error('createReview error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getGameReviews = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getGameReviews as any)(...args);
      console.log('getGameReviews result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getGameReviews failed';
      setError(errorMessage);
      console.error('getGameReviews error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getReviewById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getReviewById as any)(...args);
      console.log('getReviewById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getReviewById failed';
      setError(errorMessage);
      console.error('getReviewById error:', err);
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
    createReview, getGameReviews, getReviewById
  };
};