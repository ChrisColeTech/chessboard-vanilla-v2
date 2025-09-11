import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { OpeningsPage } from "../../pages/chess/OpeningsPage";

export const OpeningsPageWrapper: React.FC = () => {
  usePageInstructions("openings");
  
  return <OpeningsPage />;
};
