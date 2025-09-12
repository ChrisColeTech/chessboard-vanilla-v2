import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileAnalyticsPage } from "../../pages/progress/MobileAnalyticsPage";

export const MobileAnalyticsPageWrapper = () => {
  usePageInstructions("analytics");
  
  return <MobileAnalyticsPage />;
};
