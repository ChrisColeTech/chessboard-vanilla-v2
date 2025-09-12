import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileStatsPage } from "../../pages/progress/MobileStatsPage";

export const MobileStatsPageWrapper = () => {
  usePageInstructions("stats");
  
  return <MobileStatsPage />;
};
