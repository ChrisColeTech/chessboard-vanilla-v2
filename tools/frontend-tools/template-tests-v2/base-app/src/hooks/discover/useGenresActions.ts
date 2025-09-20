/**
 * Genres Actions Hook
 * 
 * Provides action methods for Genres page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useGenresActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToTrending = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('trending');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToTrending
  };
}