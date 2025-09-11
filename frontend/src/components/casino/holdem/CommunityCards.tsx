import React from 'react';
import { CardWrapper } from './CardWrapper';
import type { PositionedCard } from '../../../types/casino/poker.types';

interface CommunityCardsProps {
  cards: PositionedCard[];
  size?: string;
  yPosition?: number;
  onCardClick?: (card: PositionedCard) => void;
  onDragStart?: (card: PositionedCard) => void;
}

export const CommunityCards: React.FC<CommunityCardsProps> = ({
  cards,
  size = "15vw",
  yPosition = 30,
  onCardClick,
  onDragStart
}) => {
  // Fixed positions for 5 community cards with proper spacing
  const cardPositions = [13, 31, 49, 67, 85];

  return (
    <>
      {cards.map((card, index) => (
        <CardWrapper
          key={card.id}
          card={{
            ...card,
            x: cardPositions[index] || 50,
            y: yPosition
          }}
          size={size}
          onCardClick={onCardClick}
          onDragStart={onDragStart}
        />
      ))}
    </>
  );
};