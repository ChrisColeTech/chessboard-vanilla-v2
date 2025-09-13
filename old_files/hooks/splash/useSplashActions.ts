import { useCallback } from 'react'
import { useAppStore } from '../../stores/appStore'

export function useSplashActions() {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage)

  const goToMinimal = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('minimalsplash')
    }, 100)
  }, [setCurrentChildPage])

  const goToAnimated = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('animatedsplash')
    }, 100)
  }, [setCurrentChildPage])

  const goToProgress = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('loadingprogress')
    }, 100)
  }, [setCurrentChildPage])

  const goToBranded = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('brandedsplash')
    }, 100)
  }, [setCurrentChildPage])
  const goToLuxurysplash = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('luxurysplash')
    }, 100)
  }, [setCurrentChildPage])

  const goToFunctional = useCallback(() => {
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {
      setCurrentChildPage('functionalsplash')
    }, 100)
  }, [setCurrentChildPage])

  return {
    goToMinimal,
    goToAnimated,
    goToProgress,
    goToBranded,
    goToLuxurysplash,
    goToFunctional
  }
}