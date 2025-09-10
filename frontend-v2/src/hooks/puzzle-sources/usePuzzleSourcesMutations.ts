import { useState } from 'react';

/**
 * Mutation hooks for puzzle-sources POST/PUT/DELETE operations
 * No mutation methods available for this domain
 */
export const usePuzzleSourcesMutations = () => {
  const [loading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = async (_data: any) => {
    setError('No mutation methods available for puzzle-sources domain');
    return null;
  };
  
  return {
    loading,
    error,
    mutate
  };
};