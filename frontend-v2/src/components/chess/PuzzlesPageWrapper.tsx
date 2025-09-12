import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { PuzzlesPage } from "../../pages/chess/PuzzlesPage";

export const PuzzlesPageWrapper = () => {
  usePageInstructions("puzzles");
  
  return <PuzzlesPage />;
};
