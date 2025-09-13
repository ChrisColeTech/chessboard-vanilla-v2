import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { LuxurysplashPage } from "../../pages";

export const LuxurysplashPageWrapper: React.FC = () => {
  usePageInstructions("luxurysplash");
  usePageActions("luxurysplash");

  return <LuxurysplashPage />;
};
