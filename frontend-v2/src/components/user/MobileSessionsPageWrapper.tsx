import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileSessionsPage } from "../../pages/user/MobileSessionsPage";

export const MobileSessionsPageWrapper = () => {
  usePageInstructions("sessions");
  
  return <MobileSessionsPage />;
};
