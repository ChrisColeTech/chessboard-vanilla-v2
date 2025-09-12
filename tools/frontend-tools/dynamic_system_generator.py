#!/usr/bin/env python3
"""
Dynamic System Generator
Creates dynamic file loading system for instructions and actions
"""

from pathlib import Path
from base_generator import BaseFrontendGenerator


class DynamicSystemGenerator(BaseFrontendGenerator):
    """Generates dynamic file loading system for instructions and actions"""
    
    def generate_dynamic_system(self):
        """Generate complete dynamic system"""
        print("🔧 Setting up dynamic system...")
        
        # Create supporting types and contexts
        self._create_action_sheet_types()
        self._create_action_sheet_context()
        self._create_instructions_context()
        
        # Create dynamic services
        self._create_dynamic_instructions_service()
        self._create_dynamic_page_actions_service()
        
        # Update core hooks and components
        self._update_page_instructions_hook()
        self._update_action_sheet_container()
        
        # Create individual page files
        self._create_basic_action_files()
        self._create_basic_instruction_files()
        
        print("✅ Dynamic system setup complete!")
    
    def generate_mobile_page_variant(self, page_name: str, parent: str, icon: str = "Navigation", description: str = ""):
        """Generate mobile page variant with desktop/mobile switching support"""
        print(f"📱 Creating mobile page variant: {page_name}")
        
        # Create desktop page component
        self._create_desktop_page_component(page_name, parent, icon, description)
        
        # Create mobile page component  
        self._create_mobile_page_component(page_name, parent, icon, description)
        
        # Create desktop wrapper
        self._create_desktop_page_wrapper(page_name, parent)
        
        # Create mobile wrapper
        self._create_mobile_page_wrapper(page_name, parent)
        
        # Create instruction and action files
        self._create_page_instruction_file(page_name.lower(), f"{page_name} Instructions", description)
        self._create_page_action_file(page_name.lower(), icon)
        
        print(f"✅ Mobile page variant {page_name} created!")

    def _create_dynamic_instructions_service(self):
        """Create the dynamic instructions service"""
        content = '''interface PageInstructions {
  id: string;
  title: string;
  instructions: string[];
}

interface PageInstructionsModule {
  pageInstructions: PageInstructions;
}

class DynamicInstructionsService {
  private instructionsCache: Map<string, PageInstructions> = new Map();
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Use import.meta.glob to dynamically import all instruction files
      const instructionModules = import.meta.glob('./pages/*.ts', { eager: true }) as Record<string, PageInstructionsModule>;
      
      for (const [, module] of Object.entries(instructionModules)) {
        if (module.pageInstructions) {
          this.instructionsCache.set(module.pageInstructions.id, module.pageInstructions);
        }
      }
      
      this.initialized = true;
      console.log(`🔄 [DYNAMIC INSTRUCTIONS] Loaded ${this.instructionsCache.size} instruction files`);
    } catch (error) {
      console.error('❌ [DYNAMIC INSTRUCTIONS] Failed to load instruction files:', error);
    }
  }

  getInstructions(pageId: string): PageInstructions | null {
    if (!this.initialized) {
      // Synchronously initialize if not already done
      this.initialize();
    }
    
    const instructions = this.instructionsCache.get(pageId);
    if (!instructions) {
      console.warn(`⚠️ [DYNAMIC INSTRUCTIONS] No instructions found for page: ${pageId}`);
      return null;
    }
    
    return instructions;
  }

  listAvailablePages(): string[] {
    return Array.from(this.instructionsCache.keys());
  }

  reload(): void {
    this.instructionsCache.clear();
    this.initialized = false;
    this.initialize();
  }
}

export const dynamicInstructionsService = new DynamicInstructionsService();'''
        
        file_path = self.frontend_path / "src" / "services" / "instructions" / "InstructionsService.dynamic.ts"
        self.write_file(file_path, content)

    def _create_dynamic_page_actions_service(self):
        """Create the dynamic page actions service"""
        content = '''import type { ActionSheetAction } from '../../types/core/action-sheet.types';

interface PageActions {
  id: string;
  actions: ActionSheetAction[];
}

interface PageActionsModule {
  pageActions: PageActions;
}

class DynamicPageActionsService {
  private actionsCache: Map<string, ActionSheetAction[]> = new Map();
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Use import.meta.glob to dynamically import all action files
      const actionModules = import.meta.glob('./pages/*.ts', { eager: true }) as Record<string, PageActionsModule>;
      
      for (const [, module] of Object.entries(actionModules)) {
        if (module.pageActions) {
          this.actionsCache.set(module.pageActions.id, module.pageActions.actions);
        }
      }
      
      this.initialized = true;
      console.log(`🔄 [DYNAMIC ACTIONS] Loaded ${this.actionsCache.size} action files`);
    } catch (error) {
      console.error('❌ [DYNAMIC ACTIONS] Failed to load action files:', error);
    }
  }

  getActions(pageId: string): ActionSheetAction[] {
    if (!this.initialized) {
      // Synchronously initialize if not already done
      this.initialize();
    }
    
    const actions = this.actionsCache.get(pageId);
    if (!actions) {
      console.warn(`⚠️ [DYNAMIC ACTIONS] No actions found for page: ${pageId}`);
      return [];
    }
    
    return actions;
  }

  listAvailablePages(): string[] {
    return Array.from(this.actionsCache.keys());
  }

  reload(): void {
    this.actionsCache.clear();
    this.initialized = false;
    this.initialize();
  }
}

const dynamicPageActionsService = new DynamicPageActionsService();

// Export as object matching the original PAGE_ACTIONS structure
export const DYNAMIC_PAGE_ACTIONS = new Proxy({}, {
  get(_, pageId: string | symbol) {
    if (typeof pageId === 'string') {
      return dynamicPageActionsService.getActions(pageId);
    }
    return undefined;
  }
}) as Record<string, ActionSheetAction[]>;'''
        
        file_path = self.frontend_path / "src" / "constants" / "actions" / "page-actions.dynamic.ts"
        self.write_file(file_path, content)

    def _update_page_instructions_hook(self):
        """Update usePageInstructions hook to use dynamic service"""
        content = '''import { useEffect } from 'react'
import { useInstructions } from '../../contexts/InstructionsContext'
import { dynamicInstructionsService } from '../../services/instructions/InstructionsService.dynamic'

/**
 * Hook to automatically set page instructions from dynamic service
 * Supports hierarchical page IDs like 'uitests.audio-demo'
 * Uses dynamic file loading for zero-configuration instruction management
 */
export const usePageInstructions = (pageId: string) => {
  const { setInstructions } = useInstructions()

  useEffect(() => {
    const pageInstructions = dynamicInstructionsService.getInstructions(pageId)
    
    if (pageInstructions) {
      setInstructions(pageInstructions.title, [...pageInstructions.instructions])
    }
  }, [pageId, setInstructions])
}'''
        
        file_path = self.frontend_path / "src" / "hooks" / "core" / "usePageInstructions.ts"
        self.write_file(file_path, content)

    def _update_action_sheet_container(self):
        """Create ActionSheetContainer with dynamic actions support"""
        content = '''import React, { useEffect, useState } from 'react';
import { DYNAMIC_PAGE_ACTIONS } from '../../constants/actions/page-actions.dynamic';
import { useActionSheet } from '../../contexts/ActionSheetContext';
import type { ActionSheetAction } from '../../types/core/action-sheet.types';

export const ActionSheetContainer: React.FC = () => {
  const { isOpen, currentPage, closeActionSheet } = useActionSheet();
  const [delayedActionSheetPage, setDelayedActionSheetPage] = useState<string | null>(null);

  // Delay loading to ensure dynamic system is initialized
  useEffect(() => {
    if (currentPage) {
      const timer = setTimeout(() => {
        setDelayedActionSheetPage(currentPage);
      }, 100);
      return () => clearTimeout(timer);
    } else {
      setDelayedActionSheetPage(null);
    }
  }, [currentPage]);

  if (!isOpen || !delayedActionSheetPage) {
    return null;
  }

  // Get actions from dynamic system
  const actions = DYNAMIC_PAGE_ACTIONS[delayedActionSheetPage] || [];

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center p-4 pointer-events-auto">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={closeActionSheet}
      />
      
      {/* Action Sheet */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full max-h-96 overflow-y-auto">
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-4">
            Actions for {delayedActionSheetPage}
          </h3>
          
          {actions.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              No actions available for this page
            </p>
          ) : (
            <div className="space-y-2">
              {actions.map((action: ActionSheetAction) => (
                <button
                  key={action.id}
                  className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                    action.variant === 'primary' 
                      ? 'bg-blue-600 hover:bg-blue-700 text-white'
                      : action.variant === 'destructive'
                      ? 'bg-red-600 hover:bg-red-700 text-white'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                  }`}
                  onClick={() => {
                    action.onPress?.();
                    console.log(`Action pressed: ${action.id}`);
                  }}
                >
                  <span className="flex items-center">
                    {action.icon && <action.icon className="w-5 h-5 mr-3" />}
                    {action.label}
                  </span>
                </button>
              ))}
            </div>
          )}
          
          <button
            onClick={closeActionSheet}
            className="w-full mt-4 p-3 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};'''
        
        file_path = self.frontend_path / "src" / "components" / "ui" / "ActionSheetContainer.tsx"
        self.write_file(file_path, content)

    def _create_basic_action_files(self):
        """Create basic action files for common pages"""
        basic_pages = [
            'play', 'playchess', 'playpuzzles', 'casino', 'slots', 
            'worker', 'uitests', 'dragtest', 'uiaudiotest', 'layout', 'splash', 'users'
        ]
        
        for page_id in basic_pages:
            action_content = f'''import {{ Navigation, Play, Settings }} from 'lucide-react'
import type {{ ActionSheetAction }} from '../../../types/core/action-sheet.types'

export const pageActions = {{
  id: '{page_id}',
  actions: [
    {{
      id: '{page_id}-action',
      label: '{page_id.title().replace("test", " Test")} Action',
      icon: Navigation,
      variant: 'default'
    }},
    {{
      id: '{page_id}-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    }},
    {{
      id: '{page_id}-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }}
  ] as ActionSheetAction[]
}}'''
            
            file_path = self.frontend_path / "src" / "constants" / "actions" / "pages" / f"{page_id}.ts"
            self.write_file(file_path, action_content)
        
        print(f"✅ Created {len(basic_pages)} basic action files")

    def _create_basic_instruction_files(self):
        """Create basic instruction files for common pages"""
        basic_pages = [
            ('play', 'Play Instructions'),
            ('playchess', 'Play Chess Instructions'), 
            ('playpuzzles', 'Chess Puzzles Instructions'),
            ('casino', 'Casino Instructions'),
            ('slots', 'Slots Instructions'),
            ('worker', 'Chess Worker Instructions'),
            ('uitests', 'UI Tests Instructions'),
            ('dragtest', 'Drag Test Instructions'),
            ('uiaudiotest', 'Audio Test Instructions'),
            ('layout', 'Layout Instructions'),
            ('splash', 'Splash Screen Instructions')
        ]
        
        for page_id, title in basic_pages:
            instruction_content = f'''export const pageInstructions = {{
  id: '{page_id}',
  title: '{title}',
  instructions: [
    'Use this page to work with {page_id.replace("test", " test")} features',
    'Use the action sheet to interact with available options',
    'Navigate using the action menu to explore different options'
  ]
}}'''
            
            file_path = self.frontend_path / "src" / "services" / "instructions" / "pages" / f"{page_id}.ts"
            self.write_file(file_path, instruction_content)
        
        print(f"✅ Created {len(basic_pages)} basic instruction files")

    def _create_action_sheet_types(self):
        """Create action sheet type definitions"""
        content = '''import type { LucideIcon } from 'lucide-react';

export interface ActionSheetAction {
  id: string;
  label: string;
  icon?: LucideIcon;
  variant?: 'default' | 'primary' | 'secondary' | 'destructive';
  onPress?: () => void;
}

export interface PageActions {
  id: string;
  actions: ActionSheetAction[];
}

export interface ActionSheetConfiguration {
  [pageId: string]: ActionSheetAction[];
}'''
        
        file_path = self.frontend_path / "src" / "types" / "core" / "action-sheet.types.ts"
        self.write_file(file_path, content)

    def _create_action_sheet_context(self):
        """Create ActionSheetContext"""
        content = '''import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface ActionSheetContextType {
  isOpen: boolean;
  currentPage: string | null;
  openActionSheet: (page: string) => void;
  closeActionSheet: () => void;
}

const ActionSheetContext = createContext<ActionSheetContextType | undefined>(undefined);

export const useActionSheet = () => {
  const context = useContext(ActionSheetContext);
  if (!context) {
    throw new Error('useActionSheet must be used within an ActionSheetProvider');
  }
  return context;
};

interface ActionSheetProviderProps {
  children: ReactNode;
}

export const ActionSheetProvider: React.FC<ActionSheetProviderProps> = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState<string | null>(null);

  const openActionSheet = (page: string) => {
    setCurrentPage(page);
    setIsOpen(true);
  };

  const closeActionSheet = () => {
    setIsOpen(false);
    setCurrentPage(null);
  };

  return (
    <ActionSheetContext.Provider value={{
      isOpen,
      currentPage,
      openActionSheet,
      closeActionSheet
    }}>
      {children}
    </ActionSheetContext.Provider>
  );
};'''
        
        file_path = self.frontend_path / "src" / "contexts" / "ActionSheetContext.tsx"
        self.write_file(file_path, content)

    def _create_instructions_context(self):
        """Create InstructionsContext"""
        content = '''import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface InstructionsContextType {
  title: string;
  instructions: string[];
  isOpen: boolean;
  setInstructions: (title: string, instructions: string[]) => void;
  clearInstructions: () => void;
  showInstructions: (title: string, instructions: string[]) => void;
  openInstructions: () => void;
  closeInstructions: () => void;
}

const InstructionsContext = createContext<InstructionsContextType | undefined>(undefined);

export const useInstructions = () => {
  const context = useContext(InstructionsContext);
  if (!context) {
    throw new Error('useInstructions must be used within an InstructionsProvider');
  }
  return context;
};

interface InstructionsProviderProps {
  children: ReactNode;
}

export const InstructionsProvider: React.FC<InstructionsProviderProps> = ({ children }) => {
  const [title, setTitle] = useState<string>('');
  const [instructions, setInstructionsState] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const setInstructions = (newTitle: string, newInstructions: string[]) => {
    setTitle(newTitle);
    setInstructionsState(newInstructions);
  };

  const clearInstructions = () => {
    setTitle('');
    setInstructionsState([]);
    setIsOpen(false);
  };

  const showInstructions = (newTitle: string, newInstructions: string[]) => {
    setTitle(newTitle);
    setInstructionsState(newInstructions);
    setIsOpen(true);
  };

  const openInstructions = () => {
    setIsOpen(true);
  };

  const closeInstructions = () => {
    setIsOpen(false);
  };

  return (
    <InstructionsContext.Provider value={{
      title,
      instructions,
      isOpen,
      setInstructions,
      clearInstructions,
      showInstructions,
      openInstructions,
      closeInstructions
    }}>
      {children}
    </InstructionsContext.Provider>
  );
};'''
        
        file_path = self.frontend_path / "src" / "contexts" / "InstructionsContext.tsx"
        self.write_file(file_path, content)

    def _create_desktop_page_component(self, page_name: str, parent: str, icon: str, description: str):
        """Create desktop page component"""
        content = f'''import React from 'react';
import {{ usePageInstructions }} from '../../hooks/core/usePageInstructions';

interface {page_name}PageProps {{
  className?: string;
}}

export const {page_name}Page: React.FC<{page_name}PageProps> = ({{ className }}) => {{
  // Auto-load instructions for this page
  usePageInstructions('{page_name.lower()}');

  return (
    <div className={{`{page_name.lower()}-page ${{className || ''}}`}}>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">{page_name}</h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-600 mb-4">{description or f"Welcome to the {page_name} page."}</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">Desktop Features</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Full desktop interface</li>
                <li>• Enhanced functionality</li>
                <li>• Desktop-optimized layout</li>
              </ul>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold mb-2">Actions</h3>
              <p className="text-sm text-gray-600">
                Use the action sheet to access {page_name.lower()} features
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}};'''
        
        page_dir = self.frontend_path / "src" / "pages" / parent
        page_dir.mkdir(parents=True, exist_ok=True)
        file_path = page_dir / f"{page_name}Page.tsx"
        self.write_file(file_path, content)

    def _create_mobile_page_component(self, page_name: str, parent: str, icon: str, description: str):
        """Create mobile page component"""
        content = f'''import React from 'react';
import {{ usePageInstructions }} from '../../hooks/core/usePageInstructions';

interface Mobile{page_name}PageProps {{
  className?: string;
}}

export const Mobile{page_name}Page: React.FC<Mobile{page_name}PageProps> = ({{ className }}) => {{
  // Auto-load instructions for this page
  usePageInstructions('{page_name.lower()}');

  return (
    <div className={{`mobile-{page_name.lower()}-page ${{className || ''}}`}}>
      <div className="px-4 py-6">
        <h1 className="text-2xl font-bold mb-4">{page_name}</h1>
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
          <p className="text-gray-600 text-sm mb-4">{description or f"Welcome to the mobile {page_name} page."}</p>
          <div className="space-y-3">
            <div className="border rounded-lg p-3">
              <h3 className="font-medium text-sm mb-2">Mobile Features</h3>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>• Touch-optimized interface</li>
                <li>• Mobile-responsive layout</li>
                <li>• Gesture support</li>
              </ul>
            </div>
            <div className="border rounded-lg p-3">
              <h3 className="font-medium text-sm mb-2">Quick Actions</h3>
              <p className="text-xs text-gray-600">
                Tap the action button to access {page_name.lower()} features
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}};'''
        
        page_dir = self.frontend_path / "src" / "pages" / parent
        page_dir.mkdir(parents=True, exist_ok=True)
        file_path = page_dir / f"Mobile{page_name}Page.tsx"
        self.write_file(file_path, content)

    def _create_desktop_page_wrapper(self, page_name: str, parent: str):
        """Create desktop page wrapper"""
        content = f'''import React from 'react';
import {{ {page_name}Page }} from '../../pages/{parent}/{page_name}Page';

interface {page_name}PageWrapperProps {{
  className?: string;
}}

export const {page_name}PageWrapper: React.FC<{page_name}PageWrapperProps> = ({{ className }}) => {{
  return (
    <div className={{`{page_name.lower()}-page-wrapper desktop-variant ${{className || ''}}`}}>
      <{page_name}Page />
    </div>
  );
}};'''
        
        component_dir = self.frontend_path / "src" / "components" / parent
        component_dir.mkdir(parents=True, exist_ok=True)
        file_path = component_dir / f"{page_name}PageWrapper.tsx"
        self.write_file(file_path, content)

    def _create_mobile_page_wrapper(self, page_name: str, parent: str):
        """Create mobile page wrapper"""
        content = f'''import React from 'react';
import {{ Mobile{page_name}Page }} from '../../pages/{parent}/Mobile{page_name}Page';

interface Mobile{page_name}PageWrapperProps {{
  className?: string;
}}

export const Mobile{page_name}PageWrapper: React.FC<Mobile{page_name}PageWrapperProps> = ({{ className }}) => {{
  return (
    <div className={{`mobile-{page_name.lower()}-page-wrapper mobile-variant ${{className || ''}}`}}>
      <Mobile{page_name}Page />
    </div>
  );
}};'''
        
        component_dir = self.frontend_path / "src" / "components" / parent
        component_dir.mkdir(parents=True, exist_ok=True)
        file_path = component_dir / f"Mobile{page_name}PageWrapper.tsx"
        self.write_file(file_path, content)

    def _create_page_instruction_file(self, page_id: str, title: str, description: str):
        """Create instruction file for a page"""
        content = f'''export const pageInstructions = {{
  id: '{page_id}',
  title: '{title}',
  instructions: [
    '{description or f"Use this page to work with {page_id} features"}',
    'Use the action sheet to interact with available options',
    'Navigate using the action menu to explore different options'
  ]
}}'''
        
        file_path = self.frontend_path / "src" / "services" / "instructions" / "pages" / f"{page_id}.ts"
        self.write_file(file_path, content)

    def _create_page_action_file(self, page_id: str, icon: str):
        """Create action file for a page"""
        content = f'''import {{ Navigation, Play, Settings, {icon} }} from 'lucide-react'
import type {{ ActionSheetAction }} from '../../../types/core/action-sheet.types'

export const pageActions = {{
  id: '{page_id}',
  actions: [
    {{
      id: '{page_id}-main',
      label: '{page_id.title().replace("-", " ")} Action',
      icon: {icon},
      variant: 'default'
    }},
    {{
      id: '{page_id}-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    }},
    {{
      id: '{page_id}-start',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }}
  ] as ActionSheetAction[]
}}'''
        
        file_path = self.frontend_path / "src" / "constants" / "actions" / "pages" / f"{page_id}.ts"
        self.write_file(file_path, content)