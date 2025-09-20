/**
 * Downloads Actions Hook
 * 
 * Provides action methods for Downloads page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useDownloadsActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToPlaylists = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('playlists');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPlaylists
  };
}