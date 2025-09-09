import React from "react";
import { useAppStore } from "../../stores/appStore";
import { PlayMainPage } from "../../components/play/PlayMainPage";
import { PlayChessPageWrapper } from "../../components/play/PlayChessPageWrapper";
import { PlayPuzzlesPageWrapper } from "../../components/play/PlayPuzzlesPageWrapper";

export const PlayPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = PlayMainPage;

  if (currentChildPage === "playchess") {
    CurrentPageComponent = PlayChessPageWrapper;
  } else if (currentChildPage === "playpuzzles") {
    CurrentPageComponent = PlayPuzzlesPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};