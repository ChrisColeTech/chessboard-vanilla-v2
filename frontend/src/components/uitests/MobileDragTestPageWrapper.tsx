import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { MobileDragTestPage } from "../../pages/uitests/MobileDragTestPage";

export const MobileDragTestPageWrapper: React.FC = () => {
  usePageInstructions("dragtest");  // Shared instructions with desktop version
  usePageActions("dragtest");       // Shared actions with desktop version
  
  return <MobileDragTestPage />;
};