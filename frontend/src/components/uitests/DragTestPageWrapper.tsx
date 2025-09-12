import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { DragTestPage } from "../../pages/uitests/DragTestPage";
import { MobileDragTestPage } from "../../pages/uitests/MobileDragTestPage";

export const DragTestPageWrapper: React.FC = () => {
  const isMobile = useIsMobile();
  
  usePageInstructions("dragtest");
  usePageActions("dragtest");

  return isMobile ? <MobileDragTestPage /> : <DragTestPage />;
};
