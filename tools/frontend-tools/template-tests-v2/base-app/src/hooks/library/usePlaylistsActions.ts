/**
 * Playlists Actions Hook
 * 
 * Provides action methods for Playlists page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePlaylistsActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToDownloads = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('downloads');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToDownloads
  };
}