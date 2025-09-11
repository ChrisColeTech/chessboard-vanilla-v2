import React from "react";
import { useAppStore } from "../../stores/appStore";
import { UserMainPage } from "./UserMainPage";
import { UsersPageWrapper } from "../../components/user/UsersPageWrapper";
import { AuthPageWrapper } from "../../components/user/AuthPageWrapper";
import { SessionsPageWrapper } from "../../components/user/SessionsPageWrapper";
import { ProfilesPageWrapper } from "../../components/user/ProfilesPageWrapper";

export const UserPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = UserMainPage;

    if (currentChildPage === "users") {
    CurrentPageComponent = UsersPageWrapper;
  } else   if (currentChildPage === "auth") {
    CurrentPageComponent = AuthPageWrapper;
  } else   if (currentChildPage === "sessions") {
    CurrentPageComponent = SessionsPageWrapper;
  } else   if (currentChildPage === "profiles") {
    CurrentPageComponent = ProfilesPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
