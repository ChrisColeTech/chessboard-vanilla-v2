import { useState } from 'react';
import { LearningModulesAPIClient } from '../../clients/LearningModulesAPIClient';

/**
 * LearningModules domain hook for learning-modules operations
 * Uses real backend endpoints: learning-modules
 */
export const useLearningModules = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new LearningModulesAPIClient();

  // Real API methods from backend config
  const getModulesByPath = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getModulesByPath as any)(...args);
      console.log('getModulesByPath result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getModulesByPath failed';
      setError(errorMessage);
      console.error('getModulesByPath error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getModuleById = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getModuleById as any)(...args);
      console.log('getModuleById result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getModuleById failed';
      setError(errorMessage);
      console.error('getModuleById error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const completeModule = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.completeModule as any)(...args);
      console.log('completeModule result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'completeModule failed';
      setError(errorMessage);
      console.error('completeModule error:', err);
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
    getModulesByPath, getModuleById, completeModule
  };
};