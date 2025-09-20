/**
 * Settings Actions Hook
 * 
 * Provides action methods for Settings page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useSettingsActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToStats = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('stats');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToStats
  };
}