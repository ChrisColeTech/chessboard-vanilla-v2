/**
 * PlayPuzzles Actions Hook
 * 
 * Provides action methods for PlayPuzzles page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePlayPuzzlesActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToPlayChess = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('playchess');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPlayChess
  };
}