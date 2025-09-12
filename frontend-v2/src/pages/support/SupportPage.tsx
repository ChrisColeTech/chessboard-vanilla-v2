import { useAppStore } from "../../stores/appStore";
import { SupportMainPage } from "./SupportMainPage";
import { GameReviewsPageWrapper } from "../../components/support/GameReviewsPageWrapper";
import { PuzzleSourcesPageWrapper } from "../../components/support/PuzzleSourcesPageWrapper";
import { HelpPageWrapper } from "../../components/support/HelpPageWrapper";
import { SubscriptionsPageWrapper } from "../../components/support/SubscriptionsPageWrapper";

export const SupportPage = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = SupportMainPage;

    if (currentChildPage === "game-reviews") {
    CurrentPageComponent = GameReviewsPageWrapper;
  } else   if (currentChildPage === "puzzle-sources") {
    CurrentPageComponent = PuzzleSourcesPageWrapper;
  } else   if (currentChildPage === "help") {
    CurrentPageComponent = HelpPageWrapper;
  } else   if (currentChildPage === "subscriptions") {
    CurrentPageComponent = SubscriptionsPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
