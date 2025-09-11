import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { PuzzleSourcesPage } from "../../pages/support/PuzzleSourcesPage";

export const PuzzleSourcesPageWrapper: React.FC = () => {
  usePageInstructions("puzzle-sources");
  
  return <PuzzleSourcesPage />;
};
