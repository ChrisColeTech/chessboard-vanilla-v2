import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { ForgotPasswordPageContent } from "../../pages/user/ForgotPasswordPageContent";
import AuthLayout from "./AuthLayout";
import type { AuthPage } from "../../components/auth/AuthRouter";

interface ForgotPasswordPageWrapperProps {
  onNavigate?: (page: AuthPage) => void;
}

export const ForgotPasswordPageWrapper: React.FC<ForgotPasswordPageWrapperProps> = ({ onNavigate }) => {
  usePageInstructions("forgotPassword");
  
  return (
    <AuthLayout>
      <ForgotPasswordPageContent onNavigate={onNavigate} />
    </AuthLayout>
  );
};