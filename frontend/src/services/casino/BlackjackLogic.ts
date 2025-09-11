import type { BlackjackCard, BlackjackHand, GameResult } from '../../types/casino/blackjack.types'
import { BLACKJACK_RULES } from '../../constants/casino/blackjack.constants'

export class BlackjackLogic {
  calculateHandValue(cards: BlackjackCard[]): { value: number; isSoft: boolean } {
    let value = 0
    let aces = 0
    
    // Count non-ace cards first
    cards.forEach(card => {
      if (card.isVisible) {
        if (card.rank === 'A') {
          aces++
        } else {
          value += card.value
        }
      }
    })
    
    // Handle aces (11 or 1)
    let softAces = 0
    for (let i = 0; i < aces; i++) {
      if (value + 11 <= BLACKJACK_RULES.BLACKJACK_VALUE && softAces === 0) {
        value += 11
        softAces++
      } else {
        value += 1
      }
    }
    
    return {
      value,
      isSoft: softAces > 0
    }
  }

  createHand(cards: BlackjackCard[]): BlackjackHand {
    const handValue = this.calculateHandValue(cards)
    
    return {
      cards: [...cards],
      value: handValue.value,
      isSoft: handValue.isSoft,
      isBusted: handValue.value > BLACKJACK_RULES.BLACKJACK_VALUE,
      isBlackjack: this.isBlackjack(cards)
    }
  }

  isBlackjack(cards: BlackjackCard[]): boolean {
    if (cards.length !== 2) return false
    
    const visibleCards = cards.filter(card => card.isVisible)
    if (visibleCards.length !== 2) return false
    
    const handValue = this.calculateHandValue(cards)
    return handValue.value === BLACKJACK_RULES.BLACKJACK_VALUE
  }

  shouldDealerHit(dealerHand: BlackjackCard[]): boolean {
    const handValue = this.calculateHandValue(dealerHand)
    
    // Dealer hits on soft 17
    if (handValue.value < BLACKJACK_RULES.DEALER_HITS_UNDER) return true
    if (handValue.value === BLACKJACK_RULES.DEALER_HITS_UNDER && handValue.isSoft) return true
    
    return false
  }

  determineWinner(
    playerHand: BlackjackCard[], 
    dealerHand: BlackjackCard[]
  ): GameResult {
    const playerValue = this.calculateHandValue(playerHand)
    const dealerValue = this.calculateHandValue(dealerHand)
    
    const playerBlackjack = this.isBlackjack(playerHand)
    const dealerBlackjack = this.isBlackjack(dealerHand)
    
    // Blackjack scenarios
    if (playerBlackjack && dealerBlackjack) return 'push'
    if (playerBlackjack && !dealerBlackjack) return 'blackjack'
    if (!playerBlackjack && dealerBlackjack) return 'dealer-wins'
    
    // Bust scenarios
    if (playerValue.value > BLACKJACK_RULES.BLACKJACK_VALUE) return 'dealer-wins'
    if (dealerValue.value > BLACKJACK_RULES.BLACKJACK_VALUE) return 'player-wins'
    
    // Value comparison
    if (playerValue.value > dealerValue.value) return 'player-wins'
    if (dealerValue.value > playerValue.value) return 'dealer-wins'
    
    return 'push'
  }

  calculatePayout(result: GameResult, betAmount: number): number {
    switch (result) {
      case 'blackjack':
        return Math.floor(betAmount * (1 + BLACKJACK_RULES.BLACKJACK_PAYOUT))
      case 'player-wins':
        return betAmount * (1 + BLACKJACK_RULES.REGULAR_PAYOUT)
      case 'push':
        return betAmount // Return original bet
      case 'dealer-wins':
        return 0
      default:
        return 0
    }
  }

  getGameResultMessage(result: GameResult): string {
    switch (result) {
      case 'blackjack':
        return 'BLACKJACK! 🎉'
      case 'player-wins':
        return 'YOU WIN! 🎊'
      case 'dealer-wins':
        return 'DEALER WINS 😔'
      case 'push':
        return 'PUSH - TIE 🤝'
      default:
        return ''
    }
  }

  canPlayerDouble(playerHand: BlackjackCard[], balance: number, currentBet: number): boolean {
    // Can only double on first two cards
    if (playerHand.length !== 2) return false
    
    // Must have enough balance to double the bet
    if (balance < currentBet) return false
    
    return true
  }

  async playDealerTurn(
    dealerHand: BlackjackCard[],
    deck: BlackjackCard[],
    onCardDealt: (card: BlackjackCard) => void,
    onThinking: (isThinking: boolean) => void
  ): Promise<{ finalHand: BlackjackCard[], remainingDeck: BlackjackCard[] }> {
    let currentHand = [...dealerHand]
    let currentDeck = [...deck]
    
    // Reveal hidden card first
    if (currentHand.length > 1 && !currentHand[1].isVisible) {
      currentHand[1] = { ...currentHand[1], isVisible: true }
      await this.delay(500)
    }
    
    while (this.shouldDealerHit(currentHand)) {
      onThinking(true)
      
      // Dealer thinking delay (1-2 seconds)
      const thinkingTime = 1000 + Math.random() * 1000
      await this.delay(thinkingTime)
      
      onThinking(false)
      
      // Deal card
      if (currentDeck.length === 0) break
      
      const newCard = { ...currentDeck.pop()!, isVisible: true }
      currentHand.push(newCard)
      
      onCardDealt(newCard)
      
      // Brief pause after dealing
      await this.delay(600)
    }
    
    onThinking(false)
    return { finalHand: currentHand, remainingDeck: currentDeck }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}