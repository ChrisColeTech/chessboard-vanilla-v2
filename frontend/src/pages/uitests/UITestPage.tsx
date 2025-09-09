import React from "react";
import { useAppStore } from "../../stores/appStore";
import { UITestsMainPage } from "../../components/uitests/UITestsMainPage";
import { DragTestPageWrapper } from "../../components/uitests/DragTestPageWrapper";
import { UIAudioTestPageWrapper } from "../../components/uitests/UIAudioTestPageWrapper";
import { LayoutTestPageWrapper } from "../../components/uitests/LayoutTestPageWrapper";
import { MobileDragTestPageWrapper } from "../../components/uitests/MobileDragTestPageWrapper";

export const UITestPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = UITestsMainPage;

  if (currentChildPage === "dragtest") {
    CurrentPageComponent = DragTestPageWrapper;
  } else if (currentChildPage === "uiaudiotest") {
    CurrentPageComponent = UIAudioTestPageWrapper;
  } else if (currentChildPage === "layouttest") {
    CurrentPageComponent = LayoutTestPageWrapper;
  } else if (currentChildPage === "mobiledragtest") {
    CurrentPageComponent = MobileDragTestPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};
