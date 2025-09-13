// GameStatusBar.tsx - Game status display following SRP
// Single Responsibility: Display current game status and turn information

import React from 'react';
import type { PieceColor, ComputerDifficulty } from '../../types';

interface GameStatusBarProps {
  /** Current active player */
  currentPlayer: PieceColor;
  /** Whether it's the human player's turn */
  isPlayerTurn: boolean;
  /** Whether the computer is currently thinking */
  isComputerThinking: boolean;
  /** Current computer difficulty level */
  skillLevel: ComputerDifficulty;
  /** Optional game status message */
  statusMessage?: string;
  /** Whether the game is over */
  isGameOver?: boolean;
}

export const GameStatusBar: React.FC<GameStatusBarProps> = ({
  currentPlayer,
  isPlayerTurn,
  isComputerThinking,
  skillLevel,
  statusMessage,
  isGameOver = false
}) => {
  const getStatusMessage = (): string => {
    if (statusMessage) return statusMessage;
    if (isGameOver) return 'Game Over';
    if (isPlayerTurn) return 'Your Turn';
    if (isComputerThinking) return 'Computer Thinking...';
    return 'Computer\'s Turn';
  };

  const getStatusColor = (): string => {
    if (isGameOver) return 'text-destructive';
    if (isPlayerTurn) return 'text-primary';
    if (isComputerThinking) return 'text-primary';
    return 'text-foreground';
  };

  return (
    <div className="bg-card border-b border-border px-2 sm:px-4 py-2">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-4">
        {/* Main status - always visible */}
        <div className="flex items-center gap-2 sm:gap-4 justify-center sm:justify-start">
          <span className={`font-medium text-sm sm:text-base ${getStatusColor()}`}>
            {getStatusMessage()}
          </span>
          
          {isComputerThinking && (
            <div className="flex items-center gap-2 text-primary">
              <div className="animate-spin rounded-full h-3 w-3 sm:h-4 sm:w-4 border-b-2 border-primary"></div>
              <span className="text-xs sm:text-sm">Level {skillLevel}</span>
            </div>
          )}
        </div>
        
        {/* Player info - responsive */}
        <div className="flex items-center justify-center sm:justify-end">
          <span className="text-xs sm:text-sm text-muted-foreground">
            <span className="hidden sm:inline">Playing as </span>
            {currentPlayer === 'white' ? '⚪ White' : '⚫ Black'}
          </span>
        </div>
      </div>
    </div>
  );
};