import React, { useState, useEffect } from "react";
import {
  MobileChessboardLayout,
  CapturedPieces,
  MobileChessBoard,
} from "../../components/chess";
import { useMobileDragTestActions } from "../../hooks/uitests/useMobileDragTestActions";
import { useChessGameStore } from "../../stores/chessGameStore";
import type { MobileChessGameState } from "../../types";

export const MobileDragTestPage: React.FC = () => {
  // Setup actions (handled by wrapper for page instructions and action sheet context)
  useMobileDragTestActions();
  
  const [gameState, setGameState] = useState<MobileChessGameState | null>(null);

  // Use store for captured pieces instead of local state
  const capturedPieces = useChessGameStore(state => state.capturedPieces);
  const setCapturedPieces = useChessGameStore(state => state.setCapturedPieces);
  const whiteCaptured = capturedPieces.filter(p => p.color === 'white');
  const blackCaptured = capturedPieces.filter(p => p.color === 'black');

  // Clear captured pieces when page loads
  useEffect(() => {
    setCapturedPieces([]);
  }, [setCapturedPieces]);

  const handleGameStateChange = (newGameState: MobileChessGameState) => {
    setGameState(newGameState);
    console.log('🎮 [MOBILE DRAG TEST] Game state updated:', {
      isCheck: newGameState.isCheck,
      isCheckmate: newGameState.isCheckmate,
      activeColor: newGameState.activeColor
    });
  };

  return (
    <div className="relative min-h-full">
      {/* Background Effects */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="bg-sparkle bg-sparkle-lg bg-orb-foreground-30 top-1/4 left-1/4 animation-delay-300"></div>
        <div className="bg-sparkle bg-sparkle-sm bg-orb-foreground-40 bottom-1/3 left-1/3 animation-delay-700"></div>
        <div className="bg-sparkle bg-sparkle-md bg-orb-foreground-50 top-2/3 right-1/3 animation-delay-1200"></div>
      </div>

      {/* Mobile Layout fills entire page */}
      <MobileChessboardLayout
        topPieces={
          <CapturedPieces
            pieces={blackCaptured}
            position="normal"
          />
        }
        center={
          <MobileChessBoard 
            gridSize={4}
            pieceConfig="mobile-test"
            onGameStateChange={handleGameStateChange}
          />
        }
        bottomPieces={
          <CapturedPieces
            pieces={whiteCaptured}
            position="normal"
          />
        }
      />
      
      {/* Game Status Display - Only critical game states */}
      {gameState?.isCheckmate && (
        <div className="absolute top-4 left-4 bg-red-800/90 text-white px-3 py-1 rounded text-sm font-medium animate-pulse">
          CHECKMATE!
        </div>
      )}
      
    </div>
  );
};
