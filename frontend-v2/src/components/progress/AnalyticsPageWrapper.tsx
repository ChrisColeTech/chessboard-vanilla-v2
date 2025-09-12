import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AnalyticsPage } from "../../pages/progress/AnalyticsPage";

export const AnalyticsPageWrapper = () => {
  usePageInstructions("analytics");
  
  return <AnalyticsPage />;
};
