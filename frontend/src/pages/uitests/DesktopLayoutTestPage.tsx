import React, { useState } from 'react';
import { ChessboardLayout } from '../../components/chess/ChessboardLayout';
import { MobileChessBoard } from '../../components/chess/MobileChessBoard';
import { CapturedPieces } from '../../components/chess/CapturedPieces';

export const DesktopLayoutTestPage: React.FC = () => {
  const [showElements, setShowElements] = useState(true);

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
    <div className="relative h-full flex flex-col">
      {/* Test Header */}
      <div className="flex-shrink-0 bg-card border-b border-border px-4 py-2">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold text-foreground">Desktop Layout Test</h1>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowElements(!showElements)}
              className="text-xs bg-primary text-primary-foreground px-3 py-1 rounded hover:bg-primary/90 transition-colors"
            >
              {showElements ? 'Hide' : 'Show'} Elements
            </button>
          </div>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          Testing desktop chess layout with AuthLayout pinning pattern
        </p>
      </div>

      {/* Desktop Chess Layout Test - Following AuthLayout pattern */}
      <div className="flex-1 flex flex-col py-4 px-4 relative">
        <div className="flex-1 flex items-stretch justify-center">
          <div className="w-full max-w-6xl flex flex-col">
            <div className="flex-1 flex flex-col justify-center items-center">
              <ChessboardLayout
                topLeft={showElements ? <div className="text-xs text-muted-foreground p-2">Top Left</div> : undefined}
                top={showElements ? <CapturedPieces pieces={blackCaptured} position="normal" /> : undefined}
                topRight={showElements ? <div className="text-xs text-muted-foreground p-2">Top Right</div> : undefined}
                left={showElements ? <div className="text-xs text-muted-foreground p-2">Left</div> : undefined}
                center={
                  <div className="w-full h-full flex items-center justify-center min-h-0 min-w-0 overflow-hidden">
                    <MobileChessBoard 
                      gridSize={8} 
                      pieceConfig="standard-chess"
                    />
                  </div>
                }
                right={showElements ? <div className="text-xs text-muted-foreground p-2">Right</div> : undefined}
                bottomLeft={showElements ? <div className="text-xs text-muted-foreground p-2">Bottom Left</div> : undefined}
                bottom={showElements ? <CapturedPieces pieces={whiteCaptured} position="normal" /> : undefined}
                bottomRight={showElements ? <div className="text-xs text-muted-foreground p-2">Bottom Right</div> : undefined}
                className="w-full h-full"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Layout Info Panel */}
      <div className="flex-shrink-0 bg-muted border-t border-border px-4 py-2">
        <div className="text-xs text-muted-foreground">
          <strong>Layout Structure:</strong> flex-1 → flex items-stretch justify-center → max-w-6xl flex-col → flex-1 flex-col justify-center items-center
        </div>
        <div className="text-xs text-muted-foreground mt-1">
          <strong>Pattern:</strong> AuthLayout three-layer nesting with proper pinning between header and tabbar
        </div>
      </div>
    </div>
  );
};