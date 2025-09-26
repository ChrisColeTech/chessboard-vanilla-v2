"""
ActionRegistryManager - Manages integration of generated actions with the central registry system.

This module handles:
- PAGE_ACTIONS registry integration
- COMMON_ACTIONS sibling navigation
- COMMON_ACTION_GROUPS creation
- Uses pages.config.json as source of truth
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

try:
    from .config import PageConfig
    from .file_writer import FileWriter
    from .config_integration import ConfigIntegration
except ImportError:
    # For standalone testing
    import sys
    sys.path.append(str(Path(__file__).parent))
    from config import PageConfig
    from file_writer import FileWriter
    
    sys.path.append(str(Path(__file__).parent.parent / "shared"))
    from config_integration import ConfigIntegration


class ActionRegistryManager:
    """Manages integration of generated actions with the central registry system."""
    
    def __init__(self, frontend_root: Path, file_writer: Optional[FileWriter] = None):
        self.frontend_root = frontend_root
        self.file_writer = file_writer or FileWriter()
        
        # Core action system files
        self.page_actions_path = frontend_root / "src/constants/actions/page-actions.constants.ts"
        self.common_actions_path = frontend_root / "src/constants/actions/common-actions.constants.ts"
        
        # Config integration
        self.config_integration = ConfigIntegration(frontend_root)
        
    def register_parent_actions(self, parent_id: str) -> bool:
        """
        Register parent actions in PAGE_ACTIONS registry.
        Uses pages.config.json to get accurate parent information.
        """
        try:
            # Get parent info from config
            parent_info = self._get_page_info(parent_id)
            if not parent_info or parent_info.get('type') != 'parent':
                raise ValueError(f"Invalid or missing parent page: {parent_id}")
            
            # Get children for this parent
            children = self._get_children_for_parent(parent_id)
            
            if not self.page_actions_path.exists():
                raise FileNotFoundError(f"PAGE_ACTIONS file not found: {self.page_actions_path}")
            
            content = self.page_actions_path.read_text(encoding='utf-8')
            
            # Add import for parent actions
            import_statement = f"import {{ pageActions as {parent_id}Actions }} from './pages/{parent_id}'"
            if not self._has_import(content, f"from './pages/{parent_id}'"):
                content = self._add_import(content, import_statement)
            
            # Add registry entry
            registry_entry = f"  {parent_id}: {parent_id}Actions.actions,"
            if not self._has_registry_entry(content, parent_id):
                content = self._add_registry_entry(content, registry_entry)
            
            # Write updated content
            self.page_actions_path.write_text(content, encoding='utf-8')
            
            print(f"  ✅ Registered parent '{parent_id}' in PAGE_ACTIONS registry")
            return True
            
        except Exception as e:
            print(f"  ❌ Error registering parent actions: {e}")
            return False
    
    def register_child_actions(self, parent_id: str) -> bool:
        """
        Register child actions with common action merging.
        Uses pages.config.json to get accurate child and sibling information.
        """
        try:
            # Get all children for this parent from config
            children = self._get_children_for_parent(parent_id)
            
            if not children:
                print(f"  ℹ️  No children found for parent '{parent_id}'")
                return True
            
            if not self.page_actions_path.exists():
                raise FileNotFoundError(f"PAGE_ACTIONS file not found: {self.page_actions_path}")
            
            content = self.page_actions_path.read_text(encoding='utf-8')
            
            # Process each child
            for child in children:
                child_id = child['id']
                
                # Add import for child actions
                import_statement = f"import {{ pageActions as {child_id}Actions }} from './pages/{child_id}'"
                if not self._has_import(content, f"from './pages/{child_id}'"):
                    content = self._add_import(content, import_statement)
                
                # Generate sibling list (all children except current)
                siblings = [c['id'] for c in children if c['id'] != child_id]
                sibling_actions = [f"'go-to-{sibling}'" for sibling in siblings]
                
                # Add registry entry with common action merging
                if sibling_actions:
                    registry_entry = f"""  {child_id}: mergeWithCommonActions([
    ...{child_id}Actions.actions
  ], [{', '.join(sibling_actions)}]),"""
                else:
                    # No siblings, just merge with empty array
                    registry_entry = f"""  {child_id}: mergeWithCommonActions([
    ...{child_id}Actions.actions
  ], []),"""
                
                if not self._has_registry_entry(content, child_id):
                    content = self._add_registry_entry(content, registry_entry)
            
            # Write updated content
            self.page_actions_path.write_text(content, encoding='utf-8')
            
            print(f"  ✅ Registered {len(children)} child pages in PAGE_ACTIONS registry")
            return True
            
        except Exception as e:
            print(f"  ❌ Error registering child actions: {e}")
            return False
    
    def add_sibling_navigation(self, parent_id: str) -> bool:
        """
        Add sibling navigation actions to common actions.
        Uses pages.config.json to get accurate sibling relationships.
        """
        try:
            # Get children for this parent from config
            children = self._get_children_for_parent(parent_id)
            
            if not children:
                print(f"  ℹ️  No children found for parent '{parent_id}', skipping sibling navigation")
                return True
            
            if not self.common_actions_path.exists():
                raise FileNotFoundError(f"COMMON_ACTIONS file not found: {self.common_actions_path}")
            
            content = self.common_actions_path.read_text(encoding='utf-8')
            
            # Add navigation actions for each child
            for child in children:
                child_id = child['id']
                child_name = child['name']
                
                action_definition = f'''  "go-to-{child_id}": {{
    id: "go-to-{child_id}",
    label: "→ {child_name}",
    icon: Navigation,
    variant: "secondary",
  }},'''
                
                if not self._has_common_action(content, f'"go-to-{child_id}"'):
                    content = self._add_common_action(content, action_definition)
            
            # Add sibling group if there are multiple children
            if len(children) > 1:
                sibling_group = f'''{parent_id}Siblings: [
    {', '.join([f"'go-to-{child['id']}'" for child in children])}
  ],'''
                
                if not self._has_action_group(content, f'{parent_id}Siblings'):
                    content = self._add_action_group(content, sibling_group)
            
            # Write updated content
            self.common_actions_path.write_text(content, encoding='utf-8')
            
            print(f"  ✅ Added sibling navigation for {len(children)} children")
            return True
            
        except Exception as e:
            print(f"  ❌ Error adding sibling navigation: {e}")
            return False
    
    def validate_registry_integration(self, page_id: str) -> List[str]:
        """Validate that page is properly integrated in registry."""
        issues = []
        
        if not self.page_actions_path.exists():
            issues.append("PAGE_ACTIONS file not found")
            return issues
        
        content = self.page_actions_path.read_text(encoding='utf-8')
        
        # Check import exists
        if f"from './pages/{page_id}'" not in content:
            issues.append(f"Missing import for {page_id}")
        
        # Check registry entry exists
        if f"{page_id}:" not in content:
            issues.append(f"Missing registry entry for {page_id}")
        
        return issues
    
    def _get_page_info(self, page_id: str) -> Optional[Dict]:
        """Get page information from pages.config.json"""
        try:
            config_data = self.config_integration.load_config()
            return config_data.get('pages', {}).get(page_id)
        except Exception as e:
            print(f"  ⚠️  Error loading page config: {e}")
            return None
    
    def _get_children_for_parent(self, parent_id: str) -> List[Dict]:
        """Get all children for a parent from pages.config.json"""
        try:
            config_data = self.config_integration.load_config()
            pages = config_data.get('pages', {})
            
            children = []
            for page_id, page_info in pages.items():
                if page_info.get('type') == 'child' and page_info.get('parent_id') == parent_id:
                    children.append(page_info)
            
            # Sort by creation date for consistent ordering
            children.sort(key=lambda x: x.get('created_at', ''))
            return children
            
        except Exception as e:
            print(f"  ⚠️  Error getting children for parent {parent_id}: {e}")
            return []
    
    def _has_import(self, content: str, import_path: str) -> bool:
        """Check if import already exists, handling both single and double quotes."""
        # Normalize the import path to handle both quote styles
        normalized_path = import_path.replace("'", '"')
        
        # Check for both single and double quote variations
        single_quote_path = import_path.replace('"', "'")
        double_quote_path = import_path.replace("'", '"')
        
        return (single_quote_path in content or 
                double_quote_path in content)
    
    def _add_import(self, content: str, import_statement: str) -> str:
        """Add import statement to the imports section."""
        lines = content.split('\n')
        
        # Find the last import line
        last_import_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                last_import_index = i
        
        if last_import_index >= 0:
            # Insert after the last import
            lines.insert(last_import_index + 1, import_statement)
            return '\n'.join(lines)
        
        # Fallback: add at the beginning after comments
        for i, line in enumerate(lines):
            if not line.strip().startswith('/*') and not line.strip().startswith('*') and not line.strip().startswith('//') and line.strip():
                lines.insert(i, import_statement)
                return '\n'.join(lines)
        
        return content
    
    def _has_registry_entry(self, content: str, page_id: str) -> bool:
        """Check if registry entry already exists."""
        return f"{page_id}:" in content
    
    def _add_registry_entry(self, content: str, registry_entry: str) -> str:
        """Add registry entry to PAGE_ACTIONS object."""
        # Find the export const PAGE_ACTIONS declaration
        export_match = re.search(r'export const PAGE_ACTIONS.*?\{', content, re.DOTALL)
        if not export_match:
            return content
        
        # Find the very last closing brace and semicolon of the entire object
        # We need to count braces to find the correct closing brace
        start_pos = export_match.end() - 1  # Position of the opening brace
        brace_count = 1
        pos = start_pos
        
        while pos < len(content) and brace_count > 0:
            pos += 1
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
        
        if brace_count == 0:
            # Found the matching closing brace
            # Insert the registry entry before the closing brace
            before_close = content[:pos]
            after_close = content[pos:]
            
            # Add comma if the last entry doesn't have one
            if not before_close.rstrip().endswith(','):
                registry_entry = ',' + registry_entry
            
            return before_close + registry_entry + '\n' + after_close
        
        return content
    
    def _has_common_action(self, content: str, action_id: str) -> bool:
        """Check if common action already exists."""
        return action_id in content
    
    def _add_common_action(self, content: str, action_definition: str) -> str:
        """Add action definition to COMMON_ACTIONS."""
        # Find the closing of COMMON_ACTIONS object - handle both }; and } patterns
        pattern = r"(export\s+const\s+COMMON_ACTIONS.*?\{.*?)(}\s*;?\s*\n)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return content.replace(match.group(0), f"{match.group(1)}{action_definition}\n{match.group(2)}")
        
        # Fallback pattern for simpler format
        pattern2 = r"(COMMON_ACTIONS\s*=\s*\{[^}]*)(}\s*;?\s*)"
        match2 = re.search(pattern2, content, re.DOTALL)
        
        if match2:
            return content.replace(match2.group(0), f"{match2.group(1)}{action_definition}\n{match2.group(2)}")
        
        return content
    
    def _has_action_group(self, content: str, group_name: str) -> bool:
        """Check if action group already exists."""
        return f"{group_name}:" in content
    
    def _add_action_group(self, content: str, group_definition: str) -> str:
        """Add action group to COMMON_ACTION_GROUPS."""
        # Find the closing of COMMON_ACTION_GROUPS object - handle different patterns
        pattern = r"(export\s+const\s+COMMON_ACTION_GROUPS\s*=\s*\{.*?)(}\s*;?\s*)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Add before the closing brace, ensuring proper comma separation
            existing_content = match.group(1)
            if not existing_content.rstrip().endswith(',') and not existing_content.rstrip().endswith('{'):
                group_definition = ',' + group_definition
            return content.replace(match.group(0), f"{match.group(1)}  {group_definition}\n{match.group(2)}")
        
        # Fallback pattern for simpler format
        pattern2 = r"(COMMON_ACTION_GROUPS\s*=\s*\{[^}]*)(}\s*;?\s*)"
        match2 = re.search(pattern2, content, re.DOTALL)
        
        if match2:
            # Add before the closing brace, ensuring proper comma separation
            existing_content = match2.group(1)
            if not existing_content.rstrip().endswith(',') and not existing_content.rstrip().endswith('{'):
                group_definition = ',' + group_definition
            return content.replace(match2.group(0), f"{match2.group(1)}  {group_definition}\n{match2.group(2)}")
        
        return content


# Convenience functions for direct usage
def register_parent_page_actions(frontend_root: Path, parent_id: str) -> bool:
    """Convenience function to register parent page actions."""
    manager = ActionRegistryManager(frontend_root)
    return manager.register_parent_actions(parent_id)


def register_child_page_actions(frontend_root: Path, parent_id: str) -> bool:
    """Convenience function to register child page actions."""
    manager = ActionRegistryManager(frontend_root)
    success = manager.register_child_actions(parent_id)
    if success:
        manager.add_sibling_navigation(parent_id)
    return success


def validate_page_registry_integration(frontend_root: Path, page_id: str) -> List[str]:
    """Convenience function to validate page registry integration."""
    manager = ActionRegistryManager(frontend_root)
    return manager.validate_registry_integration(page_id)


