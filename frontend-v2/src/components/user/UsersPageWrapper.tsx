import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { UsersPage } from "../../pages/user/UsersPage";

export const UsersPageWrapper = () => {
  usePageInstructions("users");
  
  return <UsersPage />;
};
