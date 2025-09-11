import { useState } from 'react';
import { StudyPlansAPIClient } from '../../clients/StudyPlansAPIClient';

/**
 * StudyPlans domain hook for study-plans operations
 * Uses real backend endpoints: study-plans
 */
export const useStudyPlans = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new StudyPlansAPIClient();

  // Real API methods from backend config
  const getUserStudyPlans = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserStudyPlans as any)(...args);
      console.log('getUserStudyPlans result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserStudyPlans failed';
      setError(errorMessage);
      console.error('getUserStudyPlans error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const createStudyPlan = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.createStudyPlan as any)(...args);
      console.log('createStudyPlan result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'createStudyPlan failed';
      setError(errorMessage);
      console.error('createStudyPlan error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const updatePlan = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.updatePlan as any)(...args);
      console.log('updatePlan result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'updatePlan failed';
      setError(errorMessage);
      console.error('updatePlan error:', err);
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
    getUserStudyPlans, createStudyPlan, updatePlan
  };
};