import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileAuthPage } from "../../pages/user/MobileAuthPage";

export const MobileAuthPageWrapper = () => {
  usePageInstructions("auth");
  
  return <MobileAuthPage />;
};
