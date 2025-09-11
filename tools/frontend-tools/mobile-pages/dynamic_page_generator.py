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
        
        print(f"✅ Child page '{config.name}' created successfully!")
        if config.mobile:
            print(f"✅ Mobile variant 'Mobile{config.name}' created successfully!")
        print(f"✅ Single responsive wrapper created!")
        print(f"✅ Parent page routing updated automatically!")
            
        print(f"\n📋 Architecture improvements:")
        print(f"   ✅ Single wrapper with internal mobile switching")
        print(f"   ✅ Reduced component duplication")
        print(f"   ✅ Cleaner parent routing logic")
        print(f"   ✅ Mobile switching handled in wrapper, not parent")
        
    def _create_child_page_component(self, config: PageConfig) -> None:
        """Create the main child page component"""
        content = f'''import React from "react";

interface {config.name}PageProps {{
  // Add props as needed
}}

export const {config.name}Page: React.FC<{config.name}PageProps> = () => {{
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6">
      <h1 className="text-2xl font-bold text-white mb-4">
        {config.name} Page
      </h1>
      <p className="text-slate-300 text-center max-w-md">
        {config.description or f"Welcome to the {config.name.lower()} page. Use the action menu to interact with available options."}
      </p>
    </div>
  );
}};
'''
        file_path = self.pages_dir / config.parent / f"{config.name}Page.tsx"
        self._write_file(file_path, content)

    def _create_responsive_wrapper(self, config: PageConfig) -> None:
        """Create single responsive wrapper component that handles mobile switching"""
        if config.mobile:
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
}};
'''
        else:
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
        self._write_file(file_path, content)

    def _create_mobile_child_page(self, mobile_config: PageConfig, original_name: str) -> None:
        """Create mobile version of child page"""
        content = f'''import React from "react";

interface {mobile_config.name}PageProps {{
  // Add mobile-specific props as needed
}}

export const {mobile_config.name}Page: React.FC<{mobile_config.name}PageProps> = () => {{
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-4">
      <h1 className="text-xl font-bold text-white mb-3">
        {original_name} (Mobile)
      </h1>
      <p className="text-slate-300 text-center text-sm max-w-xs">
        {mobile_config.description or f"Mobile-optimized {original_name.lower()} interface."}
      </p>
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
        parent_page_path = self.pages_dir / config.parent / f"{config.parent.capitalize()}Page.tsx"
        if not parent_page_path.exists():
            # Try common variations
            parent_page_path = self.pages_dir / config.parent / f"UI{config.parent.capitalize()}Page.tsx"
            if not parent_page_path.exists():
                parent_page_path = self.pages_dir / config.parent / f"{config.parent}Page.tsx"
        
        if not parent_page_path.exists():
            print(f"⚠️  Could not find parent page file: {parent_page_path}")
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