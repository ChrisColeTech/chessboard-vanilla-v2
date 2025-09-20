import { useCallback, useRef } from 'react';
import { useChessAudio } from '../../services/audio/audioService';
import { useIsMobile } from '../core/useIsMobile';

/**
 * Optimized UI Hover Sound Hook with enhanced cooldown protection
 * Uses the same working audioService as the original with better rapid-fire prevention
 */
export function useUIHoverSoundOptimized() {
  const { playMove } = useChessAudio();
  const isMobile = useIsMobile();
  
  // Enhanced cooldown mechanism to prevent rapid-fire sounds
  const lastPlayTimeRef = useRef<number>(0);
  const lastHoveredContextRef = useRef<string | null>(null);
  const HOVER_COOLDOWN_MS = 300; // Minimum time between hover sounds

  const playUIHover = useCallback((context?: string) => {
    // Skip hover sounds on mobile devices (no hover on touch)
    if (isMobile) {
      return false;
    }
    
    const contextKey = context || 'unknown';
    const now = Date.now();
    const timeSinceLastPlay = now - lastPlayTimeRef.current;
    
    // Prevent rapid-fire sounds with both time and context-based cooldown
    if (timeSinceLastPlay < HOVER_COOLDOWN_MS && lastHoveredContextRef.current === contextKey) {
      console.log(`🔊 [UI HOVER OPTIMIZED] Skipped duplicate hover sound for: ${contextKey} (${timeSinceLastPlay}ms ago)`);
      return false; // Skip if same context within cooldown period
    }
    
    try {
      // Update last play time and context before playing to prevent race conditions
      lastPlayTimeRef.current = now;
      lastHoveredContextRef.current = contextKey;
      
      console.log(`🔊 [UI HOVER OPTIMIZED] Playing hover sound for: ${contextKey}`);
      // Use the same method as original: chess move sound for hover feedback
      playMove(false); // false = move sound (not capture)
      
      return true;
    } catch (error) {
      console.warn(`🔊 [UI HOVER OPTIMIZED] Failed to play hover sound for ${contextKey}:`, error);
      return false;
    }
  }, [playMove, isMobile]);

  return { playUIHover };
}