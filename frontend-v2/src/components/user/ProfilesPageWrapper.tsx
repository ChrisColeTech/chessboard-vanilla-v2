import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { ProfilesPage } from "../../pages/user/ProfilesPage";

export const ProfilesPageWrapper: React.FC = () => {
  usePageInstructions("profiles");
  
  return <ProfilesPage />;
};
