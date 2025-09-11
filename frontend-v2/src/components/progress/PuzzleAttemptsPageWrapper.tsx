import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { PuzzleAttemptsPage } from "../../pages/progress/PuzzleAttemptsPage";

export const PuzzleAttemptsPageWrapper: React.FC = () => {
  usePageInstructions("puzzle-attempts");
  
  return <PuzzleAttemptsPage />;
};
