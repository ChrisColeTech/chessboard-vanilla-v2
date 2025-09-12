import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AchievementsPage } from "../../pages/progress/AchievementsPage";

export const AchievementsPageWrapper = () => {
  usePageInstructions("achievements");
  
  return <AchievementsPage />;
};
