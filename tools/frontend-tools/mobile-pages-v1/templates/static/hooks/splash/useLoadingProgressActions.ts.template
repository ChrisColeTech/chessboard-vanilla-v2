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
 * Hook for Progressive Piece Assembly - Loading Progress Variant (CONCEPT 3)
 * 
 * DESIGN INTENT: Dashboard showing systematic chess piece assembly with technical precision.
 * Each piece group has individual progress tracking showing professional setup sequence.
 * Status messages use proper chess terminology for educational training atmosphere.
 */
export function useLoadingProgressActions() {
  const [animationKey, setAnimationKey] = useState(0)
  const [pieceGroups, setPieceGroups] = useState<PieceGroup[]>([])
  const [currentStatus, setCurrentStatus] = useState('Preparing training board...')
  const { goToMinimal, goToAnimated, goToBranded } = useSplashActions()
  const openSplashModal = useAppStore((state) => state.openSplashModal)

  // Chess piece groups for progressive assembly
  const initialPieceGroups: PieceGroup[] = useMemo(() => [
    {
      id: 'king',
      name: 'King',
      symbol: '♔',
      progress: 0,
      completed: false,
      delay: 200,
      speed: 400
    },
    {
      id: 'queen',
      name: 'Queen',
      symbol: '♕',
      progress: 0,
      completed: false,
      delay: 600,
      speed: 400
    },
    {
      id: 'rooks',
      name: 'Rooks',
      symbol: '♖',
      progress: 0,
      completed: false,
      delay: 1000,
      speed: 400
    },
    {
      id: 'bishops',
      name: 'Bishops',
      symbol: '♗',
      progress: 0,
      completed: false,
      delay: 1400,
      speed: 400
    },
    {
      id: 'knights',
      name: 'Knights',
      symbol: '♘',
      progress: 0,
      completed: false,
      delay: 1800,
      speed: 400
    },
    {
      id: 'pawns',
      name: 'Pawns',
      symbol: '♙',
      progress: 0,
      completed: false,
      delay: 2200,
      speed: 400
    }
  ], [])

  // Progressive piece assembly animation
  useEffect(() => {
    setPieceGroups(initialPieceGroups.map(group => ({
      ...group,
      progress: 0,
      completed: false
    })))
    setCurrentStatus('Preparing training board...')

    const timeouts: NodeJS.Timeout[] = []
    const intervals: NodeJS.Timeout[] = []

    const statusMessages = [
      'Placing the king...',
      'Positioning the queen...',
      'Setting up rooks...',
      'Placing bishops...',
      'Deploying knights...',
      'Arranging pawns...',
      'Board setup complete!'
    ]

    initialPieceGroups.forEach((group, index) => {
      const startTimeout = setTimeout(() => {
        setCurrentStatus(statusMessages[index])
        
        const interval = setInterval(() => {
          setPieceGroups(prev => prev.map(g => {
            if (g.id === group.id && !g.completed && g.progress < 100) {
              const increment = Math.random() * 12 + 8 // 8-20% increment for faster, more consistent filling
              const newProgress = Math.min(g.progress + increment, 100)
              return {
                ...g,
                progress: Math.round(newProgress),
                completed: newProgress >= 100
              }
            }
            return g
          }))
        }, group.speed / 30)

        intervals.push(interval)
        
        // Stop interval when complete
        const stopTimeout = setTimeout(() => {
          clearInterval(interval)
        }, group.speed + 200)
        timeouts.push(stopTimeout)
        
      }, group.delay)
      
      timeouts.push(startTimeout)
    })

    // Final status
    const finalTimeout = setTimeout(() => {
      setCurrentStatus('Training session ready!')
    }, 3000)
    timeouts.push(finalTimeout)

    return () => {
      timeouts.forEach(clearTimeout)
      intervals.forEach(clearInterval)
    }
  }, [animationKey, initialPieceGroups])

  const testProgressBar = useCallback(() => {
    // No audio needed for piece assembly test
  }, [])

  const restartAnimation = useCallback(() => {
    setAnimationKey(prev => prev + 1)
  }, [])

  const toggleFullscreen = useCallback(() => {
    openSplashModal('loadingprogress')
  }, [openSplashModal])

  const overallProgress = useMemo(() => {
    if (pieceGroups.length === 0) return 0
    const totalProgress = pieceGroups.reduce((sum, group) => sum + group.progress, 0)
    return Math.round(totalProgress / pieceGroups.length)
  }, [pieceGroups])

  return {
    testProgressBar,
    restartAnimation,
    toggleFullscreen,
    pieceGroups,
    currentStatus,
    overallProgress,
    // Cross-navigation
    goToMinimal,
    goToAnimated,
    goToBranded,
    animationKey
  }
}