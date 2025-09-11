import React from "react";
import { useAppStore } from "../../stores/appStore";
import { LearningMainPage } from "./LearningMainPage";
import { LearningFeaturePageWrapper } from "../../components/learning/LearningFeaturePageWrapper";
import { TutorialsPageWrapper } from "../../components/learning/TutorialsPageWrapper";
import { LearningModulesPageWrapper } from "../../components/learning/LearningModulesPageWrapper";
import { TutorialStepsPageWrapper } from "../../components/learning/TutorialStepsPageWrapper";
import { StudyPlansPageWrapper } from "../../components/learning/StudyPlansPageWrapper";

export const LearningPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = LearningMainPage;

    if (currentChildPage === "learning") {
    CurrentPageComponent = LearningFeaturePageWrapper;
  } else   if (currentChildPage === "tutorials") {
    CurrentPageComponent = TutorialsPageWrapper;
  } else   if (currentChildPage === "learning-modules") {
    CurrentPageComponent = LearningModulesPageWrapper;
  } else   if (currentChildPage === "tutorial-steps") {
    CurrentPageComponent = TutorialStepsPageWrapper;
  } else   if (currentChildPage === "study-plans") {
    CurrentPageComponent = StudyPlansPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
