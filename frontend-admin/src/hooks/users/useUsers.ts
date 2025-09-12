import { useState } from 'react';
import { UsersAPIClient } from '../../clients/UsersAPIClient';

/**
 * Users domain hook for users operations
 * Uses real backend endpoints: users
 */
export const useUsers = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new UsersAPIClient();

  // Real API methods from backend config
  const getUserProfile = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserProfile as any)(...args);
      console.log('getUserProfile result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserProfile failed';
      setError(errorMessage);
      console.error('getUserProfile error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const updateUserProfile = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.updateUserProfile as any)(...args);
      console.log('updateUserProfile result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'updateUserProfile failed';
      setError(errorMessage);
      console.error('updateUserProfile error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getUserPreferences = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserPreferences as any)(...args);
      console.log('getUserPreferences result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserPreferences failed';
      setError(errorMessage);
      console.error('getUserPreferences error:', err);
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
    getUserProfile, updateUserProfile, getUserPreferences
  };
};