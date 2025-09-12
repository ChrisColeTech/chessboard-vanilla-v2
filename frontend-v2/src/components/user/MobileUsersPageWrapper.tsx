import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileUsersPage } from "../../pages/user/MobileUsersPage";

export const MobileUsersPageWrapper = () => {
  usePageInstructions("users");
  
  return <MobileUsersPage />;
};
