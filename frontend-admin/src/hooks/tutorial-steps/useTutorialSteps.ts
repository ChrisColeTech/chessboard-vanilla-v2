import { useState } from 'react';
import { TutorialStepsAPIClient } from '../../clients/TutorialStepsAPIClient';

/**
 * TutorialSteps domain hook for tutorial-steps operations
 * Uses real backend endpoints: tutorial-steps
 */
export const useTutorialSteps = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new TutorialStepsAPIClient();

  // Real API methods from backend config
  const getStepsByTutorial = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getStepsByTutorial as any)(...args);
      console.log('getStepsByTutorial result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getStepsByTutorial failed';
      setError(errorMessage);
      console.error('getStepsByTutorial error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const completeStep = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.completeStep as any)(...args);
      console.log('completeStep result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'completeStep failed';
      setError(errorMessage);
      console.error('completeStep error:', err);
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
    getStepsByTutorial, completeStep
  };
};