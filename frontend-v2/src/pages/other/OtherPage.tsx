import React from "react";
import { useAppStore } from "../../stores/appStore";
import { OtherMainPage } from "./OtherMainPage";
import { AiOpponentsPageWrapper } from "../../components/other/AiOpponentsPageWrapper";

export const OtherPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = OtherMainPage;

    if (currentChildPage === "ai-opponents") {
    CurrentPageComponent = AiOpponentsPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
