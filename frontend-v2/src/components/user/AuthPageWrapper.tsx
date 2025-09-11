import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AuthPage } from "../../pages/user/AuthPage";

export const AuthPageWrapper: React.FC = () => {
  usePageInstructions("auth");
  
  return <AuthPage />;
};
