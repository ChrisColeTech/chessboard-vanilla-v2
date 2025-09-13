// /src/pages/PlayPuzzlesPage.tsx - Professional chess puzzle gameplay with dual layouts
import React, { useEffect } from "react";
import { MobileChessBoard } from "../../components/chess/MobileChessBoard";
import { CapturedPieces } from "../../components/chess/CapturedPieces";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { useInstructions } from "../../contexts/InstructionsContext";
import { useChessGameStore } from "../../stores/chessGameStore";
import { usePuzzleService } from "../../hooks/puzzle/usePuzzleService";
import { usePuzzleStore, useCurrentHint } from "../../stores/puzzleStore";
import { updatePuzzleConfiguration } from "../../utils/puzzle.utils";
import { usePlayActions } from "../../hooks/chess/usePlayActions";

export const PlayPuzzlesPage: React.FC = () => {
  // Use store for captured pieces
  const capturedPieces = useChessGameStore(state => state.capturedPieces);
  const setCapturedPieces = useChessGameStore(state => state.setCapturedPieces);
  const whiteCapturedPieces = capturedPieces.filter(p => p.color === 'white');
  const blackCapturedPieces = capturedPieces.filter(p => p.color === 'black');

  // Mobile responsive hook
  const isMobile = useIsMobile();

  // Instructions context for hints
  const { setInstructions } = useInstructions();

  // Puzzle service and state
  const { loadRandomPuzzle } = usePuzzleService();
  const { currentPuzzle, isLoading, error, setCurrentHint } = usePuzzleStore();
  const currentHint = useCurrentHint();
  
  // Actions (hint is available but not used in this component)
  const { hint: _hint } = usePlayActions();

  // Load initial puzzle and clear captured pieces when page loads
  useEffect(() => {
    setCapturedPieces([]);
    setCurrentHint(null);
    loadRandomPuzzle();
    console.log('🧩 [PUZZLES] Loading initial puzzle...');
  }, [setCapturedPieces, setCurrentHint, loadRandomPuzzle]);

  // Update puzzle configuration when puzzle changes
  useEffect(() => {
    if (currentPuzzle && currentPuzzle.fen) {
      console.log('🧩 [PUZZLES] Current puzzle loaded:', {
        id: currentPuzzle.id,
        fen: currentPuzzle.fen,
        rating: currentPuzzle.rating,
        themes: currentPuzzle.themes,
        solution: currentPuzzle.solution_moves
      });
      
      // Clear any existing hint when new puzzle loads
      setCurrentHint(null);
      
      // Update the global puzzle configuration with the new FEN
      updatePuzzleConfiguration(currentPuzzle.fen);
    }
  }, [currentPuzzle, setCurrentHint]);

  // Set dynamic instructions based on hint state
  useEffect(() => {
    if (currentHint) {
      setInstructions("💡 Puzzle Hint", [
        `Next move: ${currentHint}`,
        "This is the next move in the solution sequence",
        "Make this move on the board to continue"
      ]);
    } else {
      setInstructions("🧩 Puzzle Mode", [
        "Solve chess puzzles to improve your skills",
        "Use the action menu to get hints or skip puzzles", 
        "Complete the puzzle by making the correct moves",
        "Click 'Got it!' to close this dialog"
      ]);
    }
  }, [currentHint, setInstructions]);

  // Show loading state
  if (isLoading && !currentPuzzle) {
    return (
      <div className="relative min-h-full flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🧩</div>
          <p className="text-lg">Loading puzzle...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (error && !currentPuzzle) {
    return (
      <div className="relative min-h-full flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">❌</div>
          <p className="text-lg text-red-500">Error loading puzzle: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-full">
      {/* Mobile Layout */}
      {isMobile ? (
        <MobileChessboardLayout
          topPieces={
            <CapturedPieces
              pieces={whiteCapturedPieces}
              position="normal"
            />
          }
          center={<MobileChessBoard gridSize={8} pieceConfig="puzzle" />}
          bottomPieces={
            <CapturedPieces
              pieces={blackCapturedPieces}
              position="normal"
            />
          }
        />
      ) : (
        /* Desktop Layout */
        <ChessboardLayout
          top={
            <CapturedPieces
              pieces={whiteCapturedPieces}
              position="normal"
            />
          }
          center={
            <div style={{
              width: "100%",
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              minHeight: "0",
              minWidth: "0",
              overflow: "hidden"
            }}>
              <MobileChessBoard gridSize={8} pieceConfig="puzzle" />
            </div>
          }
          bottom={
            <CapturedPieces
              pieces={blackCapturedPieces}
              position="normal"
            />
          }
          className="h-full"
        />
      )}
    </div>
  );
};