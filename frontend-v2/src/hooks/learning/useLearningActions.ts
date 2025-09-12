import { useCallback } from "react";
import { useAppStore } from "../../stores/appStore";
import { useUIClickSoundOptimized } from "../audio/useUIClickSoundOptimized";

export const useLearningActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const { playMove } = useUIClickSoundOptimized();

  const goToLearningFeature = useCallback(() => {
    setCurrentChildPage('learning');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToTutorials = useCallback(() => {
    setCurrentChildPage('tutorials');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToLearningModules = useCallback(() => {
    setCurrentChildPage('learning-modules');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToTutorialSteps = useCallback(() => {
    setCurrentChildPage('tutorial-steps');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToStudyPlans = useCallback(() => {
    setCurrentChildPage('study-plans');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const backToMain = useCallback(() => {
    setCurrentChildPage(null);
  }, [setCurrentChildPage]);

  return {
    goToLearningFeature,
    goToTutorials,
    goToLearningModules,
    goToTutorialSteps,
    goToStudyPlans,
    backToMain
  };
};
