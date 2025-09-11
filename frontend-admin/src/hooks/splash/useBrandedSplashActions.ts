import { useCallback, useState, useEffect, useMemo } from 'react'
import { useSplashActions } from './useSplashActions'
import { useAppStore } from '../../stores/appStore'

interface PieceGroup {
  id: string
  name: string
  symbol: string
  progress: number
  completed: boolean
  delay: number
  speed: number
}

/**
 * Hook for Progressive Piece Assembly - Branded Academy Variant (CONCEPT 3)
 * 
 * DESIGN INTENT: Luxury chess academy with medallion piece assembly and rotating GM quotes.
 * Premium institutional branding showing prestige and grandmaster-level instruction.
 */
export function useBrandedSplashActions() {
  const [animationKey, setAnimationKey] = useState(0)
  const [pieceGroups, setPieceGroups] = useState<PieceGroup[]>([])
  const [currentQuote, setCurrentQuote] = useState('')
  const { goToMinimal, goToAnimated, goToProgress } = useSplashActions()
  const openSplashModal = useAppStore((state) => state.openSplashModal)

  // Chess piece groups for academy medallion assembly
  const initialPieceGroups: PieceGroup[] = useMemo(() => [
    { id: 'king', name: 'King', symbol: '♔', progress: 0, completed: false, delay: 200, speed: 350 },
    { id: 'queen', name: 'Queen', symbol: '♕', progress: 0, completed: false, delay: 550, speed: 350 },
    { id: 'rooks', name: 'Rooks', symbol: '♖', progress: 0, completed: false, delay: 900, speed: 350 },
    { id: 'bishops', name: 'Bishops', symbol: '♗', progress: 0, completed: false, delay: 1250, speed: 350 },
    { id: 'knights', name: 'Knights', symbol: '♘', progress: 0, completed: false, delay: 1600, speed: 350 },
    { id: 'pawns', name: 'Pawns', symbol: '♙', progress: 0, completed: false, delay: 1950, speed: 350 }
  ], [])

  // Grandmaster inspirational quotes
  const grandmasterQuotes = useMemo(() => [
    "Every chess master was once a beginner - Irving Chernev",
    "Chess is mental torture - Garry Kasparov",
    "I prefer to lose a really good game than to win a bad one - David Levy",
    "Chess is the struggle against error - Johannes Zukertort",
    "Tactics flow from a superior position - Bobby Fischer"
  ], [])

  // Academy piece assembly animation
  useEffect(() => {
    setPieceGroups(initialPieceGroups.map(group => ({
      ...group,
      progress: 0,
      completed: false
    })))
    setCurrentQuote(grandmasterQuotes[0])

    const timeouts: NodeJS.Timeout[] = []
    const intervals: NodeJS.Timeout[] = []

    // Quote rotation
    let quoteIndex = 0
    const quoteRotation = setInterval(() => {
      quoteIndex = (quoteIndex + 1) % grandmasterQuotes.length
      setCurrentQuote(grandmasterQuotes[quoteIndex])
    }, 2500)
    intervals.push(quoteRotation)

    // Piece assembly animation
    initialPieceGroups.forEach((group) => {
      const startTimeout = setTimeout(() => {
        const interval = setInterval(() => {
          setPieceGroups(prev => prev.map(g => {
            if (g.id === group.id && !g.completed && g.progress < 100) {
              const increment = Math.random() * 15 + 10 // 10-25% increment for elegant filling
              const newProgress = Math.min(g.progress + increment, 100)
              return {
                ...g,
                progress: Math.round(newProgress),
                completed: newProgress >= 100
              }
            }
            return g
          }))
        }, group.speed / 25)

        intervals.push(interval)
        
        const stopTimeout = setTimeout(() => {
          clearInterval(interval)
        }, group.speed + 150)
        timeouts.push(stopTimeout)
        
      }, group.delay)
      
      timeouts.push(startTimeout)
    })

    return () => {
      timeouts.forEach(clearTimeout)
      intervals.forEach(clearInterval)
    }
  }, [animationKey, initialPieceGroups, grandmasterQuotes])

  const testBrandAnimation = useCallback(() => {
    // No audio needed for premium branding test
  }, [])

  const restartAnimation = useCallback(() => {
    setAnimationKey(prev => prev + 1)
  }, [])

  const toggleFullscreen = useCallback(() => {
    openSplashModal('brandedsplash')
  }, [openSplashModal])

  const overallProgress = useMemo(() => {
    if (pieceGroups.length === 0) return 0
    const totalProgress = pieceGroups.reduce((sum, group) => sum + group.progress, 0)
    return Math.round(totalProgress / pieceGroups.length)
  }, [pieceGroups])

  return {
    pieceGroups,
    currentQuote,
    overallProgress,
    testBrandAnimation,
    restartAnimation,
    toggleFullscreen,
    // Cross-navigation
    goToMinimal,
    goToAnimated,
    goToProgress,
    animationKey
  }
}