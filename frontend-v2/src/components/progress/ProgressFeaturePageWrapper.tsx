import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { ProgressFeaturePage } from "../../pages/progress/ProgressFeaturePage";

export const ProgressFeaturePageWrapper: React.FC = () => {
  usePageInstructions("progress");
  
  return <ProgressFeaturePage />;
};
