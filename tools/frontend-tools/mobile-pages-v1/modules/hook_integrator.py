"""
HookIntegrator - Generates and integrates functional hooks for page actions.

This module handles:
- Generating functional parent action hooks (not placeholder code)
- Creating proper navigation methods based on actual children
- Integrating hooks with Zustand store and navigation system
- Using pages.config.json as source of truth for child relationships

Follows Single Responsibility Principle (SRP) - only handles hook generation and integration.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

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


class HookIntegrator:
    """Generates and integrates functional hooks for page actions."""
    
    def __init__(self, frontend_root: Path, file_writer: Optional[FileWriter] = None):
        self.frontend_root = frontend_root
        self.file_writer = file_writer or FileWriter()
        
        # Hook file paths
        self.hooks_dir = frontend_root / "src/hooks"
        
        # Config integration
        self.config_integration = ConfigIntegration(frontend_root)
        
    def generate_parent_action_hook(self, parent_id: str) -> bool:
        """
        Generate functional parent action hook with real navigation methods.
        Uses pages.config.json to get accurate child information.
        """
        try:
            # Get parent info from config
            parent_info = self._get_page_info(parent_id)
            if not parent_info or parent_info.get('type') != 'parent':
                raise ValueError(f"Invalid or missing parent page: {parent_id}")
            
            # Get children for this parent
            children = self._get_children_for_parent(parent_id)
            
            # Generate hook content
            hook_content = self._generate_parent_hook_content(parent_id, parent_info, children)
            
            # Write hook file
            hook_path = self._get_parent_hook_path(parent_id)
            hook_path.parent.mkdir(parents=True, exist_ok=True)
            
            hook_path.write_text(hook_content, encoding='utf-8')
            
            print(f"  ✅ Generated functional parent hook for '{parent_id}' with {len(children)} navigation methods")
            return True
            
        except Exception as e:
            print(f"  ❌ Error generating parent hook: {e}")
            return False
    
    def generate_child_action_hook(self, child_id: str, parent_id: str) -> bool:
        """
        Generate functional child action hook with proper action handling.
        Uses pages.config.json to get accurate child and sibling information.
        """
        try:
            # Get child info from config
            child_info = self._get_page_info(child_id)
            if not child_info or child_info.get('type') != 'child':
                raise ValueError(f"Invalid or missing child page: {child_id}")
            
            # Get siblings for this child
            siblings = self._get_sibling_pages(child_id, parent_id)
            
            # Generate hook content
            hook_content = self._generate_child_hook_content(child_id, child_info, siblings)
            
            # Write hook file
            hook_path = self._get_child_hook_path(child_id, parent_id)
            hook_path.parent.mkdir(parents=True, exist_ok=True)
            
            hook_path.write_text(hook_content, encoding='utf-8')
            
            print(f"  ✅ Generated functional child hook for '{child_id}' with {len(siblings)} sibling navigation methods")
            return True
            
        except Exception as e:
            print(f"  ❌ Error generating child hook: {e}")
            return False
    
    def update_parent_hook_for_new_child(self, parent_id: str, new_child_id: str) -> bool:
        """
        Update existing parent hook to include new child navigation method.
        Uses pages.config.json for accurate child information.
        """
        try:
            hook_path = self._get_parent_hook_path(parent_id)
            
            if not hook_path.exists():
                print(f"  ⚠️  Parent hook not found, generating new one: {hook_path}")
                return self.generate_parent_action_hook(parent_id)
            
            # Get current children from config (including new one)
            children = self._get_children_for_parent(parent_id)
            parent_info = self._get_page_info(parent_id)
            
            # Regenerate entire hook with updated children
            hook_content = self._generate_parent_hook_content(parent_id, parent_info, children)
            hook_path.write_text(hook_content, encoding='utf-8')
            
            print(f"  ✅ Updated parent hook '{parent_id}' to include new child '{new_child_id}'")
            return True
            
        except Exception as e:
            print(f"  ❌ Error updating parent hook: {e}")
            return False
    
    def validate_hook_integration(self, page_id: str) -> List[str]:
        """Validate that page hook is properly generated and functional."""
        issues = []
        
        # Get page info from config
        page_info = self._get_page_info(page_id)
        if not page_info:
            issues.append(f"Page '{page_id}' not found in config")
            return issues
        
        page_type = page_info.get('type')
        parent_id = page_info.get('parent_id') if page_type == 'child' else None
        
        if page_type == 'parent':
            # Validate parent hook
            hook_path = self._get_parent_hook_path(page_id)
            if not hook_path.exists():
                issues.append(f"Parent hook file not found: {hook_path}")
            else:
                content = hook_path.read_text(encoding='utf-8')
                
                # Check for functional implementation
                if '// Navigation methods will be added here' in content:
                    issues.append(f"Parent hook '{page_id}' still contains placeholder code")
                
                # Check for Zustand store usage
                if 'useAppStore' not in content:
                    issues.append(f"Parent hook '{page_id}' not integrated with Zustand store")
                
                # Check for navigation methods based on actual children
                children = self._get_children_for_parent(page_id)
                for child in children:
                    method_name = f"goTo{child['name'].capitalize()}"
                    if method_name not in content:
                        issues.append(f"Parent hook '{page_id}' missing navigation method for child '{child['id']}'")
                        
        elif page_type == 'child':
            # Validate child hook
            hook_path = self._get_child_hook_path(page_id, parent_id)
            if not hook_path.exists():
                issues.append(f"Child hook file not found: {hook_path}")
            else:
                content = hook_path.read_text(encoding='utf-8')
                
                # Check for functional implementation
                if '// Action methods will be returned here' in content:
                    issues.append(f"Child hook '{page_id}' still contains placeholder code")
        
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
    
    def _get_sibling_pages(self, child_id: str, parent_id: str) -> List[Dict]:
        """Get sibling pages for a child (all other children of the same parent)."""
        children = self._get_children_for_parent(parent_id)
        return [child for child in children if child['id'] != child_id]
    
    def _get_parent_hook_path(self, parent_id: str) -> Path:
        """Get path to parent action hook."""
        return self.hooks_dir / f"{parent_id}/use{parent_id.capitalize()}Actions.ts"
    
    def _get_child_hook_path(self, child_id: str, parent_id: str) -> Path:
        """Get path to child action hook."""
        return self.hooks_dir / f"{parent_id}/use{child_id.capitalize()}Actions.ts"
    
    def _generate_parent_hook_content(self, parent_id: str, parent_info: Dict, children: List[Dict]) -> str:
        """Generate functional parent hook content with real navigation methods."""
        parent_name = parent_info.get('name', parent_id.capitalize())
        
        # Generate navigation methods
        navigation_methods = []
        return_methods = []
        
        for child in children:
            # Use base name without "Page" suffix for navigation methods
            raw_child_name = child.get('name', child['id'].capitalize())
            child_name = raw_child_name.replace('Page', '') if raw_child_name.endswith('Page') else raw_child_name
            method_name = f"goTo{child_name}"
            
            # Navigation method implementation
            navigation_methods.append(f'''  const {method_name} = useCallback(() => {{
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {{
      setCurrentChildPage('{child['id']}');
    }}, 100);
  }}, [setCurrentChildPage]);''')
            
            # Return method
            return_methods.append(method_name)
        
        # Generate imports
        imports = ['import { useCallback } from \'react\';']
        if children:
            imports.append('import { useAppStore } from \'../../stores/appStore\';')
        
        # Generate hook content
        hook_content = f'''/**
 * {parent_name} Actions Hook
 * 
 * Provides navigation methods for {parent_name} page and its children.
 * Generated from pages.config.json with {len(children)} child pages.
 */

{chr(10).join(imports)}

export function use{parent_name}Actions() {{'''
        
        if children:
            hook_content += f'''
  const {{ setCurrentChildPage }} = useAppStore();

{chr(10).join(navigation_methods) if navigation_methods else '  // No navigation methods - no children found'}

  return {{
    {', '.join(return_methods) if return_methods else '// No methods to return'}
  }};
}}'''
        else:
            hook_content += '''
  // No children found for this parent
  return {};
}'''
        
        return hook_content
    
    def _generate_child_hook_content(self, child_id: str, child_info: Dict, siblings: List[Dict]) -> str:
        """Generate functional child hook content."""
        # Use base name without "Page" suffix for hook naming
        raw_name = child_info.get('name', child_id.capitalize())
        child_name = raw_name.replace('Page', '') if raw_name.endswith('Page') else raw_name
        
        # Generate sibling navigation methods
        sibling_methods = []
        return_methods = []
        
        for sibling in siblings:
            # Use base name without "Page" suffix for sibling navigation
            raw_sibling_name = sibling.get('name', sibling['id'].capitalize())
            sibling_name = raw_sibling_name.replace('Page', '') if raw_sibling_name.endswith('Page') else raw_sibling_name
            method_name = f"goTo{sibling_name}"
            
            # Sibling navigation method
            sibling_methods.append(f'''  const {method_name} = useCallback(() => {{
    setTimeout(() => {{
      setCurrentChildPage('{sibling['id']}');
    }}, 100);
  }}, [setCurrentChildPage]);''')
            
            # Return method
            return_methods.append(method_name)
        
        # Generate imports (only import useCallback if we have siblings that need it)
        imports = []
        if siblings:
            imports.append('import { useCallback } from \'react\';')
            imports.append('import { useAppStore } from \'../../stores/appStore\';')
        
        # Generate hook content
        hook_content = f'''/**
 * {child_name} Actions Hook
 * 
 * Provides action methods for {child_name} page including sibling navigation.
 * Generated from pages.config.json with {len(siblings)} sibling pages.
 */

{chr(10).join(imports)}

export function use{child_name}Actions() {{'''
        
        if siblings:
            hook_content += f'''
  const {{ setCurrentChildPage }} = useAppStore();

{chr(10).join(sibling_methods) if sibling_methods else '  // No sibling navigation methods'}

  return {{
    {', '.join(return_methods) if return_methods else '// No methods to return'}
  }};
}}'''
        else:
            hook_content += '''
  // No siblings found for this child
  return {};
}'''
        
        return hook_content
    
    def remove_hook_placeholders(self, hook_path: Path) -> bool:
        """Remove placeholder comments from existing hook files."""
        try:
            if not hook_path.exists():
                return False
            
            content = hook_path.read_text(encoding='utf-8')
            
            # Remove common placeholder patterns
            placeholders = [
                '// Navigation methods will be added here when children are created',
                '// Action methods will be returned here when children are created',
                '// Navigation methods will be added here',
                '// Action methods will be returned here',
                '// import { useAppStore } from \'../../stores/appStore\';',
                '// const { setSelectedTab, setCurrentChildPage } = useAppStore();'
            ]
            
            modified = False
            for placeholder in placeholders:
                if placeholder in content:
                    content = content.replace(placeholder, '')
                    modified = True
            
            # Clean up extra whitespace
            if modified:
                content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Remove multiple empty lines
                hook_path.write_text(content, encoding='utf-8')
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ Error removing placeholders from {hook_path}: {e}")
            return False
    
    def generate_hook_index_file(self, parent_id: str) -> bool:
        """Generate index file for parent hook directory."""
        try:
            parent_info = self._get_page_info(parent_id)
            if not parent_info:
                return False
                
            children = self._get_children_for_parent(parent_id)
            
            # Generate index content
            exports = [f'export {{ use{parent_info["name"]}Actions }} from \'./use{parent_info["name"]}Actions\';']
            
            for child in children:
                # Use base name without "Page" suffix for navigation methods
                raw_child_name = child.get('name', child['id'].capitalize())
                child_name = raw_child_name.replace('Page', '') if raw_child_name.endswith('Page') else raw_child_name
                exports.append(f'export {{ use{child_name}Actions }} from \'./use{child_name}Actions\';')
            
            index_content = f'''/**
 * {parent_info["name"]} Hooks Index
 * 
 * Exports all action hooks for {parent_info["name"]} and its children.
 * Generated from pages.config.json.
 */

{chr(10).join(exports)}
'''
            
            # Write index file
            index_path = self.hooks_dir / parent_id / "index.ts"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_path.write_text(index_content, encoding='utf-8')
            
            print(f"  ✅ Generated hook index file for '{parent_id}'")
            return True
            
        except Exception as e:
            print(f"  ❌ Error generating hook index: {e}")
            return False


# Convenience functions for direct usage
def generate_parent_hook(frontend_root: Path, parent_id: str) -> bool:
    """Convenience function to generate parent action hook."""
    integrator = HookIntegrator(frontend_root)
    return integrator.generate_parent_action_hook(parent_id)


def generate_child_hook(frontend_root: Path, child_id: str, parent_id: str) -> bool:
    """Convenience function to generate child action hook."""
    integrator = HookIntegrator(frontend_root)
    return integrator.generate_child_action_hook(child_id, parent_id)


def update_parent_hook(frontend_root: Path, parent_id: str, new_child_id: str) -> bool:
    """Convenience function to update parent hook for new child."""
    integrator = HookIntegrator(frontend_root)
    return integrator.update_parent_hook_for_new_child(parent_id, new_child_id)


def validate_page_hook_integration(frontend_root: Path, page_id: str) -> List[str]:
    """Convenience function to validate page hook integration."""
    integrator = HookIntegrator(frontend_root)
    return integrator.validate_hook_integration(page_id)


