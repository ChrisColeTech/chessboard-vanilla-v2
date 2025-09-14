/**
 * Dedicated BackgroundEffectsSelector component with effects management logic
 * Extracted from SettingsPanel for Single Responsibility Principle
 */

import { Sparkles, Wand2 } from "lucide-react";
import { useBackgroundEffectsManager } from "../../hooks/core/useBackgroundEffectsManager";
<<<<<<< Updated upstream
import { SegmentedControl } from "../ui/SegmentedControl";
import { BACKGROUND_EFFECTS_TOGGLE_BUTTONS } from "../../data/backgroundEffectsConfig";
import { SETTINGS_SECTIONS } from "../../data/themeConfig";

export function BackgroundEffectsSelector() {
=======
import SegmentedControl from "../ui/SegmentedControl";
import { BACKGROUND_EFFECTS_TOGGLE_BUTTONS } from "../../data/backgroundEffectsConfig";
import { SETTINGS_SECTIONS } from "../../data/themeConfig";

export default function BackgroundEffectsSelector() {
>>>>>>> Stashed changes
  const {
    currentVariant,
    isEffectsEnabled,
    selectedEffect,
    effectsOptions,
    currentDescription,
    handleBackgroundEffectsToggle,
    handleVariantChange
  } = useBackgroundEffectsManager();

  return (
    <div>
      <h3 className="text-base font-semibold text-foreground mb-3 flex items-center gap-2">
        <Sparkles className="w-4 h-4" />
        {SETTINGS_SECTIONS.BACKGROUND_EFFECTS.title}
      </h3>
      
      {/* Effects Toggle */}
      <SegmentedControl
        options={[
          {
            id: 'enabled',
            label: BACKGROUND_EFFECTS_TOGGLE_BUTTONS.enabled.label,
            icon: BACKGROUND_EFFECTS_TOGGLE_BUTTONS.enabled.icon
          },
          {
            id: 'disabled',
            label: BACKGROUND_EFFECTS_TOGGLE_BUTTONS.disabled.label,
            icon: BACKGROUND_EFFECTS_TOGGLE_BUTTONS.disabled.icon
          }
        ]}
        value={isEffectsEnabled ? 'enabled' : 'disabled'}
        onChange={(value) => {
          if ((value === 'enabled') !== isEffectsEnabled) {
            handleBackgroundEffectsToggle();
          }
        }}
        className="w-full"
        size="sm"
      />
      
      {/* Effect Style Selection */}
      {effectsOptions.length > 0 && (
        <div className="mt-4">
          <div className="flex items-center gap-2 mb-3">
            <h4 className="text-sm font-medium text-foreground flex items-center gap-2">
              <Wand2 className="w-3 h-3" />
              Effect Style
            </h4>
            {selectedEffect && isEffectsEnabled && (
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <selectedEffect.icon className="w-3 h-3" />
                <span>{selectedEffect.name}</span>
              </div>
            )}
          </div>
          
          <SegmentedControl
            options={effectsOptions}
            value={isEffectsEnabled ? currentVariant : 'gaming'} // Default preview when disabled
            onChange={handleVariantChange}
            className="w-full"
            size="sm"
            iconOnly={true}
          />
        </div>
      )}
      
      {/* Description */}
      <div className="text-xs text-muted-foreground mt-2 leading-relaxed">
        {currentDescription}
      </div>
    </div>
  );
}