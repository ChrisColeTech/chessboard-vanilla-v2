import { useCallback } from "react";

export const useUIClickSoundOptimized = () => {
  const playMove = useCallback((isCapture: boolean = false) => {
    // Audio feedback implementation
    // For now, just a console log - can be enhanced with actual audio
    console.log(`UI Sound: ${isCapture ? 'capture' : 'move'}`);
  }, []);

  const playUISound = useCallback((soundType: string) => {
    console.log(`UI Sound: ${soundType}`);
  }, []);

  return {
    playMove,
    playUISound,
  };
};
