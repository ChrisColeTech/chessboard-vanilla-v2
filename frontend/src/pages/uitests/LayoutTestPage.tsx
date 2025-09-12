import React from "react";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";

export const LayoutTestPage: React.FC = () => {

  
  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={<div className="uitest-layout-corner">Top Left</div>}
        top={<div className="uitest-layout-center"></div>}
        topRight={<div className="uitest-layout-corner">Top Right</div>}
        left={<div className="uitest-layout-corner">Left</div>}
        center={<div className="uitest-layout-center"></div>}
        right={<div className="uitest-layout-corner">Right</div>}
        bottomLeft={<div className="uitest-layout-corner">Bottom Left</div>}
        bottom={<div className="uitest-layout-center"></div>}
        bottomRight={<div className="uitest-layout-corner">Bottom Right</div>}
        className="w-full h-full"
      />
    </div>
  );
};