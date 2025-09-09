import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { LayoutTestPage } from "../../pages/uitests/LayoutTestPage";

export const LayoutTestPageWrapper: React.FC = () => {
  usePageInstructions("layout");
  usePageActions("layouttest");

  return <LayoutTestPage />;
};