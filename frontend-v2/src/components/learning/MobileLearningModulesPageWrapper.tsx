import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileLearningModulesPage } from "../../pages/learning/MobileLearningModulesPage";

export const MobileLearningModulesPageWrapper = () => {
  usePageInstructions("learning-modules");
  
  return <MobileLearningModulesPage />;
};
