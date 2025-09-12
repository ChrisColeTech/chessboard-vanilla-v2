import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { SessionsPage } from "../../pages/user/SessionsPage";

export const SessionsPageWrapper = () => {
  usePageInstructions("sessions");
  
  return <SessionsPage />;
};
