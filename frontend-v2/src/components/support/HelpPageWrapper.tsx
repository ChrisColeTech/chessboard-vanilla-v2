import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { HelpPage } from "../../pages/support/HelpPage";

export const HelpPageWrapper: React.FC = () => {
  usePageInstructions("help");
  
  return <HelpPage />;
};
