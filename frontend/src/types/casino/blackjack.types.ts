export interface BlackjackCard {
  suit: 'hearts' | 'diamonds' | 'clubs' | 'spades'
  rank: 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K'
  value: number
  isVisible: boolean
  id: string // Unique identifier for animations
}

export interface BlackjackHand {
  cards: BlackjackCard[]
  value: number
  isSoft: boolean // Contains ace counted as 11
  isBusted: boolean
  isBlackjack: boolean
}

export type GamePhase = 'betting' | 'dealing' | 'player-turn' | 'dealer-turn' | 'game-over'

export type GameResult = 'player-wins' | 'dealer-wins' | 'push' | 'blackjack' | null

export interface BlackjackGameState {
  playerHand: BlackjackHand
  dealerHand: BlackjackHand
  deck: BlackjackCard[]
  currentBet: number
  gamePhase: GamePhase
  canHit: boolean
  canStand: boolean
  canDouble: boolean
  gameResult: GameResult
  isThinking: boolean // For dealer AI
}

export interface CardProps {
  card: BlackjackCard
  isAnimating?: boolean
  animationDelay?: number
  onClick?: () => void
  className?: string
}

export interface HandProps {
  hand: BlackjackHand
  isDealer?: boolean
  showValue?: boolean
  isThinking?: boolean
  className?: string
}

export interface ActionButtonsProps {
  canHit: boolean
  canStand: boolean
  canDouble: boolean
  onHit: () => void
  onStand: () => void
  onDouble: () => void
  currentBet: number
  balance: number
  disabled?: boolean
}

export interface BetControlsProps {
  currentBet: number
  balance: number
  minBet: number
  maxBet: number
  onBetChange: (amount: number) => void
  disabled?: boolean
}