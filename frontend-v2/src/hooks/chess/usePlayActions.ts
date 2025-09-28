/**
 * Play Actions Hook
 * 
 * Provides action methods for Play page including sibling navigation.
 * Generated from pages.config.json with 2 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePlayActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToPlayChess = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('playchess');
    }, 100);
  }, [setCurrentChildPage]);
  const goToPlayPuzzles = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('playpuzzles');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPlayChess, goToPlayPuzzles
  };
}