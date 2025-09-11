import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { PuzzlesPage } from "../../pages/chess/PuzzlesPage";

export const PuzzlesPageWrapper: React.FC = () => {
  usePageInstructions("puzzles");
  
  return <PuzzlesPage />;
};
