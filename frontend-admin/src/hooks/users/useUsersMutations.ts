import { useState } from 'react';
import { UsersAPIClient } from '../../clients/UsersAPIClient';

/**
 * Mutation hooks for users POST/PUT/DELETE operations
 * Available mutation methods: updateUserProfile, updateUserPreferences, updateUserSettings
 */
export const useUsersMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new UsersAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating users data using updateUserProfile:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.updateUserProfile as any)(id || data, data);
      console.log('users mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useUsersMutations mutation error:`, err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    mutate
  };
};