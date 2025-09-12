import { useCallback } from "react";
import { useAppStore } from "../../stores/appStore";
import { useUIClickSoundOptimized } from "../audio/useUIClickSoundOptimized";

export const useUserActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);
  const { playMove } = useUIClickSoundOptimized();

  const goToUsers = useCallback(() => {
    setCurrentChildPage('users');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToAuth = useCallback(() => {
    setCurrentChildPage('auth');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToSessions = useCallback(() => {
    setCurrentChildPage('sessions');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const goToProfiles = useCallback(() => {
    setCurrentChildPage('profiles');
    playMove(false);
  }, [setCurrentChildPage, playMove]);

  const backToMain = useCallback(() => {
    setCurrentChildPage(null);
  }, [setCurrentChildPage]);

  return {
    goToUsers,
    goToAuth,
    goToSessions,
    goToProfiles,
    backToMain
  };
};
