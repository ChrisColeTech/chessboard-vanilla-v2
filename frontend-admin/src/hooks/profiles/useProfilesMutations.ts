import { useState } from 'react';
import { ProfilesAPIClient } from '../../clients/ProfilesAPIClient';

/**
 * Mutation hooks for profiles POST/PUT/DELETE operations
 * Available mutation methods: updateProfile
 */
export const useProfilesMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new ProfilesAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating profiles data using updateProfile:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.updateProfile as any)(id || data, data);
      console.log('profiles mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useProfilesMutations mutation error:`, err);
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