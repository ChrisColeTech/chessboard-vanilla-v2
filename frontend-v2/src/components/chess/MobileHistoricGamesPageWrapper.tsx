import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileHistoricGamesPage } from "../../pages/chess/MobileHistoricGamesPage";

export const MobileHistoricGamesPageWrapper = () => {
  usePageInstructions("historic-games");
  
  return <MobileHistoricGamesPage />;
};
