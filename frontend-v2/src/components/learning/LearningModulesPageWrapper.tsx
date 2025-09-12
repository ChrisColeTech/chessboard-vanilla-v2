import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { LearningModulesPage } from "../../pages/learning/LearningModulesPage";

export const LearningModulesPageWrapper = () => {
  usePageInstructions("learning-modules");
  
  return <LearningModulesPage />;
};
