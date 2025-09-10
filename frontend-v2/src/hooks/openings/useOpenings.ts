import { useState } from 'react';
import { OpeningsAPIClient } from '../../clients/OpeningsAPIClient';

/**
 * Openings domain hook for openings operations
 * Uses real backend endpoints: openings
 */
export const useOpenings = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new OpeningsAPIClient();

  // Real API methods from backend config
  const getAllOpenings = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllOpenings as any)(...args);
      console.log('getAllOpenings result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllOpenings failed';
      setError(errorMessage);
      console.error('getAllOpenings error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getOpeningByEco = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getOpeningByEco as any)(...args);
      console.log('getOpeningByEco result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getOpeningByEco failed';
      setError(errorMessage);
      console.error('getOpeningByEco error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const searchOpenings = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.searchOpenings as any)(...args);
      console.log('searchOpenings result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'searchOpenings failed';
      setError(errorMessage);
      console.error('searchOpenings error:', err);
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
    getAllOpenings, getOpeningByEco, searchOpenings
  };
};