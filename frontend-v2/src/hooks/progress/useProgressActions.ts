import { useCallback } from "react";
import { useAppStore } from "../../stores/appStore";
import { useUIClickSoundOptimized } from "../audio/useUIClickSoundOptimized";

export const useProgressActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const { playMove } = useUIClickSoundOptimized();

  const goToStats = useCallback(() => {
    setCurrentChildPage('stats');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToAchievements = useCallback(() => {
    setCurrentChildPage('achievements');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToProgressFeature = useCallback(() => {
    setCurrentChildPage('progress');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToAnalytics = useCallback(() => {
    setCurrentChildPage('analytics');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToPuzzleAttempts = useCallback(() => {
    setCurrentChildPage('puzzle-attempts');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const backToMain = useCallback(() => {
    setCurrentChildPage(null);
  }, [setCurrentChildPage]);

  return {
    goToStats,
    goToAchievements,
    goToProgressFeature,
    goToAnalytics,
    goToPuzzleAttempts,
    backToMain
  };
};
