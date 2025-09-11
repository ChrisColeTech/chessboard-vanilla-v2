import { useState } from 'react';
import { TutorialsAPIClient } from '../../clients/TutorialsAPIClient';

/**
 * Tutorials domain hook for tutorials operations
 * Uses real backend endpoints: tutorials
 */
export const useTutorials = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new TutorialsAPIClient();

  // Real API methods from backend config
  const getTutorials = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getTutorials as any)(...args);
      console.log('getTutorials result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getTutorials failed';
      setError(errorMessage);
      console.error('getTutorials error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getTutorialById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getTutorialById as any)(...args);
      console.log('getTutorialById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getTutorialById failed';
      setError(errorMessage);
      console.error('getTutorialById error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const completeTutorial = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.completeTutorial as any)(...args);
      console.log('completeTutorial result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'completeTutorial failed';
      setError(errorMessage);
      console.error('completeTutorial error:', err);
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
    getTutorials, getTutorialById, completeTutorial
  };
};