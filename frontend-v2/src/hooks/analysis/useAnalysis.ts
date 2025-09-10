import { useState } from 'react';
import { AnalysisAPIClient } from '../../clients/AnalysisAPIClient';

/**
 * Analysis domain hook for analysis operations
 * Uses real backend endpoints: analysis
 */
export const useAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AnalysisAPIClient();

  // Real API methods from backend config
  const analyzePosition = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.analyzePosition as any)(...args);
      console.log('analyzePosition result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'analyzePosition failed';
      setError(errorMessage);
      console.error('analyzePosition error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getPositionAnalysis = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getPositionAnalysis as any)(...args);
      console.log('getPositionAnalysis result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getPositionAnalysis failed';
      setError(errorMessage);
      console.error('getPositionAnalysis error:', err);
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
    analyzePosition, getPositionAnalysis
  };
};