import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { HelpPage } from "../../pages/support/HelpPage";

export const HelpPageWrapper = () => {
  usePageInstructions("help");
  
  return <HelpPage />;
};
