import React from "react";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";

export const MobileLayoutTestPage: React.FC = () => {
  return (
    <div className="uitest-mobile-container-padded">
      <MobileChessboardLayout
        topPieces={<div className="uitest-mobile-pieces">Top Pieces Area</div>}
        center={
          <div className="uitest-mobile-center-card">
            <span className="text-muted-foreground">Mobile Layout Test Center</span>
          </div>
        }
        bottomPieces={<div className="uitest-mobile-pieces">Bottom Pieces Area</div>}
      />
    </div>
  );
};