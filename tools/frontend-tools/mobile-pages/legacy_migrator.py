#!/usr/bin/env python3
"""
Legacy to Dynamic System Migrator

Automatically extracts instructions and actions from monolithic files
and creates individual page files for the new dynamic loading system.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

class LegacyMigrator:
    def __init__(self, frontend_root: str):
        self.frontend_root = Path(frontend_root)
        self.instructions_service_path = self.frontend_root / "src" / "services" / "instructions" / "InstructionsService.ts"
        self.page_actions_path = self.frontend_root / "src" / "constants" / "actions" / "page-actions.constants.ts"
        self.instructions_pages_dir = self.frontend_root / "src" / "services" / "instructions" / "pages"
        self.actions_pages_dir = self.frontend_root / "src" / "constants" / "actions" / "pages"

    def extract_instructions(self) -> Dict[str, dict]:
        """Extract all instructions from the monolithic InstructionsService"""
        print("🔍 Extracting instructions from InstructionsService.ts...")
        
        content = self.instructions_service_path.read_text()
        instructions = {}
        
        # Regex to match instructionsMap.set patterns
        pattern = r"this\.instructionsMap\.set\('([^']+)',\s*\{\s*title:\s*'([^']*(?:\\'[^']*)*)',\s*instructions:\s*\[(.*?)\]\s*\}\)"
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        for page_id, title, instructions_block in matches:
            # Parse the instructions array more robustly
            instruction_lines = []
            
            # Use a more comprehensive regex that handles nested quotes
            # Look for strings that start with ' and end with ', handling escaped quotes
            pattern = r"'((?:[^'\\]|\\.)*)'"
            raw_instructions = re.findall(pattern, instructions_block)
            
            for instruction in raw_instructions:
                # Unescape all escape sequences
                instruction = instruction.replace("\\'", "'")
                instruction = instruction.replace("\\\\", "\\")
                instruction_lines.append(instruction)
            
            instructions[page_id] = {
                'title': title.replace("\\'", "'"),
                'instructions': instruction_lines
            }
        
        print(f"✅ Extracted {len(instructions)} instruction sets")
        return instructions

    def extract_page_actions(self) -> Dict[str, List]:
        """Extract all page actions from the monolithic constants file"""
        print("🔍 Extracting page actions from page-actions.constants.ts...")
        
        content = self.page_actions_path.read_text()
        page_actions = {}
        
        # Extract the main export object with improved regex
        # Handle multi-line object with proper bracket matching
        export_pattern = r"export const PAGE_ACTIONS:\s*Record<string,\s*ActionSheetAction\[\]>\s*=\s*\{(.*)\};"
        export_match = re.search(export_pattern, content, re.DOTALL)
        
        if export_match:
            actions_content = export_match.group(1)
            
            # Extract page names and their action configurations
            # Look for patterns like: pagename: [actions] or pagename: mergeWithCommonActions([actions])
            page_pattern = r"(\w+):\s*(?:\[.*?\]|mergeWithCommonActions\([^)]*\)|.*?)(?=,\s*\w+:|$)"
            page_matches = re.findall(page_pattern, actions_content, re.DOTALL)
            
            for page_name in page_matches:
                page_actions[page_name.strip()] = []  # Extract actual actions structure later
        
        # Fallback: extract page names from simple patterns
        if not page_actions:
            simple_page_pattern = r"(\w+):\s*"
            simple_matches = re.findall(simple_page_pattern, content)
            for page_name in simple_matches:
                if page_name not in ['Record', 'ActionSheetAction', 'const', 'export']:
                    page_actions[page_name] = []
        
        print(f"✅ Found {len(page_actions)} page action sets")
        return page_actions

    def create_instruction_files(self, instructions: Dict[str, dict]) -> None:
        """Create individual instruction files"""
        print("📝 Creating instruction files...")
        
        self.instructions_pages_dir.mkdir(parents=True, exist_ok=True)
        
        for page_id, data in instructions.items():
            # Skip if file already exists
            file_path = self.instructions_pages_dir / f"{page_id}.ts"
            if file_path.exists():
                print(f"  ⏭️  Skipping {page_id} (already exists)")
                continue
                
            content = f'''export const pageInstructions = {{
  id: '{page_id}',
  title: `{data["title"]}`,
  instructions: [
'''
            
            for instruction in data['instructions']:
                # Use template literals to avoid escaping issues
                content += f"    `{instruction}`,\n"
            
            content += '''  ]
}'''
            
            file_path.write_text(content)
            print(f"  📝 Created: {page_id}.ts")

    def create_basic_action_files(self, page_actions: Dict[str, List]) -> None:
        """Create basic action files for extracted pages"""
        print("📝 Creating action files...")
        
        self.actions_pages_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced action templates for common pages
        action_templates = {
            'playchess': {
                'actions': [
                    "{ id: 'new-game', label: 'New Game', icon: RotateCcw, variant: 'default' }",
                    "{ id: 'pause-game', label: 'Pause Game', icon: Pause, variant: 'secondary' }",
                    "{ id: 'show-moves', label: 'Show Moves', icon: Eye, variant: 'default' }",
                    "{ id: 'undo-move', label: 'Undo Move', icon: Undo, variant: 'secondary' }"
                ],
                'imports': ['RotateCcw', 'Pause', 'Eye', 'Undo']
            },
            'playpuzzles': {
                'actions': [
                    "{ id: 'new-puzzle', label: 'New Puzzle', icon: RotateCcw, variant: 'default' }",
                    "{ id: 'hint', label: 'Get Hint', icon: Brain, variant: 'secondary' }",
                    "{ id: 'skip-puzzle', label: 'Skip Puzzle', icon: SkipForward, variant: 'secondary' }",
                    "{ id: 'reset-puzzle', label: 'Reset', icon: RefreshCw, variant: 'default' }"
                ],
                'imports': ['RotateCcw', 'Brain', 'SkipForward', 'RefreshCw']
            },
            'casino': {
                'actions': [
                    "{ id: 'go-to-slots', label: 'Play Slots', icon: Target, variant: 'default' }",
                    "{ id: 'go-to-blackjack', label: 'Play Blackjack', icon: Sword, variant: 'default' }",
                    "{ id: 'go-to-roulette', label: 'Play Roulette', icon: RotateCw, variant: 'default' }",
                    "{ id: 'view-stats', label: 'View Stats', icon: BarChart3, variant: 'secondary' }"
                ],
                'imports': ['Target', 'Sword', 'RotateCw', 'BarChart3']
            },
            'uitests': {
                'actions': [
                    "{ id: 'audio-demo', label: 'Audio Demo', icon: Volume2, variant: 'default' }",
                    "{ id: 'drag-test', label: 'Drag Test', icon: Move, variant: 'default' }",
                    "{ id: 'mobile-test', label: 'Mobile Test', icon: TestTube, variant: 'secondary' }",
                    "{ id: 'reset-tests', label: 'Reset Tests', icon: RotateCcw, variant: 'secondary' }"
                ],
                'imports': ['Volume2', 'Move', 'TestTube', 'RotateCcw']
            }
        }
        
        # Create files for extracted pages or use templates
        for page_name in page_actions.keys():
            file_path = self.actions_pages_dir / f"{page_name}.ts"
            if file_path.exists():
                print(f"  ⏭️  Skipping {page_name} actions (already exists)")
                continue
            
            # Use template if available, otherwise create basic template
            if page_name in action_templates:
                config = action_templates[page_name]
            else:
                config = {
                    'actions': [
                        "{ id: 'refresh', label: 'Refresh', icon: RefreshCw, variant: 'default' }",
                        "{ id: 'navigate', label: 'Navigate', icon: Navigation, variant: 'secondary' }"
                    ],
                    'imports': ['RefreshCw', 'Navigation']
                }
            
            imports = ', '.join(config['imports'])
            actions = ',\n    '.join(config['actions'])
            
            content = f'''import {{ {imports} }} from 'lucide-react'
import type {{ ActionSheetAction }} from '../../../types/core/action-sheet.types'

export const pageActions = {{
  id: '{page_name}',
  actions: [
    {actions}
  ] as ActionSheetAction[]
}}'''
            
            file_path.write_text(content)
            print(f"  📝 Created: {page_name} actions")

    def migrate(self) -> None:
        """Run the complete migration process"""
        print("🚀 Starting legacy to dynamic system migration...")
        
        # Extract instructions
        instructions = self.extract_instructions()
        self.create_instruction_files(instructions)
        
        # Extract and create basic actions
        page_actions = self.extract_page_actions()
        self.create_basic_action_files(page_actions)
        
        print("\n✅ Migration completed!")
        print(f"📊 Summary:")
        print(f"  - {len(instructions)} instruction files processed")
        print(f"  - {len(page_actions)} action pages identified")
        
        print(f"\n📋 Next steps:")
        print(f"  1. Review generated files in:")
        print(f"     - {self.instructions_pages_dir}")
        print(f"     - {self.actions_pages_dir}")
        print(f"  2. Switch services to use dynamic imports")
        print(f"  3. Test the new system end-to-end")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate legacy monolithic files to dynamic system')
    parser.add_argument('--frontend-root', default='../../../frontend', help='Frontend root directory')
    args = parser.parse_args()
    
    # Resolve frontend root path
    script_dir = Path(__file__).parent
    frontend_root = script_dir / args.frontend_root
    frontend_root = frontend_root.resolve()
    
    if not frontend_root.exists():
        print(f"❌ Frontend root directory not found: {frontend_root}")
        return 1
    
    migrator = LegacyMigrator(str(frontend_root))
    migrator.migrate()
    
    return 0

if __name__ == "__main__":
    exit(main())