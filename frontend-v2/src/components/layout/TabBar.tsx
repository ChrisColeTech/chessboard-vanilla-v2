import { HelpCircle, TrendingUp, User, Target, Settings, BookOpen } from "lucide-react";
import { MenuButton } from "./MenuButton";
import type { TabId } from "./types";
import { useAppStore } from "../../stores/appStore";

interface TabBarProps {
  currentTab: TabId;
  onTabChange: (tab: TabId) => void;
  isMenuOpen: boolean;
  onToggleMenu: () => void;
}

interface Tab {
  id: TabId;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
}

const tabs: Tab[] = [
  {
    id: "chess",
    label: "Chess",
    icon: Target,
    description: "Chess Games & Analysis",
  },
  {
    id: "user",
    label: "Account",
    icon: User,
    description: "User Profile & Auth",
  },
  {
    id: "learning",
    label: "Learn",
    icon: BookOpen,
    description: "Tutorials & Learning",
  },
  {
    id: "progress",
    label: "Progress",
    icon: TrendingUp,
    description: "Stats & Progress",
  },
  {
    id: "support",
    label: "Support",
    icon: HelpCircle,
    description: "Help & Support",
  },
  {
    id: "other",
    label: "Other",
    icon: Settings,
    description: "Other Features",
  }
];

export function TabBar({ currentTab, onTabChange, isMenuOpen, onToggleMenu }: TabBarProps) {
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);

  const handleTabClick = (tab: Tab) => {
    // Clear child page state when switching tabs (for hierarchical navigation)
    if (tab.id === currentTab) {
      setCurrentChildPage(null);
    }
    onTabChange(tab.id);
  };

  return (
    <div className="flex items-center justify-between w-full px-4 py-2 bg-background border-b border-border">
      <div className="flex items-center space-x-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          
          return (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab)}
              className={`
                flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium
                transition-all duration-200 ease-in-out
                ${isActive 
                  ? 'bg-primary text-primary-foreground shadow-md' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                }
              `}
              title={tab.description}
            >
              <Icon className="w-4 h-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </button>
          );
        })}
      </div>
      
      <MenuButton 
        isOpen={isMenuOpen} 
        onToggle={onToggleMenu} 
      />
    </div>
  );
}
