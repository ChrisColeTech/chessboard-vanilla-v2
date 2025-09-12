import { useState, useEffect } from 'react';
import { AiOpponentsAPIClient } from '../../clients/AiOpponentsAPIClient';

/**
 * Query hooks for ai-opponents GET operations
 * Available GET methods: getAllOpponents, getOpponentById, getOpponentsByDifficulty
 */
export const useAiOpponentsQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new AiOpponentsAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching ai-opponents data using getAllOpponents`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getAllOpponents as any)(params);
      setData(result);
      console.log('ai-opponents query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useAiOpponentsQueries query error:`, err);
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