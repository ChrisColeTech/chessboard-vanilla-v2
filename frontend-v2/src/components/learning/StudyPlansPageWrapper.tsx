import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { StudyPlansPage } from "../../pages/learning/StudyPlansPage";

export const StudyPlansPageWrapper: React.FC = () => {
  usePageInstructions("study-plans");
  
  return <StudyPlansPage />;
};
