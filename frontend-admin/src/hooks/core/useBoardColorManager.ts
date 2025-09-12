/**
 * Custom hook for board color and style management logic
 * Following the pattern established by useBackgroundEffectsManager
 */

import { useAppStore } from "../../stores/appStore";
import type { SegmentedControlOption } from "../../components/ui/SegmentedControl";
import { BOARD_COLOR_MODES, PREMIUM_BOARD_STYLES, type BoardColorMode, type PremiumBoardStyle } from "../../data/boardColorConfig";

export function useBoardColorManager() {
  const boardColorMode = useAppStore((state) => state.boardColorMode);
  const premiumBoardStyle = useAppStore((state) => state.premiumBoardStyle);
  const setBoardColorMode = useAppStore((state) => state.setBoardColorMode);
  const setPremiumBoardStyle = useAppStore((state) => state.setPremiumBoardStyle);

  const handleBoardColorModeChange = (mode: BoardColorMode) => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    setBoardColorMode(mode);
  };

  const handlePremiumStyleChange = (style: PremiumBoardStyle) => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    setPremiumBoardStyle(style);
  };

  // Create segmented control options for board color modes
  const colorModeOptions: SegmentedControlOption[] = Object.values(BOARD_COLOR_MODES).map(mode => ({
    id: mode.id,
    label: mode.label,
    icon: mode.icon,
    description: mode.description
  }));

  // Create segmented control options for premium board styles
  const premiumStyleOptions: SegmentedControlOption[] = Object.values(PREMIUM_BOARD_STYLES).map(style => ({
    id: style.id,
    label: style.label,
    icon: style.icon,
    description: style.description
  }));

  const isPremiumMode = boardColorMode === 'premium';
  
  // Get current descriptions
  const currentColorModeDescription = BOARD_COLOR_MODES[boardColorMode].description;
  const currentPremiumStyleDescription = isPremiumMode ? PREMIUM_BOARD_STYLES[premiumBoardStyle].description : '';

  return {
    boardColorMode,
    premiumBoardStyle,
    isPremiumMode,
    colorModeOptions,
    premiumStyleOptions,
    currentColorModeDescription,
    currentPremiumStyleDescription,
    handleBoardColorModeChange,
    handlePremiumStyleChange
  };
}