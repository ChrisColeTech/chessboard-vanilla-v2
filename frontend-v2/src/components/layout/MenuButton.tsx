import { Menu, X } from "lucide-react";

interface MenuButtonProps {
  isOpen: boolean;
  onToggle: () => void;
}

export function MenuButton({ isOpen, onToggle }: MenuButtonProps) {
  const Icon = isOpen ? X : Menu;
  
  return (
    <button
      onClick={onToggle}
      className="flex items-center justify-center w-8 h-8 rounded-lg border border-border bg-background hover:bg-accent transition-colors"
      aria-label={isOpen ? "Close menu" : "Open menu"}
    >
      <Icon className="w-4 h-4" />
    </button>
  );
}
