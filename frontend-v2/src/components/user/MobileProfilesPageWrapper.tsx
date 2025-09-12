import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileProfilesPage } from "../../pages/user/MobileProfilesPage";

export const MobileProfilesPageWrapper = () => {
  usePageInstructions("profiles");
  
  return <MobileProfilesPage />;
};
