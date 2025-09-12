import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileTutorialsPage } from "../../pages/learning/MobileTutorialsPage";

export const MobileTutorialsPageWrapper = () => {
  usePageInstructions("tutorials");
  
  return <MobileTutorialsPage />;
};
