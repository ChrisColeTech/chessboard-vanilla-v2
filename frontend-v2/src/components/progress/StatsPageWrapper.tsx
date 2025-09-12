import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { StatsPage } from "../../pages/progress/StatsPage";

export const StatsPageWrapper = () => {
  usePageInstructions("stats");
  
  return <StatsPage />;
};
