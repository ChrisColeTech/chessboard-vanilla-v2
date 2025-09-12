import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileStudyPlansPage } from "../../pages/learning/MobileStudyPlansPage";

export const MobileStudyPlansPageWrapper = () => {
  usePageInstructions("study-plans");
  
  return <MobileStudyPlansPage />;
};
