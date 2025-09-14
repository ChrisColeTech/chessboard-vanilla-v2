// GameResultModal.tsx - Game result modal following SRP
// Single Responsibility: Display game end results and next actions

import React from 'react';
import type { PieceColor } from '../../types';

interface GameResultModalProps {
  /** Whether the modal is visible */
  isOpen: boolean;
  /** Type of game result */
  resultType: 'checkmate' | 'stalemate' | 'draw' | 'resignation' | 'timeout';
  /** Winner of the game, if any */
  winner?: PieceColor;
  /** Whether the human player won */
  humanWon?: boolean;
  /** Custom result message */
  customMessage?: string;
  /** Handler for new game action */
  onNewGame: () => void;
  /** Handler for close modal action */
  onClose?: () => void;
  /** Optional game statistics */
  gameStats?: {
    moves: number;
    duration: string;
    difficulty: number;
  };
}

const GameResultModal: React.FC<GameResultModalProps> = ({
  isOpen,
  resultType,
  winner: _winner,
  humanWon,
  customMessage,
  onNewGame,
  onClose,
  gameStats
}) => {
  if (!isOpen) return null;

  const getResultMessage = (): string => {
    if (customMessage) return customMessage;
    
    switch (resultType) {
      case 'checkmate':
        if (humanWon) return '🎉 Congratulations! You won by checkmate!';
        return '💻 Computer wins by checkmate!';
      case 'stalemate':
        return '🤝 Game drawn by stalemate';
      case 'draw':
        return '🤝 Game drawn';
      case 'resignation':
        if (humanWon) return '🎉 Computer resigned - You win!';
        return '🏳️ You resigned - Computer wins';
      case 'timeout':
        return '⏰ Game ended due to timeout';
      default:
        return 'Game Over';
    }
  };

  const getResultColor = (): string => {
    if (resultType === 'draw' || resultType === 'stalemate') return 'text-blue-600';
    return humanWon ? 'text-green-600' : 'text-red-600';
  };

  const getResultIcon = (): string => {
    if (resultType === 'draw' || resultType === 'stalemate') return '🤝';
    return humanWon ? '🏆' : '💻';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-card rounded-lg shadow-xl max-w-sm w-full mx-auto">
        {/* Header */}
        <div className="p-4 sm:p-6 text-center border-b border-border">
          <div className="text-4xl sm:text-5xl mb-2">
            {getResultIcon()}
          </div>
          <h2 className="text-lg sm:text-xl font-bold text-foreground mb-2">
            Game Over
          </h2>
          <p className={`text-sm sm:text-base font-medium ${getResultColor()}`}>
            {getResultMessage()}
          </p>
        </div>
        
        {/* Game statistics */}
        {gameStats && (
          <div className="px-4 sm:px-6 py-3 bg-muted border-b border-border">
            <div className="grid grid-cols-3 gap-2 text-center text-xs sm:text-sm">
              <div>
                <div className="text-muted-foreground">Moves</div>
                <div className="font-medium">{gameStats.moves}</div>
              </div>
              <div>
                <div className="text-muted-foreground">Duration</div>
                <div className="font-medium">{gameStats.duration}</div>
              </div>
              <div>
                <div className="text-muted-foreground">AI Level</div>
                <div className="font-medium">{gameStats.difficulty}</div>
              </div>
            </div>
          </div>
        )}
        
        {/* Actions */}
        <div className="p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
            <button
              onClick={onNewGame}
              className="flex-1 bg-primary text-primary-foreground px-4 py-2 rounded font-medium hover:bg-primary/90 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50"
            >
              🔄 New Game
            </button>
            
            {onClose && (
              <button
                onClick={onClose}
                className="flex-1 sm:flex-none bg-secondary text-secondary-foreground px-4 py-2 rounded font-medium hover:bg-secondary/90 transition-colors focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-opacity-50"
              >
                Close
              </button>
            )}
          </div>
          
          {/* Additional info for first-time users */}
          {humanWon && (
            <p className="text-xs text-muted-foreground text-center mt-3">
              💡 Try increasing the difficulty level for a bigger challenge!
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default GameResultModal;
export { GameResultModal };
