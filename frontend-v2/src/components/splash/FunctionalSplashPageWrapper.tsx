import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { FunctionalSplashPage } from "../../pages/splash/FunctionalSplashPage";

export const FunctionalSplashPageWrapper: React.FC = () => {
  usePageInstructions("functionalsplash");
  usePageActions("functionalsplash");

  return <FunctionalSplashPage />;
};