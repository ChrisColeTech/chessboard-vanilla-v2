import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileGameReviewsPage } from "../../pages/support/MobileGameReviewsPage";

export const MobileGameReviewsPageWrapper = () => {
  usePageInstructions("game-reviews");
  
  return <MobileGameReviewsPage />;
};
