// Modified MobileChessBoard - converting to card table step by step
import React from "react";
import { useChessSettings } from "../../../stores/appStore";
import { PokerGrid } from "./PokerGrid";
import { CardTableOverlay } from "./CardTableOverlay";
import { CommunityCards } from "./CommunityCards";
import { PlayerCards } from "./PlayerCards";
import { ChipWrapper } from "./ChipWrapper";
import { createPositionedCard } from "../../../types/casino/poker.types";
import type { MobileChessGameState } from "../../../types";

interface MobilePokerTableProps {
  gridSize?: number;
  onGameStateChange?: (gameState: MobileChessGameState) => void;
}

// Helper function to get size multiplier based on setting
const getPieceSizeMultiplier = (size: 'small' | 'medium' | 'large'): number => {
  switch (size) {
    case 'small': return 0.55;   // Reduced by 15% (from 0.65)
    case 'medium': return 0.63;  // Reduced by 30% (from 0.9)
    case 'large': return 0.81;   // Reduced by 30% (from 1.15)
    default: return 0.63;
  }
};

export const MobilePokerTable: React.FC<MobilePokerTableProps> = ({ gridSize = 8, onGameStateChange: _onGameStateChange }) => {
  // Get piece size setting from store
  const { pieceSize } = useChessSettings();
  
  // Centralized responsive piece sizing based on grid size and user setting
  const GRID_SIZE = gridSize;
  const sizeMultiplier = getPieceSizeMultiplier(pieceSize);
  const PIECE_SIZE = `min(${100 / GRID_SIZE * sizeMultiplier}vw, ${100 / GRID_SIZE * sizeMultiplier}vh)`;
  
  // Sample card data - this will later come from game state
  const [cardsRevealed, setCardsRevealed] = React.useState(false);
  
  const communityCards = [
    createPositionedCard({ suit: 'diamonds', rank: '10' }, 'flop-1', 0, 0, { faceUp: cardsRevealed }),
    createPositionedCard({ suit: 'clubs', rank: 'J' }, 'flop-2', 0, 0, { faceUp: cardsRevealed }),
    createPositionedCard({ suit: 'hearts', rank: 'Q' }, 'flop-3', 0, 0, { faceUp: cardsRevealed }),
    createPositionedCard({ suit: 'spades', rank: 'K' }, 'turn', 0, 0, { faceUp: cardsRevealed }),
    createPositionedCard({ suit: 'diamonds', rank: 'A' }, 'river', 0, 0, { faceUp: cardsRevealed })
  ];

  const playerCards = [
    createPositionedCard({ suit: 'hearts', rank: 'A' }, 'player-card-1', 0, 0, { faceUp: cardsRevealed }),
    createPositionedCard({ suit: 'spades', rank: 'A' }, 'player-card-2', 0, 0, { faceUp: cardsRevealed })
  ];

  // Auto-flip cards after 2 seconds to demonstrate animation
  React.useEffect(() => {
    const timer = setTimeout(() => {
      setCardsRevealed(true);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleCardClick = (card: any) => {
    console.log('Card clicked:', card);
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        aspectRatio: "1",
        position: "relative",
      }}
    >
      {/* Poker Table Background - replacing ChessGrid */}
      <PokerGrid />

      {/* Card Table Overlay - Glassmorphism effects */}
      <CardTableOverlay />

      {/* Card and Chip Pool - Texas Hold'em Layout */}
      <div className="card-pool" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 2 }}>
        
        {/* Community Cards */}
        <CommunityCards 
          cards={communityCards}
          size="15vw"
          yPosition={30}
          onCardClick={handleCardClick}
        />

        {/* Player Cards */}
        <PlayerCards 
          cards={playerCards}
          size="19vw"
          yPosition={75}
          onCardClick={handleCardClick}
        />
        
        {/* Player Chip Stack (bottom left) */}
        <ChipWrapper
          chip={{
            id: 'player-chip-1',
            value: 500,
            color: '#800080',
            x: 15,
            y: 85
          }}
          size={`calc(${PIECE_SIZE} * 0.7)`}
        />
        <ChipWrapper
          chip={{
            id: 'player-chip-2',
            value: 100,
            color: '#000000',
            x: 15,
            y: 85,
            stackIndex: 1
          }}
          size={`calc(${PIECE_SIZE} * 0.7)`}
        />
        <ChipWrapper
          chip={{
            id: 'player-chip-3',
            value: 25,
            color: '#008000',
            x: 15,
            y: 85,
            stackIndex: 2
          }}
          size={`calc(${PIECE_SIZE} * 0.7)`}
        />

      </div>
    </div>
  );
};