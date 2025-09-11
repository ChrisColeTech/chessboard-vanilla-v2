#!/usr/bin/env python3
"""
Layout Generator
Generates React layout components and App.tsx with dynamic routing
"""

from pathlib import Path
from typing import Dict, List
from base_generator import BaseFrontendGenerator

class LayoutGenerator(BaseFrontendGenerator):
    """Generates layout components and main app structure"""
    
    def __init__(self, frontend_path: str = "../frontend-v2"):
        super().__init__(frontend_path)
        
        # Map domain names to tab icons and descriptions
        self.domain_tab_config = {
            'chess': {
                'icon': 'Target',
                'description': 'Chess Games & Analysis',
                'label': 'Chess'
            },
            'user': {
                'icon': 'User', 
                'description': 'User Profile & Auth',
                'label': 'Account'
            },
            'learning': {
                'icon': 'BookOpen',
                'description': 'Tutorials & Learning',
                'label': 'Learn'
            },
            'progress': {
                'icon': 'TrendingUp',
                'description': 'Stats & Progress',
                'label': 'Progress'
            },
            'support': {
                'icon': 'HelpCircle',
                'description': 'Help & Support',
                'label': 'Support'
            },
            'other': {
                'icon': 'Settings',
                'description': 'Other Features',
                'label': 'Other'
            }
        }
    
    def get_types_template(self, domains: List[str]) -> str:
        """Generate layout types with dynamic TabId"""
        tab_ids = " | ".join([f"'{domain}'" for domain in domains])
        
        return f'''export type TabId = {tab_ids};
'''
    
    def get_tab_bar_template(self, domains: List[str]) -> str:
        """Generate TabBar component with dynamic tabs"""
        # Generate imports for all icons
        icons = [self.domain_tab_config[domain]['icon'] for domain in domains]
        unique_icons = list(set(icons))
        icon_imports = ", ".join(unique_icons)
        
        # Generate tab configurations
        tab_configs = []
        for domain in domains:
            config = self.domain_tab_config[domain]
            tab_configs.append(f'''  {{
    id: "{domain}",
    label: "{config['label']}",
    icon: {config['icon']},
    description: "{config['description']}",
  }}''')
        
        tabs_array = ',\n'.join(tab_configs)
        
        return f'''import {{ {icon_imports} }} from "lucide-react";
import {{ MenuButton }} from "./MenuButton";
import type {{ TabId }} from "./types";
import {{ useAppStore }} from "../../stores/appStore";

interface TabBarProps {{
  currentTab: TabId;
  onTabChange: (tab: TabId) => void;
  isMenuOpen: boolean;
  onToggleMenu: () => void;
}}

interface Tab {{
  id: TabId;
  label: string;
  icon: React.ComponentType<{{ className?: string }}>;
  description: string;
}}

const tabs: Tab[] = [
{tabs_array}
];

export function TabBar({{ currentTab, onTabChange, isMenuOpen, onToggleMenu }}: TabBarProps) {{
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);

  const handleTabClick = (tab: Tab) => {{
    // Clear child page state when switching tabs (for hierarchical navigation)
    if (tab.id === currentTab) {{
      setCurrentChildPage(null);
    }}
    onTabChange(tab.id);
  }};

  return (
    <div className="flex items-center justify-between w-full px-4 py-2 bg-background border-b border-border">
      <div className="flex items-center space-x-1">
        {{tabs.map((tab) => {{
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          
          return (
            <button
              key={{tab.id}}
              onClick={{() => handleTabClick(tab)}}
              className={{`
                flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium
                transition-all duration-200 ease-in-out
                ${{isActive 
                  ? 'bg-primary text-primary-foreground shadow-md' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                }}
              `}}
              title={{tab.description}}
            >
              <Icon className="w-4 h-4" />
              <span className="hidden sm:inline">{{tab.label}}</span>
            </button>
          );
        }})}}
      </div>
      
      <MenuButton 
        isOpen={{isMenuOpen}} 
        onToggle={{onToggleMenu}} 
      />
    </div>
  );
}}
'''
    
    def get_app_template(self, domains: List[str]) -> str:
        """Generate main App.tsx with dynamic routing"""
        # Generate imports for parent pages
        page_imports = []
        routing_conditions = []
        
        for domain in domains:
            page_name = f"{domain.title()}Page"
            page_imports.append(f'import {{ {page_name} }} from "./pages/{domain}/{page_name}";')
            routing_conditions.append(f'      {{selectedTab === "{domain}" && <{page_name} />}}')
        
        imports_str = '\n'.join(page_imports)
        routing_str = '\n'.join(routing_conditions)
        
        return f'''import {{ useEffect }} from "react";
import {{ AppLayout }} from "./components/layout";
import {{ useGlobalUIAudio }} from "./hooks/audio/useGlobalUIAudio";

import {{ DragProvider, useDrag }} from "./providers/DragProvider";
import {{ InstructionsProvider }} from "./contexts/InstructionsContext";
import {{ DraggedPiece }} from "./components/chess/DraggedPiece";
import {{ SplashModal }} from "./components/splash/SplashModal";
import {{ useSelectedTab, useAppStore }} from "./stores/appStore";
import {{ useChessAudio }} from "./services/audio/audioService";
import {{ useAuthStatus }} from "./hooks";
import {{ AuthRouter }} from "./components/auth/AuthRouter";

{imports_str}

/*
 * This App.tsx was generated by the frontend generator.
 * The tabs and routing are automatically configured based on your domain structure.
 * 
 * Generated tabs: {', '.join(domains)}
 */

function AppContent() {{
  const selectedTab = useSelectedTab();
  const setSelectedTab = useAppStore((state) => state.setSelectedTab);
  const coinBalance = useAppStore((state) => state.coinBalance);
  const {{ draggedPiece, cursorPosition, draggedPieceSize }} = useDrag();
  const {{ preloadSounds, playGameStart }} = useChessAudio();
  const {{ isAuthenticated, isLoading: authLoading }} = useAuthStatus();

  // Initialize Global UI Audio System
  useGlobalUIAudio({{
    autoInitialize: true,
    initialConfig: {{
      enabled: true,
      autoDetection: true,
      excludeSelectors: [
        '[data-no-sound]',
        '.no-sound',
        '.chess-piece',
        '.chess-square',
        '.chess-board',
        '[disabled]',
        '.disabled',
        '[data-headlessui-state]',
        '[data-action-item]',
        '.action-sheet-item'
      ]
    }}
  }});

  // Initialize audio system on first user interaction
  useEffect(() => {{
    const handleFirstInteraction = () => {{
      preloadSounds();
      playGameStart();

      document.removeEventListener("click", handleFirstInteraction);
      document.removeEventListener("keydown", handleFirstInteraction);
    }};

    document.addEventListener("click", handleFirstInteraction, {{ once: true }});
    document.addEventListener("keydown", handleFirstInteraction, {{ once: true }});

    return () => {{
      document.removeEventListener("click", handleFirstInteraction);
      document.removeEventListener("keydown", handleFirstInteraction);
    }};
  }}, []);

  // Show auth pages if not authenticated
  if (!authLoading && !isAuthenticated) {{
    return <AuthRouter />;
  }}

  return (
    <AppLayout
      currentTab={{selectedTab}}
      onTabChange={{setSelectedTab}}
      coinBalance={{coinBalance}}
    >
      {{/* Generated page routing */}}
{routing_str}

      {{/* Global drag overlay */}}
      {{draggedPiece && (
        <DraggedPiece
          piece={{draggedPiece}}
          position={{cursorPosition}}
          size={{draggedPieceSize}}
        />
      )}}
    </AppLayout>
  );
}}

function App() {{
  return (
    <InstructionsProvider>
      <DragProvider>
        <AppContent />
        <SplashModal />
      </DragProvider>
    </InstructionsProvider>
  );
}}

export default App;
'''
    
    def get_app_layout_template(self) -> str:
        """Generate AppLayout component"""
        return '''import React, { useState } from "react";
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
'''
    
    def get_main_content_template(self) -> str:
        """Generate MainContent component"""
        return '''import React from "react";

interface MainContentProps {
  children: React.ReactNode;
}

export function MainContent({ children }: MainContentProps) {
  return (
    <main className="flex-1 overflow-hidden">
      <div className="h-full w-full p-4">
        {children}
      </div>
    </main>
  );
}
'''
    
    def get_title_bar_template(self) -> str:
        """Generate TitleBar component"""
        return '''import { Coins } from "lucide-react";

interface TitleBarProps {
  coinBalance: number;
}

export function TitleBar({ coinBalance }: TitleBarProps) {
  return (
    <div className="flex items-center justify-between w-full px-4 py-3 bg-card border-b border-border">
      <div className="flex items-center space-x-3">
        <h1 className="text-xl font-bold text-foreground">Chess App</h1>
      </div>
      
      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
        <Coins className="w-4 h-4" />
        <span className="font-medium">{coinBalance.toLocaleString()}</span>
      </div>
    </div>
  );
}
'''
    
    def get_menu_button_template(self) -> str:
        """Generate MenuButton component"""
        return '''import { Menu, X } from "lucide-react";

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
'''
    
    def get_background_effects_template(self) -> str:
        """Generate BackgroundEffects component"""
        return '''export function BackgroundEffects() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-background/95 to-accent/20" />
      
      {/* Subtle pattern overlay */}
      <div 
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />
    </div>
  );
}
'''
    
    def get_layout_index_template(self) -> str:
        """Generate layout index.ts"""
        return '''export { AppLayout } from "./AppLayout";
export { TabBar } from "./TabBar";
export { TitleBar } from "./TitleBar";
export { MainContent } from "./MainContent";
export { MenuButton } from "./MenuButton";
export { BackgroundEffects } from "./BackgroundEffects";
export type { TabId } from "./types";
'''
    
    def generate_layout_components(self, domains: List[str]):
        """Generate all layout components"""
        print("🎨 Generating layout components...")
        
        # Create layout directory
        layout_dir = self.get_src_path() / "components" / "layout"
        layout_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate types.ts
        types_content = self.get_types_template(domains)
        with open(layout_dir / "types.ts", 'w') as f:
            f.write(types_content)
        print("  📝 Generated components/layout/types.ts")
        
        # Generate TabBar.tsx
        tab_bar_content = self.get_tab_bar_template(domains)
        with open(layout_dir / "TabBar.tsx", 'w') as f:
            f.write(tab_bar_content)
        print("  📝 Generated components/layout/TabBar.tsx")
        
        # Generate AppLayout.tsx
        app_layout_content = self.get_app_layout_template()
        with open(layout_dir / "AppLayout.tsx", 'w') as f:
            f.write(app_layout_content)
        print("  📝 Generated components/layout/AppLayout.tsx")
        
        # Generate MainContent.tsx
        main_content = self.get_main_content_template()
        with open(layout_dir / "MainContent.tsx", 'w') as f:
            f.write(main_content)
        print("  📝 Generated components/layout/MainContent.tsx")
        
        # Generate TitleBar.tsx
        title_bar_content = self.get_title_bar_template()
        with open(layout_dir / "TitleBar.tsx", 'w') as f:
            f.write(title_bar_content)
        print("  📝 Generated components/layout/TitleBar.tsx")
        
        # Generate MenuButton.tsx
        menu_button_content = self.get_menu_button_template()
        with open(layout_dir / "MenuButton.tsx", 'w') as f:
            f.write(menu_button_content)
        print("  📝 Generated components/layout/MenuButton.tsx")
        
        # Generate BackgroundEffects.tsx
        bg_effects_content = self.get_background_effects_template()
        with open(layout_dir / "BackgroundEffects.tsx", 'w') as f:
            f.write(bg_effects_content)
        print("  📝 Generated components/layout/BackgroundEffects.tsx")
        
        # Generate index.ts
        index_content = self.get_layout_index_template()
        with open(layout_dir / "index.ts", 'w') as f:
            f.write(index_content)
        print("  📝 Generated components/layout/index.ts")
        
        print("✅ Layout components generated successfully!")
    
    def generate_main_app(self, domains: List[str]):
        """Generate main App.tsx with dynamic routing"""
        print("🚀 Generating main App.tsx...")
        
        app_content = self.get_app_template(domains)
        app_file = self.get_src_path() / "App.tsx"
        
        with open(app_file, 'w') as f:
            f.write(app_content)
        
        print("  📝 Generated App.tsx with dynamic routing")
        print(f"  🎯 Configured tabs: {', '.join(domains)}")
        print("✅ Main app generated successfully!")
    
    def generate_full_layout(self, domains: List[str]):
        """Generate complete layout system"""
        print("🏗️ Generating complete layout system...")
        
        self.generate_layout_components(domains)
        self.generate_main_app(domains)
        
        print("✅ Complete layout system generated successfully!")
    
    def get_instructions_fab_template(self) -> str:
        """Generate InstructionsFAB component"""
        return '''import React from 'react';
import { HelpCircle } from 'lucide-react';

interface InstructionsFABProps {
  onClick: () => void;
}

export const InstructionsFAB: React.FC<InstructionsFABProps> = ({ onClick }) => {
  const handleClick = () => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    onClick();
  };
  
  return (
    <button
      onClick={handleClick}
      className="absolute bottom-4 right-4 sm:right-8 lg:right-20 w-12 h-12 bg-primary hover:bg-primary/90 text-primary-foreground rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center group z-30"
      aria-label="Show instructions"
    >
      <HelpCircle className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
    </button>
  );
};
'''
    
    def get_action_sheet_container_template(self) -> str:
        """Generate ActionSheetContainer component"""
        return '''import React from 'react';

export const ActionSheetContainer: React.FC = () => {
  // This component would contain the action sheet logic
  // For now, it's a placeholder that can be enhanced later
  return (
    <div id="action-sheet-container" className="fixed inset-0 pointer-events-none z-50">
      {/* Action sheets will be rendered here */}
    </div>
  );
};
'''
    
    def generate_core_components(self):
        """Generate core components like FAB, ActionSheets, etc."""
        print("🎯 Generating core components...")
        
        # Create core directory
        core_dir = self.get_src_path() / "components" / "core"
        core_dir.mkdir(parents=True, exist_ok=True)
        
        # Create ui directory
        ui_dir = self.get_src_path() / "components" / "ui"
        ui_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate InstructionsFAB
        fab_content = self.get_instructions_fab_template()
        with open(core_dir / "InstructionsFAB.tsx", 'w') as f:
            f.write(fab_content)
        print("  📝 Generated components/core/InstructionsFAB.tsx")
        
        # Generate ActionSheetContainer
        action_sheet_content = self.get_action_sheet_container_template()
        with open(ui_dir / "ActionSheetContainer.tsx", 'w') as f:
            f.write(action_sheet_content)
        print("  📝 Generated components/ui/ActionSheetContainer.tsx")
        
        # Generate core index
        core_index_content = '''export { InstructionsFAB } from "./InstructionsFAB";
'''
        with open(core_dir / "index.ts", 'w') as f:
            f.write(core_index_content)
        print("  📝 Generated components/core/index.ts")
        
        # Generate ui index
        ui_index_content = '''export { ActionSheetContainer } from "./ActionSheetContainer";
'''
        with open(ui_dir / "index.ts", 'w') as f:
            f.write(ui_index_content)
        print("  📝 Generated components/ui/index.ts")
        
        print("✅ Core components generated successfully!")
    
    def generate_all_layout_infrastructure(self, domains: List[str]):
        """Generate complete layout infrastructure including core components"""
        print("🏗️ Generating complete layout infrastructure...")
        
        self.generate_layout_components(domains)
        self.generate_core_components()
        self.generate_main_app(domains)
        
        print("✅ Complete layout infrastructure generated successfully!")
    
    def get_drag_provider_template(self) -> str:
        """Generate DragProvider context"""
        return '''import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface DragContextType {
  draggedPiece: string | null;
  cursorPosition: { x: number; y: number };
  draggedPieceSize: number;
  startDrag: (piece: string, position: { x: number; y: number }, size?: number) => void;
  endDrag: () => void;
  updateCursor: (position: { x: number; y: number }) => void;
}

const DragContext = createContext<DragContextType | undefined>(undefined);

export const useDrag = () => {
  const context = useContext(DragContext);
  if (!context) {
    throw new Error('useDrag must be used within a DragProvider');
  }
  return context;
};

interface DragProviderProps {
  children: ReactNode;
}

export const DragProvider: React.FC<DragProviderProps> = ({ children }) => {
  const [draggedPiece, setDraggedPiece] = useState<string | null>(null);
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  const [draggedPieceSize, setDraggedPieceSize] = useState(40);

  const startDrag = (piece: string, position: { x: number; y: number }, size = 40) => {
    setDraggedPiece(piece);
    setCursorPosition(position);
    setDraggedPieceSize(size);
  };

  const endDrag = () => {
    setDraggedPiece(null);
  };

  const updateCursor = (position: { x: number; y: number }) => {
    setCursorPosition(position);
  };

  return (
    <DragContext.Provider value={{
      draggedPiece,
      cursorPosition,
      draggedPieceSize,
      startDrag,
      endDrag,
      updateCursor
    }}>
      {children}
    </DragContext.Provider>
  );
};
'''
    
    def get_instructions_context_template(self) -> str:
        """Generate InstructionsContext"""
        return '''import React, { createContext, useContext, type ReactNode } from 'react';
import { useInstructions } from '../hooks/useInstructions';

interface InstructionsContextType {
  title: string;
  instructions: string[];
  setInstructions: (title: string, instructions: string[]) => void;
}

const InstructionsContext = createContext<InstructionsContextType | undefined>(undefined);

export const useInstructionsContext = () => {
  const context = useContext(InstructionsContext);
  if (!context) {
    throw new Error('useInstructionsContext must be used within an InstructionsProvider');
  }
  return context;
};

interface InstructionsProviderProps {
  children: ReactNode;
}

export const InstructionsProvider: React.FC<InstructionsProviderProps> = ({ children }) => {
  const { title, instructions, setInstructions } = useInstructions();

  return (
    <InstructionsContext.Provider value={{
      title,
      instructions,
      setInstructions
    }}>
      {children}
    </InstructionsContext.Provider>
  );
};
'''
    
    def get_global_ui_audio_template(self) -> str:
        """Generate useGlobalUIAudio hook"""
        return '''import { useEffect } from 'react';

interface GlobalUIAudioConfig {
  enabled: boolean;
  autoDetection: boolean;
  excludeSelectors: string[];
}

interface UseGlobalUIAudioProps {
  autoInitialize: boolean;
  initialConfig: GlobalUIAudioConfig;
}

export const useGlobalUIAudio = ({ autoInitialize, initialConfig }: UseGlobalUIAudioProps) => {
  useEffect(() => {
    if (!autoInitialize) return;

    const handleClick = (event: Event) => {
      const target = event.target as HTMLElement;
      
      // Check if element should be excluded
      const shouldExclude = initialConfig.excludeSelectors.some(selector => {
        if (selector.startsWith('[') && selector.endsWith(']')) {
          const attr = selector.slice(1, -1);
          return target.hasAttribute(attr);
        }
        if (selector.startsWith('.')) {
          const className = selector.slice(1);
          return target.classList.contains(className);
        }
        return target.matches(selector);
      });

      if (!shouldExclude && initialConfig.enabled) {
        // Play UI sound (placeholder implementation)
        console.log('UI Sound: click');
      }
    };

    if (initialConfig.autoDetection) {
      document.addEventListener('click', handleClick);
    }

    return () => {
      document.removeEventListener('click', handleClick);
    };
  }, [autoInitialize, initialConfig]);

  return {
    playUISound: (soundType: string) => {
      console.log(`UI Sound: ${soundType}`);
    }
  };
};
'''
    
    def get_chess_audio_template(self) -> str:
        """Generate useChessAudio hook"""
        return '''import { useCallback } from 'react';

export const useChessAudio = () => {
  const preloadSounds = useCallback(() => {
    console.log('Chess Audio: Preloading sounds');
  }, []);

  const playGameStart = useCallback(() => {
    console.log('Chess Audio: Game start sound');
  }, []);

  const playMove = useCallback((isCapture: boolean = false) => {
    console.log(`Chess Audio: ${isCapture ? 'Capture' : 'Move'} sound`);
  }, []);

  const playCheck = useCallback(() => {
    console.log('Chess Audio: Check sound');
  }, []);

  const playCheckmate = useCallback(() => {
    console.log('Chess Audio: Checkmate sound');
  }, []);

  return {
    preloadSounds,
    playGameStart,
    playMove,
    playCheck,
    playCheckmate
  };
};
'''
    
    def get_auth_status_template(self) -> str:
        """Generate useAuthStatus hook"""
        return '''import { useState, useEffect } from 'react';

export const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate auth check
    const checkAuth = async () => {
      setIsLoading(true);
      // Placeholder: Always authenticated for now
      setTimeout(() => {
        setIsAuthenticated(true);
        setIsLoading(false);
      }, 100);
    };

    checkAuth();
  }, []);

  return {
    isAuthenticated,
    isLoading,
    login: () => setIsAuthenticated(true),
    logout: () => setIsAuthenticated(false)
  };
};
'''
    
    def get_auth_router_template(self) -> str:
        """Generate AuthRouter component"""
        return '''import React from 'react';

export const AuthRouter: React.FC = () => {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="card-gaming p-8 max-w-md w-full mx-4">
        <h1 className="text-2xl font-bold text-center mb-6">Authentication</h1>
        <p className="text-muted-foreground text-center">
          Authentication system placeholder. This would contain login/register forms.
        </p>
      </div>
    </div>
  );
};
'''
    
    def get_dragged_piece_template(self) -> str:
        """Generate DraggedPiece component"""
        return '''import React from 'react';

interface DraggedPieceProps {
  piece: string;
  position: { x: number; y: number };
  size: number;
}

export const DraggedPiece: React.FC<DraggedPieceProps> = ({ piece, position, size }) => {
  return (
    <div
      className="fixed pointer-events-none z-50 select-none"
      style={{
        left: position.x - size / 2,
        top: position.y - size / 2,
        width: size,
        height: size,
        fontSize: size * 0.8,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      {piece}
    </div>
  );
};
'''
    
    def get_splash_modal_template(self) -> str:
        """Generate SplashModal component"""
        return '''import React from 'react';

export const SplashModal: React.FC = () => {
  // Placeholder splash modal - could be enhanced with actual splash functionality
  return null;
};
'''
    
    def get_updated_app_store_template(self) -> str:
        """Generate updated appStore with missing exports"""
        return '''import { create } from "zustand";
import { persist, subscribeWithSelector } from "zustand/middleware";

export type TabId = 'chess' | 'user' | 'learning' | 'progress' | 'support' | 'other';

interface AppState {
  selectedTab: TabId;
  currentChildPage: string | null;
  coinBalance: number;
  setSelectedTab: (tab: TabId) => void;
  setCurrentChildPage: (childPage: string | null) => void;
  setCoinBalance: (balance: number) => void;
}

export const useAppStore = create<AppState>()(
  subscribeWithSelector(
    persist(
      (set) => ({
        selectedTab: 'chess',
        currentChildPage: null,
        coinBalance: 1000,
        setSelectedTab: (tab) => set({ selectedTab: tab }),
        setCurrentChildPage: (childPage) => set({ currentChildPage: childPage }),
        setCoinBalance: (balance) => set({ coinBalance: balance }),
      }),
      {
        name: 'chess-app-store',
        partialize: (state) => ({
          selectedTab: state.selectedTab,
          currentChildPage: state.currentChildPage,
          coinBalance: state.coinBalance,
        }),
      }
    )
  )
);

export const useSelectedTab = () => useAppStore((state) => state.selectedTab);
'''
    
    def generate_missing_dependencies(self):
        """Generate all missing providers, contexts, hooks, and components"""
        print("🔧 Generating missing dependencies...")
        
        # Create directories
        providers_dir = self.get_src_path() / "providers"
        providers_dir.mkdir(parents=True, exist_ok=True)
        
        contexts_dir = self.get_src_path() / "contexts"
        contexts_dir.mkdir(parents=True, exist_ok=True)
        
        audio_hooks_dir = self.get_src_path() / "hooks" / "audio"
        audio_hooks_dir.mkdir(parents=True, exist_ok=True)
        
        audio_services_dir = self.get_src_path() / "services" / "audio"
        audio_services_dir.mkdir(parents=True, exist_ok=True)
        
        auth_components_dir = self.get_src_path() / "components" / "auth"
        auth_components_dir.mkdir(parents=True, exist_ok=True)
        
        chess_components_dir = self.get_src_path() / "components" / "chess"
        chess_components_dir.mkdir(parents=True, exist_ok=True)
        
        splash_components_dir = self.get_src_path() / "components" / "splash"
        splash_components_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate DragProvider
        drag_provider_content = self.get_drag_provider_template()
        with open(providers_dir / "DragProvider.tsx", 'w') as f:
            f.write(drag_provider_content)
        print("  📝 Generated providers/DragProvider.tsx")
        
        # Generate InstructionsContext
        instructions_context_content = self.get_instructions_context_template()
        with open(contexts_dir / "InstructionsContext.tsx", 'w') as f:
            f.write(instructions_context_content)
        print("  📝 Generated contexts/InstructionsContext.tsx")
        
        # Generate useGlobalUIAudio
        global_ui_audio_content = self.get_global_ui_audio_template()
        with open(audio_hooks_dir / "useGlobalUIAudio.ts", 'w') as f:
            f.write(global_ui_audio_content)
        print("  📝 Generated hooks/audio/useGlobalUIAudio.ts")
        
        # Generate useChessAudio (audio service)
        chess_audio_content = self.get_chess_audio_template()
        with open(audio_services_dir / "audioService.ts", 'w') as f:
            f.write(chess_audio_content)
        print("  📝 Generated services/audio/audioService.ts")
        
        # Generate useAuthStatus hook
        auth_status_content = self.get_auth_status_template()
        hooks_file = self.get_src_path() / "hooks" / "index.ts"
        
        # Read existing hooks index and add useAuthStatus
        if hooks_file.exists():
            with open(hooks_file, 'r') as f:
                existing_content = f.read()
        else:
            existing_content = ""
        
        # Add useAuthStatus export if not already present
        if "useAuthStatus" not in existing_content:
            auth_hook_export = '''
// Auth hooks
export const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate auth check
    const checkAuth = async () => {
      setIsLoading(true);
      // Placeholder: Always authenticated for now
      setTimeout(() => {
        setIsAuthenticated(true);
        setIsLoading(false);
      }, 100);
    };

    checkAuth();
  }, []);

  return {
    isAuthenticated,
    isLoading,
    login: () => setIsAuthenticated(true),
    logout: () => setIsAuthenticated(false)
  };
};
'''
            # Update hooks index to include React imports and useAuthStatus
            updated_content = '''import { useState, useEffect } from "react";
''' + existing_content + auth_hook_export
            
            with open(hooks_file, 'w') as f:
                f.write(updated_content)
            print("  📝 Updated hooks/index.ts with useAuthStatus")
        
        # Generate AuthRouter
        auth_router_content = self.get_auth_router_template()
        with open(auth_components_dir / "AuthRouter.tsx", 'w') as f:
            f.write(auth_router_content)
        print("  📝 Generated components/auth/AuthRouter.tsx")
        
        # Generate DraggedPiece
        dragged_piece_content = self.get_dragged_piece_template()
        with open(chess_components_dir / "DraggedPiece.tsx", 'w') as f:
            f.write(dragged_piece_content)
        print("  📝 Generated components/chess/DraggedPiece.tsx")
        
        # Generate SplashModal
        splash_modal_content = self.get_splash_modal_template()
        with open(splash_components_dir / "SplashModal.tsx", 'w') as f:
            f.write(splash_modal_content)
        print("  📝 Generated components/splash/SplashModal.tsx")
        
        # Update appStore with missing exports
        app_store_content = self.get_updated_app_store_template()
        stores_dir = self.get_src_path() / "stores"
        with open(stores_dir / "appStore.ts", 'w') as f:
            f.write(app_store_content)
        print("  📝 Updated stores/appStore.ts with missing exports")
        
        print("✅ Missing dependencies generated successfully!")
    
    def generate_complete_app_infrastructure(self, domains: List[str]):
        """Generate complete app infrastructure including all dependencies"""
        print("🏗️ Generating complete app infrastructure...")
        
        self.generate_layout_components(domains)
        self.generate_core_components()
        self.generate_missing_dependencies()
        self.generate_main_app(domains)
        
        print("✅ Complete app infrastructure generated successfully!")