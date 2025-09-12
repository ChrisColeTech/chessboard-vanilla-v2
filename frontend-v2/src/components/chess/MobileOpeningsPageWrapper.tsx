import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileOpeningsPage } from "../../pages/chess/MobileOpeningsPage";

export const MobileOpeningsPageWrapper = () => {
  usePageInstructions("openings");
  
  return <MobileOpeningsPage />;
};
