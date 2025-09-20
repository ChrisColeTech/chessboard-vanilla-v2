/**
 * PageTwo Actions Hook
 * 
 * Provides action methods for PageTwo page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePageTwoActions() {
  const { setCurrentChildPage } = useAppStore();

  const goToPageOne = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('pageone');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPageOne
  };
}