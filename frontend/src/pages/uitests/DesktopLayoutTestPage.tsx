import React, { useState, useEffect } from 'react';
import { ChessboardLayout } from '../../components/chess/ChessboardLayout';
import { MobileChessBoard } from '../../components/chess/MobileChessBoard';
import { CapturedPieces } from '../../components/chess/CapturedPieces';

export const DesktopLayoutTestPage: React.FC = () => {
  const [showElements, setShowElements] = useState(true);

  // Listen for toggle events from the action sheet
  useEffect(() => {
    const handleToggle = () => {
      setShowElements(prev => !prev);
    };

    window.addEventListener('desktop-layout-toggle-elements', handleToggle);
    
    return () => {
      window.removeEventListener('desktop-layout-toggle-elements', handleToggle);
    };
  }, []);

  // Mock captured pieces for testing
  const mockCapturedPieces = [
    { id: 'black-pawn-1', type: 'pawn' as const, color: 'black' as const, position: { file: 'a' as const, rank: 1 as const } },
    { id: 'black-knight-1', type: 'knight' as const, color: 'black' as const, position: { file: 'b' as const, rank: 1 as const } },
    { id: 'white-bishop-1', type: 'bishop' as const, color: 'white' as const, position: { file: 'c' as const, rank: 1 as const } },
    { id: 'white-rook-1', type: 'rook' as const, color: 'white' as const, position: { file: 'd' as const, rank: 1 as const } },
  ];

  const whiteCaptured = mockCapturedPieces.filter(p => p.color === 'white');
  const blackCaptured = mockCapturedPieces.filter(p => p.color === 'black');

  return (
      <div className="h-full">
        <ChessboardLayout
          topLeft={
            showElements ? (
              <div className="text-xs text-muted-foreground p-2">Top Left</div>
            ) : undefined
          }
          top={
            showElements ? (
              <CapturedPieces pieces={blackCaptured} position="normal" />
            ) : undefined
          }
          topRight={
            showElements ? (
              <div className="text-xs text-muted-foreground p-2">Top Right</div>
            ) : undefined
          }
          left={
            showElements ? (
              <div className="text-xs text-muted-foreground p-2">Left</div>
            ) : undefined
          }
          center={
            <div className="w-full h-full flex items-center justify-center min-h-0 min-w-0 overflow-hidden">
              <MobileChessBoard gridSize={8} pieceConfig="standard-chess" />
            </div>
          }
          right={
            showElements ? (
              <div className="text-xs text-muted-foreground p-2">Right</div>
            ) : undefined
          }
          bottomLeft={
            showElements ? (
              <div className="text-xs text-muted-foreground p-2">
                Bottom Left
              </div>
            ) : undefined
          }
          bottom={
            showElements ? (
              <CapturedPieces pieces={whiteCaptured} position="normal" />
            ) : undefined
          }
          bottomRight={
            showElements ? (
              <div className="text-xs text-muted-foreground p-2">
                Bottom Right
              </div>
            ) : undefined
          }
          className="w-full h-full"
        />
      </div>
  );
};