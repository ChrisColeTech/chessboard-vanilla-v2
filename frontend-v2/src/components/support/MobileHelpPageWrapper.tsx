import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileHelpPage } from "../../pages/support/MobileHelpPage";

export const MobileHelpPageWrapper = () => {
  usePageInstructions("help");
  
  return <MobileHelpPage />;
};
