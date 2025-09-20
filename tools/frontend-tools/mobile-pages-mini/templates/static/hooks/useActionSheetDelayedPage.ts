import { useState, useEffect } from "react";

/**
 * Hook to manage delayed page switching for action sheets
 * Applies a delay only when switching between child pages to prevent flickering
 */
export function useActionSheetDelayedPage(
  actionSheetPage: string,
  currentPage: string,
  currentChildPage: string | null
) {
  const [delayedActionSheetPage, setDelayedActionSheetPage] =
    useState(actionSheetPage);

  useEffect(() => {
    // Apply delay only when switching between child pages of the same parent
    // Don't delay when switching main tabs or when no child page is active
    const previousChildPage =
      delayedActionSheetPage === currentPage ? null : delayedActionSheetPage;
    const isSwitchingChildPages =
      currentChildPage &&
      previousChildPage &&
      currentChildPage !== previousChildPage;

    if (isSwitchingChildPages) {
      // Small delay to prevent action sheet from flickering during child page transitions
      const timer = setTimeout(() => {
        setDelayedActionSheetPage(actionSheetPage);
      }, 150);
      return () => clearTimeout(timer);
    } else {
      // No delay for main tab changes or when no child switching
      setDelayedActionSheetPage(actionSheetPage);
    }
  }, [actionSheetPage, currentPage, currentChildPage, delayedActionSheetPage]);

  return delayedActionSheetPage;
}