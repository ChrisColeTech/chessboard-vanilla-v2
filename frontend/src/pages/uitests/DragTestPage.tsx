import React, { useState, useEffect } from "react";
import { MobileChessBoard } from "../../components/chess/MobileChessBoard";
import { CapturedPieces } from "../../components/chess/CapturedPieces";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { useChessGameStore } from "../../stores/chessGameStore";
import type { ChessPosition } from "../../types";

export const DragTestPage: React.FC = () => {
  const [selectedSquare, setSelectedSquare] = useState<ChessPosition | null>(null);
  const [validDropTargets, setValidDropTargets] = useState<ChessPosition[]>([]);
  const [moveHandler, setMoveHandler] = useState<
    ((from: ChessPosition, to: ChessPosition) => Promise<boolean>) | null
  >(null);
  
  // Use store for captured pieces
  const capturedPieces = useChessGameStore(state => state.capturedPieces);
  const setCapturedPieces = useChessGameStore(state => state.setCapturedPieces);
  const whiteCapturedPieces = capturedPieces.filter(p => p.color === 'white');
  const blackCapturedPieces = capturedPieces.filter(p => p.color === 'black');

  // Clear captured pieces when page loads
  useEffect(() => {
    setCapturedPieces([]);
  }, [setCapturedPieces]);
  
  const [piecesPosition, setPiecesPosition] = useState<'top-bottom' | 'left-right'>('top-bottom');

  // Expose toggle function globally for actions to use
  React.useEffect(() => {
    (window as any).__togglePiecesPosition = () => {
      setPiecesPosition(prev => {
        const newPosition = prev === 'top-bottom' ? 'left-right' : 'top-bottom'
        return newPosition
      })
    }
    return () => {
      delete (window as any).__togglePiecesPosition
    }
  }, [])

  const handleSquareClick = (position: ChessPosition) => {
    if (selectedSquare === null) {
      setSelectedSquare(position);
      setValidDropTargets([]);
    } else if (selectedSquare === position) {
      setSelectedSquare(null);
      setValidDropTargets([]);
    } else {
      if (moveHandler) {
        moveHandler(selectedSquare, position).then((_success: boolean) => {
          // Move completed
        });
      }
      setSelectedSquare(null);
      setValidDropTargets([]);
    }
  };

  // Use variables to avoid TypeScript unused warnings
  console.log('Debug state:', { piecesPosition, validDropTargets, setMoveHandler, handleSquareClick });

  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={<div className="uitest-layout-corner">Top Left</div>}
        top={<CapturedPieces pieces={blackCapturedPieces} position="normal" />}
        topRight={<div className="uitest-layout-corner">Top Right</div>}
        left={<div className="uitest-layout-corner">Left</div>}
        center={
          <div className="uitest-layout-center">
            <MobileChessBoard gridSize={3} pieceConfig="drag-test" />
          </div>
        }
        right={<div className="uitest-layout-corner">Right</div>}
        bottomLeft={<div className="uitest-layout-corner">Bottom Left</div>}
        bottom={<CapturedPieces pieces={whiteCapturedPieces} position="normal" />}
        bottomRight={<div className="uitest-layout-corner">Bottom Right</div>}
        className="w-full h-full"
      />
    </div>
  );
};