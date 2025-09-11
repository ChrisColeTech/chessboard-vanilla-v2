import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { GameReviewsPage } from "../../pages/support/GameReviewsPage";

export const GameReviewsPageWrapper: React.FC = () => {
  usePageInstructions("game-reviews");
  
  return <GameReviewsPage />;
};
