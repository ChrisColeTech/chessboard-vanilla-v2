import { useState } from 'react';
import { AchievementsAPIClient } from '../../clients/AchievementsAPIClient';

/**
 * Achievements domain hook for achievements operations
 * Uses real backend endpoints: achievements
 */
export const useAchievements = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new AchievementsAPIClient();

  // Real API methods from backend config
  const getAllAchievements = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getAllAchievements as any)(...args);
      console.log('getAllAchievements result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getAllAchievements failed';
      setError(errorMessage);
      console.error('getAllAchievements error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getUserAchievements = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getUserAchievements as any)(...args);
      console.log('getUserAchievements result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getUserAchievements failed';
      setError(errorMessage);
      console.error('getUserAchievements error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const unlockAchievement = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.unlockAchievement as any)(...args);
      console.log('unlockAchievement result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'unlockAchievement failed';
      setError(errorMessage);
      console.error('unlockAchievement error:', err);
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
    getAllAchievements, getUserAchievements, unlockAchievement
  };
};