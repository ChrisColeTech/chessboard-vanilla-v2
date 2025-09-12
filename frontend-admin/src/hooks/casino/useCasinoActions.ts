import { useCallback } from 'react'
import { useAppStore } from '../../stores/appStore'
import { useChessAudio } from '../../services/audio/audioService'

export const useCasinoActions = () => {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)
  const { playMove } = useChessAudio()

  const goToSlots = useCallback(() => {
    setCurrentChildPage('slots')
    playMove(false)
  }, [setCurrentChildPage, playMove])

  const goToBlackjack = useCallback(() => {
    setCurrentChildPage('blackjack')
    playMove(false)
  }, [setCurrentChildPage, playMove])

  const goToHoldem = useCallback(() => {
    setCurrentChildPage('holdem')
    playMove(false)
  }, [setCurrentChildPage, playMove])

  const goToRoulette = useCallback(() => {
    setCurrentChildPage('roulette')
    playMove(false)
  }, [setCurrentChildPage, playMove])

  const goToCraps = useCallback(() => {
    setCurrentChildPage('craps')
    playMove(false)
  }, [setCurrentChildPage, playMove])

  return {
    goToSlots,
    goToBlackjack,
    goToHoldem,
    goToRoulette,
    goToCraps
  }
}