import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { OpeningsPage } from "../../pages/chess/OpeningsPage";

export const OpeningsPageWrapper = () => {
  usePageInstructions("openings");
  
  return <OpeningsPage />;
};
