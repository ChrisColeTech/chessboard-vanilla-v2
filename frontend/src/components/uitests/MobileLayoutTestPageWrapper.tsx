import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { MobileLayoutTestPage } from "../../pages/uitests/MobileLayoutTestPage";

export const MobileLayoutTestPageWrapper: React.FC = () => {
  usePageInstructions("layouttest");  // Shared instructions with desktop version
  usePageActions("layouttest");       // Shared actions with desktop version

  return <MobileLayoutTestPage />;
};