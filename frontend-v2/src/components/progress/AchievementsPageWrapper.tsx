import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AchievementsPage } from "../../pages/progress/AchievementsPage";

export const AchievementsPageWrapper: React.FC = () => {
  usePageInstructions("achievements");
  
  return <AchievementsPage />;
};
