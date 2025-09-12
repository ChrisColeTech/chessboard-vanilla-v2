import React, { useState, useEffect } from 'react';
import type { PositionedCard } from '../../../types/casino/poker.types';

interface CardWrapperProps {
  card: PositionedCard;
  size: string;
  onDragStart?: (card: PositionedCard) => void;
  onCardClick?: (card: PositionedCard) => void;
  onDrop?: (card: PositionedCard) => void;
  setDraggedCard?: (card: PositionedCard | null) => void;
  deckPosition?: { x: number; y: number };
}

export const CardWrapper: React.FC<CardWrapperProps> = ({
  card,
  size,
  onDragStart,
  onCardClick,
  deckPosition = { x: 90, y: 10 }
}) => {
  const [position, setPosition] = useState(card.isDealing ? deckPosition : { x: card.x, y: card.y });
  const [isAnimating, setIsAnimating] = useState(false);

  // Convert card format to match image file names
  const getCardImagePath = (suit: string, rank: string) => {
    const suitMap: { [key: string]: string } = {
      'diamonds': 'diamond',
      'hearts': 'heart', 
      'clubs': 'club',
      'spades': 'spade'
    };
    
    const rankMap: { [key: string]: string } = {
      'A': '1',
      'J': 'jack',
      'Q': 'queen', 
      'K': 'king'
    };
    
    const mappedSuit = suitMap[suit] || suit;
    const mappedRank = rankMap[rank] || rank;
    
    return `/assets/casino/cards/${mappedSuit}_${mappedRank}.png`;
  };

  // Handle deal animation
  useEffect(() => {
    if (card.isDealing) {
      setIsAnimating(true);
      setTimeout(() => {
        setPosition({ x: card.x, y: card.y });
        setTimeout(() => {
          setIsAnimating(false);
        }, 500);
      }, 100);
    }
  }, [card.isDealing, card.x, card.y]);

  const handleCardClick = () => {
    if (!isAnimating) {
      onCardClick?.(card);
    }
  };

  return (
    <div
      style={{
        position: 'absolute',
        left: `${position.x}%`,
        top: `${position.y}%`,
        width: size,
        height: `calc(${size} * 1.4)`, // Card aspect ratio
        transform: `translate(-50%, -50%) rotate(${card.rotation || 0}deg)`,
        pointerEvents: isAnimating ? 'none' : 'auto',
        cursor: 'pointer',
        zIndex: 3,
        transition: card.isDealing 
          ? 'left 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94), top 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
          : 'all 0.2s ease'
      }}
      onClick={handleCardClick}
      onMouseDown={() => !isAnimating && onDragStart?.(card)}
      id="card-wrapper-isanimating-ondragstartcard-div"
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          borderRadius: '8px',
          border: '1px solid rgba(255,255,255,0.2)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
          background: card.faceUp 
            ? `url(${getCardImagePath(card.suit, card.rank)}) center/cover`
            : `url(/assets/casino/cards/back.png) center/cover`,
          backfaceVisibility: 'hidden',
          transition: 'background 0.3s ease'
        }}
      />
    </div>
  );
};