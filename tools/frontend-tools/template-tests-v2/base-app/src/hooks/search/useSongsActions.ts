/**
 * Songs Actions Hook
 * 
 * Provides action methods for Songs page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useSongsActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToArtists = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('artists');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToArtists
  };
}