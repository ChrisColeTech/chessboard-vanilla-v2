import { useCallback } from 'react'
import { useAppStore } from '../../stores/appStore'
import { useChessAudio } from '../../services/audio/audioService'
import { usePuzzleService } from '../puzzle/usePuzzleService'
import { usePuzzleStore } from '../../stores/puzzleStore'

export const usePlayActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  const { playMove } = useChessAudio()
  const { loadRandomPuzzle, getHint } = usePuzzleService()
  const { currentPuzzle } = usePuzzleStore()

  const goToPlayChess = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('playchess')
    }, 100)
  }, [setCurrentChildPage])

  const goToPlayPuzzles = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('playpuzzles')
    }, 100)
  }, [setCurrentChildPage])

  // Placeholder actions for playchess page
  const newGame = useCallback(() => {
    console.log('🎮 [PLAY CHESS] Starting new game')
    playMove(false)
  }, [playMove])

  const pauseGame = useCallback(() => {
    console.log('⏸️ [PLAY CHESS] Pausing game')
    playMove(false)
  }, [playMove])

  const showMoves = useCallback(() => {
    console.log('👁️ [PLAY CHESS] Showing possible moves')
    playMove(false)
  }, [playMove])

  const undoMove = useCallback(() => {
    console.log('⏪ [PLAY CHESS] Undoing last move')
    playMove(false)
  }, [playMove])

  // Puzzle-specific actions
  const newPuzzle = useCallback(async () => {
    console.log('🧩 [PLAY PUZZLES] Loading new puzzle')
    try {
      await loadRandomPuzzle()
      playMove(false)
    } catch (error) {
      console.error('Failed to load new puzzle:', error)
    }
  }, [loadRandomPuzzle, playMove])

  const hint = useCallback(() => {
    getHint()
    playMove(false)
  }, [getHint, playMove])

  const solvePuzzle = useCallback(async () => {
    if (currentPuzzle) {
      console.log(`✅ Solution: ${currentPuzzle.solution_moves.join(', ')}`)
      setTimeout(async () => {
        await loadRandomPuzzle()
      }, 2000)
      playMove(false)
    }
  }, [currentPuzzle, loadRandomPuzzle, playMove])

  return {
    goToPlayChess,
    goToPlayPuzzles,
    newGame,
    pauseGame,
    showMoves,
    undoMove,
    newPuzzle,
    hint,
    solvePuzzle
  }
}