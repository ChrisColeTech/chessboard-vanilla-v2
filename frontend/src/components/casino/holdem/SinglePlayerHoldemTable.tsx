import React, { useState } from 'react'
import { useSpring, animated } from '@react-spring/web'
import { useAppStore } from '../../../stores/appStore'
import { useUIClickSound } from '../../../hooks/audio/useUIClickSound'
import { getCardImagePath, STANDARD_DECK } from '../../../constants/casino/poker.constants'
import { CommunityCards } from './CommunityCards'
import { createPositionedCard } from '../../../types/casino/poker.types'

export const SinglePlayerHoldemTable: React.FC = () => {
  const { playUIClick } = useUIClickSound()
  const pokerGame = useAppStore((state) => state.pokerGame)
  const setPlayerHand = useAppStore((state) => state.setPlayerHand)
  const setDealerHand = useAppStore((state) => state.setDealerHand)
  const setCommunityCards = useAppStore((state) => state.setCommunityCards)
  const setPokerGamePhase = useAppStore((state) => state.setPokerGamePhase)
  const setIsPlayerTurn = useAppStore((state) => state.setIsPlayerTurn)
  const setShowDealerCards = useAppStore((state) => state.setShowDealerCards)
  const setPot = useAppStore((state) => state.setPot)
  const setPlayerBet = useAppStore((state) => state.setPlayerBet)
  const setDealerBet = useAppStore((state) => state.setDealerBet)
  
  const [betAmount, setBetAmount] = useState(10)

  // Table background animation
  const tableSpring = useSpring({
    opacity: 1,
    transform: 'scale(1)',
    from: { opacity: 0, transform: 'scale(0.95)' },
    config: { tension: 120, friction: 14 }
  })

  // Shuffle and deal cards
  const dealCards = () => {
    playUIClick('Deal Cards')
    
    // Simple card dealing for demo
    const shuffledDeck = [...STANDARD_DECK].sort(() => Math.random() - 0.5)
    
    // Deal 2 cards to player and dealer
    const playerCards: [any, any] = [shuffledDeck[0], shuffledDeck[1]]
    const dealerCards: [any, any] = [shuffledDeck[2], shuffledDeck[3]]
    
    setPlayerHand(playerCards)
    setDealerHand(dealerCards)
    setPokerGamePhase('preflop')
    setIsPlayerTurn(true)
    setShowDealerCards(false)
    setPot(betAmount * 2) // Ante up
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
    <animated.div style={tableSpring} className="relative w-full h-full min-h-[700px]">
      {/* Poker Table Background */}
      <div 
        className="absolute inset-0 rounded-3xl shadow-2xl"
        style={{
          background: `
            radial-gradient(ellipse at center, 
              rgba(34, 197, 94, 0.9) 0%, 
              rgba(21, 128, 61, 0.95) 60%, 
              rgba(15, 78, 46, 1) 100%
            )
          `,
          backgroundImage: `url('/assets/casino/table/green-felt.jpg')`,
          backgroundBlendMode: 'multiply',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        {/* Table border */}
        <div className="absolute inset-2 rounded-2xl border-4 border-yellow-600/30 shadow-inner"></div>
        <div className="absolute inset-4 rounded-xl border border-yellow-500/20"></div>
      </div>

      {/* Game Content */}
      <div className="relative z-10 p-6 h-full flex flex-col">
        
        {/* Dealer Area (Top) */}
        <div className="mb-6">
          <div className="text-center mb-4">
            <div className="bg-card/95 backdrop-blur-sm rounded-xl p-4 inline-block shadow-lg border border-border">
              <h3 className="font-bold text-lg mb-2">🤖 Computer Dealer</h3>
              <div className="text-sm text-muted-foreground">Bet: ${pokerGame.dealerBet}</div>
            </div>
          </div>
          
          {/* Dealer Cards */}
          {pokerGame.dealerHand && (
            <div className="flex justify-center gap-3">
              {pokerGame.dealerHand.map((card, index) => (
                <animated.div
                  key={index}
                  className="relative"
                  style={useSpring({
                    opacity: 1,
                    transform: `translateY(0px) rotateY(${pokerGame.showDealerCards ? '0deg' : '180deg'})`,
                    from: { opacity: 0, transform: `translateY(-50px) rotateY(180deg)` },
                    delay: index * 200,
                    config: { tension: 120, friction: 14 }
                  })}
                >
                  {pokerGame.showDealerCards ? (
                    <img
                      src={getCardImagePath(card)}
                      alt={`${card.rank} of ${card.suit}`}
                      className="w-20 h-30 rounded-lg shadow-lg border border-border"
                    />
                  ) : (
                    <div className="w-20 h-30 bg-gradient-to-br from-blue-800 to-blue-900 rounded-lg shadow-lg border border-blue-700 flex items-center justify-center">
                      <div className="w-4 h-6 bg-blue-300 rounded-sm opacity-60"></div>
                    </div>
                  )}
                </animated.div>
              ))}
            </div>
          )}
        </div>

        {/* Community Cards & Pot Area (Center) */}
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            {/* Pot Display */}
            <div className="mb-6">
              <div className="bg-background/90 backdrop-blur-sm rounded-xl p-4 shadow-lg border border-border">
                <div className="text-sm text-muted-foreground">Total Pot</div>
                <div className="text-3xl font-bold text-primary">${pokerGame.pot}</div>
                <div className="text-xs text-muted-foreground mt-1">
                  {pokerGame.gamePhase === 'waiting' ? 'Ready to Deal' : 
                   pokerGame.gamePhase.charAt(0).toUpperCase() + pokerGame.gamePhase.slice(1)}
                </div>
              </div>
            </div>

            {/* Community Cards */}
            <CommunityCards 
              cards={pokerGame.communityCards.map((card, index) => 
                createPositionedCard(card, `community-${index}`, 0, 0, { faceUp: true })
              )} 
            />
          </div>
        </div>

        {/* Player Area (Bottom) */}
        <div className="mb-6">
          {/* Player Cards */}
          {pokerGame.playerHand && (
            <div className="flex justify-center gap-3 mb-4">
              {pokerGame.playerHand.map((card, index) => (
                <animated.div
                  key={index}
                  className="relative"
                  style={useSpring({
                    opacity: 1,
                    transform: `translateY(0px) rotateY(0deg)`,
                    from: { opacity: 0, transform: `translateY(50px) rotateY(180deg)` },
                    delay: index * 200,
                    config: { tension: 120, friction: 14 }
                  })}
                >
                  <img
                    src={getCardImagePath(card)}
                    alt={`${card.rank} of ${card.suit}`}
                    className="w-20 h-30 rounded-lg shadow-lg border border-border hover:scale-105 transition-transform"
                  />
                </animated.div>
              ))}
            </div>
          )}
          
          <div className="text-center">
            <div className="bg-card/95 backdrop-blur-sm rounded-xl p-4 inline-block shadow-lg border border-border">
              <h3 className="font-bold text-lg mb-2">👤 You</h3>
              <div className="text-sm text-muted-foreground">
                Chips: ${pokerGame.playerChips} | Bet: ${pokerGame.playerBet}
              </div>
            </div>
          </div>
        </div>

        {/* Game Controls */}
        <div className="flex justify-center gap-4 flex-wrap">
          {pokerGame.gamePhase === 'waiting' && (
            <>
              <div className="flex items-center gap-2 mb-4">
                <label className="text-sm font-medium">Ante:</label>
                <input
                  type="number"
                  min="5"
                  max="100"
                  step="5"
                  value={betAmount}
                  onChange={(e) => setBetAmount(Number(e.target.value))}
                  className="w-20 px-2 py-1 rounded border border-border bg-background text-center"
                />
              </div>
              <button
                onClick={dealCards}
                className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
              >
                Deal Cards (${betAmount} ante)
              </button>
            </>
          )}
          
          {pokerGame.gamePhase === 'preflop' && (
            <button
              onClick={dealFlop}
              className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg transition-all"
            >
              Deal Flop
            </button>
          )}
          
          {pokerGame.gamePhase === 'flop' && (
            <button
              onClick={dealTurn}
              className="bg-green-600 hover:bg-green-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg transition-all"
            >
              Deal Turn
            </button>
          )}
          
          {pokerGame.gamePhase === 'turn' && (
            <button
              onClick={dealRiver}
              className="bg-orange-600 hover:bg-orange-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg transition-all"
            >
              Deal River
            </button>
          )}
          
          {pokerGame.gamePhase === 'river' && (
            <button
              onClick={showdown}
              className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg transition-all"
            >
              Showdown
            </button>
          )}
          
          {pokerGame.gamePhase === 'showdown' && (
            <button
              onClick={newGame}
              className="bg-green-600 hover:bg-green-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg transition-all"
            >
              New Game
            </button>
          )}
        </div>
      </div>
    </animated.div>
  )
}