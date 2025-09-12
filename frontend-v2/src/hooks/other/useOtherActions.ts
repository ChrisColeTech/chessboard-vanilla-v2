import { useCallback } from "react";
import { useAppStore } from "../../stores/appStore";
import { useUIClickSoundOptimized } from "../audio/useUIClickSoundOptimized";

export const useOtherActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const { playMove } = useUIClickSoundOptimized();

  const goToAiOpponents = useCallback(() => {
    setCurrentChildPage('ai-opponents');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const backToMain = useCallback(() => {
    setCurrentChildPage(null);
  }, [setCurrentChildPage]);

  return {
    goToAiOpponents,
    backToMain
  };
};
