import { useState, useEffect } from 'react';
import { AnalysisAPIClient } from '../../clients/AnalysisAPIClient';

/**
 * Query hooks for analysis GET operations
 * Available GET methods: getPositionAnalysis
 */
export const useAnalysisQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new AnalysisAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching analysis data using getPositionAnalysis`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getPositionAnalysis as any)(params);
      setData(result);
      console.log('analysis query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useAnalysisQueries query error:`, err);
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