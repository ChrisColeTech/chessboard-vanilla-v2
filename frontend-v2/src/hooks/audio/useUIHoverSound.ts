<<<<<<< Updated upstream
import { useCallback, useRef } from 'react'
import { useChessAudio } from '../../services/audio/audioService'
import { useIsMobile } from '../core/useIsMobile'

/**
 * Chess-themed hover sound hook
 * Uses chess move sound for UI hover feedback
 * Skips hover sounds on mobile devices (no hover on touch)
 * Includes debouncing to prevent rapid-fire sounds on hover
 */
export function useUIHoverSound() {
  const { playMove } = useChessAudio()
  const isMobile = useIsMobile()
  
  // Cooldown mechanism to prevent rapid-fire sounds
  const lastPlayTimeRef = useRef<number>(0)
  const lastHoveredContextRef = useRef<string | null>(null)
  const HOVER_COOLDOWN_MS = 300 // Minimum time between hover sounds (increased)
  
  const playUIHover = useCallback((_context?: string) => {
    // Skip hover sounds on mobile devices (no hover on touch)
    if (isMobile) {
      return
    }
    
    const context = _context || 'unknown'
    const now = Date.now()
    const timeSinceLastPlay = now - lastPlayTimeRef.current
    
    // Prevent rapid-fire sounds with both time and context-based cooldown
    if (timeSinceLastPlay < HOVER_COOLDOWN_MS && lastHoveredContextRef.current === context) {
      console.log(`🔊 [UI HOVER] Skipped duplicate hover sound for: ${context} (${timeSinceLastPlay}ms ago)`)
      return // Skip if same context within cooldown period
    }
    
    try {
      // Update last play time and context before playing to prevent race conditions
      lastPlayTimeRef.current = now
      lastHoveredContextRef.current = context
      
      console.log(`🔊 [UI HOVER] Playing hover sound for: ${context}`)
      // Play chess move sound for hover feedback
      playMove(false) // false = move sound (not capture)
    } catch (error) {
      console.warn(`🔊 [UI HOVER] Failed to play hover sound for ${context}:`, error)
    }
  }, [playMove, isMobile])
  
  return { playUIHover }
=======
import { useCallback, useRef } from 'react'
import { useChessAudio } from '../../services/audio/audioService'
import { useIsMobile } from '../core/useIsMobile'

/**
 * Chess-themed hover sound hook
 * Uses chess move sound for UI hover feedback
 * Skips hover sounds on mobile devices (no hover on touch)
 * Includes debouncing to prevent rapid-fire sounds on hover
 */
export function useUIHoverSound() {
  const { playMove } = useChessAudio()
  const isMobile = useIsMobile()
  
  // Cooldown mechanism to prevent rapid-fire sounds
  const lastPlayTimeRef = useRef<number>(0)
  const lastHoveredContextRef = useRef<string | null>(null)
  const HOVER_COOLDOWN_MS = 300 // Minimum time between hover sounds (increased)
  
  const playUIHover = useCallback((_context?: string) => {
    // Skip hover sounds on mobile devices (no hover on touch)
    if (isMobile) {
      return
    }
    
    const context = _context || 'unknown'
    const now = Date.now()
    const timeSinceLastPlay = now - lastPlayTimeRef.current
    
    // Prevent rapid-fire sounds with both time and context-based cooldown
    if (timeSinceLastPlay < HOVER_COOLDOWN_MS && lastHoveredContextRef.current === context) {
      console.log(`🔊 [UI HOVER] Skipped duplicate hover sound for: ${context} (${timeSinceLastPlay}ms ago)`)
      return // Skip if same context within cooldown period
    }
    
    try {
      // Update last play time and context before playing to prevent race conditions
      lastPlayTimeRef.current = now
      lastHoveredContextRef.current = context
      
      console.log(`🔊 [UI HOVER] Playing hover sound for: ${context}`)
      // Play chess move sound for hover feedback
      playMove(false) // false = move sound (not capture)
    } catch (error) {
      console.warn(`🔊 [UI HOVER] Failed to play hover sound for ${context}:`, error)
    }
  }, [playMove, isMobile])
  
  return { playUIHover }
>>>>>>> Stashed changes
}