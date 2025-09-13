// PlayChessPage.tsx - Human vs Computer chess gameplay orchestrator
// Following SRP: Orchestrates components, delegates business logic to services

import React, { useEffect, useCallback, useState } from "react";
import { MobileChessBoard } from "../../components/chess/MobileChessBoard";
import { CapturedPieces } from "../../components/chess/CapturedPieces";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { 
  GameStatusBar,
  GameControls, 
  DifficultySelector,
  LoadingState,
  ErrorState,
  GameResultModal
} from "../../components/play";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { usePlayGame } from "../../hooks/chess/usePlayGame";
import { useChessGameStore } from "../../stores/chessGameStore";
import type { PieceColor } from "../../types";

export const PlayChessPage: React.FC = () => {
  usePageInstructions("playchess");
  
  // Production chess game state with real validation
  const {
    gameState,
    isLoading,
    error,
    isComputerThinking,
    skillLevel,
    isPlayerTurn,
    updateSkillLevel,
    resetGame,
    getPlayGameState
  } = usePlayGame('white');

  // Visual state management
  const { 
    capturedPieces, 
    setCapturedPieces
  } = useChessGameStore();

  // UI state
  const [showDifficultySelector, setShowDifficultySelector] = useState(false);
  const isMobile = useIsMobile();

  // Separate captured pieces by color for display
  const whiteCapturedPieces = capturedPieces.filter(p => p.color === 'white');
  const blackCapturedPieces = capturedPieces.filter(p => p.color === 'black');

  // Clear captured pieces when page loads
  useEffect(() => {
    setCapturedPieces([]);
  }, [setCapturedPieces]);




  // Game controls handlers
  const handleNewGame = useCallback(() => {
    resetGame('white');
    setShowDifficultySelector(false);
  }, [resetGame]);

  const handleFlipBoard = useCallback(() => {
    const playState = getPlayGameState();
    const newPlayerColor: PieceColor = playState?.playerColor === 'white' ? 'black' : 'white';
    resetGame(newPlayerColor);
  }, [resetGame, getPlayGameState]);

  const handleDifficultyChange = useCallback(async (level: number) => {
    if (level >= 1 && level <= 10) {
      await updateSkillLevel(level as any);
    }
  }, [updateSkillLevel]);

  // Loading state
  if (isLoading) {
    return (
      <LoadingState 
        message="Initializing chess engine..."
        details="Setting up Stockfish AI opponent"
      />
    );
  }

  // Error state with recovery
  if (error) {
    return (
      <ErrorState
        message="Chess engine initialization failed"
        details={error}
        onRetry={handleNewGame}
        critical={true}
      />
    );
  }

  // Get current play state for display
  const playState = getPlayGameState();

  return (
    <div className="relative h-full flex flex-col">
      {/* Top Section - Game Status & Controls (pinned to top) */}
      <div className="flex-shrink-0">
        {/* Game Status Bar */}
        <GameStatusBar
          currentPlayer={playState?.currentPlayer || 'white'}
          isPlayerTurn={isPlayerTurn}
          isComputerThinking={isComputerThinking}
          skillLevel={skillLevel}
          isGameOver={gameState?.isGameOver}
        />

        {/* Game Controls Bar */}
        <div className="bg-card border-b border-border px-2 sm:px-4 py-2">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <GameControls
              onNewGame={handleNewGame}
              onFlipBoard={handleFlipBoard}
              disabled={isComputerThinking}
              isGameActive={!gameState?.isGameOver}
              playerColor={playState?.playerColor}
            />
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowDifficultySelector(!showDifficultySelector)}
                className="text-xs sm:text-sm bg-primary text-primary-foreground px-2 sm:px-3 py-1 rounded hover:bg-primary/90 transition-colors disabled:opacity-50"
                disabled={isComputerThinking}
              >
                AI Level {skillLevel}
              </button>
            </div>
          </div>
        </div>

        {/* Difficulty Selector */}
        {showDifficultySelector && (
          <DifficultySelector
            currentLevel={skillLevel}
            onLevelChange={handleDifficultyChange}
            disabled={isComputerThinking}
            showDescriptions={!isMobile}
          />
        )}
      </div>

      {/* Game Board - Takes remaining space between top and bottom following AuthLayout pattern */}
      <div className="flex-1 flex flex-col py-4 px-4 relative">
        {isMobile ? (
          <div className="flex-1 flex items-stretch justify-center">
            <div className="w-full flex flex-col">
              <div className="flex-1 flex flex-col justify-center items-center">
                <MobileChessboardLayout
                  topPieces={
                    <CapturedPieces
                      pieces={blackCapturedPieces}
                      position="normal"
                    />
                  }
                  center={
                    <MobileChessBoard 
                      gridSize={8} 
                      pieceConfig="standard-chess"
                    />
                  }
                  bottomPieces={
                    <CapturedPieces
                      pieces={whiteCapturedPieces}
                      position="normal"
                    />
                  }
                  className="w-full h-full"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-stretch justify-center">
            <div className="w-full max-w-6xl flex flex-col">
              <div className="flex-1 flex flex-col justify-center items-center">
                <ChessboardLayout
                  top={
                    <CapturedPieces
                      pieces={blackCapturedPieces}
                      position="normal"
                    />
                  }
                  center={
                    <div className="w-full h-full flex items-center justify-center min-h-0 min-w-0 overflow-hidden">
                      <MobileChessBoard 
                        gridSize={8} 
                        pieceConfig="standard-chess"
                      />
                    </div>
                  }
                  bottom={
                    <CapturedPieces
                      pieces={whiteCapturedPieces}
                      position="normal"
                    />
                  }
                  className="w-full h-full"
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Game Result Modal */}
      {gameState?.isGameOver && (
        <GameResultModal
          isOpen={true}
          resultType={
            gameState.isCheckmate ? 'checkmate' :
            gameState.isStalemate ? 'stalemate' :
            gameState.isDraw ? 'draw' : 'draw'
          }
          humanWon={
            gameState.isCheckmate 
              ? (playState?.currentPlayer !== playState?.playerColor) 
              : false
          }
          onNewGame={handleNewGame}
          gameStats={{
            moves: gameState.history?.length || 0,
            duration: '0:00', // TODO: Add duration tracking
            difficulty: skillLevel
          }}
        />
      )}
    </div>
  );
};
