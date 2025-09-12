import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileLearningFeaturePage } from "../../pages/learning/MobileLearningFeaturePage";

export const MobileLearningFeaturePageWrapper = () => {
  usePageInstructions("learning");
  
  return <MobileLearningFeaturePage />;
};
