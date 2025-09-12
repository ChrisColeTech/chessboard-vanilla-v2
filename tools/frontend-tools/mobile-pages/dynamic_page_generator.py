#!/usr/bin/env python3
"""
Dynamic Page Generator CLI Tool - Simplified Version

Uses the new dynamic file loading architecture:
- No file modification corruption issues  
- Just creates simple instruction and action files
- Files are auto-discovered by import.meta.glob
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class PageConfig:
    name: str
    parent: Optional[str] = None
    mobile: bool = False
    icon: str = "Navigation"
    description: str = ""

class DynamicPageGenerator:
    def __init__(self, frontend_root: str):
        self.frontend_root = Path(frontend_root)
        self.pages_dir = self.frontend_root / "src" / "pages"
        self.components_dir = self.frontend_root / "src" / "components"
        self.hooks_dir = self.frontend_root / "src" / "hooks"
        self.instructions_pages_dir = self.frontend_root / "src" / "services" / "instructions" / "pages"
        self.actions_pages_dir = self.frontend_root / "src" / "constants" / "actions" / "pages"
        
    def create_child_page(self, config: PageConfig) -> None:
        """Create a child page with all required files using dynamic loading"""
        if not config.parent:
            raise ValueError("Child pages must specify a parent")
            
        print(f"📝 Creating child page: {config.name} (parent: {config.parent})")
        
        # Create React page components
        self._create_child_page_component(config)
        self._create_responsive_wrapper(config)
        
        # Create mobile variant if requested
        if config.mobile:
            mobile_config = PageConfig(
                name=f"Mobile{config.name}",
                parent=config.parent,
                mobile=True,
                icon=config.icon,
                description=f"Mobile version of {config.description}"
            )
            self._create_mobile_child_page(mobile_config, config.name)
        
        # Create instruction file (auto-discovered)
        self._create_instruction_file(config)
        
        # Create action file (auto-discovered)
        self._create_action_file(config)
        
        # Update parent page with routing logic
        self._update_parent_page_routing(config)
        
        # Update ActionSheetContainer.tsx with action handler mappings
        self._update_action_sheet_container(config)
        
        # Update parent page action constants to include navigation to child page
        self._update_parent_page_actions(config)
        
        print(f"✅ Child page '{config.name}' created successfully!")
        if config.mobile:
            print(f"✅ Mobile variant 'Mobile{config.name}' created successfully!")
        print(f"✅ Single responsive wrapper created!")
        print(f"✅ Parent page routing updated automatically!")
        print(f"✅ ActionSheetContainer.tsx updated with action handlers!")
        print(f"✅ Parent page action sheet updated with navigation!")
            
        print(f"\n📋 Architecture improvements:")
        print(f"   ✅ Single wrapper with internal mobile switching")
        print(f"   ✅ Reduced component duplication")
        print(f"   ✅ Cleaner parent routing logic")
        print(f"   ✅ Mobile switching handled in wrapper, not parent")
        
    def _create_child_page_component(self, config: PageConfig) -> None:
        """Create the main child page component"""
        content = f'''import React from "react";
import {{ usePageData }} from "../../hooks/core/usePageData";
import {{ ChessboardLayout }} from "../../components/chess/ChessboardLayout";
import {{ DataTable }} from "../../components/ui/DataTable";

interface {config.name}PageProps {{
  // Add props as needed
}}

export const {config.name}Page: React.FC<{config.name}PageProps> = () => {{
  const {{ data, loading, error }} = usePageData("{config.name.lower()}");

  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={{<div className="uitest-layout-corner">{config.name} Top Left</div>}}
        top={{<div className="uitest-layout-center"></div>}}
        topRight={{<div className="uitest-layout-corner">{config.name} Top Right</div>}}
        left={{<div className="uitest-layout-corner">{config.name} Left</div>}}
        center={{<DataTable data={{data}} loading={{loading}} error={{error}} />}}
        right={{<div className="uitest-layout-corner">{config.name} Right</div>}}
        bottomLeft={{<div className="uitest-layout-corner">{config.name} Bottom Left</div>}}
        bottom={{<div className="uitest-layout-center"></div>}}
        bottomRight={{<div className="uitest-layout-corner">{config.name} Bottom Right</div>}}
        className="w-full h-full"
      />
    </div>
  );
}};
'''
        file_path = self.pages_dir / config.parent / f"{config.name}Page.tsx"
        self._write_file(file_path, content)

    def _create_responsive_wrapper(self, config: PageConfig) -> None:
        """Create single responsive wrapper component that handles mobile switching"""
        # Check if hooks exist in this frontend
        hooks_dir = self.frontend_root / "src" / "hooks" / "core"
        has_page_hooks = (hooks_dir / "usePageInstructions.ts").exists() and (hooks_dir / "usePageActions.ts").exists()
        has_mobile_hook = (hooks_dir / "useIsMobile.ts").exists()
        
        print(f"  🔍 Hook detection: page_hooks={has_page_hooks}, mobile_hook={has_mobile_hook}")
        
        if config.mobile:
            if has_page_hooks and has_mobile_hook:
                # Full hook support (frontend)
                content = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageActions }} from "../../hooks/core/usePageActions";
import {{ useIsMobile }} from "../../hooks/core/useIsMobile";
import {{ {config.name}Page }} from "../../pages/{config.parent}/{config.name}Page";
import {{ Mobile{config.name}Page }} from "../../pages/{config.parent}/Mobile{config.name}Page";

export const {config.name}PageWrapper: React.FC = () => {{
  const isMobile = useIsMobile();
  
  usePageInstructions("{config.name.lower()}");
  usePageActions("{config.name.lower()}");

  return isMobile ? <Mobile{config.name}Page /> : <{config.name}Page />;
}};'''
            else:
                # No hooks support (frontend-v2)
                content = f'''import React from "react";
import {{ {config.name}Page }} from "../../pages/{config.parent}/{config.name}Page";
import {{ Mobile{config.name}Page }} from "../../pages/{config.parent}/Mobile{config.name}Page";

// Mobile detection placeholder - update when useIsMobile is available
const useIsMobile = () => false;

export const {config.name}PageWrapper: React.FC = () => {{
  const isMobile = useIsMobile();

  return isMobile ? <Mobile{config.name}Page /> : <{config.name}Page />;
}};'''
        else:
            if has_page_hooks:
                # Hook support (frontend)
                content = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageActions }} from "../../hooks/core/usePageActions";
import {{ {config.name}Page }} from "../../pages/{config.parent}/{config.name}Page";

export const {config.name}PageWrapper: React.FC = () => {{
  usePageInstructions("{config.name.lower()}");
  usePageActions("{config.name.lower()}");

  return <{config.name}Page />;
}};'''
            else:
                # No hooks support (frontend-v2)
                content = f'''import React from "react";
import {{ {config.name}Page }} from "../../pages/{config.parent}/{config.name}Page";

export const {config.name}PageWrapper: React.FC = () => {{
  return <{config.name}Page />;
}};'''
        
        file_path = self.components_dir / config.parent / f"{config.name}PageWrapper.tsx"
        self._write_file(file_path, content)

    def _create_mobile_child_page(self, mobile_config: PageConfig, original_name: str) -> None:
        """Create mobile version of child page"""
        content = f'''import React from "react";
import {{ usePageData }} from "../../hooks/core/usePageData";
import {{ MobileChessboardLayout }} from "../../components/chess/MobileChessboardLayout";
import {{ DataTable }} from "../../components/ui/DataTable";

interface {mobile_config.name}PageProps {{
  // Add mobile-specific props as needed
}}

export const {mobile_config.name}Page: React.FC<{mobile_config.name}PageProps> = () => {{
  const {{ data, loading, error }} = usePageData("{original_name.lower()}");

  return (
    <div className="uitest-mobile-container-padded">
      <MobileChessboardLayout
        topPieces={{<div className="uitest-mobile-pieces">{original_name} Top Pieces</div>}}
        center={{<DataTable data={{data}} loading={{loading}} error={{error}} />}}
        bottomPieces={{<div className="uitest-mobile-pieces">{original_name} Bottom Pieces</div>}}
      />
    </div>
  );
}};
'''
        file_path = self.pages_dir / mobile_config.parent / f"{mobile_config.name}Page.tsx"
        self._write_file(file_path, content)


    def _create_instruction_file(self, config: PageConfig) -> None:
        """Create instruction file that will be auto-discovered"""
        content = f'''export const pageInstructions = {{
  id: '{config.name.lower()}',
  title: '{config.name} Instructions',
  instructions: [
    '{config.description or f"Use this page to work with {config.name.lower()} features"}',
    'Use the action sheet to interact with available options',
    'This page automatically adapts between mobile and desktop layouts'
  ]
}}'''
        file_path = self.instructions_pages_dir / f"{config.name.lower()}.ts"
        self._write_file(file_path, content)

    def _create_action_file(self, config: PageConfig) -> None:
        """Create action file that will be auto-discovered"""
        content = f'''import {{ EyeOff }} from 'lucide-react'
import type {{ ActionSheetAction }} from '../../../types/core/action-sheet.types'

export const pageActions = {{
  id: '{config.name.lower()}',
  actions: [
    {{
      id: 'toggle-{config.name.lower()}',
      label: 'Toggle {config.name}',
      icon: EyeOff,
      variant: 'default'
    }}
  ] as ActionSheetAction[]
}}'''
        file_path = self.actions_pages_dir / f"{config.name.lower()}.ts"
        self._write_file(file_path, content)

    def _update_parent_page_routing(self, config: PageConfig) -> None:
        """Update parent page with routing logic for new child page"""
        # Case-insensitive search for parent page file
        parent_dir = self.pages_dir / config.parent
        parent_page_path = None
        
        if parent_dir.exists():
            # Find parent page file by looking for files containing parent name (case insensitive)
            parent_name_lower = config.parent.lower()
            # Handle plural/singular variations (e.g., uitests -> uitest)
            parent_name_singular = parent_name_lower.rstrip('s') if parent_name_lower.endswith('s') else parent_name_lower
            
            for file in parent_dir.glob("*.tsx"):
                filename_lower = file.name.lower()
                # Skip main pages and look for the actual parent routing page
                if (('page' in filename_lower and 'main' not in filename_lower and
                     not filename_lower.startswith('mobile')) and
                    (parent_name_lower in filename_lower or 
                     parent_name_singular in filename_lower or
                     filename_lower.startswith(parent_name_lower) or
                     filename_lower.startswith(parent_name_singular))):
                    parent_page_path = file
                    break
        
        if not parent_page_path:
            print(f"⚠️  Could not find parent page file in: {parent_dir}")
            return
        
        content = parent_page_path.read_text()
        
        # Add import for single wrapper
        wrapper_import = f"import {{ {config.name}PageWrapper }} from \"../../components/{config.parent}/{config.name}PageWrapper\";"
        
        # Find import section and add new import
        import_lines = []
        other_lines = []
        in_imports = True
        
        for line in content.split('\n'):
            if line.startswith('import ') or line.startswith('from '):
                import_lines.append(line)
            elif line.strip() == '' and in_imports:
                import_lines.append(line)
            else:
                in_imports = False
                other_lines.append(line)
        
        # Add new import
        import_lines.append(wrapper_import)
        
        # Find the routing logic section and add new condition
        page_id = config.name.lower()
        
        # Single wrapper handles mobile switching internally
        new_routing = f'''  }} else if (currentChildPage === "{page_id}") {{
    CurrentPageComponent = {config.name}PageWrapper;'''
        
        # Insert routing logic before the closing brace of the routing section
        updated_content = []
        for i, line in enumerate(other_lines):
            updated_content.append(line)
            # Look for pattern like "} else if (currentChildPage === " to insert before the final }
            if ('CurrentPageComponent = ' in line and 
                i < len(other_lines) - 1 and 
                other_lines[i + 1].strip() in ['}', '  }']):
                updated_content.append(new_routing)
        
        # Rebuild content
        final_content = '\n'.join(import_lines + [''] + updated_content)
        parent_page_path.write_text(final_content)
        print(f"  📝 Updated parent page: {parent_page_path.name}")

    def _update_action_sheet_container(self, config: PageConfig) -> None:
        """Update ActionSheetContainer.tsx with action handler mappings for child page"""
        # Try multiple possible locations for ActionSheetContainer
        possible_paths = [
            self.frontend_root / "src" / "components" / "action-sheet" / "ActionSheetContainer.tsx",
            self.frontend_root / "src" / "components" / "ui" / "ActionSheetContainer.tsx"
        ]
        
        container_path = None
        for path in possible_paths:
            if path.exists():
                container_path = path
                break
                
        if not container_path:
            # Create ActionSheetContainer in the preferred location
            container_path = self.frontend_root / "src" / "components" / "ui" / "ActionSheetContainer.tsx"
            print(f"📝 ActionSheetContainer.tsx not found - creating at: {container_path}")
            self._create_action_sheet_container(container_path, config)
            return
        
        content = container_path.read_text()
        page_id = config.name.lower()
        
        # Check if this is a dynamic action system (frontend-v2) or static actionMap system (frontend)
        if 'DYNAMIC_PAGE_ACTIONS' in content:
            # Frontend-v2 uses dynamic action system - no need to update ActionSheetContainer
            # Actions are handled through the dynamic page action files
            print(f"  ✅ Detected dynamic action system - ActionSheetContainer uses DYNAMIC_PAGE_ACTIONS")
            print(f"     Child page actions will be loaded automatically from pages/{page_id}.ts")
            return
        
        # Legacy frontend system with actionMap
        # Add action handler mapping for child page  
        handler_mapping = f'''      {page_id}: {{
        'toggle-{page_id}': () => {{
          window.dispatchEvent(new CustomEvent('{page_id}-toggle'));
        }},
        // Navigation actions
        'go-to-{config.parent.lower()}': uiTestsActions.goTo{config.parent.capitalize()}
      }},'''
        
        # Find the actionMap and insert before the closing brace
        if f'{page_id}:' not in content:
            lines = content.split('\n')
            
            # Find the actionMap object and its closing brace
            for i, line in enumerate(lines):
                if 'const actionMap:' in line and 'Record<string, Record<string, Fn>>' in line:
                    # Find the matching closing brace for actionMap
                    brace_count = 0
                    for j in range(i, len(lines)):
                        if '{' in lines[j]:
                            brace_count += lines[j].count('{')
                        if '}' in lines[j]:
                            brace_count -= lines[j].count('}')
                            if brace_count == 0:
                                # Insert before the closing brace
                                lines.insert(j, handler_mapping)
                                break
                    break
            
            updated_content = '\n'.join(lines)
            container_path.write_text(updated_content)
            print(f"  📝 Updated ActionSheetContainer.tsx with {config.name} handlers")
        else:
            print(f"  ⚠️  Could not find actionMap in ActionSheetContainer.tsx")

    def _update_parent_page_actions(self, config: PageConfig) -> None:
        """Update parent page action constants to include navigation to child page"""
        # Try both legacy and dynamic action file locations
        constants_path = self.frontend_root / "src" / "constants" / "actions" / "page-actions.constants.ts"
        parent_action_path = self.frontend_root / "src" / "constants" / "actions" / "pages" / f"{config.parent.lower()}.ts"
        
        # Check if using dynamic system (frontend-v2)
        if parent_action_path.exists():
            self._update_parent_dynamic_actions(config, parent_action_path)
            return
        
        # Check if using legacy system (frontend)    
        if constants_path.exists():
            self._update_parent_legacy_actions(config, constants_path)
            return
            
        # Neither exists - create dynamic action file for parent
        print(f"📝 No parent action file found - creating dynamic action file for {config.parent}")
        self._create_parent_dynamic_actions(config, parent_action_path)

    def _create_action_sheet_container(self, container_path: Path, config: PageConfig) -> None:
        """Create a new ActionSheetContainer.tsx with dynamic action system support"""
        content = '''import React, { useEffect, useState } from 'react';
import { DYNAMIC_PAGE_ACTIONS } from '../../constants/actions/page-actions.dynamic';
import { useActionSheet } from '../../contexts/ActionSheetContext';
import { useAppStore } from '../../stores/appStore';
import type { ActionSheetAction } from '../../types/core/action-sheet.types';

export const ActionSheetContainer: React.FC = () => {
  const { isOpen, currentPage, closeActionSheet } = useActionSheet();
  const currentChildPage = useAppStore((state) => state.currentChildPage);
  const [delayedActionSheetPage, setDelayedActionSheetPage] = useState<string | null>(null);

  // Use child page if it exists, otherwise use current tab
  const actionSheetPage = currentChildPage || currentPage;

  // Delay loading to ensure dynamic system is initialized
  useEffect(() => {
    if (actionSheetPage) {
      const timer = setTimeout(() => {
        setDelayedActionSheetPage(actionSheetPage);
      }, 100);
      return () => clearTimeout(timer);
    } else {
      setDelayedActionSheetPage(null);
    }
  }, [actionSheetPage]);

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
                    closeActionSheet();
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
            className="w-full mt-4 p-3 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
            onClick={closeActionSheet}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};
'''
        
        self._write_file(container_path, content)
        print(f"  ✅ Created new ActionSheetContainer.tsx with dynamic action support")

    def _update_parent_dynamic_actions(self, config: PageConfig, parent_action_path: Path) -> None:
        """Update parent page dynamic action file with navigation to child page"""
        content = parent_action_path.read_text()
        page_id = config.name.lower()
        
        # Add navigation action with onPress handler
        nav_action = f"""    {{
      id: 'go-to-{page_id}',
      label: 'Go to {config.name}',
      icon: Navigation,
      variant: 'secondary',
      onPress: () => {{
        const setCurrentChildPage = useAppStore.getState().setCurrentChildPage;
        setCurrentChildPage('{page_id}');
      }}
    }}"""
        
        # Check if navigation action already exists
        if f"'go-to-{page_id}'" not in content:
            # Add import for useAppStore if not present
            if 'useAppStore' not in content:
                content = content.replace(
                    "import type { ActionSheetAction }",
                    "import { useAppStore } from '../../../stores/appStore';\nimport type { ActionSheetAction }"
                )
            
            # Find the actions array and insert navigation action
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'actions: [' in line:
                    # Insert after the opening bracket
                    lines.insert(i + 1, nav_action + ',')
                    break
            
            updated_content = '\n'.join(lines)
            parent_action_path.write_text(updated_content)
            print(f"  📝 Updated {config.parent} dynamic actions with go-to-{page_id} navigation")

    def _update_parent_legacy_actions(self, config: PageConfig, constants_path: Path) -> None:
        """Update legacy parent page action constants file"""
        content = constants_path.read_text()
        page_id = config.name.lower()
        parent_id = config.parent.lower()
        
        # Add navigation action to parent page actions
        nav_action = f"""    {{
      id: 'go-to-{page_id}',
      label: 'Go to {config.name}',
      icon: Navigation,
      variant: 'secondary'
    }}"""
        
        # Find the parent page actions and add the navigation action
        if f"'go-to-{page_id}'" not in content:
            # Look for the parent page actions section
            parent_section_start = f'{parent_id}: ['
            parent_section_merging = f'{parent_id}: mergeWithCommonActions(['
            
            if parent_section_start in content:
                # Simple array format
                insertion_point = content.find(parent_section_start) + len(parent_section_start)
                updated_content = (content[:insertion_point] + 
                                 f'\n{nav_action},' + 
                                 content[insertion_point:])
                constants_path.write_text(updated_content)
                
            elif parent_section_merging in content:
                # mergeWithCommonActions format - add to first parameter array
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if f'{parent_id}: mergeWithCommonActions([' in line:
                        # Find the closing bracket of the first array parameter
                        brace_count = 0
                        start_found = False
                        for j in range(i, len(lines)):
                            if '[' in lines[j]:
                                brace_count += lines[j].count('[')
                                start_found = True
                            if ']' in lines[j]:
                                brace_count -= lines[j].count(']')
                                if brace_count == 0 and start_found:
                                    # Insert before the closing bracket
                                    if not lines[j-1].strip().endswith(','):
                                        lines[j-1] += ','
                                    lines.insert(j, f'{nav_action}')
                                    break
                        break
                        
                updated_content = '\n'.join(lines)
                constants_path.write_text(updated_content)
                
            print(f"  📝 Updated {config.parent} legacy actions with go-to-{page_id} navigation")

    def _create_parent_dynamic_actions(self, config: PageConfig, parent_action_path: Path) -> None:
        """Create a new dynamic action file for parent page with navigation to child"""
        page_id = config.name.lower()
        parent_id = config.parent.lower()
        
        content = f'''import {{ Navigation, Play, Settings }} from 'lucide-react'
import {{ useAppStore }} from '../../../stores/appStore';
import type {{ ActionSheetAction }} from '../../../types/core/action-sheet.types'

export const pageActions = {{
  id: '{parent_id}',
  actions: [
    {{
      id: 'go-to-{page_id}',
      label: 'Go to {config.name}',
      icon: Navigation,
      variant: 'secondary',
      onPress: () => {{
        const setCurrentChildPage = useAppStore.getState().setCurrentChildPage;
        setCurrentChildPage('{page_id}');
      }}
    }},
    {{
      id: '{parent_id}-action',
      label: '{config.parent.capitalize()} Action',
      icon: Navigation,
      variant: 'default'
    }},
    {{
      id: '{parent_id}-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    }},
    {{
      id: '{parent_id}-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }}
  ] as ActionSheetAction[]
}}'''
        
        self._write_file(parent_action_path, content)
        print(f"  ✅ Created new {config.parent} dynamic action file with navigation to {config.name}")

    def _write_file(self, file_path: Path, content: str) -> None:
        """Write content to file, creating directories as needed"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"  📝 Created: {file_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate React pages using Dynamic File Loading Architecture'
    )
    parser.add_argument('command', choices=['child'], help='Type of page to create')
    parser.add_argument('name', help='Name of the page (PascalCase)')
    parser.add_argument('--parent', required=True, help='Parent page name (required for child pages)')
    parser.add_argument('--mobile', action='store_true', help='Create mobile variant')
    parser.add_argument('--icon', default='Navigation', help='Lucide icon name')
    parser.add_argument('--description', help='Description for the page')
    parser.add_argument('--frontend-root', default='../../../frontend', help='Frontend root directory')

    args = parser.parse_args()

    # Resolve frontend root path
    script_dir = Path(__file__).parent
    frontend_root = script_dir / args.frontend_root
    frontend_root = frontend_root.resolve()

    if not frontend_root.exists():
        print(f"❌ Frontend root directory not found: {frontend_root}")
        sys.exit(1)

    generator = DynamicPageGenerator(str(frontend_root))
    
    config = PageConfig(
        name=args.name,
        parent=args.parent,
        mobile=args.mobile,
        icon=args.icon,
        description=args.description or ""
    )

    try:
        if args.command == 'child':
            generator.create_child_page(config)
        print(f"\n🎉 Dynamic page generation completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()