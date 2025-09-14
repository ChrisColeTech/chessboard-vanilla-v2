import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { RegisterPageContent } from "./RegisterPageContent";
import { AuthLayout } from "../../components/auth/AuthLayout";
import type { AuthPage } from "../../components/auth/AuthRouter";

interface RegisterPageWrapperProps {
  onNavigate?: (page: AuthPage) => void;
}

export const RegisterPageWrapper: React.FC<RegisterPageWrapperProps> = ({ onNavigate }) => {
  usePageInstructions("register");
  
  return (
    <AuthLayout>
      <RegisterPageContent onNavigate={onNavigate} />
    </AuthLayout>
  );
};