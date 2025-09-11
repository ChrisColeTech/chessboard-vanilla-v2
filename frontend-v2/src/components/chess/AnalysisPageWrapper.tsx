import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AnalysisPage } from "../../pages/chess/AnalysisPage";

export const AnalysisPageWrapper: React.FC = () => {
  usePageInstructions("analysis");
  
  return <AnalysisPage />;
};
