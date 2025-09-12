import React, { useEffect } from "react";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { MobileChessBoard } from "../../components/chess/MobileChessBoard";
import { CapturedPieces } from "../../components/chess/CapturedPieces";
import { useChessGameStore } from "../../stores/chessGameStore";

export const ChessLayoutTestPage: React.FC = () => {
  
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
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={<div className="uitest-layout-corner">Chess Top Left</div>}
        top={<CapturedPieces pieces={blackCaptured} position="normal" />}
        topRight={<div className="uitest-layout-corner">Chess Top Right</div>}
        left={<div className="uitest-layout-corner">Chess Left</div>}
        center={
          <div className="uitest-layout-center">
            <MobileChessBoard gridSize={3} pieceConfig="standard-chess" />
          </div>
        }
        right={<div className="uitest-layout-corner">Chess Right</div>}
        bottomLeft={<div className="uitest-layout-corner">Chess Bottom Left</div>}
        bottom={<CapturedPieces pieces={whiteCaptured} position="normal" />}
        bottomRight={<div className="uitest-layout-corner">Chess Bottom Right</div>}
        className="w-full h-full"
      />
    </div>
  );
};