import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { LearningFeaturePage } from "../../pages/learning/LearningFeaturePage";

export const LearningFeaturePageWrapper: React.FC = () => {
  usePageInstructions("learning");
  
  return <LearningFeaturePage />;
};
