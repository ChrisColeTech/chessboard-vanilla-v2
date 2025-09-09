import { useCallback } from 'react'
import { useChessAudio } from '../../services/audio/audioService'
import { useAppStore } from '../../stores/appStore'

/**
 * Slots page actions - extracted from SlotMachineTestPage controls
 */
export function useSlotsActions() {
  const { playMove } = useChessAudio()
  const setCoinBalance = useAppStore((state) => state.setCoinBalance)

  const testSpin = useCallback(() => {
    playMove(false)
    // This matches the existing SlotMachine test spin button logic
  }, [playMove])

  const resetCoins = useCallback(() => {
    setCoinBalance(1000)
    playMove(false)
    // Reset coins to default value
  }, [setCoinBalance, playMove])

  return {
    testSpin,
    resetCoins
  }
}