import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { LayoutTestPage } from "../../pages/uitests/LayoutTestPage";
import { MobileLayoutTestPage } from "../../pages/uitests/MobileLayoutTestPage";

export const LayoutTestPageWrapper: React.FC = () => {
  const isMobile = useIsMobile();
  
  usePageInstructions("layouttest");
  usePageActions("layouttest");

  return isMobile ? <MobileLayoutTestPage /> : <LayoutTestPage />;
};
