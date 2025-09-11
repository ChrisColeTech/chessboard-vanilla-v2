import React from 'react';
import { CardWrapper } from './CardWrapper';
import type { PositionedCard } from '../../../types/casino/poker.types';

interface PlayerCardsProps {
  cards: PositionedCard[];
  size?: string;
  yPosition?: number;
  onCardClick?: (card: PositionedCard) => void;
  onDragStart?: (card: PositionedCard) => void;
}

export const PlayerCards: React.FC<PlayerCardsProps> = ({
  cards,
  size = "19vw",
  yPosition = 75,
  onCardClick,
  onDragStart
}) => {
  // Fixed positions for 2 player cards 
  const cardPositions = [40, 60];

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