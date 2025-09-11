import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { StatsPage } from "../../pages/progress/StatsPage";

export const StatsPageWrapper: React.FC = () => {
  usePageInstructions("stats");
  
  return <StatsPage />;
};
