import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { EndgamesPage } from "../../pages/chess/EndgamesPage";

export const EndgamesPageWrapper: React.FC = () => {
  usePageInstructions("endgames");
  
  return <EndgamesPage />;
};
