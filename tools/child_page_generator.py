#!/usr/bin/env python3
"""
Child Page Generator Tool

Automates the creation of child pages and their associated files for the responsive chessboard application.
This tool handles all the repetitive tasks of creating child pages, wrappers, actions, and updating existing files.

Usage:
    python child_page_generator.py --parent uitests --children "newtest,anothertest" --actions "test-action:Test Action:TestTube:default,another-action:Another Action:Settings:secondary"

Author: Automated tooling for responsive chessboard project
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class ChildPageConfig:
    """Configuration for a child page"""
    id: str
    name: str
    component_name: str
    wrapper_name: str
    hook_name: str
    actions: List[Dict[str, str]]

@dataclass
class ActionConfig:
    """Configuration for an action"""
    id: str
    label: str
    icon: str
    variant: str

class ChildPageGenerator:
    """Main class for generating child pages and their associated files"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.src_path = self.base_path / "poc/chessboard-vanilla-v2/src"
        
    def validate_paths(self) -> bool:
        """Validate that required paths exist"""
        required_paths = [
            self.src_path / "constants/actions/page-actions.constants.ts",
            self.src_path / "components/action-sheet/ActionSheetContainer.tsx",
            self.src_path / "pages",
            self.src_path / "components",
            self.src_path / "hooks"
        ]
        
        for path in required_paths:
            if not path.exists():
                print(f"❌ Required path not found: {path}")
                return False
        return True
    
    def parse_actions(self, actions_str: str) -> List[ActionConfig]:
        """Parse actions from command line format"""
        if not actions_str:
            return []
            
        actions = []
        for action_str in actions_str.split(','):
            parts = action_str.strip().split(':')
            if len(parts) == 4:
                actions.append(ActionConfig(
                    id=parts[0],
                    label=parts[1],
                    icon=parts[2],
                    variant=parts[3]
                ))
            else:
                print(f"⚠️  Invalid action format: {action_str}")
        return actions
    
    def create_child_page_component(self, config: ChildPageConfig, parent: str) -> None:
        """Create the main child page component"""
        # Extract concept name from config.id (e.g., "concept6variant1" -> "concept6")
        concept_name = self.extract_concept_name(config.id)
        css_import = f'import "./{concept_name}.css";' if concept_name else ''
        
        component_content = f'''import React from "react";
{css_import}

export const {config.component_name}: React.FC = () => {{
  return (
    <div className="p-6 {config.id}-container">
      <h1 className="text-2xl font-bold mb-4">{config.name}</h1>
      <div className="space-y-4">
        <p className="text-gray-600">
          This is the {config.name} page. Add your content here.
        </p>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 {config.id}-info-panel">
          <h2 className="text-lg font-semibold text-blue-800 mb-2">Getting Started</h2>
          <ul className="text-blue-700 space-y-1">
            <li>• Implement your page functionality</li>
            <li>• Use the action sheet for page-specific actions</li>
            <li>• Add instructions via the instructions service</li>
            <li>• Customize styling in {concept_name}.css</li>
          </ul>
        </div>
        
        <div className="{config.id}-content">
          <h3 className="text-xl font-semibold mb-2">{config.name} Content</h3>
          <p className="text-gray-500">
            Replace this section with your specific {config.name.lower()} implementation.
          </p>
        </div>
      </div>
    </div>
  );
}};
'''
        
        # Create concept folder structure
        concept_folder = self.get_concept_folder(config.id, parent)
        concept_folder.mkdir(parents=True, exist_ok=True)
        
        component_path = concept_folder / f"{config.component_name}.tsx"
        with open(component_path, 'w') as f:
            f.write(component_content)
        print(f"✅ Created component: {component_path}")
    
    def create_wrapper_component(self, config: ChildPageConfig, parent: str) -> None:
        """Create the wrapper component"""
        # Use pages root barrel export for cleaner imports
        import_statement = f'import {{ {config.component_name} }} from "../pages";'
        
        wrapper_content = f'''import React from "react";
import {{ usePageInstructions }} from "../hooks/usePageInstructions";
import {{ usePageActions }} from "../hooks/usePageActions";
{import_statement}

export const {config.wrapper_name}: React.FC = () => {{
  usePageInstructions("{config.id}");
  usePageActions("{config.id}");

  return <{config.component_name} />;
}};
'''
        
        wrapper_path = self.src_path / "components" / f"{config.wrapper_name}.tsx"
        with open(wrapper_path, 'w') as f:
            f.write(wrapper_content)
        print(f"✅ Created wrapper: {wrapper_path}")
    
    def create_actions_hook(self, config: ChildPageConfig) -> None:
        """Create the actions hook for the child page"""
        actions_list = []
        return_list = []
        
        for action in config.actions:
            function_name = self.camel_case(action.id.replace('-', '_'))
            actions_list.append(f'''  const {function_name} = useCallback(() => {{
    console.log('🎯 [{config.name.upper()}] {action.label}')
    playMove(false)
    // TODO: Implement {action.label} logic
  }}, [playMove])''')
            return_list.append(function_name)
        
        hook_content = f'''import {{ useCallback }} from 'react'
import {{ useChessAudio }} from '../services/audioService'

/**
 * {config.name} page actions
 */
export function {config.hook_name}() {{
  const {{ playMove }} = useChessAudio()

{chr(10).join(actions_list)}

  return {{
    {', '.join(return_list)}
  }}
}}
'''
        
        hook_path = self.src_path / "hooks" / f"{config.hook_name}.ts"
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        print(f"✅ Created actions hook: {hook_path}")
    
    def update_page_actions_constants(self, configs: List[ChildPageConfig]) -> None:
        """Update the PAGE_ACTIONS constants file"""
        constants_path = self.src_path / "constants/actions/page-actions.constants.ts"
        
        with open(constants_path, 'r') as f:
            content = f.read()
        
        # Track new icons that need to be imported
        new_icons = set()
        
        for config in configs:
            if config.id in content:
                print(f"⚠️  Page actions for '{config.id}' already exist, skipping...")
                continue
                
            # Generate actions array and collect icons
            actions_array = []
            for action in config.actions:
                actions_array.append(f'''    {{
      id: '{action.id}',
      label: '{action.label}',
      icon: {action.icon},
      variant: '{action.variant}'
    }}''')
                new_icons.add(action.icon)
            
            actions_str = f''',
  {config.id}: [
{',\n'.join(actions_array)}
  ]'''
            
            # Find the last closing bracket and add before it
            pattern = r'(\s*}\s*)$'
            content = re.sub(pattern, actions_str + r'\1', content)
        
        # Add missing icon imports
        self._add_missing_icons(content, new_icons, constants_path)
        
        with open(constants_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated PAGE_ACTIONS constants")
    
    def _add_missing_icons(self, content: str, new_icons: set, file_path: Path) -> str:
        """Add missing icon imports to the constants file"""
        if not new_icons:
            return content
            
        # Extract existing imports
        import_match = re.search(r'import\s*\{\s*([^}]+)\s*\}\s*from\s*[\'"]lucide-react[\'"]', content)
        
        if import_match:
            existing_imports = {icon.strip() for icon in import_match.group(1).split(',')}
            missing_icons = new_icons - existing_imports
            
            if missing_icons:
                # Add missing icons to import
                all_icons = existing_imports.union(missing_icons)
                sorted_icons = sorted(list(all_icons))
                
                # Format imports nicely (3 per line)
                icon_lines = []
                for i in range(0, len(sorted_icons), 3):
                    icon_lines.append('  ' + ', '.join(sorted_icons[i:i+3]))
                
                new_import = f'''import {{ 
{',\n'.join(icon_lines)}
}} from 'lucide-react\''''
                
                content = re.sub(r'import\s*\{[^}]+\}\s*from\s*[\'"]lucide-react[\'"]', new_import, content)
                
        return content
    
    def update_parent_actions_hook(self, parent: str, configs: List[ChildPageConfig]) -> None:
        """Update the parent's actions hook with navigation functions"""
        hook_pattern = f"use{self.pascal_case(parent)}Actions.ts"
        hook_path = None
        
        # Find the parent's actions hook
        for hook_file in (self.src_path / "hooks").glob("*.ts"):
            if hook_pattern in hook_file.name:
                hook_path = hook_file
                break
        
        if not hook_path:
            print(f"⚠️  Could not find parent actions hook for '{parent}'")
            return
        
        with open(hook_path, 'r') as f:
            content = f.read()
        
        # Ensure audio service import exists
        if "useChessAudio" not in content:
            # Add import after existing imports
            import_pattern = r"(import.*from.*'.*')"
            matches = list(re.finditer(import_pattern, content))
            if matches:
                last_import = matches[-1]
                insert_pos = last_import.end()
                content = content[:insert_pos] + f"\nimport {{ useChessAudio }} from '../services/audioService'" + content[insert_pos:]
        
        # Ensure playMove destructuring exists
        if "playMove" not in content:
            # Add to existing useChessAudio or add new line
            if "useChessAudio" in content:
                content = re.sub(r'const\s*\{\s*([^}]*)\s*\}\s*=\s*useChessAudio\(\)', r'const { \1, playMove } = useChessAudio()', content)
            else:
                # Add after setCurrentChildPage line
                content = re.sub(r'(const\s+setCurrentChildPage[^\n]*\n)', r'\1  const { playMove } = useChessAudio()\n', content)
        
        # Add navigation functions
        new_functions = []
        new_returns = []
        
        for config in configs:
            func_name = f"goTo{config.component_name.replace('Page', '')}"
            
            if func_name not in content:
                new_functions.append(f'''
  const {func_name} = useCallback(() => {{
    setCurrentChildPage('{config.id}')
    playMove(false)
  }}, [setCurrentChildPage, playMove])''')
                new_returns.append(func_name)
        
        # Add functions before return statement
        if new_functions:
            functions_str = ''.join(new_functions)
            return_pattern = r'(\s+return\s*\{)'
            content = re.sub(return_pattern, functions_str + r'\1', content)
            
            # Add to return object (look for the closing brace)
            for return_item in new_returns:
                # Add before closing brace of return object
                content = re.sub(r'(\s+)(\}[^}]*$)', rf'\1  {return_item},\n\1\2', content)
        
        with open(hook_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated parent actions hook: {hook_path}")
    
    def update_parent_page_actions(self, parent: str, configs: List[ChildPageConfig]) -> None:
        """Add navigation actions to parent's PAGE_ACTIONS"""
        constants_path = self.src_path / "constants/actions/page-actions.constants.ts"
        
        with open(constants_path, 'r') as f:
            content = f.read()
        
        # Find the parent section and add navigation actions
        parent_pattern = rf'(\s+{parent}:\s*\[[\s\S]*?)\s*\]'
        
        if re.search(parent_pattern, content):
            new_actions = []
            for config in configs:
                new_actions.append(f'''    {{
      id: 'go-to-{config.id}',
      label: 'Go to {config.name}',
      icon: Navigation,
      variant: 'secondary'
    }}''')
            
            # Add navigation actions before the closing bracket
            actions_str = ',\n' + ',\n'.join(new_actions) + '\n  ]'
            content = re.sub(parent_pattern, r'\1' + actions_str, content)
            
            with open(constants_path, 'w') as f:
                f.write(content)
            print(f"✅ Added navigation actions to parent '{parent}'")
        else:
            print(f"⚠️  Could not find parent section '{parent}' in PAGE_ACTIONS")
    
    def update_action_sheet_container(self, parent: str, configs: List[ChildPageConfig]) -> None:
        """Update ActionSheetContainer with new hooks and mappings"""
        container_path = self.src_path / "components/action-sheet/ActionSheetContainer.tsx"
        
        with open(container_path, 'r') as f:
            content = f.read()
        
        # Add imports for new hooks
        for config in configs:
            hook_import = f"import {{ {config.hook_name} }} from '../../hooks/{config.hook_name}'"
            if hook_import not in content:
                # Find last hook import and add after it
                last_import_pattern = r"(import\s*\{\s*[^}]+\}\s*from\s*'[^']*hooks/[^']*'\s*)"
                matches = list(re.finditer(last_import_pattern, content))
                if matches:
                    last_match = matches[-1]
                    insert_pos = last_match.end()
                    content = content[:insert_pos] + f"\n{hook_import}" + content[insert_pos:]
        
        # Add hook usage  
        for config in configs:
            hook_usage = f"  const {config.id}Actions = {config.hook_name}()"
            if f"{config.id}Actions" not in content:
                # Find last hook usage and add after it
                hook_usage_pattern = r"(\s+const\s+\w+Actions\s*=\s*use\w+Actions\(\))"
                matches = list(re.finditer(hook_usage_pattern, content))
                if matches:
                    last_match = matches[-1]
                    insert_pos = last_match.end()
                    content = content[:insert_pos] + f"\n{hook_usage}" + content[insert_pos:]
        
        # Add parent navigation mappings
        for config in configs:
            parent_mapping = f"'go-to-{config.id}': {parent}Actions.goTo{config.component_name.replace('Page', '')}"
            
            if f"go-to-{config.id}" not in content:
                # Find parent section and add mapping
                parent_section_pattern = rf'(\s+{parent}:\s*\{{[^}}]*)'
                match = re.search(parent_section_pattern, content)
                if match:
                    # Check if there are existing mappings
                    section_content = match.group(1)
                    if section_content.strip().endswith('{'):
                        # First mapping
                        replacement = section_content + f"\n        {parent_mapping}"
                    else:
                        # Additional mapping  
                        replacement = section_content + f",\n        {parent_mapping}"
                    
                    content = content.replace(match.group(1), replacement)
        
        # Add child page mappings
        for config in configs:
            if f"{config.id}:" not in content:
                child_actions = []
                for action in config.actions:
                    func_name = self.camel_case(action.id.replace('-', '_'))
                    child_actions.append(f"        '{action.id}': {config.id}Actions.{func_name}")
                
                child_mapping = f'''      {config.id}: {{
{',\n'.join(child_actions)}
      }},'''
                
                # Find where to insert child mapping (before layouttest)
                insert_pattern = r'(\s+layouttest:\s*\{\})'
                if re.search(insert_pattern, content):
                    content = re.sub(insert_pattern, child_mapping + '\n' + r'\1', content)
        
        # Add to dependencies array
        for config in configs:
            if f"{config.id}Actions" not in content:
                deps_pattern = r'(\], \[currentPage[^]]+)'
                deps_match = re.search(deps_pattern, content)
                if deps_match and f"{config.id}Actions" not in deps_match.group(1):
                    content = re.sub(deps_pattern, rf'\1, {config.id}Actions', content)
        
        with open(container_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated ActionSheetContainer")
    
    def update_parent_page_routing(self, parent: str, configs: List[ChildPageConfig]) -> None:
        """Update parent page component with routing for child pages"""
        # Find the parent page component
        parent_page_path = None
        parent_pages_dir = self.src_path / "pages" / parent
        
        for page_file in parent_pages_dir.glob("*.tsx"):
            if "Page.tsx" in page_file.name and parent.lower() in page_file.name.lower():
                parent_page_path = page_file
                break
        
        if not parent_page_path:
            print(f"⚠️  Could not find parent page component for '{parent}'")
            return
        
        with open(parent_page_path, 'r') as f:
            content = f.read()
        
        # Add imports for wrapper components
        import_pattern = r'(import\s*\{\s*[^}]+\}\s*from\s*"[^"]+Wrapper[^"]+"\s*;)'
        
        for config in configs:
            wrapper_import = f'import {{ {config.wrapper_name} }} from "../../components/{config.wrapper_name}";'
            if wrapper_import not in content:
                content = re.sub(import_pattern, r'\1\n' + wrapper_import, content)
        
        # Add routing conditions
        routing_pattern = r'(\s+if\s*\(\s*currentChildPage\s*===\s*"[^"]+"\s*\)\s*\{[^}]+\})'
        
        for config in configs:
            routing_condition = f''' else if (currentChildPage === "{config.id}") {{
    CurrentPageComponent = {config.wrapper_name};
  }}'''
            
            if f'"{config.id}"' not in content:
                content = re.sub(routing_pattern, r'\1' + routing_condition, content)
        
        with open(parent_page_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated parent page routing: {parent_page_path}")
    
    def create_instructions(self, config: ChildPageConfig) -> None:
        """Create instructions file for the child page"""
        instructions_dir = self.src_path / "services/instructions/pages"
        instructions_dir.mkdir(exist_ok=True)
        
        instructions_content = f'''import type {{ PageInstructions }} from '../InstructionsService'

export const {config.id}Instructions: PageInstructions = {{
  title: "{config.name} Instructions",
  instructions: [
    "Welcome to the {config.name} page",
    "Use the action sheet to access page-specific actions",
    "Implement your page functionality here",
    "Add more specific instructions as needed"
  ]
}}
'''
        
        instructions_path = instructions_dir / f"{config.id}.instructions.ts"
        with open(instructions_path, 'w') as f:
            f.write(instructions_content)
        print(f"✅ Created instructions: {instructions_path}")
        
        # Update instructions service
        service_path = self.src_path / "services/instructions/InstructionsService.ts"
        if service_path.exists():
            with open(service_path, 'r') as f:
                content = f.read()
            
            # Add import
            import_line = f"import {{ {config.id}Instructions }} from './pages/{config.id}.instructions'"
            if import_line not in content:
                # Find existing imports and add after them
                import_pattern = r"(import\s*\{[^}]+\}\s*from\s*'./pages/[^']+'\s*)"
                content = re.sub(import_pattern, r'\1\n' + import_line, content)
            
            # Add to instructions map
            map_entry = f"  {config.id}: {config.id}Instructions,"
            if map_entry not in content:
                map_pattern = r"(const\s+instructionsMap[^{]+\{[^}]+)"
                content = re.sub(map_pattern, r'\1\n' + map_entry, content)
            
            with open(service_path, 'w') as f:
                f.write(content)
            print(f"✅ Updated instructions service")
    
    def extract_concept_name(self, page_id: str) -> str:
        """Extract concept name from page ID (e.g., 'concept6variant1' -> 'concept6')"""
        import re
        match = re.match(r'(concept\d+)', page_id.lower())
        return match.group(1) if match else ''
    
    def get_concept_folder(self, page_id: str, parent: str) -> Path:
        """Get the concept folder path for organizing child pages"""
        concept_name = self.extract_concept_name(page_id)
        if concept_name:
            return self.src_path / "pages" / parent / concept_name
        else:
            return self.src_path / "pages" / parent
    
    def create_concept_css(self, concept_name: str, parent: str, variant_ids: List[str]) -> None:
        """Create empty CSS file for a concept"""
        if not concept_name:
            return
            
        concept_folder = self.src_path / "pages" / parent / concept_name
        concept_folder.mkdir(parents=True, exist_ok=True)
        
        # Create a basic empty CSS file with just a comment
        variant_comments = []
        for variant_id in variant_ids:
            variant_comments.extend([
                f'/* .{variant_id}-container */',
                f'/* .{variant_id}-info-panel */',
                f'/* .{variant_id}-content */'
            ])
        
        css_content = f'''/* {concept_name.upper()} Concept Styling */

/* Add your custom styles for {concept_name} here */

/* Available variant classes to style: */
{chr(10).join(variant_comments)}
'''
        
        css_path = concept_folder / f"{concept_name}.css"
        with open(css_path, 'w') as f:
            f.write(css_content)
        print(f"✅ Created CSS file: {css_path}")
    
    def create_master_barrel(self, parent: str, all_configs: List[ChildPageConfig]) -> None:
        """Create or update master barrel export file for all child pages"""
        pages_root = self.src_path / "pages"
        barrel_path = pages_root / "index.ts"
        
        existing_exports = set()
        
        # Read existing barrel if it exists
        if barrel_path.exists():
            with open(barrel_path, 'r') as f:
                content = f.read()
            
            # Extract existing exports using regex
            import re
            export_pattern = r"export\s*\{\s*([^}]+)\s*\}\s*from\s*['\"]([^'\"]+)['\"]"
            matches = re.findall(export_pattern, content)
            
            for component_name, import_path in matches:
                component_name = component_name.strip()
                existing_exports.add(f"export {{ {component_name} }} from '{import_path}';")
        
        # Generate exports for new child pages
        new_exports = set()
        for config in all_configs:
            concept_name = self.extract_concept_name(config.id)
            if concept_name:
                new_exports.add(f"export {{ {config.component_name} }} from './{parent}/{concept_name}/{config.component_name}';")
            else:
                new_exports.add(f"export {{ {config.component_name} }} from './{parent}/{config.component_name}';")
        
        # Merge existing and new exports
        all_exports = existing_exports.union(new_exports)
        sorted_exports = sorted(list(all_exports))
        
        barrel_content = f'''// Pages Barrel Export
// Auto-generated barrel file for all child pages

{chr(10).join(sorted_exports)}
'''
        
        with open(barrel_path, 'w') as f:
            f.write(barrel_content)
        
        new_count = len(new_exports)
        total_count = len(all_exports)
        if barrel_path.exists() and len(existing_exports) > 0:
            print(f"✅ Updated master barrel export: {barrel_path} (added {new_count}, total {total_count})")
        else:
            print(f"✅ Created master barrel export: {barrel_path} ({total_count} exports)")

    @staticmethod
    def pascal_case(text: str) -> str:
        """Convert text to PascalCase"""
        return ''.join(word.capitalize() for word in text.replace('-', ' ').replace('_', ' ').split())
    
    @staticmethod
    def camel_case(text: str) -> str:
        """Convert text to camelCase"""
        words = text.replace('-', ' ').replace('_', ' ').split()
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    def generate_child_pages(self, parent: str, children: List[str], actions_str: str) -> None:
        """Main method to generate all child pages and update files"""
        if not self.validate_paths():
            return
        
        print(f"🚀 Generating child pages for parent '{parent}'...")
        print(f"📄 Children to create: {', '.join(children)}")
        
        # Parse and prepare configurations
        actions = self.parse_actions(actions_str)
        configs = []
        
        for child in children:
            child_id = child.lower().strip()
            child_name = self.pascal_case(child_id)
            
            config = ChildPageConfig(
                id=child_id,
                name=child_name,
                component_name=f"{child_name}Page",
                wrapper_name=f"{child_name}PageWrapper",
                hook_name=f"use{child_name}Actions",
                actions=actions
            )
            configs.append(config)
        
        # Group configs by concept for CSS generation and barrel exports
        concepts_variants = {}
        concepts_configs = {}
        for config in configs:
            concept_name = self.extract_concept_name(config.id)
            if concept_name:
                if concept_name not in concepts_variants:
                    concepts_variants[concept_name] = []
                    concepts_configs[concept_name] = []
                concepts_variants[concept_name].append(config.id)
                concepts_configs[concept_name].append(config)
        
        # Generate all files and updates
        for config in configs:
            print(f"\n📝 Creating files for '{config.name}'...")
            self.create_child_page_component(config, parent)
            self.create_wrapper_component(config, parent)
            self.create_actions_hook(config)
            self.create_instructions(config)
        
        # Generate CSS files for each concept
        print(f"\n🎨 Creating concept CSS files...")
        for concept_name, variant_ids in concepts_variants.items():
            self.create_concept_css(concept_name, parent, variant_ids)
        
        # Create master barrel export
        print(f"\n📦 Creating master barrel export...")
        self.create_master_barrel(parent, configs)
        
        # Update existing files
        print(f"\n🔧 Updating existing files...")
        self.update_page_actions_constants(configs)
        self.update_parent_actions_hook(parent, configs)
        self.update_parent_page_actions(parent, configs)
        self.update_action_sheet_container(parent, configs)
        self.update_parent_page_routing(parent, configs)
        
        print(f"\n✅ Successfully generated {len(configs)} child pages!")
        print(f"📊 File structure created:")
        print(f"   📁 src/pages/")
        print(f"      📦 index.ts (updated barrel export)")
        print(f"      📁 {parent}/")
        for concept_name, variant_ids in concepts_variants.items():
            print(f"         📁 {concept_name}/")
            print(f"            🎨 {concept_name}.css")
            for variant_id in variant_ids:
                variant_name = self.pascal_case(variant_id)
                print(f"            📄 {variant_name}Page.tsx")
        
        print(f"📋 Next steps:")
        print(f"   1. Review and customize the generated components")
        print(f"   2. Customize CSS styling in each concept's CSS file")
        print(f"   3. Implement specific functionality for each page")
        print(f"   4. Update action implementations in the hooks")
        print(f"   5. Test navigation and actions")

def main():
    parser = argparse.ArgumentParser(description='Generate child pages for the responsive chessboard application')
    parser.add_argument('--parent', required=True, help='Parent tab/page (e.g., uitests, splash)')
    parser.add_argument('--children', required=True, help='Comma-separated list of child page names')
    parser.add_argument('--actions', help='Comma-separated list of actions in format: id:label:icon:variant')
    parser.add_argument('--base-path', default='/mnt/c/Projects/chessboard-vanilla-v2', help='Base path to the project')
    
    args = parser.parse_args()
    
    children = [child.strip() for child in args.children.split(',')]
    generator = ChildPageGenerator(args.base_path)
    
    generator.generate_child_pages(args.parent, children, args.actions or "")

if __name__ == "__main__":
    main()