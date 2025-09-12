import { useEffect, useRef } from "react";
import { Settings, HelpCircle, BarChart, Palette } from "lucide-react";
import { useSettings } from "../../stores/appStore";
import { useInstructions } from "../../contexts/InstructionsContext";

interface MenuDropdownProps {
  onClose: () => void;
}

export function MenuDropdown({ onClose }: MenuDropdownProps) {
  const { open: openSettings } = useSettings();
  const { openInstructions } = useInstructions();
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Focus first menu item when dropdown opens
    const firstMenuItem = menuRef.current?.querySelector(
      '[role="menuitem"]'
    ) as HTMLButtonElement;
    firstMenuItem?.focus();
  }, []);

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Escape") {
      onClose();
      return;
    }

    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const menuItems = Array.from(
        menuRef.current?.querySelectorAll('[role="menuitem"]') || []
      );
      const currentIndex = menuItems.indexOf(event.target as Element);
      const direction = event.key === "ArrowDown" ? 1 : -1;
      const nextIndex =
        (currentIndex + direction + menuItems.length) % menuItems.length;
      (menuItems[nextIndex] as HTMLButtonElement)?.focus();
    }
  };

  return (
    <div
      ref={menuRef}
      data-menu-dropdown
      role="menu"
      aria-label="Navigation menu"
      onKeyDown={handleKeyDown}
      className="menu-dropdown"
    >
      <div className="space-y-1">
        <button
          onClick={() => {
            // Note: UI click sound is handled automatically by Global UI Audio System
            openSettings();
            onClose();
          }}
          role="menuitem"
          className="menu-item"
        >
          <Settings className="menu-icon" />
          <span className="menu-text">Settings</span>
        </button>
        <button
          onClick={() => {
            // Note: UI click sound is handled automatically by Global UI Audio System
            openInstructions();
            onClose();
          }}
          role="menuitem"
          className="menu-item"
        >
          <HelpCircle className="menu-icon" />
          <span className="menu-text">Help</span>
        </button>
        <button
          onClick={() => {
            // Note: UI click sound is handled automatically by Global UI Audio System
            onClose();
          }}
          role="menuitem"
          className="menu-item"
        >
          <BarChart className="menu-icon" />
          <span className="menu-text">Stats</span>
        </button>
        <button
          onClick={() => {
            // Note: UI click sound is handled automatically by Global UI Audio System
            onClose();
          }}
          role="menuitem"
          className="menu-item"
        >
          <Palette className="menu-icon" />
          <span className="menu-text">Themes</span>
        </button>
      </div>
    </div>
  );
}
