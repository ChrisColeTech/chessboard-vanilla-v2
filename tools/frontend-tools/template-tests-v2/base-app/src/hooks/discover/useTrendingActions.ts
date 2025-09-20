/**
 * Trending Actions Hook
 * 
 * Provides action methods for Trending page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useTrendingActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToGenres = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('genres');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToGenres
  };
}