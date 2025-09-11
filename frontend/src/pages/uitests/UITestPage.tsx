import React from "react";
import { useAppStore } from "../../stores/appStore";
import { useIsMobile } from "../../hooks/core/useIsMobile";
import { UITestsMainPage } from "./UITestsMainPage";
import { DragTestPageWrapper } from "../../components/uitests/DragTestPageWrapper";
import { UIAudioTestPageWrapper } from "../../components/uitests/UIAudioTestPageWrapper";
import { LayoutTestPageWrapper } from "../../components/uitests/LayoutTestPageWrapper";
import { MobileLayoutTestPageWrapper } from "../../components/uitests/MobileLayoutTestPageWrapper";
import { MobileDragTestPageWrapper } from "../../components/uitests/MobileDragTestPageWrapper";
import { DesktopLayoutTestPageWrapper } from "../../components/uitests/DesktopLayoutTestPageWrapper";

export const UITestPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);
  const isMobile = useIsMobile();

  // Determine which component to render
  let CurrentPageComponent = UITestsMainPage;

  if (currentChildPage === "dragtest") {
    // Automatically switch between desktop and mobile drag test
    CurrentPageComponent = isMobile ? MobileDragTestPageWrapper : DragTestPageWrapper;
  } else if (currentChildPage === "uiaudiotest") {
    CurrentPageComponent = UIAudioTestPageWrapper;
  } else if (currentChildPage === "layouttest") {
    // Automatically switch between desktop and mobile layout test
    CurrentPageComponent = isMobile ? MobileLayoutTestPageWrapper : LayoutTestPageWrapper;
  } else if (currentChildPage === "desktoplayouttest") {
    CurrentPageComponent = DesktopLayoutTestPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content - use key to force re-mount when switching components */}
      <CurrentPageComponent key={`${currentChildPage}-${isMobile ? 'mobile' : 'desktop'}`} />
    </div>
  );
};
