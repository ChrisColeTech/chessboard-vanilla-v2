/**
 * Artists Actions Hook
 * 
 * Provides action methods for Artists page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useArtistsActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToSongs = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('songs');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToSongs
  };
}