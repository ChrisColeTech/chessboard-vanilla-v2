import type { ReactNode } from "react";
import { BackgroundEffects } from "./BackgroundEffects";
import { TitleBar } from "./TitleBar";
import { Header } from "./Header";
import { TabBar } from "./TabBar";
import { SettingsPanel } from "../core/SettingsPanel";
import { ActionSheetContainer } from "../action-sheet";
import { InstructionsFAB } from "../core/InstructionsFAB";
import { InstructionsModal } from "../core/InstructionsModal";
import { CoinsModal } from "../casino/CoinsModal";
import { useSettings, useCoinsModal } from "../../stores/appStore";
import { useInstructions } from "../../contexts/InstructionsContext";
import { useActionSheet } from "../../hooks";
import type { TabId } from "./types";

/**
 * GLASSMORPHISM DESIGN SYSTEM
 * ===========================
 *
 * This app uses a consistent glassmorphism design system with two main classes:
 *
 * 1. `glass-layout` - For full-width layout elements (Header, TabBar)
 *    - No rounded corners (sharp edges for layout)
 *    - Subtle glassmorphism effect
 *    - No entry animations
 *
 * 2. `card-gaming` - For content cards (modals, panels, cards)
 *    - Rounded corners for content separation
 *    - Same glassmorphism effect
 *    - Entry animations for engagement
 *
 * USAGE RULES:
 * - Header/TabBar: Use `glass-layout`
 * - Content cards/panels: Use `card-gaming`
 * - Modals/overlays: Use `card-gaming`
 * - Never mix classes - stick to the designated purpose
 */

interface AppLayoutProps {
  children: ReactNode;
  currentTab: TabId;
  onTabChange: (tab: TabId) => void;
  coinBalance?: number;
}

export function AppLayout({
  children,
  currentTab,
  onTabChange,
  coinBalance,
}: AppLayoutProps) {
  const {
    isOpen: isSettingsPanelOpen,
    open: openSettings,
    close: closeSettings,
  } = useSettings();
  const {
    isOpen: isMenuOpen,
    toggleSheet: toggleMenu,
    closeSheet: closeMenu,
  } = useActionSheet();
  const {
    instructions,
    title,
    showInstructions,
    openInstructions,
    closeInstructions,
  } = useInstructions();
  const {
    isOpen: isCoinsModalOpen,
    close: closeCoinsModal,
    coinBalance: currentCoinBalance,
  } = useCoinsModal();

  return (
    <div className="relative min-h-screen min-h-[100dvh] bg-background text-foreground">
      <BackgroundEffects />

      {/* Title Bar - Fixed positioning at the very top */}
      <div className="fixed top-0 left-0 right-0 z-30">
        <TitleBar />
      </div>

      {/* 
        Header - Fixed positioning for mobile compatibility
        ✅ Fixed to top with proper z-index, below title bar
        Hide when settings panel is open
      */}
      <header className={`fixed top-10 left-0 right-0 z-20 transition-transform duration-300 ease-out ${
        isSettingsPanelOpen ? "-translate-y-full opacity-0" : "translate-y-0 opacity-100"
      }`}>
        <Header
          onOpenSettings={openSettings}
          isSettingsOpen={isSettingsPanelOpen}
          coinBalance={coinBalance}
        />
      </header>

      {/* Main Content Area - constrained between fixed header and footer */}
      <div className="absolute top-10 bottom-[84px] left-0 right-0 z-10">
        {/* Primary Content - scrollable within the constrained area */}
        <main className="w-full h-full overflow-auto">
          <div className="w-full px-4 pt-20 pb-4 sm:px-8 sm:pt-24 sm:pb-8 lg:px-20 lg:pt-16 lg:pb-16">{children}</div>
        </main>

        {/* Instructions FAB - positioned within main content area */}
        <InstructionsFAB onClick={openInstructions} />

        {/* 
            Settings Panel - Uses `card-gaming` for rounded corners and entry animations
            ✅ Correct: Content overlay with rounded design
          */}
        <>
          {/* Backdrop - covers entire main content */}
          <div
            className={`absolute inset-0 bg-black/20 backdrop-blur-sm z-20 transition-opacity duration-300 ease-out ${
              isSettingsPanelOpen
                ? "opacity-100"
                : "opacity-0 pointer-events-none"
            }`}
            onClick={closeSettings}
          />

          {/* Settings Panel */}
          <aside
            className={`absolute top-0 right-0 h-full z-30 transform transition-transform duration-300 ease-out ${
              isSettingsPanelOpen ? "translate-x-0" : "translate-x-full"
            }`}
          >
            <SettingsPanel
              isOpen={isSettingsPanelOpen}
              onClose={closeSettings}
            />
          </aside>
        </>
      </div>

      {/* ActionSheet - Always rendered, HeadlessUI manages show/hide */}
      <ActionSheetContainer 
        currentPage={currentTab}
        onClose={closeMenu}
        isOpen={isMenuOpen}
        onOpenSettings={openSettings}
      />

      {/* 
          TabBar - Fixed positioning for mobile compatibility  
          ✅ Fixed to bottom with proper z-index
        */}
      <footer className="fixed bottom-0 left-0 right-0 z-20 glass-layout">
        <TabBar 
          currentTab={currentTab} 
          onTabChange={onTabChange}
          isMenuOpen={isMenuOpen}
          onToggleMenu={toggleMenu}
        />
      </footer>

      {/* Global Instructions Modal */}
      <InstructionsModal
        isOpen={showInstructions}
        onClose={closeInstructions}
        title={title}
        instructions={instructions}
      />

      {/* Global Coins Modal */}
      <CoinsModal
        isOpen={isCoinsModalOpen}
        onClose={closeCoinsModal}
        coinBalance={currentCoinBalance}
      />
    </div>
  );
}
