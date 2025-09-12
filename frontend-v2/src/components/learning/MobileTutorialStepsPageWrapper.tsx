import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileTutorialStepsPage } from "../../pages/learning/MobileTutorialStepsPage";

export const MobileTutorialStepsPageWrapper = () => {
  usePageInstructions("tutorial-steps");
  
  return <MobileTutorialStepsPage />;
};
