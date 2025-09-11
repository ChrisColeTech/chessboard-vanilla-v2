import { useState, useCallback, useMemo } from 'react'
import type { BlackjackGameState, BlackjackCard, GameResult } from '../../types/casino/blackjack.types'
import { CardDeckService } from '../../services/casino/CardDeckService'
import { BlackjackLogic } from '../../services/casino/BlackjackLogic'
import { useCasinoAudio } from '../../services/casino/CasinoAudioService'
import { useAppStore } from '../../stores/appStore'
import { BLACKJACK_RULES } from '../../constants/casino/blackjack.constants'

const initialGameState: BlackjackGameState = {
  playerHand: { cards: [], value: 0, isSoft: false, isBusted: false, isBlackjack: false },
  dealerHand: { cards: [], value: 0, isSoft: false, isBusted: false, isBlackjack: false },
  deck: [],
  currentBet: 0,
  gamePhase: 'betting',
  canHit: false,
  canStand: false,
  canDouble: false,
  gameResult: null,
  isThinking: false,
}

export const useBlackjack = () => {
  const [gameState, setGameState] = useState<BlackjackGameState>(initialGameState)
  const { coinBalance, setCoinBalance } = useAppStore((state) => ({
    coinBalance: state.coinBalance,
    setCoinBalance: state.setCoinBalance,
  }))
  
  const {
    playCardDeal,
    playCardShuffle,
    playChipBet,
    playChipCollect,
    playWin,
    playLose,
    playGameStart
  } = useCasinoAudio()

  const cardDeckService = useMemo(() => new CardDeckService(), [])
  const blackjackLogic = useMemo(() => new BlackjackLogic(), [])

  const placeBet = useCallback((amount: number): boolean => {
    if (amount > coinBalance) return false
    setCoinBalance(coinBalance - amount)
    return true
  }, [coinBalance, setCoinBalance])

  const addWinnings = useCallback((amount: number) => {
    setCoinBalance(coinBalance + amount)
    playChipCollect()
  }, [coinBalance, setCoinBalance, playChipCollect])

  const startNewGame = useCallback(async (betAmount: number): Promise<boolean> => {
    if (!placeBet(betAmount)) return false

    playChipBet()
    playGameStart()

    // Create new deck if needed
    const needsNewDeck = gameState.deck.length < (52 * BLACKJACK_RULES.DECK_SHUFFLE_THRESHOLD)
    const deck = needsNewDeck ? cardDeckService.createNewDeck() : [...gameState.deck]

    if (needsNewDeck) {
      playCardShuffle()
    }

    // Deal initial cards
    const newDeck = [...deck]
    
    // Player gets 2 visible cards
    const { card: playerCard1, remainingDeck: deck1 } = cardDeckService.dealCard(newDeck, true)
    const { card: dealerCard1, remainingDeck: deck2 } = cardDeckService.dealCard(deck1, true)
    const { card: playerCard2, remainingDeck: deck3 } = cardDeckService.dealCard(deck2, true)
    const { card: dealerCard2, remainingDeck: deck4 } = cardDeckService.dealCard(deck3, false) // Hidden

    const playerCards = [playerCard1, playerCard2]
    const dealerCards = [dealerCard1, dealerCard2]

    const playerHand = blackjackLogic.createHand(playerCards)
    const dealerHand = blackjackLogic.createHand([dealerCard1]) // Only count visible card

    setGameState({
      ...initialGameState,
      deck: deck4,
      playerHand,
      dealerHand: { ...dealerHand, cards: dealerCards },
      currentBet: betAmount,
      gamePhase: 'dealing',
      canHit: true,
      canStand: true,
      canDouble: blackjackLogic.canPlayerDouble(playerCards, coinBalance, betAmount),
    })

    // Deal cards with animation delays
    setTimeout(() => playCardDeal(), 100)
    setTimeout(() => playCardDeal(), 300)
    setTimeout(() => playCardDeal(), 500)
    setTimeout(() => playCardDeal(), 700)

    // Check for immediate blackjack
    setTimeout(() => {
      if (playerHand.isBlackjack) {
        handlePlayerBlackjack(dealerCards, deck4, betAmount)
      } else {
        setGameState(prev => ({ ...prev, gamePhase: 'player-turn' }))
      }
    }, 1000)

    return true
  }, [gameState.deck, coinBalance, placeBet, playChipBet, playGameStart, playCardShuffle, playCardDeal, cardDeckService, blackjackLogic])

  const handlePlayerBlackjack = useCallback(async (dealerCards: BlackjackCard[], _deck: BlackjackCard[], betAmount: number) => {
    // Reveal dealer's hidden card
    const revealedDealerCards = dealerCards.map(card => ({ ...card, isVisible: true }))
    const dealerHand = blackjackLogic.createHand(revealedDealerCards)
    
    const result: GameResult = dealerHand.isBlackjack ? 'push' : 'blackjack'
    const payout = blackjackLogic.calculatePayout(result, betAmount)
    
    setGameState(prev => ({
      ...prev,
      dealerHand,
      gamePhase: 'game-over',
      gameResult: result,
      canHit: false,
      canStand: false,
      canDouble: false,
    }))

    if (payout > 0) {
      addWinnings(payout)
      playWin(payout, betAmount)
    } else {
      playLose()
    }
  }, [blackjackLogic, addWinnings, playWin, playLose])

  const hit = useCallback(() => {
    if (gameState.gamePhase !== 'player-turn') return

    const { card: newCard, remainingDeck } = cardDeckService.dealCard(gameState.deck, true)
    const newPlayerCards = [...gameState.playerHand.cards, newCard]
    const newPlayerHand = blackjackLogic.createHand(newPlayerCards)

    playCardDeal()

    setGameState(prev => ({
      ...prev,
      deck: remainingDeck,
      playerHand: newPlayerHand,
      canDouble: false, // Can't double after hitting
    }))

    if (newPlayerHand.isBusted) {
      setTimeout(() => {
        playLose()
        setGameState(prev => ({
          ...prev,
          gamePhase: 'game-over',
          gameResult: 'dealer-wins',
          canHit: false,
          canStand: false,
        }))
      }, 500)
    }
  }, [gameState, cardDeckService, blackjackLogic, playCardDeal, playLose])

  const stand = useCallback(() => {
    if (gameState.gamePhase !== 'player-turn') return

    setGameState(prev => ({
      ...prev,
      gamePhase: 'dealer-turn',
      canHit: false,
      canStand: false,
      canDouble: false,
    }))

    // Play dealer turn
    setTimeout(() => {
      playDealerTurn()
    }, 500)
  }, [gameState.gamePhase])

  const doubleDown = useCallback(() => {
    if (!gameState.canDouble || !placeBet(gameState.currentBet)) return

    playChipBet()

    // Hit once then automatically stand
    const { card: newCard, remainingDeck } = cardDeckService.dealCard(gameState.deck, true)
    const newPlayerCards = [...gameState.playerHand.cards, newCard]
    const newPlayerHand = blackjackLogic.createHand(newPlayerCards)

    playCardDeal()

    setGameState(prev => ({
      ...prev,
      deck: remainingDeck,
      playerHand: newPlayerHand,
      currentBet: prev.currentBet * 2,
      canHit: false,
      canStand: false,
      canDouble: false,
    }))

    if (newPlayerHand.isBusted) {
      setTimeout(() => {
        playLose()
        setGameState(prev => ({
          ...prev,
          gamePhase: 'game-over',
          gameResult: 'dealer-wins',
        }))
      }, 500)
    } else {
      setTimeout(() => {
        setGameState(prev => ({ ...prev, gamePhase: 'dealer-turn' }))
        playDealerTurn()
      }, 1000)
    }
  }, [gameState, placeBet, playChipBet, cardDeckService, blackjackLogic, playCardDeal, playLose])

  const playDealerTurn = useCallback(async () => {
    const onCardDealt = (card: BlackjackCard) => {
      playCardDeal()
      setGameState(prev => ({
        ...prev,
        dealerHand: blackjackLogic.createHand([...prev.dealerHand.cards, card]),
      }))
    }

    const onThinking = (isThinking: boolean) => {
      setGameState(prev => ({ ...prev, isThinking }))
    }

    try {
      // Reveal dealer's hidden card first
      const revealedCards = gameState.dealerHand.cards.map(card => ({ ...card, isVisible: true }))
      const updatedDealerHand = blackjackLogic.createHand(revealedCards)
      
      setGameState(prev => ({
        ...prev,
        dealerHand: updatedDealerHand,
      }))

      const { finalHand } = await blackjackLogic.playDealerTurn(
        revealedCards,
        gameState.deck,
        onCardDealt,
        onThinking
      )

      const finalDealerHand = blackjackLogic.createHand(finalHand)
      const result = blackjackLogic.determineWinner(gameState.playerHand.cards, finalHand)
      const payout = blackjackLogic.calculatePayout(result, gameState.currentBet)

      setGameState(prev => ({
        ...prev,
        dealerHand: finalDealerHand,
        gamePhase: 'game-over',
        gameResult: result,
        isThinking: false,
      }))

      setTimeout(() => {
        if (payout > 0) {
          addWinnings(payout)
          playWin(payout, gameState.currentBet)
        } else {
          playLose()
        }
      }, 1000)

    } catch (error) {
      console.error('Error during dealer turn:', error)
      setGameState(prev => ({ ...prev, isThinking: false }))
    }
  }, [gameState, blackjackLogic, playCardDeal, addWinnings, playWin, playLose])

  const resetGame = useCallback(() => {
    setGameState(initialGameState)
  }, [])

  return {
    gameState,
    startNewGame,
    hit,
    stand,
    doubleDown,
    resetGame,
    canStartNewGame: gameState.gamePhase === 'betting' || gameState.gamePhase === 'game-over',
    balance: coinBalance,
  }
}