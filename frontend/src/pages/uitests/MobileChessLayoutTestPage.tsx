import React, { useEffect } from "react";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { MobileChessBoard } from "../../components/chess/MobileChessBoard";
import { CapturedPieces } from "../../components/chess/CapturedPieces";
import { useChessGameStore } from "../../stores/chessGameStore";

interface MobileChessLayoutTestPageProps {
  // Add mobile-specific props as needed
}

export const MobileChessLayoutTestPage: React.FC<MobileChessLayoutTestPageProps> = () => {
  
  // Use store for captured pieces
  const capturedPieces = useChessGameStore(state => state.capturedPieces);
  const setCapturedPieces = useChessGameStore(state => state.setCapturedPieces);
  const whiteCaptured = capturedPieces.filter(p => p.color === 'white');
  const blackCaptured = capturedPieces.filter(p => p.color === 'black');

  // Clear captured pieces when page loads
  useEffect(() => {
    setCapturedPieces([]);
  }, [setCapturedPieces]);

  return (
    <div className="uitest-mobile-container">
      <MobileChessboardLayout
        topPieces={<CapturedPieces pieces={blackCaptured} position="normal" />}
        center={
          <div className="uitest-mobile-center">
            <MobileChessBoard gridSize={3} pieceConfig="mobile-test" />
          </div>
        }
        bottomPieces={<CapturedPieces pieces={whiteCaptured} position="normal" />}
      />
    </div>
  );
};
