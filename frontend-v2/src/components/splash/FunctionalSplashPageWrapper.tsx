import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { FunctionalSplashPage } from "../../pages/splash/FunctionalSplashPage";

<<<<<<< Updated upstream
export const FunctionalSplashPageWrapper: React.FC = () => {
=======
const FunctionalSplashPageWrapper: React.FC = () => {
>>>>>>> Stashed changes
  usePageInstructions("functionalsplash");
  usePageActions("functionalsplash");

  return <FunctionalSplashPage />;
<<<<<<< Updated upstream
};
=======
};

export default FunctionalSplashPageWrapper;

export { FunctionalSplashPageWrapper };
>>>>>>> Stashed changes
