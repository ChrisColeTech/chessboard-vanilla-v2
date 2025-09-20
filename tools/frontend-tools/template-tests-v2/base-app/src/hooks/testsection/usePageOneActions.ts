/**
 * PageOne Actions Hook
 * 
 * Provides action methods for PageOne page including sibling navigation.
 * Generated from pages.config.json with 1 sibling pages.
 */

import { useCallback } from 'react';
import { useAppStore } from '../../stores/appStore';

export function usePageOneActions() {
  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);

  const goToPageTwo = useCallback(() => {
    setTimeout(() => {
      setCurrentChildPage('pagetwo');
    }, 100);
  }, [setCurrentChildPage]);

  return {
    goToPageTwo
  };
}