import React, { useState } from 'react'
import { useSpring, animated } from '@react-spring/web'
import { Play, RotateCcw, DollarSign, TrendingUp } from 'lucide-react'
import { useAppStore } from '../../../stores/appStore'
import { useUIClickSound } from '../../../hooks/audio/useUIClickSound'
import { getCardImagePath, STANDARD_DECK } from '../../../constants/casino/poker.constants'
import { Button } from '../../ui/button'

export const AppStyleHoldemTable: React.FC = () => {
  const { playUIClick } = useUIClickSound()
  const pokerGame = useAppStore((state) => state.pokerGame)
  const setPlayerHand = useAppStore((state) => state.setPlayerHand)
  const setDealerHand = useAppStore((state) => state.setDealerHand)
  const setCommunityCards = useAppStore((state) => state.setCommunityCards)
  const setPokerGamePhase = useAppStore((state) => state.setPokerGamePhase)
  const setShowDealerCards = useAppStore((state) => state.setShowDealerCards)
  const setPot = useAppStore((state) => state.setPot)
  const setPlayerBet = useAppStore((state) => state.setPlayerBet)
  const setDealerBet = useAppStore((state) => state.setDealerBet)
  
  const [betAmount, setBetAmount] = useState(10)

  // Table animation
  const tableSpring = useSpring({
    opacity: 1,
    transform: 'scale(1)',
    from: { opacity: 0, transform: 'scale(0.98)' },
    config: { tension: 120, friction: 14 }
  })

  // Shuffle and deal cards
  const dealCards = () => {
    playUIClick('Deal Cards')
    
    const shuffledDeck = [...STANDARD_DECK].sort(() => Math.random() - 0.5)
    
    const playerCards: [any, any] = [shuffledDeck[0], shuffledDeck[1]]
    const dealerCards: [any, any] = [shuffledDeck[2], shuffledDeck[3]]
    
    setPlayerHand(playerCards)
    setDealerHand(dealerCards)
    setPokerGamePhase('preflop')
    setShowDealerCards(false)
    setPot(betAmount * 2)
    setPlayerBet(betAmount)
    setDealerBet(betAmount)
  }

  const dealFlop = () => {
    playUIClick('Deal Flop')
    const shuffledDeck = [...STANDARD_DECK].sort(() => Math.random() - 0.5)
    setCommunityCards(shuffledDeck.slice(0, 3))
    setPokerGamePhase('flop')
  }

  const dealTurn = () => {
    playUIClick('Deal Turn')
    const shuffledDeck = [...STANDARD_DECK].sort(() => Math.random() - 0.5)
    setCommunityCards(shuffledDeck.slice(0, 4))
    setPokerGamePhase('turn')
  }

  const dealRiver = () => {
    playUIClick('Deal River')
    const shuffledDeck = [...STANDARD_DECK].sort(() => Math.random() - 0.5)
    setCommunityCards(shuffledDeck.slice(0, 5))
    setPokerGamePhase('river')
  }

  const showdown = () => {
    playUIClick('Showdown')
    setPokerGamePhase('showdown')
    setShowDealerCards(true)
  }

  const newGame = () => {
    playUIClick('New Game')
    setPlayerHand(null)
    setDealerHand(null)
    setCommunityCards([])
    setPokerGamePhase('waiting')
    setShowDealerCards(false)
    setPot(0)
    setPlayerBet(0)
    setDealerBet(0)
  }

  return (
    <animated.div style={tableSpring} className="flex flex-col items-center space-y-6">
      
      {/* Main Poker Table Card */}
      <div className="card-gaming p-8 rounded-3xl shadow-2xl border border-border w-full max-w-4xl">
        
        {/* Gaming accent border */}
        <div className="absolute inset-2 rounded-2xl border border-primary/20 opacity-60"></div>
        
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-4xl mb-4">♔♕</div>
          <h2 className="text-2xl font-bold text-foreground mb-2">Texas Hold'em Poker</h2>
          <p className="text-muted-foreground">Single-player vs Computer Dealer</p>
        </div>

        {/* Dealer Area */}
        <div className="mb-8">
          <div className="bg-background/50 backdrop-blur-sm p-4 rounded-xl border border-border shadow-inner">
            <div className="text-center mb-4">
              <div className="text-lg font-semibold mb-1">🤖 Computer Dealer</div>
              <div className="text-sm text-muted-foreground">Bet: ${pokerGame.dealerBet}</div>
            </div>
            
            {/* Dealer Cards */}
            {pokerGame.dealerHand && (
              <div className="flex justify-center gap-3">
                {pokerGame.dealerHand.map((card, index) => (
                  <animated.div
                    key={index}
                    style={useSpring({
                      opacity: 1,
                      transform: `rotateY(${pokerGame.showDealerCards ? '0deg' : '180deg'})`,
                      from: { opacity: 0, transform: 'rotateY(180deg)' },
                      delay: index * 200,
                      config: { tension: 120, friction: 14 }
                    })}
                  >
                    {pokerGame.showDealerCards ? (
                      <img
                        src={getCardImagePath(card)}
                        alt={`${card.rank} of ${card.suit}`}
                        className="w-16 h-24 rounded-lg shadow-lg border border-border"
                      />
                    ) : (
                      <div className="w-16 h-24 card-gaming rounded-lg border border-border flex items-center justify-center">
                        <div className="w-3 h-4 bg-primary/40 rounded-sm"></div>
                      </div>
                    )}
                  </animated.div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Community Cards & Pot */}
        <div className="mb-8">
          {/* Pot Display */}
          <div className="text-center mb-6">
            <div className="card-gaming p-4 rounded-xl inline-block border border-border">
              <div className="text-sm text-muted-foreground mb-1">Total Pot</div>
              <div className="text-2xl font-bold text-primary">${pokerGame.pot}</div>
              <div className="text-xs text-muted-foreground mt-1">
                {pokerGame.gamePhase === 'waiting' ? 'Ready to Deal' : 
                 pokerGame.gamePhase.charAt(0).toUpperCase() + pokerGame.gamePhase.slice(1)}
              </div>
            </div>
          </div>

          {/* Community Cards */}
          {pokerGame.communityCards.length > 0 && (
            <div className="bg-background/50 backdrop-blur-sm p-4 rounded-xl border border-border shadow-inner">
              <div className="text-center mb-4">
                <div className="text-sm font-medium text-muted-foreground">Community Cards</div>
              </div>
              <div className="flex justify-center gap-2">
                {pokerGame.communityCards.map((card, index) => (
                  <animated.div
                    key={index}
                    style={useSpring({
                      opacity: 1,
                      transform: 'translateY(0px) rotateY(0deg)',
                      from: { opacity: 0, transform: 'translateY(-20px) rotateY(180deg)' },
                      delay: index * 150,
                      config: { tension: 120, friction: 14 }
                    })}
                  >
                    <img
                      src={getCardImagePath(card)}
                      alt={`${card.rank} of ${card.suit}`}
                      className="w-14 h-20 rounded-lg shadow-lg border border-border hover:scale-105 transition-transform"
                    />
                  </animated.div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Player Area */}
        <div className="mb-8">
          <div className="bg-background/50 backdrop-blur-sm p-4 rounded-xl border border-border shadow-inner">
            <div className="text-center mb-4">
              <div className="text-lg font-semibold mb-1">👤 You</div>
              <div className="text-sm text-muted-foreground">
                Chips: ${pokerGame.playerChips} | Bet: ${pokerGame.playerBet}
              </div>
            </div>
            
            {/* Player Cards */}
            {pokerGame.playerHand && (
              <div className="flex justify-center gap-3">
                {pokerGame.playerHand.map((card, index) => (
                  <animated.div
                    key={index}
                    style={useSpring({
                      opacity: 1,
                      transform: 'translateY(0px) rotateY(0deg)',
                      from: { opacity: 0, transform: 'translateY(20px) rotateY(180deg)' },
                      delay: index * 200,
                      config: { tension: 120, friction: 14 }
                    })}
                  >
                    <img
                      src={getCardImagePath(card)}
                      alt={`${card.rank} of ${card.suit}`}
                      className="w-16 h-24 rounded-lg shadow-lg border border-border hover:scale-105 transition-transform"
                    />
                  </animated.div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Game Controls */}
        <div className="flex flex-col items-center space-y-4">
          
          {/* Ante Controls (when waiting) */}
          {pokerGame.gamePhase === 'waiting' && (
            <div className="flex items-center space-x-4 mb-4">
              <div className="text-sm font-medium text-muted-foreground">Ante:</div>
              <div className="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setBetAmount(Math.max(5, betAmount - 5))}
                  className="w-8 h-8 p-0"
                >
                  -
                </Button>
                <div className="card-gaming px-3 py-1 rounded border border-border min-w-[60px] text-center">
                  ${betAmount}
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setBetAmount(Math.min(100, betAmount + 5))}
                  className="w-8 h-8 p-0"
                >
                  +
                </Button>
              </div>
            </div>
          )}
          
          {/* Action Buttons */}
          <div className="flex justify-center gap-3 flex-wrap">
            {pokerGame.gamePhase === 'waiting' && (
              <Button onClick={dealCards} className="flex items-center space-x-2" size="lg">
                <Play className="w-4 h-4" />
                <span>Deal Cards (${betAmount} ante)</span>
              </Button>
            )}
            
            {pokerGame.gamePhase === 'preflop' && (
              <Button onClick={dealFlop} variant="secondary" className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>Deal Flop</span>
              </Button>
            )}
            
            {pokerGame.gamePhase === 'flop' && (
              <Button onClick={dealTurn} variant="secondary" className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>Deal Turn</span>
              </Button>
            )}
            
            {pokerGame.gamePhase === 'turn' && (
              <Button onClick={dealRiver} variant="secondary" className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>Deal River</span>
              </Button>
            )}
            
            {pokerGame.gamePhase === 'river' && (
              <Button onClick={showdown} className="flex items-center space-x-2">
                <DollarSign className="w-4 h-4" />
                <span>Showdown</span>
              </Button>
            )}
            
            {pokerGame.gamePhase === 'showdown' && (
              <Button onClick={newGame} variant="outline" className="flex items-center space-x-2">
                <RotateCcw className="w-4 h-4" />
                <span>New Game</span>
              </Button>
            )}
          </div>
        </div>
      </div>
    </animated.div>
  )
}