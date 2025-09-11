import React from 'react'
import type { CardProps } from '../../../types/casino/blackjack.types'
import { CardDeckService } from '../../../services/casino/CardDeckService'

const cardDeckService = new CardDeckService()

export const Card: React.FC<CardProps> = ({ 
  card, 
  isAnimating = false,
  animationDelay = 0,
  onClick,
  className = ''
}) => {
  const cardImagePath = cardDeckService.getCardImagePath(card)
  const cardColor = cardDeckService.getCardColor(card.suit)
  
  const animationStyle = isAnimating 
    ? {
        animation: `card-entrance 0.3s ease-out forwards`,
        animationDelay: `${animationDelay}ms`
      }
    : {}

  return (
    <div
      className={`
        relative w-20 h-28 md:w-24 md:h-32 cursor-pointer
        transform transition-transform duration-200 hover:scale-105
        ${onClick ? 'cursor-pointer' : 'cursor-default'}
        ${className}
      `}
      style={animationStyle}
      onClick={onClick}
    >
      {/* Card Image */}
      <img
        src={cardImagePath}
        alt={card.isVisible ? `${card.rank} of ${card.suit}` : 'Hidden card'}
        className="w-full h-full object-cover rounded-lg shadow-lg border border-gray-300"
        draggable={false}
      />
      
      {/* Overlay for better visibility if needed */}
      {!card.isVisible && (
        <div className="absolute inset-0 bg-blue-600 rounded-lg flex items-center justify-center">
          <div className="text-white text-2xl font-bold opacity-80">
            ♠♥♣♦
          </div>
        </div>
      )}
      
      {/* Card corner indicators for visible cards */}
      {card.isVisible && (
        <>
          <div className={`
            absolute top-1 left-1 text-xs font-bold leading-none
            ${cardColor === 'red' ? 'text-red-600' : 'text-gray-800'}
          `}>
            <div>{card.rank}</div>
            <div>{cardDeckService.getCardSuitSymbol(card.suit)}</div>
          </div>
          
          <div className={`
            absolute bottom-1 right-1 text-xs font-bold leading-none transform rotate-180
            ${cardColor === 'red' ? 'text-red-600' : 'text-gray-800'}
          `}>
            <div>{card.rank}</div>
            <div>{cardDeckService.getCardSuitSymbol(card.suit)}</div>
          </div>
        </>
      )}
    </div>
  )
}