import React from 'react'
import { useSpring, animated } from '@react-spring/web'
import { useAppStore } from '../../../stores/appStore'
import { useUIClickSound } from '../../../hooks/audio/useUIClickSound'
import { getCardImagePath } from '../../../constants/casino/poker.constants'
import { PlayerPosition } from './PlayerPosition'
import { CommunityCards } from './CommunityCards'
import { BettingControls } from './BettingControls'
import { createPositionedCard } from '../../../types/casino/poker.types'

export const HoldemTable: React.FC = () => {
  const { playUIClick } = useUIClickSound()
  const pokerGame = useAppStore((state) => state.pokerGame)
  const dealNewHand = useAppStore((state) => state.dealNewHand)
  const setPlayerHand = useAppStore((state) => state.setPlayerHand)
  
  // Table background animation
  const tableSpring = useSpring({
    opacity: 1,
    transform: 'scale(1)',
    from: { opacity: 0, transform: 'scale(0.95)' },
    config: { tension: 120, friction: 14 }
  })

  const handleDealHand = () => {
    playUIClick('Deal Cards')
    
    // Create a simple demo hand for now
    const demoHand: [any, any] = [
      { suit: 'hearts', rank: 'A' },
      { suit: 'spades', rank: 'K' }
    ]
    
    setPlayerHand(demoHand)
    dealNewHand()
  }

  return (
    <animated.div style={tableSpring} className="relative w-full h-full min-h-[600px]">
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
        {/* Felt texture overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-green-600/20 to-green-800/40 rounded-3xl"></div>
        
        {/* Table border */}
        <div className="absolute inset-2 rounded-2xl border-4 border-yellow-600/30 shadow-inner"></div>
        <div className="absolute inset-4 rounded-xl border border-yellow-500/20"></div>
      </div>

      {/* Game Content */}
      <div className="relative z-10 p-6 h-full flex flex-col">
        
        {/* AI Opponents Positions */}
        <div className="flex justify-around items-start mb-4">
          <PlayerPosition 
            player={{ 
              name: 'Sarah', 
              chips: 850, 
              position: 1, 
              isActive: true,
              hand: null,
              lastAction: null 
            }} 
            isDealer={false}
            isCurrentPlayer={false}
          />
          <PlayerPosition 
            player={{ 
              name: 'Mike', 
              chips: 1200, 
              position: 2, 
              isActive: true,
              hand: null,
              lastAction: { type: 'call', amount: 10 }
            }} 
            isDealer={true}
            isCurrentPlayer={false}
          />
          <PlayerPosition 
            player={{ 
              name: 'Bob', 
              chips: 750, 
              position: 3, 
              isActive: true,
              hand: null,
              lastAction: { type: 'fold' }
            }} 
            isDealer={false}
            isCurrentPlayer={false}
          />
        </div>

        {/* Community Cards Area */}
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            {/* Pot Display */}
            <div className="mb-6">
              <div className="bg-background/90 backdrop-blur-sm rounded-xl p-3 shadow-lg border border-border">
                <div className="text-sm text-muted-foreground">Pot</div>
                <div className="text-2xl font-bold text-primary">${pokerGame.pot}</div>
              </div>
            </div>

            {/* Community Cards */}
            <CommunityCards 
              cards={pokerGame.communityCards.map((card, index) => 
                createPositionedCard(card, `community-${index}`, 0, 0, { faceUp: true })
              )} 
            />
            
            {/* Game Phase Indicator */}
            <div className="mt-4">
              <div className="bg-accent/20 backdrop-blur-sm rounded-lg px-4 py-2 text-sm font-medium">
                {pokerGame.gamePhase === 'waiting' ? 'Ready to Deal' : 
                 pokerGame.gamePhase.charAt(0).toUpperCase() + pokerGame.gamePhase.slice(1)}
              </div>
            </div>
          </div>
        </div>

        {/* Player Position (Bottom) */}
        <div className="flex justify-center mb-4">
          <PlayerPosition 
            player={{ 
              name: 'You', 
              chips: pokerGame.playerChips, 
              position: 0, 
              isActive: true,
              hand: pokerGame.playerHand,
              lastAction: null 
            }} 
            isDealer={false}
            isCurrentPlayer={true}
            showCards={true}
          />
        </div>

        {/* Player Hand Display */}
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
                  className="w-16 h-24 rounded-lg shadow-lg border border-border hover:scale-105 transition-transform"
                />
              </animated.div>
            ))}
          </div>
        )}

        {/* Deal Button or Betting Controls */}
        {pokerGame.gamePhase === 'waiting' ? (
          <div className="flex justify-center">
            <button
              onClick={handleDealHand}
              className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
            >
              Deal Cards
            </button>
          </div>
        ) : (
          <BettingControls />
        )}
      </div>
    </animated.div>
  )
}