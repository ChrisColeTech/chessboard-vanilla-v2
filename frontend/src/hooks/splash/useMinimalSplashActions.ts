import { useCallback, useState, useEffect, useMemo } from 'react'
import { useSplashActions } from './useSplashActions'
import { useAppStore } from '../../stores/appStore'

interface ChessPiece {
  id: string
  symbol: string
  name: string
  description: string
  visible: boolean
}

/**
 * Hook for Progressive Piece Assembly - Minimal Variant (CONCEPT 3)
 * 
 * DESIGN INTENT: Educational chess piece assembly that teaches proper chess hierarchy.
 * Pieces appear in logical sequence showing board setup progress.
 * Transforms loading time into learning time about chess fundamentals.
 */
export function useMinimalSplashActions() {
  const [animationKey, setAnimationKey] = useState(0)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Learning chess fundamentals...')
  const [visiblePieces, setVisiblePieces] = useState<ChessPiece[]>([])
  const [currentPieceDescription, setCurrentPieceDescription] = useState('The most important pieces in chess')
  const { goToAnimated, goToProgress, goToBranded } = useSplashActions()
  const openSplashModal = useAppStore((state) => state.openSplashModal)

  // Chess pieces in hierarchy order
  const chessPieces: ChessPiece[] = useMemo(() => [
    {
      id: 'king',
      symbol: '♔',
      name: 'King',
      description: 'The King - most important piece to protect',
      visible: false
    },
    {
      id: 'queen',
      symbol: '♕',
      name: 'Queen', 
      description: 'The Queen - most powerful piece on the board',
      visible: false
    },
    {
      id: 'rook',
      symbol: '♖',
      name: 'Rook',
      description: 'The Rook - controls ranks and files',
      visible: false
    },
    {
      id: 'bishop',
      symbol: '♗',
      name: 'Bishop',
      description: 'The Bishop - moves diagonally across the board',
      visible: false
    },
    {
      id: 'knight',
      symbol: '♘',
      name: 'Knight',
      description: 'The Knight - unique L-shaped movement',
      visible: false
    },
    {
      id: 'pawn',
      symbol: '♙',
      name: 'Pawn',
      description: 'The Pawn - foundation of chess strategy',
      visible: false
    }
  ], [])

  // Progressive piece assembly sequence
  useEffect(() => {
    setProgress(0)
    setStatus('Learning chess fundamentals...')
    setVisiblePieces(chessPieces)
    setCurrentPieceDescription('The most important pieces in chess')

    const timeouts: NodeJS.Timeout[] = []

    chessPieces.forEach((piece, index) => {
      const delay = 800 + (index * 500) // Staggered timing
      const timeout = setTimeout(() => {
        setVisiblePieces(prev => prev.map(p => 
          p.id === piece.id ? { ...p, visible: true } : p
        ))
        setCurrentPieceDescription(piece.description)
        setStatus(`Learning about the ${piece.name}...`)
        setProgress(Math.round(((index + 1) / chessPieces.length) * 100))
      }, delay)
      timeouts.push(timeout)
    })

    // Final completion
    const completionTimeout = setTimeout(() => {
      setStatus('Ready to master chess!')
      setCurrentPieceDescription('Now you know the chess pieces!')
    }, 800 + (chessPieces.length * 500) + 300)
    timeouts.push(completionTimeout)

    return () => {
      timeouts.forEach(clearTimeout)
    }
  }, [animationKey, chessPieces])

  const testMinimalLoad = useCallback(() => {
    // No audio needed for loading test
  }, [])

  const restartAnimation = useCallback(() => {
    setAnimationKey(prev => prev + 1)
    setProgress(0)
    setStatus('Initializing...')
  }, [])

  const toggleFullscreen = useCallback(() => {
    openSplashModal('minimalsplash')
  }, [openSplashModal])

  return {
    testMinimalLoad,
    restartAnimation,
    toggleFullscreen,
    progress,
    status,
    visiblePieces,
    currentPieceDescription,
    // Cross-navigation
    goToAnimated,
    goToProgress,
    goToBranded,
    animationKey
  }
}