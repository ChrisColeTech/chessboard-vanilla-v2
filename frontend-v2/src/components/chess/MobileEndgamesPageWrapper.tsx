import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileEndgamesPage } from "../../pages/chess/MobileEndgamesPage";

export const MobileEndgamesPageWrapper = () => {
  usePageInstructions("endgames");
  
  return <MobileEndgamesPage />;
};
