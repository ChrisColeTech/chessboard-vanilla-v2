import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { SubscriptionsPage } from "../../pages/support/SubscriptionsPage";

export const SubscriptionsPageWrapper = () => {
  usePageInstructions("subscriptions");
  
  return <SubscriptionsPage />;
};
