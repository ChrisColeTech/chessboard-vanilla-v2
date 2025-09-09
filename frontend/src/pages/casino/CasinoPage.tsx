import React from "react";
import { useAppStore } from "../../stores/appStore";
import { CasinoMainPage } from "../../components/casino/CasinoMainPage";
import { SlotMachinePageWrapper } from "../../components/casino/SlotMachinePageWrapper";
import { BlackjackPageWrapper } from "../../components/casino/BlackjackPageWrapper";
import { HoldemPageWrapper } from "../../components/casino/HoldemPageWrapper";
import { RoulettePageWrapper } from "../../components/casino/RoulettePageWrapper";
import { CrapsPageWrapper } from "../../components/casino/CrapsPageWrapper";

export const CasinoPage: React.FC = () => {
  const currentChildPage = useAppStore((state) => state.currentChildPage);

  // Determine which component to render
  let CurrentPageComponent = CasinoMainPage;

  if (currentChildPage === "slots") {
    CurrentPageComponent = SlotMachinePageWrapper;
  } else if (currentChildPage === "blackjack") {
    CurrentPageComponent = BlackjackPageWrapper;
  } else if (currentChildPage === "holdem") {
    CurrentPageComponent = HoldemPageWrapper;
  } else if (currentChildPage === "roulette") {
    CurrentPageComponent = RoulettePageWrapper;
  } else if (currentChildPage === "craps") {
    CurrentPageComponent = CrapsPageWrapper;
  }

  return (
    <div className="relative h-full">
      {/* Current page content */}
      <CurrentPageComponent />
    </div>
  );
};