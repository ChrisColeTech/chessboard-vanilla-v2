import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { GamesPage } from "../../pages/chess/GamesPage";

export const GamesPageWrapper: React.FC = () => {
  usePageInstructions("games");
  
  return <GamesPage />;
};
