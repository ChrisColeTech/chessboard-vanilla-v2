import { useState } from 'react';
import { PuzzlesAPIClient } from '../../clients/PuzzlesAPIClient';

/**
 * Puzzles domain hook for puzzles operations
 * Uses real backend endpoints: puzzles
 */
export const usePuzzles = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzlesAPIClient();

  // Real API methods from backend config
  const getNextPuzzle = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getNextPuzzle as any)(...args);
      console.log('getNextPuzzle result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getNextPuzzle failed';
      setError(errorMessage);
      console.error('getNextPuzzle error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const solvePuzzle = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.solvePuzzle as any)(...args);
      console.log('solvePuzzle result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'solvePuzzle failed';
      setError(errorMessage);
      console.error('solvePuzzle error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  const getPuzzleHint = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      // Call the client method with proper error handling
      const result = await (client.getPuzzleHint as any)(...args);
      console.log('getPuzzleHint result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getPuzzleHint failed';
      setError(errorMessage);
      console.error('getPuzzleHint error:', err);
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
    getNextPuzzle, solvePuzzle, getPuzzleHint
  };
};