import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { GamesPage } from "../../pages/chess/GamesPage";

export const GamesPageWrapper = () => {
  usePageInstructions("games");
  
  return <GamesPage />;
};
