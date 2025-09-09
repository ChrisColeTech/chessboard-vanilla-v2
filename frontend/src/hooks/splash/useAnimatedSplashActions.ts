import { useCallback, useState, useEffect, useMemo } from 'react'
import { useSplashActions } from './useSplashActions'
import { useAppStore } from '../../stores/appStore'

interface OrbitingPiece {
  id: string
  symbol: string
  angle: number
  delay: number
  settleDelay: number
  visible: boolean
}

/**
 * Hook for Progressive Piece Assembly - Animated Variant (CONCEPT 3)
 * 
 * DESIGN INTENT: Orbital piece assembly with rotating chess pieces around central crown.
 * Pieces orbit in from different angles and settle into formation.
 * Creates mesmerizing circular motion completely different from other variants.
 */
export function useAnimatedSplashActions() {
  const [animationKey, setAnimationKey] = useState(0)
  const [orbitingPieces, setOrbitingPieces] = useState<OrbitingPiece[]>([])
  const { goToMinimal, goToProgress, goToBranded } = useSplashActions()
  const openSplashModal = useAppStore((state) => state.openSplashModal)

  // Chess pieces positioned in orbital formation
  const initialOrbitPieces: OrbitingPiece[] = useMemo(() => [
    { id: 'queen', symbol: '♕', angle: 0, delay: 800, settleDelay: 2500, visible: false },
    { id: 'rook1', symbol: '♖', angle: 60, delay: 1000, settleDelay: 2700, visible: false },
    { id: 'bishop1', symbol: '♗', angle: 120, delay: 1200, settleDelay: 2900, visible: false },
    { id: 'knight1', symbol: '♘', angle: 180, delay: 1400, settleDelay: 3100, visible: false },
    { id: 'bishop2', symbol: '♗', angle: 240, delay: 1600, settleDelay: 3300, visible: false },
    { id: 'knight2', symbol: '♘', angle: 300, delay: 1800, settleDelay: 3500, visible: false }
  ], [])

  // Orbital assembly animation sequence
  useEffect(() => {
    setOrbitingPieces(initialOrbitPieces)

    const timeouts: NodeJS.Timeout[] = []

    // Start orbital animation for each piece
    initialOrbitPieces.forEach((piece) => {
      const timeout = setTimeout(() => {
        setOrbitingPieces(prev => prev.map(p => 
          p.id === piece.id ? { ...p, visible: true } : p
        ))
      }, piece.delay)
      timeouts.push(timeout)
    })

    return () => {
      timeouts.forEach(clearTimeout)
    }
  }, [animationKey, initialOrbitPieces])

  const testAnimatedAssembly = useCallback(() => {
    // No audio needed for assembly test
  }, [])

  const restartAnimation = useCallback(() => {
    setAnimationKey(prev => prev + 1)
  }, [])

  const toggleFullscreen = useCallback(() => {
    openSplashModal('animatedsplash')
  }, [openSplashModal])

  return {
    testAnimatedAssembly,
    restartAnimation,
    toggleFullscreen,
    orbitingPieces,
    // Cross-navigation
    goToMinimal,
    goToProgress,
    goToBranded,
    animationKey
  }
}