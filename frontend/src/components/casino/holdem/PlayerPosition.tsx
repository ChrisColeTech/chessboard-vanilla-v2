import React from 'react'
import { animated, useSpring } from '@react-spring/web'
import { Crown, User } from 'lucide-react'
import type { Card, BetAction } from '../../../stores/appStore'
import { getCardImagePath } from '../../../constants/casino/poker.constants'

interface PlayerPositionProps {
  player: {
    name: string
    chips: number
    position: number
    isActive: boolean
    hand: [Card, Card] | null
    lastAction: BetAction | null
  }
  isDealer: boolean
  isCurrentPlayer: boolean
  showCards?: boolean
}

export const PlayerPosition: React.FC<PlayerPositionProps> = ({ 
  player, 
  isDealer, 
  isCurrentPlayer, 
  showCards = false 
}) => {
  
  // Animation for player turn indicator
  const turnSpring = useSpring({
    transform: isCurrentPlayer ? 'scale(1.05)' : 'scale(1)',
    boxShadow: isCurrentPlayer 
      ? '0 0 20px rgba(34, 197, 94, 0.6)' 
      : '0 4px 6px rgba(0, 0, 0, 0.1)',
    config: { tension: 200, friction: 20 }
  })

  // Animation for chip stack
  const chipSpring = useSpring({
    opacity: player.isActive ? 1 : 0.6,
    scale: player.isActive ? 1 : 0.9,
    config: { tension: 120, friction: 14 }
  })

  // Get action color based on last action type
  const getActionColor = (action: BetAction | null) => {
    if (!action) return 'text-muted-foreground'
    
    switch (action.type) {
      case 'fold': return 'text-red-500'
      case 'check': return 'text-blue-500'
      case 'call': return 'text-green-500'
      case 'raise': return 'text-orange-500'
      case 'all-in': return 'text-purple-500'
      default: return 'text-muted-foreground'
    }
  }

  const getActionText = (action: BetAction | null) => {
    if (!action) return ''
    
    switch (action.type) {
      case 'fold': return 'Fold'
      case 'check': return 'Check'
      case 'call': return `Call $${action.amount}`
      case 'raise': return `Raise $${action.amount}`
      case 'all-in': return `All-in $${action.amount}`
      default: return ''
    }
  }

  return (
    <animated.div style={turnSpring} className="relative">
      {/* Player Card */}
      <div className="bg-card/95 backdrop-blur-sm rounded-xl p-4 min-w-[140px] shadow-lg border border-border">
        
        {/* Dealer Button */}
        {isDealer && (
          <div className="absolute -top-2 -right-2 bg-yellow-500 text-yellow-900 w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shadow-lg">
            <Crown className="w-4 h-4" />
          </div>
        )}

        {/* Player Avatar & Name */}
        <div className="flex items-center gap-2 mb-2">
          <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="font-medium text-sm truncate">{player.name}</div>
            <div className="text-xs text-muted-foreground">
              Position {player.position}
            </div>
          </div>
        </div>

        {/* Chip Stack */}
        <animated.div style={chipSpring} className="mb-2">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full border-2 border-blue-300 shadow-sm flex items-center justify-center text-xs text-white font-bold">
              $
            </div>
            <div className="text-sm font-bold">${player.chips}</div>
          </div>
        </animated.div>

        {/* Hole Cards */}
        {player.hand && (
          <div className="flex gap-1 mb-2">
            {player.hand.map((card, index) => (
              <div key={index} className="relative">
                {showCards ? (
                  <animated.img
                    src={getCardImagePath(card)}
                    alt={`${card.rank} of ${card.suit}`}
                    className="w-8 h-12 rounded shadow-sm border border-border"
                    style={useSpring({
                      opacity: 1,
                      transform: 'rotateY(0deg)',
                      from: { opacity: 0, transform: 'rotateY(180deg)' },
                      delay: index * 100,
                      config: { tension: 120, friction: 14 }
                    })}
                  />
                ) : (
                  <div className="w-8 h-12 bg-gradient-to-br from-blue-800 to-blue-900 rounded shadow-sm border border-blue-700 flex items-center justify-center">
                    <div className="w-2 h-3 bg-blue-300 rounded-sm opacity-60"></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Last Action */}
        {player.lastAction && (
          <div className={`text-xs font-medium ${getActionColor(player.lastAction)}`}>
            {getActionText(player.lastAction)}
          </div>
        )}

        {/* Player Status */}
        <div className="flex items-center gap-1">
          <div 
            className={`w-2 h-2 rounded-full ${
              player.isActive ? 'bg-green-500' : 'bg-gray-400'
            }`}
          />
          <div className="text-xs text-muted-foreground">
            {player.isActive ? 'Active' : 'Folded'}
          </div>
        </div>
      </div>

      {/* Turn Indicator Glow */}
      {isCurrentPlayer && (
        <div className="absolute inset-0 bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-xl animate-pulse -z-10"></div>
      )}
    </animated.div>
  )
}