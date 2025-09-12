import { useState } from 'react';
import { ProfilesAPIClient } from '../../clients/ProfilesAPIClient';

/**
 * Profiles domain hook for profiles operations
 * Uses real backend endpoints: profiles
 */
export const useProfiles = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new ProfilesAPIClient();

  // Real API methods from backend config
  const getProfile = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getProfile as any)(...args);
      console.log('getProfile result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getProfile failed';
      setError(errorMessage);
      console.error('getProfile error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const updateProfile = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.updateProfile as any)(...args);
      console.log('updateProfile result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'updateProfile failed';
      setError(errorMessage);
      console.error('updateProfile error:', err);
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
    getProfile, updateProfile
  };
};