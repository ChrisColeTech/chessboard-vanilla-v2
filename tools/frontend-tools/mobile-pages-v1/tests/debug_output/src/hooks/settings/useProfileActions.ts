/**
 * Profile Actions Hook
 * 
 * Provides action methods for Profile page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function useProfileActions() {
  const { setCurrentChildPage } = useAppStore();

  const goToPreferences = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('preferences');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPreferences
  };
}