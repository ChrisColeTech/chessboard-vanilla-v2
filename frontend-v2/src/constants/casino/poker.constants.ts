<<<<<<< Updated upstream
import type { Card } from '../../stores/appStore'

// Poker hand rankings from highest to lowest
export const HAND_RANKINGS = {
  ROYAL_FLUSH: 10,
  STRAIGHT_FLUSH: 9,
  FOUR_OF_A_KIND: 8,
  FULL_HOUSE: 7,
  FLUSH: 6,
  STRAIGHT: 5,
  THREE_OF_A_KIND: 4,
  TWO_PAIR: 3,
  ONE_PAIR: 2,
  HIGH_CARD: 1,
} as const

// Card rank values for comparison (Ace can be 1 or 14)
export const RANK_VALUES = {
  '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
  'J': 11, 'Q': 12, 'K': 13, 'A': 14
} as const

// Standard deck of cards
export const STANDARD_DECK: Card[] = [
  // Hearts
  { suit: 'hearts', rank: 'A' }, { suit: 'hearts', rank: '2' }, { suit: 'hearts', rank: '3' },
  { suit: 'hearts', rank: '4' }, { suit: 'hearts', rank: '5' }, { suit: 'hearts', rank: '6' },
  { suit: 'hearts', rank: '7' }, { suit: 'hearts', rank: '8' }, { suit: 'hearts', rank: '9' },
  { suit: 'hearts', rank: '10' }, { suit: 'hearts', rank: 'J' }, { suit: 'hearts', rank: 'Q' },
  { suit: 'hearts', rank: 'K' },
  
  // Diamonds
  { suit: 'diamonds', rank: 'A' }, { suit: 'diamonds', rank: '2' }, { suit: 'diamonds', rank: '3' },
  { suit: 'diamonds', rank: '4' }, { suit: 'diamonds', rank: '5' }, { suit: 'diamonds', rank: '6' },
  { suit: 'diamonds', rank: '7' }, { suit: 'diamonds', rank: '8' }, { suit: 'diamonds', rank: '9' },
  { suit: 'diamonds', rank: '10' }, { suit: 'diamonds', rank: 'J' }, { suit: 'diamonds', rank: 'Q' },
  { suit: 'diamonds', rank: 'K' },
  
  // Clubs
  { suit: 'clubs', rank: 'A' }, { suit: 'clubs', rank: '2' }, { suit: 'clubs', rank: '3' },
  { suit: 'clubs', rank: '4' }, { suit: 'clubs', rank: '5' }, { suit: 'clubs', rank: '6' },
  { suit: 'clubs', rank: '7' }, { suit: 'clubs', rank: '8' }, { suit: 'clubs', rank: '9' },
  { suit: 'clubs', rank: '10' }, { suit: 'clubs', rank: 'J' }, { suit: 'clubs', rank: 'Q' },
  { suit: 'clubs', rank: 'K' },
  
  // Spades
  { suit: 'spades', rank: 'A' }, { suit: 'spades', rank: '2' }, { suit: 'spades', rank: '3' },
  { suit: 'spades', rank: '4' }, { suit: 'spades', rank: '5' }, { suit: 'spades', rank: '6' },
  { suit: 'spades', rank: '7' }, { suit: 'spades', rank: '8' }, { suit: 'spades', rank: '9' },
  { suit: 'spades', rank: '10' }, { suit: 'spades', rank: 'J' }, { suit: 'spades', rank: 'Q' },
  { suit: 'spades', rank: 'K' },
]

// Card image file mapping
export const getCardImagePath = (card: Card): string => {
  const suitMap = {
    hearts: 'heart',
    diamonds: 'diamond', 
    clubs: 'club',
    spades: 'spade'
  }
  
  const rankMap = {
    'A': '1',
    'J': 'jack',
    'Q': 'queen', 
    'K': 'king'
  }
  
  const suit = suitMap[card.suit]
  const rank = rankMap[card.rank as keyof typeof rankMap] || card.rank
  
  return `/assets/casino/cards/${suit}_${rank}.png`
}

// AI opponent personalities
export const AI_PERSONALITIES = {
  TIGHT_AGGRESSIVE: {
    name: 'Sarah',
    handSelectionRate: 0.15, // Plays top 15% of hands
    aggressionFactor: 3.5,   // High aggression when playing
    bluffFrequency: 0.05,    // Low bluff rate
  },
  LOOSE_AGGRESSIVE: {
    name: 'Mike',
    handSelectionRate: 0.35, // Plays top 35% of hands
    aggressionFactor: 2.8,   // Moderate-high aggression
    bluffFrequency: 0.15,    // Moderate bluff rate
  },
  CONSERVATIVE: {
    name: 'Bob',
    handSelectionRate: 0.25, // Plays top 25% of hands
    aggressionFactor: 1.2,   // Low aggression (calling station)
    bluffFrequency: 0.02,    // Very low bluff rate
  },
} as const

// Betting round configurations
export const BETTING_ROUNDS = {
  PREFLOP: { name: 'Pre-flop', communityCards: 0 },
  FLOP: { name: 'Flop', communityCards: 3 },
  TURN: { name: 'Turn', communityCards: 4 },
  RIVER: { name: 'River', communityCards: 5 },
} as const

// Default blind structure
export const DEFAULT_BLINDS = {
  small: 5,
  big: 10,
} as const

// Hand strength ratings (for AI decision making)
export const HAND_STRENGTH_PREFLOP = {
  // Premium hands
  'AA': 0.95, 'KK': 0.92, 'QQ': 0.88, 'AK': 0.85, 'AQ': 0.80,
  'JJ': 0.78, 'AJ': 0.75, 'KQ': 0.72, 'TT': 0.70, 'AT': 0.68,
  
  // Good hands  
  '99': 0.65, 'KJ': 0.62, 'QJ': 0.60, '88': 0.58, 'A9': 0.55,
  'KT': 0.52, 'QT': 0.50, '77': 0.48, 'JT': 0.45, 'A8': 0.42,
  
  // Marginal hands
  '66': 0.40, 'K9': 0.38, 'Q9': 0.35, 'J9': 0.32, '55': 0.30,
  'T9': 0.28, 'A7': 0.25, 'K8': 0.22, '44': 0.20, 'Q8': 0.18,
  
  // Weak hands (most other combinations fall here)
} as const

=======
import type { Card } from '../../stores/appStore'

// Poker hand rankings from highest to lowest
export const HAND_RANKINGS = {
  ROYAL_FLUSH: 10,
  STRAIGHT_FLUSH: 9,
  FOUR_OF_A_KIND: 8,
  FULL_HOUSE: 7,
  FLUSH: 6,
  STRAIGHT: 5,
  THREE_OF_A_KIND: 4,
  TWO_PAIR: 3,
  ONE_PAIR: 2,
  HIGH_CARD: 1,
} as const

// Card rank values for comparison (Ace can be 1 or 14)
export const RANK_VALUES = {
  '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
  'J': 11, 'Q': 12, 'K': 13, 'A': 14
} as const

// Standard deck of cards
export const STANDARD_DECK: Card[] = [
  // Hearts
  { suit: 'hearts', rank: 'A' }, { suit: 'hearts', rank: '2' }, { suit: 'hearts', rank: '3' },
  { suit: 'hearts', rank: '4' }, { suit: 'hearts', rank: '5' }, { suit: 'hearts', rank: '6' },
  { suit: 'hearts', rank: '7' }, { suit: 'hearts', rank: '8' }, { suit: 'hearts', rank: '9' },
  { suit: 'hearts', rank: '10' }, { suit: 'hearts', rank: 'J' }, { suit: 'hearts', rank: 'Q' },
  { suit: 'hearts', rank: 'K' },
  
  // Diamonds
  { suit: 'diamonds', rank: 'A' }, { suit: 'diamonds', rank: '2' }, { suit: 'diamonds', rank: '3' },
  { suit: 'diamonds', rank: '4' }, { suit: 'diamonds', rank: '5' }, { suit: 'diamonds', rank: '6' },
  { suit: 'diamonds', rank: '7' }, { suit: 'diamonds', rank: '8' }, { suit: 'diamonds', rank: '9' },
  { suit: 'diamonds', rank: '10' }, { suit: 'diamonds', rank: 'J' }, { suit: 'diamonds', rank: 'Q' },
  { suit: 'diamonds', rank: 'K' },
  
  // Clubs
  { suit: 'clubs', rank: 'A' }, { suit: 'clubs', rank: '2' }, { suit: 'clubs', rank: '3' },
  { suit: 'clubs', rank: '4' }, { suit: 'clubs', rank: '5' }, { suit: 'clubs', rank: '6' },
  { suit: 'clubs', rank: '7' }, { suit: 'clubs', rank: '8' }, { suit: 'clubs', rank: '9' },
  { suit: 'clubs', rank: '10' }, { suit: 'clubs', rank: 'J' }, { suit: 'clubs', rank: 'Q' },
  { suit: 'clubs', rank: 'K' },
  
  // Spades
  { suit: 'spades', rank: 'A' }, { suit: 'spades', rank: '2' }, { suit: 'spades', rank: '3' },
  { suit: 'spades', rank: '4' }, { suit: 'spades', rank: '5' }, { suit: 'spades', rank: '6' },
  { suit: 'spades', rank: '7' }, { suit: 'spades', rank: '8' }, { suit: 'spades', rank: '9' },
  { suit: 'spades', rank: '10' }, { suit: 'spades', rank: 'J' }, { suit: 'spades', rank: 'Q' },
  { suit: 'spades', rank: 'K' },
]

// Card image file mapping
export const getCardImagePath = (card: Card): string => {
  const suitMap = {
    hearts: 'heart',
    diamonds: 'diamond', 
    clubs: 'club',
    spades: 'spade'
  }
  
  const rankMap = {
    'A': '1',
    'J': 'jack',
    'Q': 'queen', 
    'K': 'king'
  }
  
  const suit = suitMap[card.suit]
  const rank = rankMap[card.rank as keyof typeof rankMap] || card.rank
  
  return `/assets/casino/cards/${suit}_${rank}.png`
}

// AI opponent personalities
export const AI_PERSONALITIES = {
  TIGHT_AGGRESSIVE: {
    name: 'Sarah',
    handSelectionRate: 0.15, // Plays top 15% of hands
    aggressionFactor: 3.5,   // High aggression when playing
    bluffFrequency: 0.05,    // Low bluff rate
  },
  LOOSE_AGGRESSIVE: {
    name: 'Mike',
    handSelectionRate: 0.35, // Plays top 35% of hands
    aggressionFactor: 2.8,   // Moderate-high aggression
    bluffFrequency: 0.15,    // Moderate bluff rate
  },
  CONSERVATIVE: {
    name: 'Bob',
    handSelectionRate: 0.25, // Plays top 25% of hands
    aggressionFactor: 1.2,   // Low aggression (calling station)
    bluffFrequency: 0.02,    // Very low bluff rate
  },
} as const

// Betting round configurations
export const BETTING_ROUNDS = {
  PREFLOP: { name: 'Pre-flop', communityCards: 0 },
  FLOP: { name: 'Flop', communityCards: 3 },
  TURN: { name: 'Turn', communityCards: 4 },
  RIVER: { name: 'River', communityCards: 5 },
} as const

// Default blind structure
export const DEFAULT_BLINDS = {
  small: 5,
  big: 10,
} as const

// Hand strength ratings (for AI decision making)
export const HAND_STRENGTH_PREFLOP = {
  // Premium hands
  'AA': 0.95, 'KK': 0.92, 'QQ': 0.88, 'AK': 0.85, 'AQ': 0.80,
  'JJ': 0.78, 'AJ': 0.75, 'KQ': 0.72, 'TT': 0.70, 'AT': 0.68,
  
  // Good hands  
  '99': 0.65, 'KJ': 0.62, 'QJ': 0.60, '88': 0.58, 'A9': 0.55,
  'KT': 0.52, 'QT': 0.50, '77': 0.48, 'JT': 0.45, 'A8': 0.42,
  
  // Marginal hands
  '66': 0.40, 'K9': 0.38, 'Q9': 0.35, 'J9': 0.32, '55': 0.30,
  'T9': 0.28, 'A7': 0.25, 'K8': 0.22, '44': 0.20, 'Q8': 0.18,
  
  // Weak hands (most other combinations fall here)
} as const

>>>>>>> Stashed changes
export type HandStrengthKey = keyof typeof HAND_STRENGTH_PREFLOP