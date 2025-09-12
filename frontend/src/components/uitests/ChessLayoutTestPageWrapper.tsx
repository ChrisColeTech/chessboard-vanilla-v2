import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { ChessLayoutTestPage } from "../../pages/uitests/ChessLayoutTestPage";
import { MobileChessLayoutTestPage } from "../../pages/uitests/MobileChessLayoutTestPage";

export const ChessLayoutTestPageWrapper: React.FC = () => {
  const isMobile = useIsMobile();
  
  usePageInstructions("chesslayouttest");
  usePageActions("chesslayouttest");

  return isMobile ? <MobileChessLayoutTestPage /> : <ChessLayoutTestPage />;
};
