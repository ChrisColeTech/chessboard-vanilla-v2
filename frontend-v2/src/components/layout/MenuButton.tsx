import { Menu } from "lucide-react";

interface MenuButtonProps {
  isMenuOpen: boolean;
  onToggleMenu: () => void;
}

export function MenuButton({ isMenuOpen, onToggleMenu }: MenuButtonProps) {

  const handleMenuClick = () => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    onToggleMenu();
  };

  const handleMenuHover = () => {
    // Note: UI hover sound is handled automatically by Global UI Audio System
  };

  return (
    <button
      onClick={handleMenuClick}
      onMouseEnter={handleMenuHover}
      data-menu-button
      aria-expanded={isMenuOpen}
      aria-haspopup="menu"
      aria-label="Open navigation menu"
      className={`w-full h-full tab-button ${
        isMenuOpen ? "menu-button-active" : "menu-button-inactive"
      }`}
     id="menu-button-menu-btn">
      <Menu
        className={`w-4 h-4 mb-0 transition-all duration-300 ${
          isMenuOpen
            ? "scale-110 text-primary"
            : "text-muted-foreground hover:scale-105 hover:text-foreground"
        }`}
      />
      <span className="leading-tight font-medium">Menu</span>
    </button>
  );
}
