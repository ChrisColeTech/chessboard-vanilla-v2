import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { EndgamesPage } from "../../pages/chess/EndgamesPage";

export const EndgamesPageWrapper = () => {
  usePageInstructions("endgames");
  
  return <EndgamesPage />;
};
