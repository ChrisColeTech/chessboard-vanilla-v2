import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { MobileSubscriptionsPage } from "../../pages/support/MobileSubscriptionsPage";

export const MobileSubscriptionsPageWrapper = () => {
  usePageInstructions("subscriptions");
  
  return <MobileSubscriptionsPage />;
};
