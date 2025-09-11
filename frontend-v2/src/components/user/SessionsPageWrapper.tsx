import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { SessionsPage } from "../../pages/user/SessionsPage";

export const SessionsPageWrapper: React.FC = () => {
  usePageInstructions("sessions");
  
  return <SessionsPage />;
};
