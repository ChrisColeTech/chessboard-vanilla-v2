import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { HistoricGamesPage } from "../../pages/chess/HistoricGamesPage";

export const HistoricGamesPageWrapper = () => {
  usePageInstructions("historic-games");
  
  return <HistoricGamesPage />;
};
