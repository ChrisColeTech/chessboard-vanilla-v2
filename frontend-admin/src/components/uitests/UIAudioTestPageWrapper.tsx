import React from "react";
import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { UIAudioTestPage } from "../../pages/uitests/UIAudioTestPage";

export const UIAudioTestPageWrapper: React.FC = () => {
  usePageInstructions("uiaudiotest");
  usePageActions("uiaudiotest");

  return <UIAudioTestPage />;
};
