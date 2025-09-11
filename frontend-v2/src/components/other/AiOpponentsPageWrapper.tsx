import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AiOpponentsPage } from "../../pages/other/AiOpponentsPage";

export const AiOpponentsPageWrapper: React.FC = () => {
  usePageInstructions("ai-opponents");
  
  return <AiOpponentsPage />;
};
