import { useState } from 'react';
import { HelpAPIClient } from '../../clients/HelpAPIClient';

/**
 * Help domain hook for help operations
 * Uses real backend endpoints: help
 */
export const useHelp = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new HelpAPIClient();

  // Real API methods from backend config
  const getAllHelp = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllHelp as any)(...args);
      console.log('getAllHelp result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllHelp failed';
      setError(errorMessage);
      console.error('getAllHelp error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getHelpByCategory = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getHelpByCategory as any)(...args);
      console.log('getHelpByCategory result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getHelpByCategory failed';
      setError(errorMessage);
      console.error('getHelpByCategory error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const searchHelp = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.searchHelp as any)(...args);
      console.log('searchHelp result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'searchHelp failed';
      setError(errorMessage);
      console.error('searchHelp error:', err);
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
    getAllHelp, getHelpByCategory, searchHelp
  };
};