import { useState } from 'react';

/**
 * Mutation hooks for help POST/PUT/DELETE operations
 * No mutation methods available for this domain
 */
export const useHelpMutations = () => {
  const [loading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = async (_data: any) => {
    setError('No mutation methods available for help domain');
    return null;
  };
  
  return {
    loading,
    error,
    mutate
  };
};