/**
 * Preferences Actions Hook
 * 
 * Provides action methods for Preferences page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePreferencesActions() {
  const { setCurrentChildPage } = useAppStore();

  const goToProfile = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('profile');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToProfile
  };
}