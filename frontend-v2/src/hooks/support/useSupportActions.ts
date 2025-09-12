import { useCallback } from "react";
import { useAppStore } from "../../stores/appStore";
import { useUIClickSoundOptimized } from "../audio/useUIClickSoundOptimized";

export const useSupportActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const { playMove } = useUIClickSoundOptimized();

  const goToGameReviews = useCallback(() => {
    setCurrentChildPage('game-reviews');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToPuzzleSources = useCallback(() => {
    setCurrentChildPage('puzzle-sources');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToHelp = useCallback(() => {
    setCurrentChildPage('help');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToSubscriptions = useCallback(() => {
    setCurrentChildPage('subscriptions');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const backToMain = useCallback(() => {
    setCurrentChildPage(null);
  }, [setCurrentChildPage]);

  return {
    goToGameReviews,
    goToPuzzleSources,
    goToHelp,
    goToSubscriptions,
    backToMain
  };
};
