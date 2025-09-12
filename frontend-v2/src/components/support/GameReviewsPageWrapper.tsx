import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { GameReviewsPage } from "../../pages/support/GameReviewsPage";

export const GameReviewsPageWrapper = () => {
  usePageInstructions("game-reviews");
  
  return <GameReviewsPage />;
};
