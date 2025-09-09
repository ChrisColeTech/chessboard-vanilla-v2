import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { DragTestPage } from "../../pages/uitests/DragTestPage";

export const DragTestPageWrapper: React.FC = () => {
  usePageInstructions("dragtest");
  usePageActions("dragtest");

  return <DragTestPage />;
};
