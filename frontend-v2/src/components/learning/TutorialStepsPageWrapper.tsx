import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { TutorialStepsPage } from "../../pages/learning/TutorialStepsPage";

export const TutorialStepsPageWrapper: React.FC = () => {
  usePageInstructions("tutorial-steps");
  
  return <TutorialStepsPage />;
};
