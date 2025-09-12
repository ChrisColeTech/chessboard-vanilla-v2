import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobilePuzzleAttemptsPage } from "../../pages/progress/MobilePuzzleAttemptsPage";

export const MobilePuzzleAttemptsPageWrapper = () => {
  usePageInstructions("puzzle-attempts");
  
  return <MobilePuzzleAttemptsPage />;
};
