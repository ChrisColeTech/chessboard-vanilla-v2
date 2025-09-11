import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { UsersPage } from "../../pages/user/UsersPage";

export const UsersPageWrapper: React.FC = () => {
  usePageInstructions("users");
  
  return <UsersPage />;
};
