import { useState } from 'react';
import { AuthAPIClient } from '../../clients/AuthAPIClient';

/**
 * Mutation hooks for auth POST/PUT/DELETE operations
 * Available mutation methods: register, login, updateProfile, changePassword, verifyToken, forgotPassword, resetPassword, logout, checkEmailAvailability, checkUsernameAvailability, deleteAccount
 */
export const useAuthMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AuthAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating auth data using register:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.register as any)(id || data, data);
      console.log('auth mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useAuthMutations mutation error:`, err);
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