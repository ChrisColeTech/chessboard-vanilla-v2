import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileAnalysisPage } from "../../pages/chess/MobileAnalysisPage";

export const MobileAnalysisPageWrapper = () => {
  usePageInstructions("analysis");
  
  return <MobileAnalysisPage />;
};
