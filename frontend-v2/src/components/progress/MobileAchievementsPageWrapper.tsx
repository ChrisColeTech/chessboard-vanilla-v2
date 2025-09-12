import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileAchievementsPage } from "../../pages/progress/MobileAchievementsPage";

export const MobileAchievementsPageWrapper = () => {
  usePageInstructions("achievements");
  
  return <MobileAchievementsPage />;
};
