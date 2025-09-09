# Document 33: Worker Test Page Code Examples

## Overview
This document contains comprehensive code examples supporting the Worker Test Page implementation phases outlined in Document 32. All examples follow the established gaming UI patterns and mobile-first responsive design principles.

---

## Phase 1: Foundation Architecture

### Challenge System Types
```typescript
// src/types/chess-challenges.ts
export interface ChessChallenge {
  id: string
  title: string
  description: string
  difficulty: 1 | 2 | 3 | 4 | 5
  position: string // FEN string
  expectedMoves: string[]
  storyContext?: string
  hints: string[]
  category: 'opening' | 'tactics' | 'endgame' | 'historical'
  historicalContext?: {
    players: string[]
    tournament: string
    year: number
    significance: string
  }
}

export interface ChallengeProgress {
  challengeId: string
  completed: boolean
  attempts: number
  bestTime?: number
  hintsUsed: number
  completedAt?: Date
}

export interface UserProgress {
  challengesCompleted: ChallengeProgress[]
  skillsUnlocked: string[]
  currentStreak: number
  totalScore: number
  achievements: string[]
}

export type ChallengeCategory = 
  | 'story' 
  | 'quick' 
  | 'tactical' 
  | 'educational'

export interface ChallengeMode {
  id: string
  name: string
  description: string
  icon: string
  challenges: ChessChallenge[]
  unlockRequirement?: string
}
```

### Challenge Data Structure
```typescript
// src/data/challenges.ts
import type { ChessChallenge, ChallengeMode } from '../types/chess-challenges'

export const STORY_CHALLENGES: ChessChallenge[] = [
  {
    id: 'immortal-game-sacrifice',
    title: 'The Immortal Game',
    description: 'Adolf Anderssen made a stunning queen sacrifice. Can you find this brilliant move?',
    difficulty: 4,
    position: 'r2qkb1r/ppp2ppp/2n1bn2/2bpp3/3PP3/2N1BN2/PPP2PPP/R2QKB1R w KQkq - 0 6',
    expectedMoves: ['Qxd8+', 'Nxd8', 'Bxf7+'],
    category: 'historical',
    storyContext: 'In 1851, Adolf Anderssen played this immortal combination against Lionel Kieseritzky at the Café de la Régence in Paris. This game became famous for its brilliant sacrificial attack.',
    hints: [
      'Look for a forcing move that creates immediate threats',
      'Sometimes the most obvious capture is the right answer',
      'The queen sacrifice leads to a beautiful mating attack'
    ],
    historicalContext: {
      players: ['Adolf Anderssen', 'Lionel Kieseritzky'],
      tournament: 'Casual Game at Café de la Régence',
      year: 1851,
      significance: 'One of the most famous chess games ever played, showcasing romantic chess style'
    }
  },
  {
    id: 'opera-game-development',
    title: 'The Opera Game',
    description: 'Young Paul Morphy needs to develop quickly and attack. What\'s the best developing move?',
    difficulty: 2,
    position: 'rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2',
    expectedMoves: ['Nf3', 'Bc4', 'd3'],
    category: 'historical',
    storyContext: '13-year-old Paul Morphy was playing at the Paris Opera House against the Duke of Brunswick. He needed to develop quickly for a brilliant attack.',
    hints: [
      'Develop your pieces toward the center',
      'Knights before bishops in the opening',
      'Control the center while developing'
    ],
    historicalContext: {
      players: ['Paul Morphy', 'Duke of Brunswick & Count Isouard'],
      tournament: 'Paris Opera House',
      year: 1858,
      significance: 'Morphy\'s masterpiece demonstrating rapid development and attacking play'
    }
  }
]

export const QUICK_CHALLENGES: ChessChallenge[] = [
  {
    id: 'save-the-king-basic',
    title: 'Escape Check!',
    description: 'Your king is in check from the enemy queen. Find the safest escape square!',
    difficulty: 1,
    position: 'rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3',
    expectedMoves: ['Ke2', 'Kf2'],
    category: 'tactics',
    hints: [
      'When in check, you must move the king, block the attack, or capture the attacker',
      'Look for the safest square where the king won\'t be attacked again',
      'Sometimes the simplest move is the best'
    ]
  },
  {
    id: 'find-best-opening',
    title: 'Best Opening Move',
    description: 'The game just started. What\'s a strong opening move for White?',
    difficulty: 1,
    position: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    expectedMoves: ['e4', 'd4', 'Nf3', 'c4'],
    category: 'opening',
    hints: [
      'Good opening moves control the center',
      'Moving central pawns (e4, d4) is always strong',
      'Developing knights (Nf3) is also excellent'
    ]
  },
  {
    id: 'mate-in-one',
    title: 'Checkmate Puzzle',
    description: 'You can checkmate Black in just one move! Can you find it?',
    difficulty: 2,
    position: '6k1/5ppp/8/8/8/8/5PPP/R3K2R w K - 0 1',
    expectedMoves: ['Ra8#'],
    category: 'tactics',
    hints: [
      'Look for a move that attacks the king with no escape',
      'The rook can deliver mate from the back rank',
      'Make sure the king has no escape squares'
    ]
  }
]

export const CHALLENGE_MODES: ChallengeMode[] = [
  {
    id: 'story',
    name: 'Story Adventure',
    description: 'Learn chess through famous historical games',
    icon: '📖',
    challenges: STORY_CHALLENGES
  },
  {
    id: 'quick',
    name: 'Quick Challenges',
    description: 'Fast puzzles to improve your chess skills',
    icon: '⚡',
    challenges: QUICK_CHALLENGES
  },
  {
    id: 'tactical',
    name: 'Tactical Training',
    description: 'Master chess tactics and combinations',
    icon: '🎯',
    challenges: [] // Populated dynamically based on difficulty
  }
]
```

### Challenge Management Hook
```typescript
// src/hooks/useChessChallenges.ts
import { useState, useEffect, useCallback } from 'react'
import { CHALLENGE_MODES } from '../data/challenges'
import type { 
  ChessChallenge, 
  ChallengeProgress, 
  UserProgress, 
  ChallengeCategory 
} from '../types/chess-challenges'

interface UseChessChallengesReturn {
  currentChallenge: ChessChallenge | null
  availableModes: typeof CHALLENGE_MODES
  userProgress: UserProgress
  selectChallenge: (challengeId: string) => void
  completeChallenge: (challengeId: string, timeMs: number, hintsUsed: number) => void
  getNextChallenge: () => ChessChallenge | null
  getProgressStats: () => {
    totalCompleted: number
    currentStreak: number
    averageTime: number
    skillsUnlocked: number
  }
  resetProgress: () => void
}

const STORAGE_KEY = 'chess-challenge-progress'

export const useChessChallenges = (): UseChessChallengesReturn => {
  const [currentChallenge, setCurrentChallenge] = useState<ChessChallenge | null>(null)
  const [userProgress, setUserProgress] = useState<UserProgress>({
    challengesCompleted: [],
    skillsUnlocked: ['opening-basics'],
    currentStreak: 0,
    totalScore: 0,
    achievements: []
  })

  // Load progress from localStorage
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        const parsed = JSON.parse(saved) as UserProgress
        setUserProgress(parsed)
      } catch (error) {
        console.warn('Failed to parse saved challenge progress:', error)
      }
    }
  }, [])

  // Save progress to localStorage
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(userProgress))
  }, [userProgress])

  const selectChallenge = useCallback((challengeId: string) => {
    // Find challenge across all modes
    for (const mode of CHALLENGE_MODES) {
      const challenge = mode.challenges.find(c => c.id === challengeId)
      if (challenge) {
        setCurrentChallenge(challenge)
        return
      }
    }
    console.warn(`Challenge not found: ${challengeId}`)
  }, [])

  const completeChallenge = useCallback((challengeId: string, timeMs: number, hintsUsed: number) => {
    setUserProgress(prev => {
      const existingProgress = prev.challengesCompleted.find(p => p.challengeId === challengeId)
      
      if (existingProgress) {
        // Update existing progress
        const updatedProgress = prev.challengesCompleted.map(p => 
          p.challengeId === challengeId
            ? {
                ...p,
                attempts: p.attempts + 1,
                bestTime: p.bestTime ? Math.min(p.bestTime, timeMs) : timeMs,
                hintsUsed: p.hintsUsed + hintsUsed,
                completedAt: new Date()
              }
            : p
        )
        
        return {
          ...prev,
          challengesCompleted: updatedProgress,
          currentStreak: prev.currentStreak + 1,
          totalScore: prev.totalScore + calculateScore(timeMs, hintsUsed)
        }
      } else {
        // New completion
        const newProgress: ChallengeProgress = {
          challengeId,
          completed: true,
          attempts: 1,
          bestTime: timeMs,
          hintsUsed,
          completedAt: new Date()
        }
        
        return {
          ...prev,
          challengesCompleted: [...prev.challengesCompleted, newProgress],
          currentStreak: prev.currentStreak + 1,
          totalScore: prev.totalScore + calculateScore(timeMs, hintsUsed)
        }
      }
    })
    
    // Check for new achievements
    checkAchievements(challengeId, timeMs, hintsUsed)
  }, [])

  const getNextChallenge = useCallback((): ChessChallenge | null => {
    // Simple algorithm: find first uncompleted challenge
    for (const mode of CHALLENGE_MODES) {
      for (const challenge of mode.challenges) {
        const progress = userProgress.challengesCompleted.find(p => p.challengeId === challenge.id)
        if (!progress || !progress.completed) {
          return challenge
        }
      }
    }
    return null
  }, [userProgress])

  const getProgressStats = useCallback(() => {
    const totalChallenges = CHALLENGE_MODES.reduce((sum, mode) => sum + mode.challenges.length, 0)
    const completed = userProgress.challengesCompleted.filter(p => p.completed).length
    const totalTime = userProgress.challengesCompleted.reduce((sum, p) => sum + (p.bestTime || 0), 0)
    
    return {
      totalCompleted: completed,
      currentStreak: userProgress.currentStreak,
      averageTime: completed > 0 ? Math.round(totalTime / completed) : 0,
      skillsUnlocked: userProgress.skillsUnlocked.length
    }
  }, [userProgress])

  const resetProgress = useCallback(() => {
    setUserProgress({
      challengesCompleted: [],
      skillsUnlocked: ['opening-basics'],
      currentStreak: 0,
      totalScore: 0,
      achievements: []
    })
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  const calculateScore = (timeMs: number, hintsUsed: number): number => {
    const baseScore = 100
    const timePenalty = Math.floor(timeMs / 1000) // 1 point per second
    const hintPenalty = hintsUsed * 20 // 20 points per hint
    return Math.max(10, baseScore - timePenalty - hintPenalty)
  }

  const checkAchievements = (challengeId: string, timeMs: number, hintsUsed: number) => {
    // Achievement logic would go here
    // Examples: "First Victory", "Speed Demon", "No Hints Needed", etc.
  }

  return {
    currentChallenge,
    availableModes: CHALLENGE_MODES,
    userProgress,
    selectChallenge,
    completeChallenge,
    getNextChallenge,
    getProgressStats,
    resetProgress
  }
}
```

---

## Phase 2: Responsive Layout Components

### Mobile-First Collapsible Section
```typescript
// src/components/chess/CollapsibleSection.tsx
import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

interface CollapsibleSectionProps {
  title: string
  icon?: string
  children: React.ReactNode
  defaultExpanded?: boolean
  className?: string
}

export function CollapsibleSection({ 
  title, 
  icon, 
  children, 
  defaultExpanded = false,
  className = ''
}: CollapsibleSectionProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded)

  return (
    <div className={`card-gaming ${className}`}>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 flex items-center justify-between text-left hover:bg-foreground/5 transition-colors"
        aria-expanded={isExpanded}
      >
        <div className="flex items-center gap-3">
          {icon && <span className="text-xl">{icon}</span>}
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-muted-foreground" />
        ) : (
          <ChevronDown className="w-5 h-5 text-muted-foreground" />
        )}
      </button>
      
      {isExpanded && (
        <div className="px-4 pb-4 border-t border-border/20">
          <div className="pt-4">
            {children}
          </div>
        </div>
      )}
    </div>
  )
}
```

### Responsive Challenge Grid
```typescript
// src/components/chess/ChallengeGrid.tsx
import { useState } from 'react'
import type { ChallengeMode } from '../../types/chess-challenges'

interface ChallengeGridProps {
  modes: ChallengeMode[]
  onSelectChallenge: (challengeId: string) => void
  className?: string
}

export function ChallengeGrid({ modes, onSelectChallenge, className = '' }: ChallengeGridProps) {
  return (
    <div className={`space-y-4 ${className}`}>
      {/* Mobile: Single column stack */}
      <div className="space-y-3 sm:hidden">
        {modes.map(mode => (
          <div key={mode.id} className="card-gaming p-4">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xl">{mode.icon}</span>
              <div>
                <h4 className="font-semibold text-foreground">{mode.name}</h4>
                <p className="text-sm text-muted-foreground">{mode.description}</p>
              </div>
            </div>
            
            <div className="space-y-2">
              {mode.challenges.slice(0, 3).map(challenge => (
                <button
                  key={challenge.id}
                  onClick={() => onSelectChallenge(challenge.id)}
                  className="w-full p-3 text-left bg-foreground/5 hover:bg-foreground/10 
                           rounded-lg border border-border/20 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-foreground">{challenge.title}</span>
                    <div className="flex">
                      {Array.from({ length: challenge.difficulty }, (_, i) => (
                        <span key={i} className="text-yellow-500">⭐</span>
                      ))}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Tablet & Desktop: Grid layout */}
      <div className="hidden sm:grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {modes.map(mode => (
          <div key={mode.id} className="card-gaming p-4">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">{mode.icon}</span>
              <div>
                <h4 className="font-semibold text-foreground">{mode.name}</h4>
                <p className="text-sm text-muted-foreground">{mode.description}</p>
              </div>
            </div>
            
            <div className="space-y-2">
              {mode.challenges.slice(0, 4).map(challenge => (
                <button
                  key={challenge.id}
                  onClick={() => onSelectChallenge(challenge.id)}
                  className="w-full p-3 text-left bg-foreground/5 hover:bg-foreground/10 
                           rounded-lg border border-border/20 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-foreground text-sm">{challenge.title}</span>
                    <div className="flex">
                      {Array.from({ length: challenge.difficulty }, (_, i) => (
                        <span key={i} className="text-yellow-500 text-sm">⭐</span>
                      ))}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

### Responsive Status Bar
```typescript
// src/components/chess/EngineStatusBar.tsx
import { CheckCircle, XCircle, Clock, Zap } from 'lucide-react'
import { useStockfish } from '../../hooks/useStockfish'

interface EngineStatusBarProps {
  className?: string
}

export function EngineStatusBar({ className = '' }: EngineStatusBarProps) {
  const { isReady, isThinking, skillLevel, error } = useStockfish()

  return (
    <div className={`card-gaming p-4 ${className}`}>
      {/* Mobile: Compact single row */}
      <div className="flex items-center justify-between sm:hidden">
        <div className="flex items-center gap-2">
          {isReady ? (
            <CheckCircle className="w-4 h-4 text-green-500" />
          ) : (
            <XCircle className="w-4 h-4 text-red-500" />
          )}
          <span className="text-sm font-medium text-foreground">
            {isReady ? 'Ready' : 'Starting...'}
          </span>
        </div>
        
        <div className="flex items-center gap-3 text-sm text-muted-foreground">
          <div className="flex items-center gap-1">
            <Zap className="w-3 h-3" />
            <span>Skill: {skillLevel}</span>
          </div>
          {isThinking && (
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3 animate-spin" />
              <span>Thinking</span>
            </div>
          )}
        </div>
      </div>

      {/* Tablet & Desktop: Expanded layout */}
      <div className="hidden sm:block">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
            🎯 Computer Status
          </h3>
        </div>
        
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
          <div className="flex items-center gap-2">
            {isReady ? (
              <>
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span className="text-foreground">Ready to play!</span>
              </>
            ) : (
              <>
                <XCircle className="w-4 h-4 text-red-500" />
                <span className="text-red-500">Starting up...</span>
              </>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-foreground" />
            <span className="text-foreground">Skill Level: {skillLevel}/20</span>
          </div>
          
          <div className="flex items-center gap-2">
            {isThinking ? (
              <>
                <Clock className="w-4 h-4 text-yellow-500 animate-spin" />
                <span className="text-foreground">Thinking...</span>
              </>
            ) : (
              <>
                <Clock className="w-4 h-4 text-green-500" />
                <span className="text-foreground">Ready</span>
              </>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            <span className="text-muted-foreground">Response: Fast</span>
          </div>
        </div>
        
        {error && (
          <div className="mt-3 p-2 bg-red-500/10 border border-red-500/20 rounded-lg">
            <span className="text-red-500 text-sm">Error: {error}</span>
          </div>
        )}
      </div>
    </div>
  )
}
```

---

## Phase 3: Chess Board Component

### Mini Chess Board Display
```typescript
// src/components/chess/ChessBoardMini.tsx
import { useMemo } from 'react'

interface ChessBoardMiniProps {
  position: string // FEN string
  className?: string
  highlightSquares?: string[]
}

// Unicode chess pieces
const PIECE_SYMBOLS = {
  'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
  'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
} as const

type PieceSymbol = keyof typeof PIECE_SYMBOLS

export function ChessBoardMini({ position, className = '', highlightSquares = [] }: ChessBoardMiniProps) {
  const boardState = useMemo(() => {
    return parseFenToBoard(position)
  }, [position])

  const getSquareColor = (file: number, rank: number): string => {
    const squareName = String.fromCharCode(97 + file) + (8 - rank).toString()
    const isHighlighted = highlightSquares.includes(squareName)
    const isLight = (file + rank) % 2 === 0
    
    if (isHighlighted) {
      return isLight ? 'bg-yellow-200' : 'bg-yellow-300'
    }
    
    return isLight ? 'bg-slate-100' : 'bg-slate-400'
  }

  return (
    <div className={`inline-block ${className}`}>
      {/* Mobile: Smaller board */}
      <div className="block sm:hidden">
        <div className="grid grid-cols-8 gap-0 border-2 border-gray-600 w-64 h-64 mx-auto">
          {boardState.map((row, rankIndex) =>
            row.map((piece, fileIndex) => (
              <div
                key={`${fileIndex}-${rankIndex}`}
                className={`
                  flex items-center justify-center text-xl font-bold
                  ${getSquareColor(fileIndex, rankIndex)}
                `}
              >
                {piece && PIECE_SYMBOLS[piece as PieceSymbol]}
              </div>
            ))
          )}
        </div>
        
        {/* File labels (a-h) */}
        <div className="grid grid-cols-8 gap-0 w-64 mx-auto mt-1">
          {Array.from({ length: 8 }, (_, i) => (
            <div key={i} className="text-center text-sm font-medium text-muted-foreground">
              {String.fromCharCode(97 + i)}
            </div>
          ))}
        </div>
      </div>

      {/* Tablet & Desktop: Larger board */}
      <div className="hidden sm:block">
        <div className="flex">
          {/* Rank labels (8-1) */}
          <div className="flex flex-col justify-between pr-2">
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} className="h-12 flex items-center text-sm font-medium text-muted-foreground">
                {8 - i}
              </div>
            ))}
          </div>
          
          {/* Board */}
          <div>
            <div className="grid grid-cols-8 gap-0 border-2 border-gray-600">
              {boardState.map((row, rankIndex) =>
                row.map((piece, fileIndex) => (
                  <div
                    key={`${fileIndex}-${rankIndex}`}
                    className={`
                      w-12 h-12 flex items-center justify-center text-2xl font-bold
                      ${getSquareColor(fileIndex, rankIndex)}
                    `}
                  >
                    {piece && PIECE_SYMBOLS[piece as PieceSymbol]}
                  </div>
                ))
              )}
            </div>
            
            {/* File labels (a-h) */}
            <div className="grid grid-cols-8 gap-0 mt-1">
              {Array.from({ length: 8 }, (_, i) => (
                <div key={i} className="w-12 text-center text-sm font-medium text-muted-foreground">
                  {String.fromCharCode(97 + i)}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function parseFenToBoard(fen: string): (string | null)[][] {
  const boardPart = fen.split(' ')[0]
  const ranks = boardPart.split('/')
  
  return ranks.map(rank => {
    const squares: (string | null)[] = []
    
    for (const char of rank) {
      if (char >= '1' && char <= '8') {
        // Empty squares
        const emptyCount = parseInt(char)
        for (let i = 0; i < emptyCount; i++) {
          squares.push(null)
        }
      } else {
        // Piece
        squares.push(char)
      }
    }
    
    return squares
  })
}
```

### Challenge Display Component
```typescript
// src/components/chess/ChallengeDisplay.tsx
import { useState } from 'react'
import { Lightbulb, Eye, SkipForward, ThumbsUp } from 'lucide-react'
import { ChessBoardMini } from './ChessBoardMini'
import { ComputerAnalysis } from './ComputerAnalysis'
import type { ChessChallenge } from '../../types/chess-challenges'

interface ChallengeDisplayProps {
  challenge: ChessChallenge
  onAskComputer: () => void
  onShowAnswer: () => void
  onSkipChallenge: () => void
  onCompleteChallenge: (success: boolean) => void
  isComputerThinking: boolean
  className?: string
}

export function ChallengeDisplay({
  challenge,
  onAskComputer,
  onShowAnswer,
  onSkipChallenge,
  onCompleteChallenge,
  isComputerThinking,
  className = ''
}: ChallengeDisplayProps) {
  const [hintsUsed, setHintsUsed] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)

  const handleHint = () => {
    if (hintsUsed < challenge.hints.length) {
      setHintsUsed(hintsUsed + 1)
    }
  }

  const handleShowAnswer = () => {
    setShowAnswer(true)
    onShowAnswer()
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Mobile Layout */}
      <div className="space-y-4 lg:hidden">
        {/* Challenge Header */}
        <div className="card-gaming p-4">
          <div className="flex items-start justify-between mb-3">
            <h3 className="text-lg font-semibold text-foreground">{challenge.title}</h3>
            <div className="flex">
              {Array.from({ length: challenge.difficulty }, (_, i) => (
                <span key={i} className="text-yellow-500 text-sm">⭐</span>
              ))}
            </div>
          </div>
          
          <p className="text-foreground mb-4">{challenge.description}</p>
          
          {challenge.storyContext && (
            <div className="bg-primary/10 border border-primary/20 rounded-lg p-3 mb-4">
              <p className="text-sm text-foreground italic">{challenge.storyContext}</p>
            </div>
          )}
        </div>

        {/* Chess Board */}
        <div className="card-gaming p-4">
          <ChessBoardMini 
            position={challenge.position}
            className="w-full"
          />
        </div>

        {/* Action Buttons */}
        <div className="card-gaming p-4 space-y-3">
          <div className="grid grid-cols-1 gap-3">
            <button
              onClick={onAskComputer}
              disabled={isComputerThinking}
              className="btn-gaming-primary w-full py-3 px-4 disabled:opacity-50"
            >
              {isComputerThinking ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  Computer is thinking...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  🤔 Ask Computer
                </span>
              )}
            </button>
            
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={handleHint}
                disabled={hintsUsed >= challenge.hints.length}
                className="btn-gaming-secondary py-2 px-3 text-sm disabled:opacity-50"
              >
                <Lightbulb className="w-4 h-4 inline mr-1" />
                Hint ({hintsUsed}/{challenge.hints.length})
              </button>
              
              <button
                onClick={handleShowAnswer}
                className="btn-gaming-secondary py-2 px-3 text-sm"
              >
                <Eye className="w-4 h-4 inline mr-1" />
                Show Answer
              </button>
            </div>
            
            <button
              onClick={onSkipChallenge}
              className="text-muted-foreground hover:text-foreground text-sm py-2"
            >
              <SkipForward className="w-4 h-4 inline mr-1" />
              Skip Challenge
            </button>
          </div>

          {/* Hint Display */}
          {hintsUsed > 0 && (
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
              <p className="text-sm text-foreground">
                <strong>Hint:</strong> {challenge.hints[hintsUsed - 1]}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Desktop Layout */}
      <div className="hidden lg:grid lg:grid-cols-2 gap-6">
        {/* Left Column: Challenge Info */}
        <div className="space-y-4">
          <div className="card-gaming p-6">
            <div className="flex items-start justify-between mb-4">
              <h3 className="text-xl font-semibold text-foreground">{challenge.title}</h3>
              <div className="flex">
                {Array.from({ length: challenge.difficulty }, (_, i) => (
                  <span key={i} className="text-yellow-500">⭐</span>
                ))}
              </div>
            </div>
            
            <p className="text-foreground text-lg mb-6">{challenge.description}</p>
            
            {challenge.storyContext && (
              <div className="bg-primary/10 border border-primary/20 rounded-lg p-4 mb-6">
                <h4 className="font-medium text-foreground mb-2">Historical Context:</h4>
                <p className="text-sm text-foreground italic">{challenge.storyContext}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                onClick={onAskComputer}
                disabled={isComputerThinking}
                className="btn-gaming-primary w-full py-3 px-4 disabled:opacity-50"
              >
                {isComputerThinking ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                    Computer is thinking...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    🤔 Ask Computer
                  </span>
                )}
              </button>
              
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={handleHint}
                  disabled={hintsUsed >= challenge.hints.length}
                  className="btn-gaming-secondary py-2 px-3 text-sm disabled:opacity-50"
                >
                  <Lightbulb className="w-4 h-4 inline mr-1" />
                  Hint
                </button>
                
                <button
                  onClick={handleShowAnswer}
                  className="btn-gaming-secondary py-2 px-3 text-sm"
                >
                  <Eye className="w-4 h-4 inline mr-1" />
                  Answer
                </button>
                
                <button
                  onClick={onSkipChallenge}
                  className="text-muted-foreground hover:text-foreground text-sm py-2"
                >
                  <SkipForward className="w-4 h-4 inline mr-1" />
                  Skip
                </button>
              </div>
            </div>

            {/* Hint Display */}
            {hintsUsed > 0 && (
              <div className="mt-4 bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                <p className="text-sm text-foreground">
                  <strong>Hint {hintsUsed}:</strong> {challenge.hints[hintsUsed - 1]}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Chess Board */}
        <div className="card-gaming p-6">
          <ChessBoardMini 
            position={challenge.position}
            className="w-full"
          />
          
          {challenge.historicalContext && (
            <div className="mt-6 bg-muted/20 rounded-lg p-4">
              <h4 className="font-medium text-foreground mb-2">Game Details:</h4>
              <div className="text-sm text-muted-foreground space-y-1">
                <p><strong>Players:</strong> {challenge.historicalContext.players.join(' vs ')}</p>
                <p><strong>Event:</strong> {challenge.historicalContext.tournament}</p>
                <p><strong>Year:</strong> {challenge.historicalContext.year}</p>
                <p className="pt-2 italic">{challenge.historicalContext.significance}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
```

---

## Phase 4: Computer Analysis Component

### User-Friendly Analysis Display
```typescript
// src/components/chess/ComputerAnalysis.tsx
import { useState, useEffect } from 'react'
import { Brain, Clock, Star, ThumbsUp, RotateCcw } from 'lucide-react'

interface ComputerAnalysisProps {
  move: string | null
  analysis: string
  confidence: number // 1-5
  thinkingTime: number // milliseconds
  onGoodChoice: () => void
  onTryAnother: () => void
  isVisible: boolean
  className?: string
}

export function ComputerAnalysis({
  move,
  analysis,
  confidence,
  thinkingTime,
  onGoodChoice,
  onTryAnother,
  isVisible,
  className = ''
}: ComputerAnalysisProps) {
  const [displayAnalysis, setDisplayAnalysis] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  // Typewriter effect for analysis text
  useEffect(() => {
    if (!isVisible || !analysis) return

    setIsTyping(true)
    setDisplayAnalysis('')
    
    let currentIndex = 0
    const typingSpeed = 30 // milliseconds per character
    
    const timer = setInterval(() => {
      if (currentIndex < analysis.length) {
        setDisplayAnalysis(analysis.slice(0, currentIndex + 1))
        currentIndex++
      } else {
        clearInterval(timer)
        setIsTyping(false)
      }
    }, typingSpeed)

    return () => clearInterval(timer)
  }, [analysis, isVisible])

  if (!isVisible) return null

  const formatThinkingTime = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(1)}s`
  }

  return (
    <div className={`card-gaming ${className}`}>
      {/* Mobile Layout */}
      <div className="p-4 sm:hidden">
        <div className="flex items-center gap-2 mb-3">
          <Brain className="w-5 h-5 text-primary" />
          <h4 className="font-semibold text-foreground">Computer Says:</h4>
        </div>
        
        {move && (
          <div className="mb-3 p-3 bg-primary/10 border border-primary/20 rounded-lg">
            <p className="text-foreground font-medium">
              I suggest: <span className="font-mono bg-background px-2 py-1 rounded">{move}</span>
            </p>
          </div>
        )}
        
        <div className="mb-4">
          <p className="text-foreground whitespace-pre-wrap">
            {displayAnalysis}
            {isTyping && <span className="animate-pulse">|</span>}
          </p>
        </div>
        
        <div className="flex items-center justify-between mb-4 text-sm">
          <div className="flex items-center gap-1">
            <span className="text-muted-foreground">Confidence:</span>
            <div className="flex">
              {Array.from({ length: 5 }, (_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < confidence ? 'text-yellow-500 fill-current' : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
          </div>
          
          <div className="flex items-center gap-1 text-muted-foreground">
            <Clock className="w-4 h-4" />
            <span>{formatThinkingTime(thinkingTime)}</span>
          </div>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={onGoodChoice}
            className="btn-gaming-primary flex-1 py-2 px-3 text-sm"
          >
            <ThumbsUp className="w-4 h-4 inline mr-1" />
            Good choice!
          </button>
          <button
            onClick={onTryAnother}
            className="btn-gaming-secondary flex-1 py-2 px-3 text-sm"
          >
            <RotateCcw className="w-4 h-4 inline mr-1" />
            Try another?
          </button>
        </div>
      </div>

      {/* Desktop Layout */}
      <div className="hidden sm:block p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Brain className="w-6 h-6 text-primary" />
            <h4 className="text-lg font-semibold text-foreground">Computer Analysis</h4>
          </div>
          
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>Thinking time: {formatThinkingTime(thinkingTime)}</span>
            </div>
            
            <div className="flex items-center gap-1">
              <span>Confidence:</span>
              <div className="flex">
                {Array.from({ length: 5 }, (_, i) => (
                  <Star
                    key={i}
                    className={`w-4 h-4 ${
                      i < confidence ? 'text-yellow-500 fill-current' : 'text-gray-300'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
        
        {move && (
          <div className="mb-4 p-4 bg-primary/10 border border-primary/20 rounded-lg">
            <p className="text-foreground text-lg">
              <strong>Recommended move:</strong>{' '}
              <span className="font-mono bg-background px-3 py-1 rounded text-primary font-bold">
                {move}
              </span>
            </p>
          </div>
        )}
        
        <div className="mb-6">
          <p className="text-foreground text-lg leading-relaxed whitespace-pre-wrap">
            {displayAnalysis}
            {isTyping && <span className="animate-pulse">|</span>}
          </p>
        </div>
        
        <div className="flex items-center justify-center gap-4">
          <button
            onClick={onGoodChoice}
            className="btn-gaming-primary px-6 py-3"
          >
            <ThumbsUp className="w-5 h-5 inline mr-2" />
            That makes sense!
          </button>
          <button
            onClick={onTryAnother}
            className="btn-gaming-secondary px-6 py-3"
          >
            <RotateCcw className="w-5 h-5 inline mr-2" />
            Try another position
          </button>
        </div>
      </div>
    </div>
  )
}
```

### Move Explanation Utility
```typescript
// src/utils/move-explainer.ts
export interface MoveExplanation {
  move: string
  explanation: string
  strategicReason: string[]
  confidence: number
}

export class MoveExplainer {
  static explainMove(move: string, position: string, context: 'opening' | 'middlegame' | 'endgame'): MoveExplanation {
    // This would contain sophisticated move explanation logic
    // For now, providing example patterns

    const explanations = this.getExplanationPatterns(move, context)
    
    return {
      move,
      explanation: this.generateExplanation(move, context),
      strategicReason: explanations.reasons,
      confidence: explanations.confidence
    }
  }

  private static getExplanationPatterns(move: string, context: string) {
    // Opening patterns
    if (context === 'opening') {
      if (move === 'e4') {
        return {
          reasons: ['Controls the center', 'Opens lines for pieces', 'Classic opening principle'],
          confidence: 5
        }
      }
      if (move === 'd4') {
        return {
          reasons: ['Controls central squares', 'Supports piece development', 'Solid opening choice'],
          confidence: 5
        }
      }
      if (move.includes('Nf3') || move.includes('Nc3')) {
        return {
          reasons: ['Develops a piece toward center', 'Knights before bishops', 'Controls important squares'],
          confidence: 4
        }
      }
    }

    // Tactical patterns
    if (move.includes('x')) {
      return {
        reasons: ['Captures enemy piece', 'Gains material advantage', 'Removes defender'],
        confidence: 4
      }
    }

    if (move.includes('+')) {
      return {
        reasons: ['Gives check to enemy king', 'Forces opponent to respond', 'Maintains initiative'],
        confidence: 4
      }
    }

    if (move.includes('#')) {
      return {
        reasons: ['Delivers checkmate!', 'Game winning move', 'Perfect tactical execution'],
        confidence: 5
      }
    }

    // Default explanation
    return {
      reasons: ['Solid positional move', 'Improves piece coordination', 'Maintains balance'],
      confidence: 3
    }
  }

  private static generateExplanation(move: string, context: string): string {
    const patterns = this.getExplanationPatterns(move, context)
    
    let explanation = `I suggest ${move}!\n\n`
    explanation += `This is a ${context === 'opening' ? 'strong opening' : context === 'endgame' ? 'precise endgame' : 'good positional'} move because:\n\n`
    
    patterns.reasons.forEach((reason, index) => {
      explanation += `• ${reason}\n`
    })

    // Add contextual advice
    if (context === 'opening') {
      explanation += `\nRemember: In the opening, develop your pieces quickly and control the center!`
    } else if (context === 'endgame') {
      explanation += `\nIn the endgame, every move counts. Activate your king and push your pawns!`
    } else {
      explanation += `\nLook for tactics and maintain good piece coordination in the middlegame.`
    }

    return explanation
  }
}
```

---

## Phase 5: Progress Tracking Components

### Progress Dashboard
```typescript
// src/components/chess/ProgressDashboard.tsx
import { Trophy, Target, Clock, TrendingUp } from 'lucide-react'
import { useChessChallenges } from '../../hooks/useChessChallenges'

interface ProgressDashboardProps {
  className?: string
}

export function ProgressDashboard({ className = '' }: ProgressDashboardProps) {
  const { userProgress, getProgressStats } = useChessChallenges()
  const stats = getProgressStats()

  const getSkillBadge = (skill: string) => {
    const skillConfig = {
      'opening-basics': { emoji: '🏁', name: 'Opening Master' },
      'tactical-vision': { emoji: '🎯', name: 'Tactical Eye' },
      'endgame-technique': { emoji: '👑', name: 'Endgame Expert' },
      'positional-play': { emoji: '🧠', name: 'Strategic Mind' }
    }
    
    return skillConfig[skill as keyof typeof skillConfig] || { emoji: '⭐', name: skill }
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Mobile Layout */}
      <div className="space-y-4 lg:hidden">
        <div className="card-gaming p-4">
          <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
            <Trophy className="w-5 h-5" />
            Your Progress
          </h3>
          
          <div className="space-y-4">
            {/* Challenges Completed */}
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-foreground">Challenges completed:</span>
                <span className="text-muted-foreground">{stats.totalCompleted}/20</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(stats.totalCompleted / 20) * 100}%` }}
                />
              </div>
            </div>

            {/* Skills Unlocked */}
            <div>
              <h4 className="text-sm font-medium text-foreground mb-2">Skills learned:</h4>
              <div className="space-y-2">
                {userProgress.skillsUnlocked.map(skill => {
                  const badge = getSkillBadge(skill)
                  return (
                    <div key={skill} className="flex items-center gap-2">
                      <span className="text-lg">{badge.emoji}</span>
                      <span className="text-sm text-foreground">{badge.name}</span>
                    </div>
                  )
                })}
                
                {userProgress.skillsUnlocked.length < 4 && (
                  <div className="flex items-center gap-2 opacity-50">
                    <span className="text-lg">🔒</span>
                    <span className="text-sm text-muted-foreground">More skills to unlock!</span>
                  </div>
                )}
              </div>
            </div>

            {/* Current Streak */}
            {userProgress.currentStreak > 0 && (
              <div className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <span className="text-lg">🔥</span>
                  <span className="text-sm font-medium text-foreground">
                    {userProgress.currentStreak} challenge streak!
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Desktop Layout */}
      <div className="hidden lg:block">
        <div className="card-gaming p-6">
          <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-3">
            <Trophy className="w-6 h-6" />
            Your Chess Progress
          </h3>
          
          <div className="grid grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
            {/* Challenges Stat */}
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <Target className="w-8 h-8 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">{stats.totalCompleted}</div>
              <div className="text-sm text-muted-foreground">Challenges Completed</div>
            </div>

            {/* Streak Stat */}
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <span className="text-2xl">🔥</span>
              </div>
              <div className="text-2xl font-bold text-foreground">{userProgress.currentStreak}</div>
              <div className="text-sm text-muted-foreground">Current Streak</div>
            </div>

            {/* Average Time */}
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <Clock className="w-8 h-8 text-green-500" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {stats.averageTime > 0 ? `${(stats.averageTime / 1000).toFixed(1)}s` : '-'}
              </div>
              <div className="text-sm text-muted-foreground">Average Time</div>
            </div>

            {/* Skills Unlocked */}
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <TrendingUp className="w-8 h-8 text-purple-500" />
              </div>
              <div className="text-2xl font-bold text-foreground">{stats.skillsUnlocked}</div>
              <div className="text-sm text-muted-foreground">Skills Mastered</div>
            </div>
          </div>

          {/* Progress Bars */}
          <div className="space-y-4 mb-6">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-foreground font-medium">Story Mode Progress</span>
                <span className="text-muted-foreground">{Math.min(stats.totalCompleted, 6)}/6</span>
              </div>
              <div className="w-full bg-muted rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${(Math.min(stats.totalCompleted, 6) / 6) * 100}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-foreground font-medium">Overall Progress</span>
                <span className="text-muted-foreground">{stats.totalCompleted}/20</span>
              </div>
              <div className="w-full bg-muted rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${(stats.totalCompleted / 20) * 100}%` }}
                />
              </div>
            </div>
          </div>

          {/* Skills Grid */}
          <div>
            <h4 className="text-lg font-semibold text-foreground mb-4">Chess Skills</h4>
            <div className="grid grid-cols-2 gap-4">
              {['opening-basics', 'tactical-vision', 'endgame-technique', 'positional-play'].map(skill => {
                const badge = getSkillBadge(skill)
                const isUnlocked = userProgress.skillsUnlocked.includes(skill)
                
                return (
                  <div
                    key={skill}
                    className={`
                      p-4 rounded-lg border transition-all
                      ${isUnlocked 
                        ? 'bg-primary/10 border-primary/30 text-foreground' 
                        : 'bg-muted/30 border-border text-muted-foreground'
                      }
                    `}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{isUnlocked ? badge.emoji : '🔒'}</span>
                      <div>
                        <div className="font-medium">{badge.name}</div>
                        <div className="text-sm opacity-70">
                          {isUnlocked ? 'Mastered!' : 'Keep practicing'}
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

---

## Phase 6: Main WorkerTestPage Implementation

### Complete Transformed Page
```typescript
// src/pages/WorkerTestPage.tsx
import React, { useState, useCallback } from 'react'
import { Crown, Settings } from 'lucide-react'
import { useStockfish } from '../hooks/useStockfish'
import { useChessChallenges } from '../hooks/useChessChallenges'
import { CollapsibleSection } from '../components/chess/CollapsibleSection'
import { EngineStatusBar } from '../components/chess/EngineStatusBar'
import { ChallengeGrid } from '../components/chess/ChallengeGrid'
import { ChallengeDisplay } from '../components/chess/ChallengeDisplay'
import { ComputerAnalysis } from '../components/chess/ComputerAnalysis'
import { ProgressDashboard } from '../components/chess/ProgressDashboard'
import { MoveExplainer } from '../utils/move-explainer'

export const WorkerTestPage: React.FC = () => {
  const { 
    isReady, 
    isThinking, 
    skillLevel, 
    setSkillLevel, 
    requestMove, 
    evaluatePosition,
    error 
  } = useStockfish()
  
  const {
    currentChallenge,
    availableModes,
    selectChallenge,
    completeChallenge,
    getNextChallenge
  } = useChessChallenges()

  const [computerMove, setComputerMove] = useState<string | null>(null)
  const [computerAnalysis, setComputerAnalysis] = useState('')
  const [analysisConfidence, setAnalysisConfidence] = useState(0)
  const [responseTime, setResponseTime] = useState(0)
  const [showAnalysis, setShowAnalysis] = useState(false)

  const handleSelectChallenge = useCallback((challengeId: string) => {
    selectChallenge(challengeId)
    setShowAnalysis(false)
    setComputerMove(null)
    setComputerAnalysis('')
  }, [selectChallenge])

  const handleAskComputer = useCallback(async () => {
    if (!currentChallenge || !isReady) return

    setShowAnalysis(false)
    const startTime = Date.now()

    try {
      // Request move from Stockfish
      const move = await requestMove(currentChallenge.position, 2000)
      const endTime = Date.now()
      
      if (move) {
        setComputerMove(move)
        setResponseTime(endTime - startTime)
        
        // Generate user-friendly explanation
        const explanation = MoveExplainer.explainMove(
          move, 
          currentChallenge.position,
          currentChallenge.category === 'opening' ? 'opening' : 'middlegame'
        )
        
        setComputerAnalysis(explanation.explanation)
        setAnalysisConfidence(explanation.confidence)
        setShowAnalysis(true)
      }
    } catch (err) {
      console.error('Failed to get computer analysis:', err)
      setComputerAnalysis('Sorry, I had trouble analyzing this position. Please try again!')
      setAnalysisConfidence(1)
      setShowAnalysis(true)
    }
  }, [currentChallenge, isReady, requestMove])

  const handleShowAnswer = useCallback(() => {
    if (!currentChallenge) return

    const expectedMove = currentChallenge.expectedMoves[0]
    setComputerMove(expectedMove)
    
    // Create explanation for the expected answer
    const explanation = MoveExplainer.explainMove(
      expectedMove,
      currentChallenge.position,
      currentChallenge.category === 'opening' ? 'opening' : 'middlegame'
    )
    
    setComputerAnalysis(`The best answer is ${expectedMove}!\n\n${explanation.explanation}`)
    setAnalysisConfidence(5)
    setShowAnalysis(true)
  }, [currentChallenge])

  const handleCompleteChallenge = useCallback((success: boolean) => {
    if (!currentChallenge) return

    completeChallenge(currentChallenge.id, responseTime, 0)
    
    // Auto-select next challenge
    setTimeout(() => {
      const next = getNextChallenge()
      if (next) {
        selectChallenge(next.id)
      }
    }, 1500)
  }, [currentChallenge, responseTime, completeChallenge, getNextChallenge, selectChallenge])

  const handleSkillLevelChange = useCallback((level: number) => {
    setSkillLevel(level)
  }, [setSkillLevel])

  return (
    <div className="space-y-4">
      {/* Header with chess theme */}
      <div className="text-center py-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-foreground flex items-center justify-center gap-3">
          <Crown className="w-8 h-8 text-primary" />
          Chess Computer Challenges
        </h1>
        <p className="text-muted-foreground mt-2">
          Learn chess through interactive challenges and computer analysis
        </p>
      </div>

      {/* Engine Status */}
      <EngineStatusBar />

      {/* Skill Level Control */}
      <CollapsibleSection 
        title="Difficulty Level" 
        icon="🎚️"
        defaultExpanded={false}
        className="lg:hidden"
      >
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm text-muted-foreground mb-2">
              <span>Beginner</span>
              <span>Expert</span>
            </div>
            <input
              type="range"
              min="1"
              max="20"
              value={skillLevel}
              onChange={(e) => handleSkillLevelChange(parseInt(e.target.value))}
              className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer"
              disabled={!isReady}
            />
            <div className="mt-2 text-center">
              <span className="text-foreground font-medium">Level {skillLevel}/20</span>
            </div>
          </div>
        </div>
      </CollapsibleSection>

      {/* Desktop skill level - always visible */}
      <div className="hidden lg:block card-gaming p-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Settings className="w-5 h-5" />
            Computer Skill Level
          </h3>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">Beginner</span>
            <input
              type="range"
              min="1"
              max="20"
              value={skillLevel}
              onChange={(e) => handleSkillLevelChange(parseInt(e.target.value))}
              className="w-48 h-2 bg-muted rounded-lg appearance-none cursor-pointer"
              disabled={!isReady}
            />
            <span className="text-sm text-muted-foreground">Expert</span>
            <span className="text-foreground font-medium min-w-[80px]">
              Level {skillLevel}/20
            </span>
          </div>
        </div>
      </div>

      {/* Challenge Selection */}
      {!currentChallenge && (
        <CollapsibleSection 
          title="Chess Challenges" 
          icon="🏆"
          defaultExpanded={true}
        >
          <ChallengeGrid 
            modes={availableModes}
            onSelectChallenge={handleSelectChallenge}
          />
        </CollapsibleSection>
      )}

      {/* Current Challenge */}
      {currentChallenge && (
        <ChallengeDisplay
          challenge={currentChallenge}
          onAskComputer={handleAskComputer}
          onShowAnswer={handleShowAnswer}
          onSkipChallenge={() => handleSelectChallenge('')}
          onCompleteChallenge={handleCompleteChallenge}
          isComputerThinking={isThinking}
        />
      )}

      {/* Computer Analysis */}
      {showAnalysis && (
        <ComputerAnalysis
          move={computerMove}
          analysis={computerAnalysis}
          confidence={analysisConfidence}
          thinkingTime={responseTime}
          onGoodChoice={() => handleCompleteChallenge(true)}
          onTryAnother={() => {
            const next = getNextChallenge()
            if (next) handleSelectChallenge(next.id)
          }}
          isVisible={showAnalysis}
        />
      )}

      {/* Progress Dashboard */}
      <CollapsibleSection 
        title="Your Progress" 
        icon="📊"
        defaultExpanded={false}
      >
        <ProgressDashboard />
      </CollapsibleSection>

      {/* Error Display */}
      {error && (
        <div className="card-gaming p-4 border-red-500/50 bg-red-500/5">
          <div className="flex items-center gap-2">
            <span className="text-red-500 text-lg">⚠️</span>
            <div>
              <h4 className="font-medium text-red-500">Computer Error</h4>
              <p className="text-sm text-red-400">{error}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
```

---

## Conclusion

This comprehensive code implementation transforms the technical WorkerTestPage into an engaging, educational chess challenge interface. The code examples demonstrate:

1. **Mobile-First Design**: All components are responsive and touch-optimized
2. **Game-Like Interface**: Interactive challenges with visual chess boards
3. **Educational Focus**: User-friendly explanations and progressive learning
4. **Complete Stockfish Integration**: Natural testing through gameplay
5. **Modern React Patterns**: Hooks, TypeScript, and performance optimization

The implementation maintains the established gaming UI aesthetic while providing genuine educational value and comprehensive engine testing through natural user interactions.

All components follow the architectural patterns established in the broader application, ensuring consistency and maintainability while delivering an engaging chess learning experience.