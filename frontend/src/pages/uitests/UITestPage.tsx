import React from "react";
import { useAppStore } from "../../stores/appStore";
import { UITestsMainPage } from "./UITestsMainPage";
import { DragTestPageWrapper } from "../../components/uitests/DragTestPageWrapper";

import { UIAudioTestPageWrapper } from "../../components/uitests/UIAudioTestPageWrapper";

import { LayoutTestPageWrapper } from "../../components/uitests/LayoutTestPageWrapper";

import { ChessLayoutTestPageWrapper } from "../../components/uitests/ChessLayoutTestPageWrapper";


export const UITestPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render - single wrapper handles mobile switching internally
  let CurrentPageComponent = UITestsMainPage;

  if (currentChildPage === "dragtest") {
    CurrentPageComponent = DragTestPageWrapper;
  } else if (currentChildPage === "uiaudiotest") {
    CurrentPageComponent = UIAudioTestPageWrapper;
  } else if (currentChildPage === "layouttest") {
    CurrentPageComponent = LayoutTestPageWrapper;
  } else if (currentChildPage === "chesslayouttest") {
    CurrentPageComponent = ChessLayoutTestPageWrapper;
  }

  return (
    <div className="relative h-full">
      <CurrentPageComponent key={currentChildPage || 'main'} />
    </div>
  );
};