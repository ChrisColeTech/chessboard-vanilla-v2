import { useState } from 'react';

/**
 * Mutation hooks for ai-opponents POST/PUT/DELETE operations
 * No mutation methods available for this domain
 */
export const useAiOpponentsMutations = () => {
  const [loading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = async (_data: any) => {
    setError('No mutation methods available for ai-opponents domain');
    return null;
  };
  
  return {
    loading,
    error,
    mutate
  };
};