import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { AuthPage } from "../../pages/user/AuthPage";

export const AuthPageWrapper = () => {
  usePageInstructions("auth");
  
  return <AuthPage />;
};
