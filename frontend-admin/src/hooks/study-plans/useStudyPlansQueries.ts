import { useState, useEffect } from 'react';
import { StudyPlansAPIClient } from '../../clients/StudyPlansAPIClient';

/**
 * Query hooks for study-plans GET operations
 * Available GET methods: getUserStudyPlans
 */
export const useStudyPlansQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new StudyPlansAPIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Fetching study-plans data using getUserStudyPlans`);
      // Call the GET method with type casting for flexibility
      const result = await (client.getUserStudyPlans as any)(params);
      setData(result);
      console.log('study-plans query result:', result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`$useStudyPlansQueries query error:`, err);
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