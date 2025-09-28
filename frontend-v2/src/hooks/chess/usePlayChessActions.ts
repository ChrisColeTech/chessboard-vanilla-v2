/**
 * PlayChess Actions Hook
 * 
 * Provides action methods for PlayChess page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePlayChessActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToPlayPuzzles = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('playpuzzles');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPlayPuzzles
  };
}