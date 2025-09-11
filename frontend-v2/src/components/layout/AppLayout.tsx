import React, { useState } from "react";
import { BackgroundEffects } from "./BackgroundEffects";
import { MainContent } from "./MainContent";
import { TabBar } from "./TabBar";
import { TitleBar } from "./TitleBar";
import { ActionSheetContainer } from "../ui/ActionSheetContainer";
import type { TabId } from "./types";

interface AppLayoutProps {
  children: React.ReactNode;
  currentTab: TabId;
  onTabChange: (tab: TabId) => void;
  coinBalance: number;
}

export function AppLayout({ children, currentTab, onTabChange, coinBalance }: AppLayoutProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="h-screen w-screen overflow-hidden bg-background text-foreground relative">
      {/* Background effects */}
      <BackgroundEffects />
      
      {/* Main app structure */}
      <div className="relative z-10 flex flex-col h-full">
        {/* Title bar */}
        <TitleBar coinBalance={coinBalance} />
        
        {/* Tab navigation */}
        <TabBar 
          currentTab={currentTab}
          onTabChange={onTabChange}
          isMenuOpen={isMenuOpen}
          onToggleMenu={toggleMenu}
        />
        
        {/* Main content area */}
        <MainContent>
          {children}
        </MainContent>
      </div>
      
      {/* Action sheets overlay */}
      <ActionSheetContainer />
    </div>
  );
}
