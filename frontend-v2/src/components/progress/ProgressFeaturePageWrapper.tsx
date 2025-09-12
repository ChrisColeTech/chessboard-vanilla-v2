import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { ProgressFeaturePage } from "../../pages/progress/ProgressFeaturePage";

export const ProgressFeaturePageWrapper = () => {
  usePageInstructions("progress");
  
  return <ProgressFeaturePage />;
};
