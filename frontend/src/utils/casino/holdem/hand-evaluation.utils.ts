import type { Card } from '../../../stores/appStore'
import { HAND_RANKINGS, RANK_VALUES } from '../../../constants/casino/poker.constants'

export interface HandEvaluation {
  ranking: number
  description: string
  cards: Card[]
  kickers: Card[]
  strength: number // 0-1 relative strength
}

// Evaluate the best 5-card hand from up to 7 cards (2 hole + 5 community)
export function evaluateHand(cards: Card[]): HandEvaluation {
  if (cards.length < 5) {
    return {
      ranking: HAND_RANKINGS.HIGH_CARD,
      description: 'High Card',
      cards: cards.slice(0, 5),
      kickers: [],
      strength: 0
    }
  }

  // Sort cards by rank value (descending)
  const sortedCards = [...cards].sort((a, b) => RANK_VALUES[b.rank] - RANK_VALUES[a.rank])
  
  // Check for each hand type from highest to lowest
  const royalFlush = checkRoyalFlush(sortedCards)
  if (royalFlush) return royalFlush
  
  const straightFlush = checkStraightFlush(sortedCards)
  if (straightFlush) return straightFlush
  
  const fourOfAKind = checkFourOfAKind(sortedCards)
  if (fourOfAKind) return fourOfAKind
  
  const fullHouse = checkFullHouse(sortedCards)
  if (fullHouse) return fullHouse
  
  const flush = checkFlush(sortedCards)
  if (flush) return flush
  
  const straight = checkStraight(sortedCards)
  if (straight) return straight
  
  const threeOfAKind = checkThreeOfAKind(sortedCards)
  if (threeOfAKind) return threeOfAKind
  
  const twoPair = checkTwoPair(sortedCards)
  if (twoPair) return twoPair
  
  const onePair = checkOnePair(sortedCards)
  if (onePair) return onePair
  
  return checkHighCard(sortedCards)
}

function checkRoyalFlush(cards: Card[]): HandEvaluation | null {
  const suits = ['hearts', 'diamonds', 'clubs', 'spades'] as const
  
  for (const suit of suits) {
    const suitCards = cards.filter(card => card.suit === suit)
    if (suitCards.length >= 5) {
      const royalRanks = ['A', 'K', 'Q', 'J', '10']
      const hasRoyal = royalRanks.every(rank => 
        suitCards.some(card => card.rank === rank)
      )
      
      if (hasRoyal) {
        return {
          ranking: HAND_RANKINGS.ROYAL_FLUSH,
          description: 'Royal Flush',
          cards: suitCards.filter(card => royalRanks.includes(card.rank)),
          kickers: [],
          strength: 1.0
        }
      }
    }
  }
  
  return null
}

function checkStraightFlush(cards: Card[]): HandEvaluation | null {
  const suits = ['hearts', 'diamonds', 'clubs', 'spades'] as const
  
  for (const suit of suits) {
    const suitCards = cards.filter(card => card.suit === suit)
    if (suitCards.length >= 5) {
      const straight = checkStraight(suitCards)
      if (straight) {
        return {
          ranking: HAND_RANKINGS.STRAIGHT_FLUSH,
          description: 'Straight Flush',
          cards: straight.cards,
          kickers: [],
          strength: 0.9 + (RANK_VALUES[straight.cards[0].rank as keyof typeof RANK_VALUES] / 1000)
        }
      }
    }
  }
  
  return null
}

function checkFourOfAKind(cards: Card[]): HandEvaluation | null {
  const rankCounts = getRankCounts(cards)
  
  for (const [rank, count] of rankCounts.entries()) {
    if (count >= 4) {
      const quadCards = cards.filter(card => card.rank === rank).slice(0, 4)
      const kicker = cards.find(card => card.rank !== rank)
      
      return {
        ranking: HAND_RANKINGS.FOUR_OF_A_KIND,
        description: `Four ${rank}s`,
        cards: kicker ? [...quadCards, kicker] : quadCards,
        kickers: kicker ? [kicker] : [],
        strength: 0.8 + (RANK_VALUES[rank as keyof typeof RANK_VALUES] / 1000)
      }
    }
  }
  
  return null
}

function checkFullHouse(cards: Card[]): HandEvaluation | null {
  const rankCounts = getRankCounts(cards)
  let threeRank: string | null = null
  let pairRank: string | null = null
  
  // Find the highest three of a kind
  for (const [rank, count] of rankCounts.entries()) {
    if (count >= 3 && (!threeRank || RANK_VALUES[rank as keyof typeof RANK_VALUES] > RANK_VALUES[threeRank as keyof typeof RANK_VALUES])) {
      threeRank = rank
    }
  }
  
  // Find the highest pair (excluding the three of a kind)
  for (const [rank, count] of rankCounts.entries()) {
    if (count >= 2 && rank !== threeRank && (!pairRank || RANK_VALUES[rank as keyof typeof RANK_VALUES] > RANK_VALUES[pairRank as keyof typeof RANK_VALUES])) {
      pairRank = rank
    }
  }
  
  if (threeRank && pairRank) {
    const threeCards = cards.filter(card => card.rank === threeRank).slice(0, 3)
    const pairCards = cards.filter(card => card.rank === pairRank).slice(0, 2)
    
    return {
      ranking: HAND_RANKINGS.FULL_HOUSE,
      description: `${threeRank}s full of ${pairRank}s`,
      cards: [...threeCards, ...pairCards],
      kickers: [],
      strength: 0.7 + (RANK_VALUES[threeRank as keyof typeof RANK_VALUES] / 1000) + (RANK_VALUES[pairRank as keyof typeof RANK_VALUES] / 100000)
    }
  }
  
  return null
}

function checkFlush(cards: Card[]): HandEvaluation | null {
  const suits = ['hearts', 'diamonds', 'clubs', 'spades'] as const
  
  for (const suit of suits) {
    const suitCards = cards.filter(card => card.suit === suit)
    if (suitCards.length >= 5) {
      const flushCards = suitCards.slice(0, 5)
      
      return {
        ranking: HAND_RANKINGS.FLUSH,
        description: `${suit.charAt(0).toUpperCase() + suit.slice(1)} Flush`,
        cards: flushCards,
        kickers: flushCards.slice(1),
        strength: 0.6 + (RANK_VALUES[flushCards[0].rank as keyof typeof RANK_VALUES] / 1000)
      }
    }
  }
  
  return null
}

function checkStraight(cards: Card[]): HandEvaluation | null {
  const uniqueRanks = Array.from(new Set(cards.map(card => card.rank)))
  const sortedRanks = uniqueRanks.sort((a, b) => RANK_VALUES[b as keyof typeof RANK_VALUES] - RANK_VALUES[a as keyof typeof RANK_VALUES])
  
  // Check for ace-low straight (A-2-3-4-5)
  if (sortedRanks.includes('A') && sortedRanks.includes('2') && 
      sortedRanks.includes('3') && sortedRanks.includes('4') && 
      sortedRanks.includes('5')) {
    const straightCards = ['5', '4', '3', '2', 'A'].map(rank => 
      cards.find(card => card.rank === rank)!
    )
    
    return {
      ranking: HAND_RANKINGS.STRAIGHT,
      description: 'Straight (5 high)',
      cards: straightCards,
      kickers: [],
      strength: 0.5 + (5 / 1000) // 5-high straight
    }
  }
  
  // Check for regular straights
  for (let i = 0; i <= sortedRanks.length - 5; i++) {
    let isConsecutive = true
    for (let j = 0; j < 4; j++) {
      if (RANK_VALUES[sortedRanks[i + j] as keyof typeof RANK_VALUES] - RANK_VALUES[sortedRanks[i + j + 1] as keyof typeof RANK_VALUES] !== 1) {
        isConsecutive = false
        break
      }
    }
    
    if (isConsecutive) {
      const straightRanks = sortedRanks.slice(i, i + 5)
      const straightCards = straightRanks.map(rank => 
        cards.find(card => card.rank === rank)!
      )
      
      return {
        ranking: HAND_RANKINGS.STRAIGHT,
        description: `Straight (${straightRanks[0]} high)`,
        cards: straightCards,
        kickers: [],
        strength: 0.5 + (RANK_VALUES[straightRanks[0] as keyof typeof RANK_VALUES] / 1000)
      }
    }
  }
  
  return null
}

function checkThreeOfAKind(cards: Card[]): HandEvaluation | null {
  const rankCounts = getRankCounts(cards)
  
  for (const [rank, count] of rankCounts.entries()) {
    if (count >= 3) {
      const threeCards = cards.filter(card => card.rank === rank).slice(0, 3)
      const kickers = cards.filter(card => card.rank !== rank).slice(0, 2)
      
      return {
        ranking: HAND_RANKINGS.THREE_OF_A_KIND,
        description: `Three ${rank}s`,
        cards: [...threeCards, ...kickers],
        kickers,
        strength: 0.4 + (RANK_VALUES[rank as keyof typeof RANK_VALUES] / 1000)
      }
    }
  }
  
  return null
}

function checkTwoPair(cards: Card[]): HandEvaluation | null {
  const rankCounts = getRankCounts(cards)
  const pairs: string[] = []
  
  for (const [rank, count] of rankCounts.entries()) {
    if (count >= 2) {
      pairs.push(rank)
    }
  }
  
  if (pairs.length >= 2) {
    pairs.sort((a, b) => RANK_VALUES[b as keyof typeof RANK_VALUES] - RANK_VALUES[a as keyof typeof RANK_VALUES])
    const highPair = pairs[0]
    const lowPair = pairs[1]
    
    const highPairCards = cards.filter(card => card.rank === highPair).slice(0, 2)
    const lowPairCards = cards.filter(card => card.rank === lowPair).slice(0, 2)
    const kicker = cards.find(card => card.rank !== highPair && card.rank !== lowPair)
    
    return {
      ranking: HAND_RANKINGS.TWO_PAIR,
      description: `Two Pair (${highPair}s and ${lowPair}s)`,
      cards: kicker ? [...highPairCards, ...lowPairCards, kicker] : [...highPairCards, ...lowPairCards],
      kickers: kicker ? [kicker] : [],
      strength: 0.3 + (RANK_VALUES[highPair as keyof typeof RANK_VALUES] / 1000) + (RANK_VALUES[lowPair as keyof typeof RANK_VALUES] / 100000)
    }
  }
  
  return null
}

function checkOnePair(cards: Card[]): HandEvaluation | null {
  const rankCounts = getRankCounts(cards)
  
  for (const [rank, count] of rankCounts.entries()) {
    if (count >= 2) {
      const pairCards = cards.filter(card => card.rank === rank).slice(0, 2)
      const kickers = cards.filter(card => card.rank !== rank).slice(0, 3)
      
      return {
        ranking: HAND_RANKINGS.ONE_PAIR,
        description: `Pair of ${rank}s`,
        cards: [...pairCards, ...kickers],
        kickers,
        strength: 0.2 + (RANK_VALUES[rank as keyof typeof RANK_VALUES] / 1000)
      }
    }
  }
  
  return null
}

function checkHighCard(cards: Card[]): HandEvaluation {
  const highCards = cards.slice(0, 5)
  
  return {
    ranking: HAND_RANKINGS.HIGH_CARD,
    description: `${cards[0].rank} High`,
    cards: highCards,
    kickers: highCards.slice(1),
    strength: 0.1 + (RANK_VALUES[cards[0].rank as keyof typeof RANK_VALUES] / 1000)
  }
}

function getRankCounts(cards: Card[]): Map<string, number> {
  const counts = new Map<string, number>()
  
  for (const card of cards) {
    counts.set(card.rank, (counts.get(card.rank) || 0) + 1)
  }
  
  return counts
}

// Compare two hands - returns positive if hand1 wins, negative if hand2 wins, 0 for tie
export function compareHands(hand1: HandEvaluation, hand2: HandEvaluation): number {
  if (hand1.ranking !== hand2.ranking) {
    return hand1.ranking - hand2.ranking
  }
  
  // Same ranking, compare by strength
  return hand1.strength - hand2.strength
}