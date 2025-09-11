import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { HistoricGamesPage } from "../../pages/chess/HistoricGamesPage";

export const HistoricGamesPageWrapper: React.FC = () => {
  usePageInstructions("historic-games");
  
  return <HistoricGamesPage />;
};
