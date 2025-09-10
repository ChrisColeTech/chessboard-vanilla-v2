import { Settings, X, Volume2, VolumeX } from "lucide-react";
import { useTheme, useAppStore, useChessSettings } from "../../stores/appStore";
import { useUIClickSound } from "../../hooks/audio/useUIClickSound";
import { BackgroundEffectsSelector } from "../settings/BackgroundEffectsSelector";
import { BoardColorSelector } from "../settings/BoardColorSelector";
import { ThemeSelector } from "../settings/ThemeSelector";
import { PieceSetSelector } from "../settings/PieceSetSelector";
import { SegmentedControl, type SegmentedControlOption } from "../ui/SegmentedControl";
import { SETTINGS_SECTIONS } from "../../data/themeConfig";
import { useCallback } from "react";

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsPanel({ onClose }: SettingsPanelProps) {
  const { isDarkMode, toggleMode } = useTheme();
  const { playUIClick } = useUIClickSound();
  const { pieceSize, setPieceSize } = useChessSettings();
  
  // Piece Size Options
  const pieceSizeOptions: SegmentedControlOption[] = [
    { id: 'small', label: 'Small' },
    { id: 'medium', label: 'Medium' },
    { id: 'large', label: 'Large' }
  ];
  
  // Audio Options
  const audioOptions: SegmentedControlOption[] = [
    { id: 'true', label: 'On', icon: Volume2 },
    { id: 'false', label: 'Off', icon: VolumeX }
  ];
  
  // Get audio state from store
  const audioEnabled = useAppStore((state) => state.audioEnabled);
  const setAudioEnabled = useAppStore((state) => state.setAudioEnabled);
  
  // Audio state is managed by the global audioService automatically

  const handleModeToggle = () => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    toggleMode();
  };

  const handleCloseClick = () => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    onClose();
  };

  const handleAudioToggle = useCallback(() => {
    const newAudioState = !audioEnabled;
    
    // Update store (which will trigger useEffect to sync with global service)
    setAudioEnabled(newAudioState);
    
    // Note: UI click sound is handled automatically by Global UI Audio System
  }, [audioEnabled, setAudioEnabled, playUIClick]);

  return (
    <div className="settings-panel">
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="settings-header">
          <div className="flex items-center gap-2">
            <Settings className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Settings</h2>
          </div>
          <button onClick={handleCloseClick} className="settings-close-btn">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Settings Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Board Color */}
          <BoardColorSelector />

          {/* Piece Size Toggle */}
          {/* Size values controlled in: src/components/chess/MobileChessBoard.tsx:getPieceSizeMultiplier() */}
          <div>
            <h3 className="text-base font-semibold text-foreground mb-3">Piece Size</h3>
            <SegmentedControl
              options={pieceSizeOptions}
              value={pieceSize}
              onChange={(value) => setPieceSize(value as 'small' | 'medium' | 'large')}
              className="w-full"
              size="sm"
            />
          </div>

          {/* Piece Set Selector */}
          <PieceSetSelector />

          {/* Sound Effects Toggle */}
          <div>
            <h3 className="text-base font-semibold text-foreground mb-3 flex items-center gap-2">
              {audioEnabled ? (
                <Volume2 className="w-4 h-4" />
              ) : (
                <VolumeX className="w-4 h-4" />
              )}
              Sound Effects
            </h3>
            <SegmentedControl
              options={audioOptions}
              value={audioEnabled.toString()}
              onChange={(value) => {
                if (value !== audioEnabled.toString()) {
                  handleAudioToggle();
                }
              }}
              className="w-full"
              size="sm"
            />
          </div>

          {/* Background Effects */}
          <BackgroundEffectsSelector />

          {/* Light/Dark Mode Toggle */}
          <div>
            <h3 className="text-base font-semibold text-foreground mb-3 flex items-center gap-2">
              <SETTINGS_SECTIONS.BRIGHTNESS.icon className="w-4 h-4" />
              {SETTINGS_SECTIONS.BRIGHTNESS.title}
            </h3>
            <SegmentedControl
              options={[
                {
                  id: 'light',
                  label: SETTINGS_SECTIONS.BRIGHTNESS.modes.light.label,
                  icon: SETTINGS_SECTIONS.BRIGHTNESS.modes.light.icon
                },
                {
                  id: 'dark',
                  label: SETTINGS_SECTIONS.BRIGHTNESS.modes.dark.label,
                  icon: SETTINGS_SECTIONS.BRIGHTNESS.modes.dark.icon
                }
              ]}
              value={isDarkMode ? 'dark' : 'light'}
              onChange={(value) => {
                if ((value === 'dark') !== isDarkMode) {
                  handleModeToggle();
                }
              }}
              className="w-full"
              size="sm"
            />
          </div>

          {/* Theme Selector */}
          <ThemeSelector />
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border settings-footer">
          <div className="text-xs text-muted-foreground text-center">
            Settings Panel - Theme & More
          </div>
        </div>
      </div>
    </div>
  );
}
