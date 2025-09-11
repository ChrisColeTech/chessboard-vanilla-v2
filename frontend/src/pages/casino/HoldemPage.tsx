import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { MobilePokerTable } from "../../components/casino/holdem/MobilePokerTable";

export const HoldemPage: React.FC = () => {
  usePageInstructions("holdem");
  
  return (
    <div className="relative min-h-full">
      {/* Background Effects */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="bg-sparkle bg-sparkle-lg bg-orb-primary-30 top-1/4 left-1/4 animation-delay-300"></div>
        <div className="bg-sparkle bg-sparkle-sm bg-orb-accent-40 bottom-1/3 left-1/3 animation-delay-700"></div>
        <div className="bg-sparkle bg-sparkle-md bg-orb-foreground-50 top-2/3 right-1/3 animation-delay-1200"></div>
      </div>

      {/* Mobile Layout fills entire page - Now using mobile poker table */}
      <MobileChessboardLayout
        topPieces={
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            Top Area
          </div>
        }
        center={
          <MobilePokerTable 
            gridSize={4}
          />
        }
        bottomPieces={
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            Bottom Area
          </div>
        }
      />
    </div>
  );
};