import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobilePuzzlesPage } from "../../pages/chess/MobilePuzzlesPage";

export const MobilePuzzlesPageWrapper = () => {
  usePageInstructions("puzzles");
  
  return <MobilePuzzlesPage />;
};
