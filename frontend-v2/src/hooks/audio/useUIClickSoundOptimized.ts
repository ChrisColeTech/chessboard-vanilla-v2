<<<<<<< Updated upstream
import { useCallback, useRef } from "react";
import { useChessAudio } from "../../services/audio/audioService";

/**
 * Optimized UI Click Sound Hook with cooldown protection
 * Uses the same working audioService as the original
 */
export function useUIClickSoundOptimized() {
  const { playMove } = useChessAudio();
  const lastPlayTimeRef = useRef<number>(0);
  const CLICK_COOLDOWN_MS = 50;

  const playUIClick = useCallback(
    (context?: string) => {
      // Simple cooldown protection to prevent rapid-fire
      const now = Date.now();
      if (now - lastPlayTimeRef.current < CLICK_COOLDOWN_MS) {
        return false;
      }

      try {
        // Use the same method as original: chess capture sound for UI click feedback
        playMove(true); // true = capture sound for pronounced click feedback

        lastPlayTimeRef.current = now;

        if (context) {
          console.log(
            `🔊 [UI CLICK OPTIMIZED] Playing click sound for: ${context}`
          );
        }

        return true;
      } catch (error) {
        console.warn(
          `🔊 [UI CLICK OPTIMIZED] Failed to play click sound:`,
          error
        );
        return false;
      }
    },
    [playMove]
  );

  return { playUIClick, playMove };
}
=======
import { useCallback, useRef } from "react";
import { useChessAudio } from "../../services/audio/audioService";

/**
 * Optimized UI Click Sound Hook with cooldown protection
 * Uses the same working audioService as the original
 */
export function useUIClickSoundOptimized() {
  const { playMove } = useChessAudio();
  const lastPlayTimeRef = useRef<number>(0);
  const CLICK_COOLDOWN_MS = 50;

  const playUIClick = useCallback(
    (context?: string) => {
      // Simple cooldown protection to prevent rapid-fire
      const now = Date.now();
      if (now - lastPlayTimeRef.current < CLICK_COOLDOWN_MS) {
        return false;
      }

      try {
        // Use the same method as original: chess capture sound for UI click feedback
        playMove(true); // true = capture sound for pronounced click feedback

        lastPlayTimeRef.current = now;

        if (context) {
          console.log(
            `🔊 [UI CLICK OPTIMIZED] Playing click sound for: ${context}`
          );
        }

        return true;
      } catch (error) {
        console.warn(
          `🔊 [UI CLICK OPTIMIZED] Failed to play click sound:`,
          error
        );
        return false;
      }
    },
    [playMove]
  );

  return { playUIClick, playMove };
}
>>>>>>> Stashed changes
