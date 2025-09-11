import { useState } from 'react';

/**
 * Mutation hooks for historic-games POST/PUT/DELETE operations
 * No mutation methods available for this domain
 */
export const useHistoricGamesMutations = () => {
  const [loading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = async (_data: any) => {
    setError('No mutation methods available for historic-games domain');
    return null;
  };
  
  return {
    loading,
    error,
    mutate
  };
};