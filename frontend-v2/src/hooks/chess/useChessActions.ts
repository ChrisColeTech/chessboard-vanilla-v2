import { useCallback } from "react";
import { useAppStore } from "../../stores/appStore";
import { useUIClickSoundOptimized } from "../audio/useUIClickSoundOptimized";

export const useChessActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const { playMove } = useUIClickSoundOptimized();

  const goToPuzzles = useCallback(() => {
    setCurrentChildPage('puzzles');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToGames = useCallback(() => {
    setCurrentChildPage('games');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToOpenings = useCallback(() => {
    setCurrentChildPage('openings');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToAnalysis = useCallback(() => {
    setCurrentChildPage('analysis');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToEndgames = useCallback(() => {
    setCurrentChildPage('endgames');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToHistoricGames = useCallback(() => {
    setCurrentChildPage('historic-games');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const backToMain = useCallback(() => {
    setCurrentChildPage(null);
  }, [setCurrentChildPage]);

  return {
    goToPuzzles,
    goToGames,
    goToOpenings,
    goToAnalysis,
    goToEndgames,
    goToHistoricGames,
    backToMain
  };
};
