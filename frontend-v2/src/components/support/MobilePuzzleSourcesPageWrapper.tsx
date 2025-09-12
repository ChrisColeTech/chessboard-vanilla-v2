import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobilePuzzleSourcesPage } from "../../pages/support/MobilePuzzleSourcesPage";

export const MobilePuzzleSourcesPageWrapper = () => {
  usePageInstructions("puzzle-sources");
  
  return <MobilePuzzleSourcesPage />;
};
