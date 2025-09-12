import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { TutorialStepsPage } from "../../pages/learning/TutorialStepsPage";

export const TutorialStepsPageWrapper = () => {
  usePageInstructions("tutorial-steps");
  
  return <TutorialStepsPage />;
};
