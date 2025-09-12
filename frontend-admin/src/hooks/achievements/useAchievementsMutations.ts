import { useState } from 'react';
import { AchievementsAPIClient } from '../../clients/AchievementsAPIClient';

/**
 * Mutation hooks for achievements POST/PUT/DELETE operations
 * Available mutation methods: unlockAchievement
 */
export const useAchievementsMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AchievementsAPIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Mutating achievements data using unlockAchievement:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.unlockAchievement as any)(id || data, data);
      console.log('achievements mutation result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`$useAchievementsMutations mutation error:`, err);
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