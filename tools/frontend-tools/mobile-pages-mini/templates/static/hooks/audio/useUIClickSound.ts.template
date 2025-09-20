import { useChessAudio } from '../../services/audio/audioService'

/**
 * Chess-themed click sound hook
 * Uses chess capture sound for UI click feedback
 */
export function useUIClickSound() {
  const { playMove } = useChessAudio()
  
  const playUIClick = (_context?: string) => {
    console.log(`🔊 [UI CLICK HOOK] playUIClick called with context:`, _context);
    try {
      console.log(`🔊 [UI CLICK HOOK] Calling playMove(true) for capture sound`);
      // Play chess capture sound for UI click feedback
      playMove(true) // true = capture sound for pronounced click feedback
    } catch (error) {
      console.warn(`🔊 [UI CLICK] Failed to play click sound:`, error)
    }
  }
  
  return { playUIClick }
}