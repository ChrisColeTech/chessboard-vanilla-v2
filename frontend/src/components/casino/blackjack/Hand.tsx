import React from 'react'
import type { HandProps } from '../../../types/casino/blackjack.types'
import { Card } from './Card'

export const Hand: React.FC<HandProps> = ({ 
  hand, 
  isDealer = false,
  showValue = true,
  isThinking = false,
  className = ''
}) => {
  return (
    <div className={`flex flex-col items-center space-y-4 ${className}`}>
      {/* Cards */}
      <div className="flex space-x-2 justify-center">
        {hand.cards.map((card, index) => (
          <Card
            key={card.id}
            card={card}
            isAnimating={true}
            animationDelay={index * 200}
          />
        ))}
      </div>
      
      {/* Hand Value and Status */}
      {showValue && hand.cards.some(card => card.isVisible) && (
        <div className="text-center">
          {isDealer && isThinking ? (
            <div className="flex items-center space-x-2 text-muted-foreground">
              <span className="text-2xl">🤔</span>
              <span className="text-sm animate-pulse">Thinking...</span>
            </div>
          ) : (
            <div className="space-y-1">
              {/* Hand Value */}
              <div className="text-2xl font-bold">
                {hand.value}
                {hand.isSoft && hand.value <= 21 && (
                  <span className="text-sm text-yellow-600 ml-1">(soft)</span>
                )}
              </div>
              
              {/* Status Indicators */}
              <div className="flex flex-col items-center space-y-1">
                {hand.isBlackjack && (
                  <div className="text-lg font-bold text-yellow-500 animate-pulse">
                    ♠ BLACKJACK! ♠
                  </div>
                )}
                
                {hand.isBusted && (
                  <div className="text-lg font-bold text-red-500 animate-pulse">
                    💥 BUST! 💥
                  </div>
                )}
                
                {!hand.isBlackjack && !hand.isBusted && hand.value === 21 && (
                  <div className="text-sm font-semibold text-green-600">
                    Twenty-One!
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}