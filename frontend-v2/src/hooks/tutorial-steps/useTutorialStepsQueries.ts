import { useState, useEffect } from 'react';
import { TutorialStepsAPIClient } from '../../clients/TutorialStepsAPIClient';

/**
 * Query hooks for tutorial-steps GET operations
 * Available GET methods: getStepsByTutorial
 */
export const useTutorialStepsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new TutorialStepsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching tutorial-steps data using getStepsByTutorial`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getStepsByTutorial as any)(params);
      setData(result);
      console.log('tutorial-steps query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useTutorialStepsQueries query error:`, err);
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