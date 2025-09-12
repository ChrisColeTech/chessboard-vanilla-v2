import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { PuzzleSourcesPage } from "../../pages/support/PuzzleSourcesPage";

export const PuzzleSourcesPageWrapper = () => {
  usePageInstructions("puzzle-sources");
  
  return <PuzzleSourcesPage />;
};
