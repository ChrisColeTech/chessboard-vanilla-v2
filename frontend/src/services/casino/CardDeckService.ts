import type { BlackjackCard } from '../../types/casino/blackjack.types'
import { CARD_SUITS, CARD_RANKS, CARD_VALUES } from '../../constants/casino/blackjack.constants'

export class CardDeckService {
  createNewDeck(): BlackjackCard[] {
    const deck: BlackjackCard[] = []
    
    CARD_SUITS.forEach(suit => {
      CARD_RANKS.forEach(rank => {
        deck.push({
          suit,
          rank,
          value: CARD_VALUES[rank],
          isVisible: false,
          id: `${suit}-${rank}-${Date.now()}-${Math.random()}`
        })
      })
    })
    
    return this.shuffleDeck(deck)
  }

  shuffleDeck(deck: BlackjackCard[]): BlackjackCard[] {
    // Fisher-Yates shuffle using crypto-secure RNG
    const shuffled = [...deck]
    const crypto = window.crypto || (window as any).msCrypto
    
    if (!crypto) {
      // Fallback to Math.random if crypto not available
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
      }
      return shuffled
    }
    
    for (let i = shuffled.length - 1; i > 0; i--) {
      const randomBytes = new Uint32Array(1)
      crypto.getRandomValues(randomBytes)
      const j = Math.floor((randomBytes[0] / 0x100000000) * (i + 1))
      ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    
    return shuffled
  }

  dealCard(deck: BlackjackCard[], visible: boolean = true): { card: BlackjackCard, remainingDeck: BlackjackCard[] } {
    if (deck.length === 0) {
      throw new Error('Cannot deal from empty deck')
    }
    
    const newDeck = [...deck]
    const card = newDeck.pop()!
    
    return {
      card: { ...card, isVisible: visible },
      remainingDeck: newDeck
    }
  }

  getCardImagePath(card: BlackjackCard): string {
    if (!card.isVisible) {
      return '/assets/casino/cards/back.png'
    }
    
    // Convert rank to match file naming convention
    let fileName: string
    if (card.rank === 'A') {
      fileName = `${card.suit}_1.png`
    } else if (['J', 'Q', 'K'].includes(card.rank)) {
      fileName = `${card.suit}_${card.rank.toLowerCase()}.png`
    } else {
      fileName = `${card.suit}_${card.rank}.png`
    }
    
    return `/assets/casino/cards/${fileName}`
  }

  getCardDisplayValue(card: BlackjackCard): string {
    return card.rank === 'A' ? 'A' : card.rank
  }

  getCardSuitSymbol(suit: BlackjackCard['suit']): string {
    const symbols = {
      hearts: '♥',
      diamonds: '♦',
      clubs: '♣',
      spades: '♠'
    }
    return symbols[suit]
  }

  getCardColor(suit: BlackjackCard['suit']): 'red' | 'black' {
    return suit === 'hearts' || suit === 'diamonds' ? 'red' : 'black'
  }
}