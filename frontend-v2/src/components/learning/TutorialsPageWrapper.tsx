import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { TutorialsPage } from "../../pages/learning/TutorialsPage";

export const TutorialsPageWrapper: React.FC = () => {
  usePageInstructions("tutorials");
  
  return <TutorialsPage />;
};
