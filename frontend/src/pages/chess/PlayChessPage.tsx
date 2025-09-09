// /src/pages/PlayPage.tsx - Professional chess gameplay with dual layouts
import React, { useEffect } from "react";
import { MobileChessBoard } from "../../components/chess/MobileChessBoard";
import { CapturedPieces } from "../../components/chess/CapturedPieces";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { useChessGameStore } from "../../stores/chessGameStore";

export const PlayChessPage: React.FC = () => {
  usePageInstructions("playchess");
  
  // Use store for captured pieces
  const capturedPieces = useChessGameStore(state => state.capturedPieces);
  const setCapturedPieces = useChessGameStore(state => state.setCapturedPieces);
  const whiteCapturedPieces = capturedPieces.filter(p => p.color === 'white');
  const blackCapturedPieces = capturedPieces.filter(p => p.color === 'black');

  // Mobile responsive hook
  const isMobile = useIsMobile();

  // Clear captured pieces when page loads
  useEffect(() => {
    setCapturedPieces([]);
  }, [setCapturedPieces]);

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
          center={<MobileChessBoard gridSize={8} pieceConfig="standard-chess" />}
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
              <MobileChessBoard gridSize={8} pieceConfig="standard-chess" />
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
