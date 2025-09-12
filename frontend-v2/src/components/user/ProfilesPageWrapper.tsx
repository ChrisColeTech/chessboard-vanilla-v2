import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { ProfilesPage } from "../../pages/user/ProfilesPage";

export const ProfilesPageWrapper = () => {
  usePageInstructions("profiles");
  
  return <ProfilesPage />;
};
