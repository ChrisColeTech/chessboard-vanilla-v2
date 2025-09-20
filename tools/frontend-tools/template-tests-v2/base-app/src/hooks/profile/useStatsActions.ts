/**
 * Stats Actions Hook
 * 
 * Provides action methods for Stats page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useStatsActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToSettings = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('settings');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToSettings
  };
}