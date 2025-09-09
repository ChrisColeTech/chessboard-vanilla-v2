import { useCallback } from 'react'
import { useUIClickSound } from './useUIClickSound'

/**
 * Hook for action sheet audio integration
 * Following established pattern from useUIClickSound.ts and useChessAudio()
 * SRP - ONLY handles action sheet specific audio, no other business logic
 */
export function useActionSheetAudio() {
  const { playUIClick } = useUIClickSound()

  const playActionSound = useCallback((actionLabel: string) => {
    // All action sheet items use consistent UI click sound (chess capture sound)
    playUIClick(`Action: ${actionLabel}`)
  }, [playUIClick])

  return {
    playActionSound
  }
}