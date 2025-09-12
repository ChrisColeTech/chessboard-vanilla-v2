import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { TutorialsPage } from "../../pages/learning/TutorialsPage";

export const TutorialsPageWrapper = () => {
  usePageInstructions("tutorials");
  
  return <TutorialsPage />;
};
