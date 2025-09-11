import { useState } from 'react';
import { LearningAPIClient } from '../../clients/LearningAPIClient';

/**
 * Learning domain hook for learning operations
 * Uses real backend endpoints: learning
 */
export const useLearning = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new LearningAPIClient();

  // Real API methods from backend config
  const getLearningPaths = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getLearningPaths as any)(...args);
      console.log('getLearningPaths result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getLearningPaths failed';
      setError(errorMessage);
      console.error('getLearningPaths error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getLearningPathById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getLearningPathById as any)(...args);
      console.log('getLearningPathById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getLearningPathById failed';
      setError(errorMessage);
      console.error('getLearningPathById error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const enrollInPath = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.enrollInPath as any)(...args);
      console.log('enrollInPath result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'enrollInPath failed';
      setError(errorMessage);
      console.error('enrollInPath error:', err);
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
    getLearningPaths, getLearningPathById, enrollInPath
  };
};