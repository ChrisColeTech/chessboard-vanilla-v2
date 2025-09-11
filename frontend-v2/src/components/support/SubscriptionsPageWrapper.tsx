import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { SubscriptionsPage } from "../../pages/support/SubscriptionsPage";

export const SubscriptionsPageWrapper: React.FC = () => {
  usePageInstructions("subscriptions");
  
  return <SubscriptionsPage />;
};
