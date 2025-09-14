import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
<<<<<<< Updated upstream
import { LuxurysplashPage } from "../../pages";

export const LuxurysplashPageWrapper: React.FC = () => {
=======
import { LuxurysplashPage } from "../../pages/splash/LuxurysplashPage";

const LuxurysplashPageWrapper: React.FC = () => {
>>>>>>> Stashed changes
  usePageInstructions("luxurysplash");
  usePageActions("luxurysplash");

  return <LuxurysplashPage />;
};
<<<<<<< Updated upstream
=======

export default LuxurysplashPageWrapper;
export { LuxurysplashPageWrapper };
>>>>>>> Stashed changes
