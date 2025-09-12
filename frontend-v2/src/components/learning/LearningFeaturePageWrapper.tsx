import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { LearningFeaturePage } from "../../pages/learning/LearningFeaturePage";

export const LearningFeaturePageWrapper = () => {
  usePageInstructions("learning");
  
  return <LearningFeaturePage />;
};
