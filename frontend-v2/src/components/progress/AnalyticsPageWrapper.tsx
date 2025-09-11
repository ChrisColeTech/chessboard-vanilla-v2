import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AnalyticsPage } from "../../pages/progress/AnalyticsPage";

export const AnalyticsPageWrapper: React.FC = () => {
  usePageInstructions("analytics");
  
  return <AnalyticsPage />;
};
