import { useAppStore } from "../../stores/appStore";
import { ProgressMainPage } from "./ProgressMainPage";
import { StatsPageWrapper } from "../../components/progress/StatsPageWrapper";
import { AchievementsPageWrapper } from "../../components/progress/AchievementsPageWrapper";
import { ProgressFeaturePageWrapper } from "../../components/progress/ProgressFeaturePageWrapper";
import { AnalyticsPageWrapper } from "../../components/progress/AnalyticsPageWrapper";
import { PuzzleAttemptsPageWrapper } from "../../components/progress/PuzzleAttemptsPageWrapper";

export const ProgressPage = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = ProgressMainPage;

    if (currentChildPage === "stats") {
    CurrentPageComponent = StatsPageWrapper;
  } else   if (currentChildPage === "achievements") {
    CurrentPageComponent = AchievementsPageWrapper;
  } else   if (currentChildPage === "progress") {
    CurrentPageComponent = ProgressFeaturePageWrapper;
  } else   if (currentChildPage === "analytics") {
    CurrentPageComponent = AnalyticsPageWrapper;
  } else   if (currentChildPage === "puzzle-attempts") {
    CurrentPageComponent = PuzzleAttemptsPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
