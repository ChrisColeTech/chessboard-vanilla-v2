import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { MobileDragTestPage } from "../../pages/uitests/MobileDragTestPage";

export const MobileDragTestPageWrapper: React.FC = () => {
  usePageInstructions("mobiledragtest");  // Loads instructions for this page
  usePageActions("mobiledragtest");       // Sets action context for action sheet
  
  return <MobileDragTestPage />;
};