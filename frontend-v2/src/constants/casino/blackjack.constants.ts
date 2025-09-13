export const BLACKJACK_RULES = {
  BLACKJACK_VALUE: 21,
  DEALER_HITS_UNDER: 17,
  BLACKJACK_PAYOUT: 1.5, // 3:2 payout
  REGULAR_PAYOUT: 1.0,
  MIN_BET: 5,
  MAX_BET: 100,
  DECK_SHUFFLE_THRESHOLD: 0.75, // Shuffle at 75% deck penetration
  INITIAL_BALANCE: 350,
} as const

export const CARD_VALUES = {
  'A': 11, // Default ace value, adjusted in game logic
  '2': 2,
  '3': 3,
  '4': 4,
  '5': 5,
  '6': 6,
  '7': 7,
  '8': 8,
  '9': 9,
  '10': 10,
  'J': 10,
  'Q': 10,
  'K': 10,
} as const

export const CARD_SUITS = ['hearts', 'diamonds', 'clubs', 'spades'] as const
export const CARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] as const

export const ANIMATION_DURATIONS = {
  CARD_DEAL: 300,
  CARD_FLIP: 200,
  DEALER_THINKING: 1500,
  GAME_RESULT: 1000,
} as const

export const DEALER_NAMES = [
  'Dealer',
  'Chess Master Chen',
  'Lady Fortune',
  'The House',
] as const