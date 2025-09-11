import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { LearningModulesPage } from "../../pages/learning/LearningModulesPage";

export const LearningModulesPageWrapper: React.FC = () => {
  usePageInstructions("learning-modules");
  
  return <LearningModulesPage />;
};
