import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileGamesPage } from "../../pages/chess/MobileGamesPage";

export const MobileGamesPageWrapper = () => {
  usePageInstructions("games");
  
  return <MobileGamesPage />;
};
