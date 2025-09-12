import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileProgressFeaturePage } from "../../pages/progress/MobileProgressFeaturePage";

export const MobileProgressFeaturePageWrapper = () => {
  usePageInstructions("progress");
  
  return <MobileProgressFeaturePage />;
};
