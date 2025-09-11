import { useState } from 'react';
import { SessionsAPIClient } from '../../clients/SessionsAPIClient';

/**
 * Mutation hooks for sessions POST/PUT/DELETE operations
 * Available mutation methods: createSession, expireSession
 */
export const useSessionsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new SessionsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating sessions data using createSession:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.createSession as any)(id || data, data);
      console.log('sessions mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useSessionsMutations mutation error:`, err);
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