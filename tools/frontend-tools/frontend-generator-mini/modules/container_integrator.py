"""
ContainerIntegrator - Integrates generated pages with ActionSheetContainer system.

This module handles:
- Ensuring generated pages connect to ActionSheetContainer
- Adding proper action handling imports and setup
- Integrating with the central action execution system  
- Using pages.config.json as source of truth

Follows Single Responsibility Principle (SRP) - only handles container integration.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add parent directory to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from shared.name_standardizer import NameStandardizer

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


class ContainerIntegrator:
    """Integrates generated pages with ActionSheetContainer system."""
    
    def __init__(self, frontend_root: Path, file_writer: Optional[FileWriter] = None):
        self.frontend_root = frontend_root
        self.file_writer = file_writer or FileWriter()
        
        # Key container integration file
        self.app_tsx_path = frontend_root / "src/App.tsx"
        self.action_sheet_container_path = frontend_root / "src/components/shared/ActionSheetContainer.tsx"
        
        # Config integration
        self.config_integration = ConfigIntegration(frontend_root)
        
    def integrate_parent_page(self, parent_id: str) -> bool:
        """
        Integrate parent page with ActionSheetContainer.
        Uses pages.config.json to get accurate parent information.
        """
        try:
            # Get parent info from config
            parent_info = self._get_page_info(parent_id)
            if not parent_info or parent_info.get('type') != 'parent':
                raise ValueError(f"Invalid or missing parent page: {parent_id}")
            
            # Check if ActionSheetContainer exists
            if not self.action_sheet_container_path.exists():
                print(f"  ⚠️  ActionSheetContainer not found: {self.action_sheet_container_path}")
                return False
            
            # Ensure parent page has proper action handling
            parent_page_path = self._get_parent_page_path(parent_id)
            if not parent_page_path.exists():
                print(f"  ⚠️  Parent page not found: {parent_page_path}")
                return False
            
            success = True
            
            # Step 1: Add action handling to parent page
            if not self._add_action_handling_to_parent(parent_page_path, parent_id):
                success = False
            
            # Step 2: Ensure parent is connected to ActionSheetContainer
            if not self._ensure_container_connection(parent_id):
                success = False
            
            if success:
                print(f"  ✅ Integrated parent '{parent_id}' with ActionSheetContainer")
            else:
                print(f"  ❌ Failed to integrate parent '{parent_id}' with ActionSheetContainer")
            
            return success
            
        except Exception as e:
            print(f"  ❌ Error integrating parent container: {e}")
            return False
    
    def integrate_child_pages(self, parent_id: str) -> bool:
        """
        Integrate child pages with ActionSheetContainer.
        Uses pages.config.json to get accurate child information.
        """
        try:
            # Get children for this parent from config
            children = self._get_children_for_parent(parent_id)
            
            if not children:
                print(f"  ℹ️  No children found for parent '{parent_id}'")
                return True
            
            success = True
            
            # Process each child
            for child in children:
                child_id = child['id']
                
                # Add action handling to child page
                child_page_path = self._get_child_page_path(child_id, parent_id)
                if child_page_path.exists():
                    if not self._add_action_handling_to_child(child_page_path, child_id, parent_id):
                        success = False
                else:
                    print(f"  ⚠️  Child page not found: {child_page_path}")
                    success = False
                
                # Handle mobile variant if it exists
                if child.get('has_mobile', False):
                    mobile_page_path = self._get_mobile_child_page_path(child_id, parent_id)
                    if mobile_page_path.exists():
                        if not self._add_action_handling_to_mobile_child(mobile_page_path, child_id, parent_id):
                            success = False
            
            if success:
                print(f"  ✅ Integrated {len(children)} child pages with ActionSheetContainer")
            else:
                print(f"  ❌ Some child pages failed container integration")
            
            return success
            
        except Exception as e:
            print(f"  ❌ Error integrating child containers: {e}")
            return False
    
    def validate_container_integration(self, page_id: str) -> List[str]:
        """Validate that page is properly integrated with container system."""
        issues = []
        
        # Get page info from config
        page_info = self._get_page_info(page_id)
        if not page_info:
            issues.append(f"Page '{page_id}' not found in config")
            return issues
        
        page_type = page_info.get('type')
        
        if page_type == 'parent':
            # Validate parent integration
            parent_page_path = self._get_parent_page_path(page_id)
            if parent_page_path.exists():
                content = parent_page_path.read_text(encoding='utf-8')
                
                # Check for action handling imports
                if 'usePageActions' not in content:
                    issues.append(f"Parent '{page_id}' missing usePageActions hook")
                
                # Check for ActionSheetContainer usage
                if 'ActionSheetContainer' not in content:
                    issues.append(f"Parent '{page_id}' not connected to ActionSheetContainer")
            else:
                issues.append(f"Parent page file not found: {parent_page_path}")
                
        elif page_type == 'child':
            # Validate child integration
            parent_id = page_info.get('parent_id')
            child_page_path = self._get_child_page_path(page_id, parent_id)
            
            if child_page_path.exists():
                content = child_page_path.read_text(encoding='utf-8')
                
                # Check for action handling
                if 'usePageActions' not in content:
                    issues.append(f"Child '{page_id}' missing usePageActions hook")
            else:
                issues.append(f"Child page file not found: {child_page_path}")
        
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
    
    def _get_parent_page_path(self, parent_id: str) -> Path:
        """Get path to parent page component."""
        return self.frontend_root / f"src/pages/{parent_id}/{NameStandardizer.to_pascal_case(parent_id)}Page.tsx"
    
    def _get_child_page_path(self, child_id: str, parent_id: str) -> Path:
        """Get path to child page component."""
        child_name = NameStandardizer.to_pascal_case(child_id)
        return self.frontend_root / f"src/pages/{parent_id}/{child_name}.tsx"
    
    def _get_mobile_child_page_path(self, child_id: str, parent_id: str) -> Path:
        """Get path to mobile child page component."""
        child_name = NameStandardizer.to_pascal_case(child_id)
        return self.frontend_root / f"src/pages/{parent_id}/Mobile{child_name}.tsx"
    
    def _add_action_handling_to_parent(self, page_path: Path, parent_id: str) -> bool:
        """Add action handling imports and hooks to parent page."""
        try:
            content = page_path.read_text(encoding='utf-8')
            
            # Check if already has action handling
            if 'usePageActions' in content and 'ActionSheetContainer' in content:
                return True
            
            modified = False
            
            # Add usePageActions import if missing
            if 'usePageActions' not in content:
                import_line = 'import { usePageActions } from "../../hooks/core/usePageActions";'
                if not self._has_import(content, 'usePageActions'):
                    content = self._add_import(content, import_line)
                    modified = True
            
            # Add ActionSheetContainer import if missing
            if 'ActionSheetContainer' not in content:
                container_import = 'import { ActionSheetContainer } from "../../components/shared/ActionSheetContainer";'
                if not self._has_import(content, 'ActionSheetContainer'):
                    content = self._add_import(content, container_import)
                    modified = True
            
            # Add hook usage if missing (check for the actual function call)
            if f'usePageActions("{parent_id}")' not in content:
                hook_usage = f'  usePageActions("{parent_id}");'
                content = self._add_hook_usage(content, hook_usage)
                modified = True
            
            # Add ActionSheetContainer to JSX if missing
            if '<ActionSheetContainer' not in content:
                content = self._add_action_sheet_container_to_jsx(content)
                modified = True
            
            if modified:
                page_path.write_text(content, encoding='utf-8')
                return True
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error adding action handling to parent {parent_id}: {e}")
            return False
    
    def _add_action_handling_to_child(self, page_path: Path, child_id: str, parent_id: str) -> bool:
        """Add action handling to child page."""
        try:
            content = page_path.read_text(encoding='utf-8')
            
            # Check if already has action handling
            if 'usePageActions' in content:
                return True
            
            modified = False
            
            # Add usePageActions import if missing
            import_line = 'import { usePageActions } from "../../hooks/core/usePageActions";'
            if not self._has_import(content, 'usePageActions'):
                content = self._add_import(content, import_line)
                modified = True
            
            # Add hook usage if missing
            if f'usePageActions("{child_id}")' not in content:
                hook_usage = f'  usePageActions("{child_id}");'
                content = self._add_hook_usage(content, hook_usage)
                modified = True
            
            if modified:
                page_path.write_text(content, encoding='utf-8')
                return True
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error adding action handling to child {child_id}: {e}")
            return False
    
    def _add_action_handling_to_mobile_child(self, page_path: Path, child_id: str, parent_id: str) -> bool:
        """Add action handling to mobile child page."""
        try:
            content = page_path.read_text(encoding='utf-8')
            
            # Check if already has action handling
            if 'usePageActions' in content:
                return True
            
            modified = False
            
            # Add usePageActions import if missing
            import_line = 'import { usePageActions } from "../../hooks/core/usePageActions";'
            if not self._has_import(content, 'usePageActions'):
                content = self._add_import(content, import_line)
                modified = True
            
            # Add hook usage if missing
            if f'usePageActions("{child_id}")' not in content:
                hook_usage = f'  usePageActions("{child_id}");'
                content = self._add_hook_usage(content, hook_usage)
                modified = True
            
            if modified:
                page_path.write_text(content, encoding='utf-8')
                return True
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error adding action handling to mobile child {child_id}: {e}")
            return False
    
    def _ensure_container_connection(self, parent_id: str) -> bool:
        """Ensure parent page is properly connected to ActionSheetContainer."""
        try:
            # This is handled by _add_action_handling_to_parent
            # Additional container-specific logic could go here
            return True
        except Exception as e:
            print(f"  ❌ Error ensuring container connection for {parent_id}: {e}")
            return False
    
    def _has_import(self, content: str, import_name: str) -> bool:
        """Check if import already exists."""
        return import_name in content
    
    def _add_import(self, content: str, import_statement: str) -> str:
        """Add import statement to the imports section."""
        # Find the last import and add after it
        import_pattern = r"(import.*?from.*?[\"'].*?[\"'];?\s*\n)"
        matches = list(re.finditer(import_pattern, content))
        
        if matches:
            last_import = matches[-1]
            insert_pos = last_import.end()
            return content[:insert_pos] + import_statement + '\n' + content[insert_pos:]
        else:
            # No imports found, add at the top
            return import_statement + '\n\n' + content
    
    def _add_hook_usage(self, content: str, hook_usage: str) -> str:
        """Add hook usage inside component function."""
        # Find the component function and add hook usage
        function_pattern = r"(function\s+\w+\s*\([^)]*\)\s*\{|const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*\{)"
        match = re.search(function_pattern, content)
        
        if match:
            insert_pos = match.end()
            # Insert after opening brace with proper indentation
            return content[:insert_pos] + '\n' + hook_usage + '\n' + content[insert_pos:]
        
        return content
    
    def _add_action_sheet_container_to_jsx(self, content: str) -> str:
        """Add ActionSheetContainer to JSX return statement."""
        # Find the return statement in the component
        return_pattern = r"(return\s*\([^;]*?)(</[^>]+>\s*\);?\s*})"
        match = re.search(return_pattern, content, re.DOTALL)
        
        if match:
            # Add ActionSheetContainer before closing tag
            return content.replace(
                match.group(0),
                match.group(1) + '      <ActionSheetContainer />\n    ' + match.group(2)
            )
        
        return content


# Convenience functions for direct usage
def integrate_parent_container(frontend_root: Path, parent_id: str) -> bool:
    """Convenience function to integrate parent with container."""
    integrator = ContainerIntegrator(frontend_root)
    return integrator.integrate_parent_page(parent_id)


def integrate_child_containers(frontend_root: Path, parent_id: str) -> bool:
    """Convenience function to integrate children with container."""
    integrator = ContainerIntegrator(frontend_root)
    return integrator.integrate_child_pages(parent_id)


def validate_page_container_integration(frontend_root: Path, page_id: str) -> List[str]:
    """Convenience function to validate page container integration."""
    integrator = ContainerIntegrator(frontend_root)
    return integrator.validate_container_integration(page_id)


