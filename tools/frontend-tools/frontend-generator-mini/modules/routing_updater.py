"""
Parent Routing Updater for dynamic injection of child page routes.
"""

from pathlib import Path
from typing import Dict, List, Optional
import sys
import re

# Add parent directory to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from shared.name_standardizer import NameStandardizer

try:
    from .config import GenerationContext, PageConfig, ProjectCapabilities
    from .template_engine import TemplateEngine
    from .file_writer import FileWriter
    from .variable_generator import VariableGenerator
except ImportError:
    from config import GenerationContext, PageConfig, ProjectCapabilities
    from template_engine import TemplateEngine
    from file_writer import FileWriter
    from variable_generator import VariableGenerator


class RoutingUpdateError(Exception):
    """Raised when routing update fails."""
    pass


class ParentRoutingUpdater:
    """Handles dynamic updates to parent page routing when children are added."""
    
    def __init__(self, template_engine: TemplateEngine, file_writer: FileWriter, 
                 variable_generator: VariableGenerator):
        self.template_engine = template_engine
        self.file_writer = file_writer
        self.variable_generator = variable_generator
        
        # Routing patterns for injection
        self.route_import_pattern = re.compile(r'(// Child page imports\s*\n)', re.MULTILINE)
        self.route_config_pattern = re.compile(r'(// Child page routes\s*\n)', re.MULTILINE)
        self.switch_route_pattern = re.compile(r'(// Child page components\s*\n)', re.MULTILINE)
    
    def update_parent_routing(self, context: GenerationContext, child_name: str) -> None:
        """Update parent page routing to include new child page."""
        config = context.config
        
        if not config.parent:
            raise RoutingUpdateError("Cannot update routing: no parent specified")
        
        print(f"🔄 Updating {config.parent} routing for child: {child_name}")
        
        # Find parent page file
        parent_page_path = self._find_parent_page_file(context, config.parent)
        if not parent_page_path:
            print(f"  ⚠️  Parent page file not found for: {config.parent}")
            return
        
        # Read current parent content
        try:
            current_content = parent_page_path.read_text(encoding='utf-8')
        except Exception as e:
            raise RoutingUpdateError(f"Failed to read parent page file: {e}")
        
        # Generate routing updates
        updates = self._generate_routing_updates(context, child_name)
        
        # Apply updates to parent content
        updated_content = self._apply_routing_updates(current_content, updates)
        
        if updated_content != current_content:
            # Write updated content back
            self.file_writer.write_file(
                parent_page_path,
                updated_content,
                "ParentRoutingUpdater",
                "/tools/frontend-tools/mobile-pages-v2/modules/routing_updater.py"
            )
            print(f"  ✅ Updated routing in: {parent_page_path.name}")
        else:
            print(f"  ℹ️  No routing updates needed")
    
    def _find_parent_page_file(self, context: GenerationContext, parent_name: str) -> Optional[Path]:
        """Find the main parent page file for routing updates."""
        parent_dir = context.pages_dir / parent_name.lower()
        
        if not parent_dir.exists():
            return None
        
        # Look for main parent page file (e.g., SettingsPage.tsx)
        parent_page_file = parent_dir / f"{NameStandardizer.to_pascal_case(parent_name)}Page.tsx"
        
        return parent_page_file if parent_page_file.exists() else None
    
    def _generate_routing_updates(self, context: GenerationContext, child_name: str) -> Dict[str, str]:
        """Generate routing update content for child page."""
        config = context.config
        
        # Generate variables for routing templates
        variables = {
            'CHILD_NAME': child_name,  # Keep original casing for component names
            'CHILD_ID': child_name.lower(),
            'PARENT_ID': config.parent.lower(),
            'HAS_MOBILE': str(config.mobile).lower()
        }
        
        # Generate import statement
        import_content = self.template_engine.render_template(
            'routing/child-import.template',
            variables
        )
        
        # Generate route configuration
        route_config_content = self.template_engine.render_template(
            'routing/child-route-config.template', 
            variables
        )
        
        # Generate switch case
        switch_content = self.template_engine.render_template(
            'routing/child-switch-case.template',
            variables
        )
        
        return {
            'import': import_content.strip(),
            'route_config': route_config_content.strip(),
            'switch_case': switch_content.strip()
        }
    
    def _apply_routing_updates(self, content: str, updates: Dict[str, str]) -> str:
        """Apply routing updates to parent page content."""
        updated_content = content
        
        # Update imports
        if self.route_import_pattern.search(updated_content):
            updated_content = self.route_import_pattern.sub(
                f"\\1{updates['import']}\n",
                updated_content
            )
        else:
            # If no import marker found, add import after existing imports
            updated_content = self._inject_after_last_import(updated_content, updates['import'])
        
        # Update route configuration
        if self.route_config_pattern.search(updated_content):
            updated_content = self.route_config_pattern.sub(
                f"\\1{updates['route_config']}\n",
                updated_content
            )
        else:
            # If no route config marker found, add before routes array end
            updated_content = self._inject_before_routes_end(updated_content, updates['route_config'])
        
        # Update switch cases
        if self.switch_route_pattern.search(updated_content):
            updated_content = self.switch_route_pattern.sub(
                f"\\1{updates['switch_case']}\n",
                updated_content
            )
        else:
            # If no switch marker found, add before default case
            updated_content = self._inject_before_default_case(updated_content, updates['switch_case'])
        
        return updated_content
    
    def _inject_after_last_import(self, content: str, import_statement: str) -> str:
        """Inject import statement after the last existing import."""
        import_pattern = re.compile(r'^import .+;$', re.MULTILINE)
        imports = list(import_pattern.finditer(content))
        
        if imports:
            last_import = imports[-1]
            insert_pos = last_import.end()
            return content[:insert_pos] + f"\n{import_statement}" + content[insert_pos:]
        
        return content
    
    def _inject_before_routes_end(self, content: str, route_config: str) -> str:
        """Inject route configuration before routes array end."""
        routes_end_pattern = re.compile(r'(\s*];\s*$)', re.MULTILINE)
        match = routes_end_pattern.search(content)
        
        if match:
            insert_pos = match.start(1)
            return content[:insert_pos] + f",\n    {route_config}" + content[insert_pos:]
        
        return content
    
    def _inject_before_default_case(self, content: str, switch_case: str) -> str:
        """Inject switch case before default case."""
        default_pattern = re.compile(r'(\s*default:\s*)', re.MULTILINE)
        match = default_pattern.search(content)
        
        if match:
            insert_pos = match.start(1)
            return content[:insert_pos] + f"    {switch_case}\n\n" + content[insert_pos:]
        
        return content
    
    def validate_routing_injection(self, context: GenerationContext, child_name: str) -> Dict[str, bool]:
        """Validate that routing was properly injected."""
        config = context.config
        validation_results = {}
        
        parent_page_path = self._find_parent_page_file(context, config.parent)
        if not parent_page_path:
            return {'parent_file_exists': False}
        
        try:
            content = parent_page_path.read_text(encoding='utf-8')
            
            # Check for child import
            child_import_pattern = f"import.*{child_name}.*from"
            validation_results['has_import'] = bool(re.search(child_import_pattern, content))
            
            # Check for route configuration
            child_route_pattern = f"path.*{child_name.lower()}"
            validation_results['has_route_config'] = bool(re.search(child_route_pattern, content))
            
            # Check for switch case
            child_case_pattern = f"case.*{child_name.lower()}"
            validation_results['has_switch_case'] = bool(re.search(child_case_pattern, content))
            
            validation_results['parent_file_exists'] = True
            
        except Exception as e:
            print(f"  ⚠️  Error validating routing injection: {e}")
            validation_results['validation_error'] = True
        
        return validation_results
    
    def remove_child_routing(self, context: GenerationContext, child_name: str) -> None:
        """Remove child page routing from parent (for cleanup/migration)."""
        config = context.config
        
        if not config.parent:
            return
        
        print(f"🧹 Removing {child_name} routing from {config.parent}")
        
        parent_page_path = self._find_parent_page_file(context, config.parent)
        if not parent_page_path:
            return
        
        try:
            content = parent_page_path.read_text(encoding='utf-8')
            
            # Remove import
            import_pattern = f"import.*{child_name}.*from.*;\n?"
            content = re.sub(import_pattern, "", content)
            
            # Remove route config
            route_pattern = f".*path.*{child_name.lower()}.*,?\n?"
            content = re.sub(route_pattern, "", content)
            
            # Remove switch case
            case_pattern = f".*case.*{child_name.lower()}.*:.*\n.*return.*{child_name}.*;\n?"
            content = re.sub(case_pattern, "", content, flags=re.MULTILINE)
            
            self.file_writer.write_file(
                parent_page_path,
                content,
                "ParentRoutingUpdater",
                "/tools/frontend-tools/mobile-pages-v2/modules/routing_updater.py"
            )
            
            print(f"  ✅ Removed {child_name} routing from parent")
            
        except Exception as e:
            print(f"  ⚠️  Error removing routing: {e}")
    
    def get_child_routes_in_parent(self, context: GenerationContext, parent_name: str) -> List[str]:
        """Get list of child routes already configured in parent."""
        parent_page_path = self._find_parent_page_file(context, parent_name)
        if not parent_page_path:
            return []
        
        try:
            content = parent_page_path.read_text(encoding='utf-8')
            
            # Find all case statements in switch
            case_pattern = re.compile(r'case\s+[\'"]([^\'"]+)[\'"]:', re.MULTILINE)
            cases = case_pattern.findall(content)
            
            # Filter out 'main' case (parent landing page)
            child_routes = [case for case in cases if case != 'main']
            
            return sorted(child_routes)
            
        except Exception:
            return []
    
    def sync_routing_with_filesystem(self, context: GenerationContext, parent_name: str) -> Dict[str, List[str]]:
        """Sync parent routing with actual child files on filesystem."""
        # Get child files from filesystem
        parent_dir = context.pages_dir / parent_name.lower()
        filesystem_children = []
        
        if parent_dir.exists():
            for file_path in parent_dir.glob("*.tsx"):
                if not file_path.name.endswith("Page.tsx") and not file_path.name.endswith("MainPage.tsx"):
                    # Extract child name from filename
                    child_name = file_path.stem
                    if child_name.startswith("Mobile"):
                        child_name = child_name[6:]  # Remove Mobile prefix
                    if child_name.endswith("Page"):
                        child_name = child_name[:-4]  # Remove Page suffix
                    
                    if child_name.lower() not in filesystem_children:
                        filesystem_children.append(child_name.lower())
        
        # Get child routes from parent routing
        routing_children = self.get_child_routes_in_parent(context, parent_name)
        
        # Find differences
        missing_in_routing = [child for child in filesystem_children if child not in routing_children]
        missing_in_filesystem = [child for child in routing_children if child not in filesystem_children]
        
        return {
            'filesystem_children': filesystem_children,
            'routing_children': routing_children,
            'missing_in_routing': missing_in_routing,
            'missing_in_filesystem': missing_in_filesystem,
            'in_sync': len(missing_in_routing) == 0 and len(missing_in_filesystem) == 0
        }