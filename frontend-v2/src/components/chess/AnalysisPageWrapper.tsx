import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AnalysisPage } from "../../pages/chess/AnalysisPage";

export const AnalysisPageWrapper = () => {
  usePageInstructions("analysis");
  
  return <AnalysisPage />;
};
