#!/usr/bin/env python3
"""
Frontend Page Generator CLI Tool

Follows the Phase 2 Mobile Switching Architecture documented in:
/mnt/c/Projects/chessboard-vanilla-v2/docs/47-navigation-action-sheets-architecture.md

Automates creation of:
- Parent pages with routing and mobile switching
- Child pages with wrappers and mobile variants
- Action configurations and hooks
- Instruction configurations
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class PageConfig:
    name: str
    parent: Optional[str] = None
    mobile: bool = False
    icon: str = "Navigation"
    description: str = ""

class PageGenerator:
    def __init__(self, frontend_root: str):
        self.frontend_root = Path(frontend_root)
        self.pages_dir = self.frontend_root / "src" / "pages"
        self.components_dir = self.frontend_root / "src" / "components"
        self.hooks_dir = self.frontend_root / "src" / "hooks"
        self.constants_dir = self.frontend_root / "src" / "constants"
        self.services_dir = self.frontend_root / "src" / "services"
        
    def create_parent_page(self, config: PageConfig) -> None:
        """Create a parent page with all required files"""
        print(f"Creating parent page: {config.name}")
        
        # Create directories
        parent_pages_dir = self.pages_dir / config.name
        parent_components_dir = self.components_dir / config.name
        parent_hooks_dir = self.hooks_dir / config.name
        
        parent_pages_dir.mkdir(parents=True, exist_ok=True)
        parent_components_dir.mkdir(parents=True, exist_ok=True)
        parent_hooks_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate files
        self._create_parent_main_page(config)
        self._create_parent_router_page(config)
        self._create_parent_actions_hook(config)
        self._create_parent_instructions(config)
        self._create_parent_action_constants(config)
        self._update_common_actions(config)
        
        print(f"✅ Parent page '{config.name}' created successfully")
        print(f"📝 Manual steps needed:")
        print(f"   1. Add to TabId type in src/components/layout/types.ts")
        print(f"   2. Add tab configuration in src/components/layout/TabBar.tsx") 
        print(f"   3. Add routing in src/App.tsx")
        
    def create_child_page(self, config: PageConfig) -> None:
        """Create a child page with wrapper and optional mobile variant"""
        if not config.parent:
            raise ValueError("Child pages must specify a parent")
            
        print(f"Creating child page: {config.name} (parent: {config.parent})")
        
        # Create child page
        self._create_child_page_component(config)
        self._create_child_page_wrapper(config)
        
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
            self._create_mobile_child_wrapper(mobile_config, config.name)
        
        # Update parent routing
        self._update_parent_routing(config)
        
        # Update action configurations
        self._update_parent_actions(config)
        self._update_action_constants(config)
        self._update_action_handlers(config)
        
        # Update instructions
        self._update_instructions(config)
        
        print(f"✅ Child page '{config.name}' created successfully")
        if config.mobile:
            print(f"✅ Mobile variant 'Mobile{config.name}' created successfully")

    def _create_parent_main_page(self, config: PageConfig) -> None:
        """Create the main page component for parent"""
        content = f'''import React from "react";
import {{ useAppStore }} from "../../stores/appStore";

export const {config.name}MainPage: React.FC = () => {{
  return (
    <div className="relative h-full">
      <section className="space-y-4">
        <div className="card-gaming p-8">
          <h1 className="text-2xl font-bold mb-4">{config.name}</h1>
          <p className="text-muted-foreground">
            {config.description or f"Welcome to the {config.name} section. Use the action sheet to navigate to specific {config.name.lower()} features."}
          </p>
        </div>
      </section>
    </div>
  );
}};
'''
        file_path = self.pages_dir / config.name / f"{config.name}MainPage.tsx"
        self._write_file(file_path, content)

    def _create_parent_router_page(self, config: PageConfig) -> None:
        """Create the router page for parent with child routing"""
        content = f'''import React from "react";
import {{ useAppStore }} from "../../stores/appStore";
import {{ useIsMobile }} from "../../hooks/core/useIsMobile";
import {{ {config.name}MainPage }} from "./{config.name}MainPage";

export const {config.name}Page: React.FC = () => {{
  const currentChildPage = useAppStore((state) => state.currentChildPage);
  const isMobile = useIsMobile();

  // Determine which component to render
  let CurrentPageComponent = {config.name}MainPage;

  // Add child page routing here as pages are created
  // Example:
  // if (currentChildPage === "childpage") {{
  //   CurrentPageComponent = isMobile ? MobileChildPageWrapper : ChildPageWrapper;
  // }}

  return (
    <div className="relative h-full">
      {{/* Current page content - use key to force re-mount when switching components */}}
      <CurrentPageComponent key={{`${{currentChildPage}}-${{isMobile ? 'mobile' : 'desktop'}}`}} />
    </div>
  );
}};
'''
        file_path = self.pages_dir / config.name / f"{config.name}Page.tsx"
        self._write_file(file_path, content)

    def _create_parent_actions_hook(self, config: PageConfig) -> None:
        """Create actions hook for parent"""
        content = f'''import {{ useCallback }} from 'react';
import {{ useAppStore }} from '../../stores/appStore';

/**
 * {config.name} page actions hook
 * Handles actions specific to the {config.name.lower()} section
 */
export function use{config.name}Actions() {{
  const setCurrentChildPage = useAppStore((state) => state.setCurrentChildPage);

  // Navigation actions to child pages will be added here
  // Example:
  // const goToChildPage = useCallback(() => {{
  //   setTimeout(() => {{
  //     setCurrentChildPage('childpage');
  //   }}, 100);
  // }}, [setCurrentChildPage]);

  return {{
    // Add child navigation actions here
  }};
}}
'''
        file_path = self.hooks_dir / config.name / f"use{config.name}Actions.ts"
        self._write_file(file_path, content)

    def _create_parent_instructions(self, config: PageConfig) -> None:
        """Create instructions for parent"""
        content = f'''export const {config.name.lower()}Instructions = {{
  title: '{config.name} Instructions',
  instructions: [
    'Welcome to the {config.name.lower()} section',
    'Use the action sheet to navigate to specific features',
    'Each feature has its own dedicated interface and tools',
    'Features automatically adapt between mobile and desktop layouts'
  ]
}};
'''
        file_path = self.services_dir / "instructions" / "pages" / f"{config.name.lower()}.instructions.ts"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self._write_file(file_path, content)

    def _create_parent_action_constants(self, config: PageConfig) -> None:
        """Create action constants for parent"""
        # This will be added to the main page-actions.constants.ts file
        # We'll update it when child pages are added
        pass

    def _create_child_page_component(self, config: PageConfig) -> None:
        """Create child page component"""
        content = f'''import React, {{ useState, useEffect }} from "react";

export const {config.name}Page: React.FC = () => {{
  const [isActive, setIsActive] = useState(true);

  // Example of global action listener
  useEffect(() => {{
    const handleToggle = () => {{
      setIsActive(prev => !prev);
    }};

    // Listen for custom events from action sheet
    window.addEventListener('{config.name.lower()}-toggle', handleToggle);
    
    return () => {{
      window.removeEventListener('{config.name.lower()}-toggle', handleToggle);
    }};
  }}, []);

  return (
    <div className="relative h-full">
      <section className="space-y-4">
        {{isActive && (
          <div className="card-gaming p-8">
            <h1 className="text-2xl font-bold mb-4">{config.name}</h1>
            <p className="text-muted-foreground">
              {config.description or f"This is the {config.name.lower()} page. Use the action sheet to interact with this feature."}
            </p>
          </div>
        )}}
      </section>
    </div>
  );
}};
'''
        file_path = self.pages_dir / config.parent / f"{config.name}Page.tsx"
        self._write_file(file_path, content)

    def _create_child_page_wrapper(self, config: PageConfig) -> None:
        """Create wrapper for child page"""
        content = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageActions }} from "../../hooks/core/usePageActions";
import {{ {config.name}Page }} from "../../pages/{config.parent}/{config.name}Page";

export const {config.name}PageWrapper: React.FC = () => {{
  usePageInstructions("{config.name.lower()}");
  usePageActions("{config.name.lower()}");

  return <{config.name}Page />;
}};
'''
        file_path = self.components_dir / config.parent / f"{config.name}PageWrapper.tsx"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self._write_file(file_path, content)

    def _create_mobile_child_page(self, mobile_config: PageConfig, original_name: str) -> None:
        """Create mobile variant of child page"""
        content = f'''import React, {{ useState, useEffect }} from "react";

export const {mobile_config.name}Page: React.FC = () => {{
  const [isActive, setIsActive] = useState(true);

  // Example of global action listener (shared with desktop)
  useEffect(() => {{
    const handleToggle = () => {{
      setIsActive(prev => !prev);
    }};

    // Listen for same events as desktop version
    window.addEventListener('{original_name.lower()}-toggle', handleToggle);
    
    return () => {{
      window.removeEventListener('{original_name.lower()}-toggle', handleToggle);
    }};
  }}, []);

  return (
    <div className="relative h-full">
      {{/* Mobile-optimized layout */}}
      <section className="space-y-2 p-4">
        {{isActive && (
          <div className="card-gaming p-4">
            <h1 className="text-xl font-bold mb-2">{original_name}</h1>
            <p className="text-sm text-muted-foreground">
              Mobile version - {mobile_config.description}
            </p>
          </div>
        )}}
      </section>
    </div>
  );
}};
'''
        file_path = self.pages_dir / mobile_config.parent / f"{mobile_config.name}Page.tsx"
        self._write_file(file_path, content)

    def _create_mobile_child_wrapper(self, mobile_config: PageConfig, original_name: str) -> None:
        """Create wrapper for mobile child page"""
        content = f'''import React from "react";
import {{ usePageInstructions }} from "../../hooks/core/usePageInstructions";
import {{ usePageActions }} from "../../hooks/core/usePageActions";
import {{ {mobile_config.name}Page }} from "../../pages/{mobile_config.parent}/{mobile_config.name}Page";

export const {mobile_config.name}PageWrapper: React.FC = () => {{
  usePageInstructions("{original_name.lower()}");  // Shared instructions with desktop version
  usePageActions("{original_name.lower()}");       // Shared actions with desktop version

  return <{mobile_config.name}Page />;
}};
'''
        file_path = self.components_dir / mobile_config.parent / f"{mobile_config.name}PageWrapper.tsx"
        self._write_file(file_path, content)

    def _update_parent_routing(self, config: PageConfig) -> None:
        """Update parent router with child page routing"""
        router_file = self.pages_dir / config.parent / f"{config.parent}Page.tsx"
        
        if not router_file.exists():
            print(f"⚠️  Parent router file not found: {router_file}")
            return
        
        content = router_file.read_text()
        
        # Add import for child wrapper
        import_line = f'import {{ {config.name}PageWrapper }} from "../../components/{config.parent}/{config.name}PageWrapper";'
        if config.mobile:
            import_line += f'\nimport {{ Mobile{config.name}PageWrapper }} from "../../components/{config.parent}/Mobile{config.name}PageWrapper";'
        
        # Find import section and add new import
        if 'import {' in content and f'{config.name}PageWrapper' not in content:
            lines = content.split('\n')
            last_import_idx = -1
            for i, line in enumerate(lines):
                if line.startswith('import '):
                    last_import_idx = i
            
            if last_import_idx >= 0:
                lines.insert(last_import_idx + 1, import_line)
                content = '\n'.join(lines)
        
        # Add routing logic
        routing_logic = f'''
  if (currentChildPage === "{config.name.lower()}") {{'''
        
        if config.mobile:
            routing_logic += f'''
    CurrentPageComponent = isMobile ? Mobile{config.name}PageWrapper : {config.name}PageWrapper;'''
        else:
            routing_logic += f'''
    CurrentPageComponent = {config.name}PageWrapper;'''
        
        routing_logic += '''
  }'''
        
        # Insert routing logic before the return statement
        if f'currentChildPage === "{config.name.lower()}"' not in content:
            content = content.replace(
                '  // Add child page routing here as pages are created',
                f'  // Add child page routing here as pages are created{routing_logic}'
            )
        
        self._write_file(router_file, content)

    def _update_parent_actions(self, config: PageConfig) -> None:
        """Update parent actions hook with child navigation"""
        actions_file = self.hooks_dir / config.parent / f"use{config.parent}Actions.ts"
        
        if not actions_file.exists():
            print(f"⚠️  Parent actions file not found: {actions_file}")
            return
        
        content = actions_file.read_text()
        
        # Add navigation action
        action_func = f'''
  const goTo{config.name} = useCallback(() => {{
    setTimeout(() => {{
      setCurrentChildPage('{config.name.lower()}');
    }}, 100);
  }}, [setCurrentChildPage]);'''
        
        # Add to actions if not already present
        if f'goTo{config.name}' not in content:
            content = content.replace(
                '  // Navigation actions to child pages will be added here',
                f'  // Navigation actions to child pages will be added here{action_func}'
            )
            
            # Update return statement
            content = content.replace(
                '    // Add child navigation actions here',
                f'    goTo{config.name}'
            )
        
        self._write_file(actions_file, content)

    def _update_action_constants(self, config: PageConfig) -> None:
        """Update page action constants"""
        constants_file = self.constants_dir / "actions" / "page-actions.constants.ts"
        
        if not constants_file.exists():
            print(f"⚠️  Page actions constants file not found: {constants_file}")
            return
        
        content = constants_file.read_text()
        
        # Add action configuration for child page
        action_config = f'''  {config.name.lower()}: mergeWithCommonActions([
    {{
      id: 'toggle-{config.name.lower()}',
      label: 'Toggle {config.name}',
      icon: EyeOff,
      variant: 'default'
    }}
  ], ['go-to-{config.parent.lower()}']),'''
        
        # Insert before the closing brace
        if f'{config.name.lower()}:' not in content:
            content = content.replace(
                '}',
                action_config + '\n}',
                1  # Only replace the first occurrence (end of export)
            )
        
        self._write_file(constants_file, content)

    def _update_action_handlers(self, config: PageConfig) -> None:
        """Update action sheet handlers"""
        handler_file = self.components_dir / "action-sheet" / "ActionSheetContainer.tsx"
        
        if not handler_file.exists():
            print(f"⚠️  Action sheet container file not found: {handler_file}")
            return
        
        content = handler_file.read_text()
        
        # Add action handler mapping
        handler_mapping = f'''      {config.name.lower()}: {{
        'toggle-{config.name.lower()}': () => {{
          window.dispatchEvent(new CustomEvent('{config.name.lower()}-toggle'));
        }},
        // Navigation actions
        'go-to-{config.parent.lower()}': {config.parent.lower()}Actions.goTo{config.parent}
      }},'''
        
        # Insert before the closing brace of actionMap
        if f'{config.name.lower()}:' not in content:
            # Find the actionMap closing brace
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'actionMap:' in line and '{' in line:
                    # Find matching closing brace
                    brace_count = 1
                    start_idx = i + 1
                    for j in range(start_idx, len(lines)):
                        if '{' in lines[j]:
                            brace_count += lines[j].count('{')
                        if '}' in lines[j]:
                            brace_count -= lines[j].count('}')
                            if brace_count == 0:
                                lines.insert(j, handler_mapping)
                                break
                    break
            content = '\n'.join(lines)
        
        self._write_file(handler_file, content)

    def _update_instructions(self, config: PageConfig) -> None:
        """Update instructions service with child page instructions"""
        instructions_file = self.services_dir / "instructions" / "InstructionsService.ts"
        
        if not instructions_file.exists():
            print(f"⚠️  Instructions service file not found: {instructions_file}")
            return
        
        content = instructions_file.read_text()
        
        # Add instruction mapping
        default_desc = f"Use this page to work with {config.name.lower()} features"
        instruction_mapping = f'''
    this.instructionsMap.set('{config.name.lower()}', {{
      title: '{config.name} Instructions',
      instructions: [
        '{config.description or default_desc}',
        'Use the action sheet to interact with available options',
        'This page automatically adapts between mobile and desktop layouts'
      ]
    }});'''
        
        # Insert before the closing brace of constructor
        if f"'{config.name.lower()}'," not in content:
            content = content.replace(
                '  }\\n\\n  private',
                instruction_mapping + '\\n  }\\n\\n  private'
            )
        
        self._write_file(instructions_file, content)

    def _update_common_actions(self, config: PageConfig) -> None:
        """Update common actions with navigation to new parent"""
        common_actions_file = self.constants_dir / "actions" / "common-actions.constants.ts"
        
        if not common_actions_file.exists():
            print(f"⚠️  Common actions file not found: {common_actions_file}")
            return
        
        content = common_actions_file.read_text()
        
        # Add navigation action to parent
        nav_action = f'''  'go-to-{config.name.lower()}': {{
    id: 'go-to-{config.name.lower()}',
    label: 'Go to {config.name}',
    icon: {config.icon},
    variant: 'secondary'
  }},'''
        
        # Insert into COMMON_ACTIONS
        if f"'go-to-{config.name.lower()}'" not in content:
            # Find a good place to insert (before the export)
            content = content.replace(
                '} as const',
                nav_action + '\\n} as const'
            )
        
        self._write_file(common_actions_file, content)

    def _write_file(self, file_path: Path, content: str) -> None:
        """Write content to file, creating directories if needed"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"  📝 Created: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate React pages following Phase 2 Mobile Switching Architecture")
    parser.add_argument("command", choices=["parent", "child"], help="Type of page to create")
    parser.add_argument("name", help="Name of the page (PascalCase)")
    parser.add_argument("--parent", help="Parent page name (required for child pages)")
    parser.add_argument("--mobile", action="store_true", help="Create mobile variant (child pages only)")
    parser.add_argument("--icon", default="Navigation", help="Lucide icon name (default: Navigation)")
    parser.add_argument("--description", help="Description for the page")
    parser.add_argument("--frontend-root", default="/mnt/c/Projects/chessboard-vanilla-v2/frontend", help="Frontend root directory")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.command == "child" and not args.parent:
        print("❌ Error: Child pages must specify --parent")
        sys.exit(1)
    
    # Create page configuration
    config = PageConfig(
        name=args.name,
        parent=args.parent,
        mobile=args.mobile,
        icon=args.icon,
        description=args.description or ""
    )
    
    # Initialize generator
    generator = PageGenerator(args.frontend_root)
    
    try:
        if args.command == "parent":
            generator.create_parent_page(config)
        else:
            generator.create_child_page(config)
            
        print("\\n🎉 Page generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()