// Import the base Card from appStore
import type { Card as BaseCard } from '../../stores/appStore';

// Extended card type with position and animation properties
export interface PositionedCard extends BaseCard {
  id: string;
  x: number;
  y: number;
  rotation?: number;
  faceUp?: boolean;
  isDealing?: boolean;
  isFlipping?: boolean;
}

// Helper function to convert BaseCard to PositionedCard
export const createPositionedCard = (
  baseCard: BaseCard, 
  id: string, 
  x: number = 0, 
  y: number = 0,
  options: Partial<Pick<PositionedCard, 'rotation' | 'faceUp' | 'isDealing' | 'isFlipping'>> = {}
): PositionedCard => ({
  ...baseCard,
  id,
  x,
  y,
  rotation: options.rotation || 0,
  faceUp: options.faceUp !== undefined ? options.faceUp : true,
  isDealing: options.isDealing || false,
  isFlipping: options.isFlipping || false,
});