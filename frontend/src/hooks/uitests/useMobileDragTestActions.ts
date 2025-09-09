import { useCallback } from 'react'
import { useChessAudio } from '../../services/audio/audioService'

/**
 * Mobile Drag Test page actions - extracted from MobileDragTestPage controls
 */
export function useMobileDragTestActions() {
  const { playMove, playGameStart } = useChessAudio()

  const resetBoard = useCallback(() => {
    if (typeof window !== 'undefined' && (window as any).__wrapperChessBoardReset) {
      (window as any).__wrapperChessBoardReset()
      playGameStart() // Play welcome/new game sound when resetting board
    }
  }, [playGameStart])

  const testMoveSound = useCallback(() => {
    playMove(false)
  }, [playMove])

  const testCaptureSound = useCallback(() => {
    playMove(true)
  }, [playMove])

  const flipBoard = useCallback(() => {
    if (typeof window !== 'undefined' && (window as any).__wrapperChessBoardFlip) {
      (window as any).__wrapperChessBoardFlip()
      playMove(false)
    }
  }, [playMove])

  return {
    resetBoard,
    testMoveSound,
    testCaptureSound,
    flipBoard
  }
}