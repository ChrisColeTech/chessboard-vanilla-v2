import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { PuzzleAttemptsPage } from "../../pages/progress/PuzzleAttemptsPage";

export const PuzzleAttemptsPageWrapper = () => {
  usePageInstructions("puzzle-attempts");
  
  return <PuzzleAttemptsPage />;
};
