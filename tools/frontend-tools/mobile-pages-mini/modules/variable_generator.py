"""
Variable Generator for creating template variables from page configuration.
"""

from typing import Dict, List
import sys
from pathlib import Path

# Add parent directory to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from shared.name_standardizer import NameStandardizer

try:
    from .config import PageConfig, ProjectCapabilities, GenerationContext
except ImportError:
    from config import PageConfig, ProjectCapabilities, GenerationContext


class VariableGenerator:
    """Generates template variables from configuration and project state."""
    
    def __init__(self):
        pass
    
    
    def generate_parent_variables(self, context: GenerationContext) -> Dict[str, str]:
        """Generate variables for parent page templates."""
        config = context.config
        capabilities = context.capabilities
        
        # Check for existing children of this parent
        children = self._get_existing_children(context, config.page_id)
        
        # Generate routing variables based on children
        if children:
            routing_vars = self.generate_routing_variables(children)
            child_imports = routing_vars['CHILD_IMPORTS']
            child_routing_logic = routing_vars['CHILD_ROUTING_LOGIC']
            child_navigation_actions = self.generate_child_navigation_actions(children)
            child_navigation_icons = self.generate_child_navigation_icons(children)
            # Clean up the child_navigation_icons (remove leading comma and whitespace)
            clean_icons = child_navigation_icons.lstrip(', ') if child_navigation_icons else ''
            child_navigation_icons_import = f"import {{ {clean_icons} }} from 'lucide-react'" if clean_icons else ''
        else:
            child_imports = '// Child imports will be added here when children are created'
            child_routing_logic = '// Child routing logic will be added here when children are created'
            child_navigation_actions = '// Child navigation actions will be added here when children are created'
            child_navigation_icons = ''
            child_navigation_icons_import = ''
        
        # Mobile support variables
        if config.mobile:
            mobile_import = f'\nimport {{ Mobile{config.base_name}MainPage }} from "./Mobile{config.base_name}MainPage";'
            mobile_hook_import = 'import { useIsMobile } from "../../hooks/core/useIsMobile";'
            mobile_main_page_logic = f'isMobile ? Mobile{config.base_name}MainPage : {config.base_name}MainPage'
            mobile_detection = 'const isMobile = useIsMobile();'
        else:
            mobile_import = ''
            mobile_hook_import = '// Mobile hook import will be added when mobile support is enabled'
            mobile_main_page_logic = f'{config.base_name}MainPage'
            mobile_detection = '// Mobile detection will be added when mobile support is enabled'

        variables = {
            # Basic parent information
            'PARENT_NAME': config.base_name,  # base_name is already PascalCase
            'PARENT_ID': config.page_id,
            'PARENT_DISPLAY_NAME': config.display_name,
            
            # Hook imports and store usage
            'HOOK_IMPORTS': self._generate_parent_hook_imports(context),
            'HOOK_STORE_USAGE': self._generate_parent_hook_store_usage(context),
            
            # Navigation methods (will be generated dynamically)
            'NAVIGATION_METHODS': self._generate_navigation_methods(context),
            'RETURN_METHODS': self._generate_return_methods(context),
            
            # Child routing logic (dynamic based on actual children)
            'CHILD_IMPORTS': child_imports,
            'CHILD_ROUTING_LOGIC': child_routing_logic,
            'CHILD_NAVIGATION_ACTIONS': child_navigation_actions,
            'CHILD_NAVIGATION_ICONS': child_navigation_icons,
            'CHILD_NAVIGATION_ICONS_IMPORT': child_navigation_icons_import,
            
            # Mobile support
            'MOBILE_IMPORT': mobile_import,
            'MOBILE_HOOK_IMPORT': mobile_hook_import,
            'MOBILE_MAIN_PAGE_LOGIC': mobile_main_page_logic,
            'MOBILE_DETECTION': mobile_detection
        }
        
        return variables
    
    def generate_child_variables(self, context: GenerationContext) -> Dict[str, str]:
        """Generate variables for child page templates."""
        config = context.config
        
        variables = {
            # Basic child information
            'CHILD_NAME': config.base_name,  # base_name is already PascalCase
            'CHILD_ID': config.page_id,
            'CHILD_DISPLAY_NAME': config.display_name,
            'PARENT_ID': config.parent_id,
            
            # Mobile variant information
            'MOBILE_CHILD_NAME': f"Mobile{config.base_name}",  # base_name is already PascalCase
            
            # Description with fallback
            'CHILD_DESCRIPTION': self._escape_description(config.description) or f"Use this page to work with {config.display_name.lower()} features",
            
            # Sibling navigation for child hooks
            'SIBLING_NAVIGATION_METHODS': self._generate_sibling_navigation_methods(context),
            'SIBLING_RETURN_METHODS': self._generate_sibling_return_methods(context)
        }
        
        return variables
    
    def generate_wrapper_variables(self, context: GenerationContext, wrapper_type: str) -> Dict[str, str]:
        """Generate variables for child wrapper templates."""
        config = context.config
        capabilities = context.capabilities
        
        base_variables = self.generate_child_variables(context)
        
        # Add wrapper-specific variables
        if wrapper_type == "child-wrapper-full-hooks.tsx.template":
            base_variables.update({
                'HOOK_IMPORTS': self._generate_full_hook_imports(),
                'HOOK_USAGE': self._generate_full_hook_usage(config),
                'MOBILE_DETECTION': 'const isMobile = useIsMobile();',
                'MOBILE_IMPORT': f'import {{ Mobile{config.page_name} }} from "../../pages/{config.parent_id}/Mobile{config.page_name}";',
                'RENDER_LOGIC': f'isMobile ? <Mobile{config.page_name} /> : <{config.page_name} />'
            })
        elif wrapper_type == "child-wrapper-basic-hooks.tsx.template":
            base_variables.update({
                'HOOK_IMPORTS': self._generate_basic_hook_imports(),
                'HOOK_USAGE': self._generate_basic_hook_usage(config),
                'RENDER_LOGIC': f'<{config.page_name} />'
            })
        else:
            base_variables.update({
                'RENDER_LOGIC': f'<{config.page_name} />'
            })
        
        return base_variables
    
    def _generate_navigation_methods(self, context: GenerationContext) -> str:
        """Generate navigation methods for parent actions hook."""
        config = context.config
        
        methods = []
        
        # Get existing children for this parent
        children = self._get_existing_children(context, config.page_id)
        
        if not children:
            return '  // Navigation methods will be added here when children are created'
        
        # Generate methods for existing children
        for child_config in children:
            method_name = f"goTo{child_config.base_name}"
            methods.append(f"""  const {method_name} = useCallback(() => {{
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {{
      setCurrentChildPage('{child_config.page_id}');
    }}, 100);
  }}, [setCurrentChildPage]);""")
        
        return '\n\n'.join(methods)
    
    def _generate_return_methods(self, context: GenerationContext) -> str:
        """Generate return object for parent actions hook."""
        config = context.config
        
        methods = []
        
        # Get existing children for this parent
        children = self._get_existing_children(context, config.page_id)
        
        if not children:
            return '// Navigation methods will be added here when children are created'
        
        # Add methods for existing children
        for child_config in children:
            methods.append(f"goTo{child_config.base_name}")
        
        # Note: Other parent navigation methods would be added here if needed
        
        return ',\n    '.join(methods)
    
    def _generate_child_routing_placeholder(self, context: GenerationContext) -> str:
        """Generate placeholder for child routing logic in parent page."""
        return "// Child page routing - wrappers handle mobile switching internally\n  // Routes will be auto-generated by the page generator"
    
    def _generate_full_hook_imports(self) -> str:
        """Generate imports for full hooks wrapper."""
        return '''import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";
import { useIsMobile } from "../../hooks/core/useIsMobile";'''
    
    def _generate_basic_hook_imports(self) -> str:
        """Generate imports for basic hooks wrapper."""
        return '''import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageActions } from "../../hooks/core/usePageActions";'''
    
    def _generate_full_hook_usage(self, config: PageConfig) -> str:
        """Generate hook usage for full hooks wrapper."""
        return f'''usePageInstructions("{config.page_id}");
  usePageActions("{config.page_id}");'''
    
    def _generate_basic_hook_usage(self, config: PageConfig) -> str:
        """Generate hook usage for basic hooks wrapper."""
        return f'''usePageInstructions("{config.page_id}");
  usePageActions("{config.page_id}");'''
    
    def _escape_description(self, description: str) -> str:
        """Escape single quotes in description for JavaScript."""
        if not description:
            return ""
        return description.replace("'", "\\'")
    
    def generate_routing_variables(self, child_configs: List[PageConfig]) -> Dict[str, str]:
        """Generate routing logic variables for multiple children."""
        routing_conditions = []
        imports = []
        
        for config in child_configs:
            # Skip main pages - they shouldn't be treated as child routes
            if config.page_id.endswith('main'):
                continue
                
            # config.base_name is already properly PascalCase formatted
            wrapper_name = f"{config.base_name}PageWrapper"
            
            # Import statement
            imports.append(f'import {{ {wrapper_name} }} from "../../components/{config.parent_id}/{config.base_name}PageWrapper";')
            
            # Routing condition
            condition = f'''  if (currentChildPage === "{config.page_id}") {{
    CurrentPageComponent = {wrapper_name};
  }}'''
            routing_conditions.append(condition)
        
        return {
            'CHILD_IMPORTS': '\n'.join(imports),
            'CHILD_ROUTING_LOGIC': ' else'.join(routing_conditions) if routing_conditions else '// No child pages yet'
        }
    
    def generate_child_navigation_actions(self, child_configs: List[PageConfig]) -> str:
        """Generate child navigation action definitions for parent action sheets."""
        if not child_configs:
            return '// Child navigation actions will be added here when children are created'
        
        actions = []
        for config in child_configs:
            action = f'''    {{
      id: 'go-to-{config.page_id}',
      label: 'Go to {config.base_name}',
      icon: Navigation,
      variant: 'secondary'
    }},'''
            actions.append(action)
        
        return '\n'.join(actions)
    
    def generate_child_navigation_icons(self, child_configs: List[PageConfig]) -> str:
        """Generate icon imports needed for child navigation actions."""
        if not child_configs:
            return ''
        
        # For now, all child navigation uses Navigation icon
        # In the future, this could be customized per child
        return ', Navigation'
    
    def _get_existing_children(self, context: GenerationContext, parent_id: str) -> List[PageConfig]:
        """Get existing children for a parent from page config."""
        try:
            # Import the PageConfigManager from shared 
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
            from page_config_manager import PageConfigManager
            
            # Initialize page config manager
            config_manager = PageConfigManager(context.frontend_root)
            
            # Get children for this parent
            children_info = config_manager.get_children_for_parent(parent_id)
            
            # Convert PageInfo objects to PageConfig objects
            child_configs = []
            for child_info in children_info:
                # Use the original name from child_info to preserve capitalization
                child_config = PageConfig(
                    name=child_info.name,
                    parent=parent_id,
                    mobile=child_info.has_mobile,
                    description=child_info.description
                )
                child_configs.append(child_config)
            
            return child_configs
            
        except Exception as e:
            print(f"Warning: Could not load children for parent '{parent_id}': {e}")
            return []
    
    def generate_action_sheet_container_variables(self, context: GenerationContext) -> Dict[str, str]:
        """Generate variables for dynamic ActionSheetContainer template."""
        try:
            # Import the PageConfigManager from shared 
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
            from page_config_manager import PageConfigManager
            
            # Initialize page config manager
            config_manager = PageConfigManager(context.frontend_root)
            
            # Get all pages from config (returns Dict[str, PageInfo])
            all_pages_dict = config_manager.get_all_pages()
            
            # Generate dynamic imports for all page hooks
            hook_imports = []
            hook_initializations = []
            hook_dependencies = []
            action_mappings = []
            
            for page_id, page_info in all_pages_dict.items():
                page_id = page_info.id
                page_name = page_info.name
                page_type = page_info.type
                
                if page_type == 'parent':
                    # Parent page hook - ensure PascalCase using proven algorithm
                    pascal_case_name = NameStandardizer.to_pascal_case(page_name)
                    hook_name = f"use{pascal_case_name}Actions"
                    hook_var = f"{page_id}Actions"
                    
                    # Import path should use actual filename, not page_id
                    hook_imports.append(f'import {{ {hook_name} }} from "../../hooks/{page_id}/{hook_name}";')
                    hook_initializations.append(f'  const {hook_var} = {hook_name}();')
                    hook_dependencies.append(f'    {hook_var},')
                    
                    # Get children for parent to generate action mappings
                    children = config_manager.get_children_for_parent(page_id)
                    
                    # Generate action mappings for parent
                    parent_mappings = []
                    for child in children:
                        child_id = child.id
                        child_name = NameStandardizer.to_pascal_case(child.name)
                        method_name = f"goTo{child_name}"
                        parent_mappings.append(f'        "go-to-{child_id}": {hook_var}.{method_name},')
                    
                    if parent_mappings:
                        action_mappings.append(f'''      {page_id}: {{
{chr(10).join(parent_mappings)}
      }},''')
                
                elif page_type == 'child':
                    # Child pages need action mappings that delegate to their parent's hook methods
                    parent_id = page_info.parent_id
                    if parent_id:
                        # Get parent hook variable name
                        parent_hook_var = f"{parent_id}Actions"
                        
                        # Get siblings for this child (other children with same parent)
                        siblings = config_manager.get_children_for_parent(parent_id)
                        
                        # Generate sibling navigation mappings
                        child_mappings = []
                        for sibling in siblings:
                            if sibling.id != page_id:  # Exclude self
                                sibling_id = sibling.id
                                sibling_name = NameStandardizer.to_pascal_case(sibling.name)
                                method_name = f"goTo{sibling_name}"
                                child_mappings.append(f'        "go-to-{sibling_id}": {parent_hook_var}.{method_name},')
                        
                        if child_mappings:
                            action_mappings.append(f'''      {page_id}: {{
{chr(10).join(child_mappings)}
      }},''')
            
            if hook_imports and hook_initializations and action_mappings:
                return {
                    'DYNAMIC_HOOK_IMPORTS': '\n'.join(hook_imports),
                    'DYNAMIC_HOOK_INITIALIZATIONS': '\n'.join(hook_initializations),
                    'DYNAMIC_HOOK_DEPENDENCIES': '\n'.join(hook_dependencies),
                    'DYNAMIC_ACTION_MAPPINGS': '\n'.join(action_mappings)
                }
            else:
                return {
                    'DYNAMIC_HOOK_IMPORTS': '// No dynamic hooks available - add pages first',
                    'DYNAMIC_HOOK_INITIALIZATIONS': '  // No hooks to initialize',
                    'DYNAMIC_HOOK_DEPENDENCIES': '    // No hook dependencies',
                    'DYNAMIC_ACTION_MAPPINGS': '      // No action mappings available'
                }
            
        except Exception as e:
            print(f"Warning: Could not generate ActionSheetContainer variables: {e}")
            return {
                'DYNAMIC_HOOK_IMPORTS': '// No dynamic hooks available - add pages first',
                'DYNAMIC_HOOK_INITIALIZATIONS': '  // No hooks to initialize',
                'DYNAMIC_HOOK_DEPENDENCIES': '    // No hook dependencies',
                'DYNAMIC_ACTION_MAPPINGS': '      // No action mappings available'
            }
    
    def generate_page_actions_registry_variables(self, context: GenerationContext) -> Dict[str, str]:
        """Generate variables for dynamic PAGE_ACTIONS registry template."""
        try:
            # Import the PageConfigManager from shared 
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
            from page_config_manager import PageConfigManager
            
            # Initialize page config manager
            config_manager = PageConfigManager(context.frontend_root)
            
            # Get all pages from config (returns Dict[str, PageInfo])
            all_pages_dict = config_manager.get_all_pages()
            
            # Generate dynamic imports for all page actions
            action_imports = []
            registry_entries = []
            seen_imports = set()  # Track imports to avoid duplicates
            
            for page_id, page_info in all_pages_dict.items():
                # Use the page_info.id for consistency but keep page_id from the dict key for deduplication
                actual_page_id = page_info.id
                page_type = page_info.type
                
                # Avoid duplicate imports
                if actual_page_id not in seen_imports:
                    action_imports.append(f'import {{ pageActions as {actual_page_id}Actions }} from "./pages/{actual_page_id}";')
                    seen_imports.add(actual_page_id)
                
                if page_type == 'parent':
                    # Parent pages also use mergeWithCommonActions to include global actions like "open-settings"
                    registry_entries.append(f'  {actual_page_id}: mergeWithCommonActions([...{actual_page_id}Actions.actions], []),')
                elif page_type == 'child':
                    # Child pages use mergeWithCommonActions with sibling navigation
                    parent_id = page_info.parent_id
                    siblings = config_manager.get_children_for_parent(parent_id)
                    sibling_actions = [f"'go-to-{sibling.id}'" for sibling in siblings if sibling.id != actual_page_id]
                    
                    if sibling_actions:
                        registry_entries.append(f'''  {actual_page_id}: mergeWithCommonActions([
    ...{actual_page_id}Actions.actions
  ], [{', '.join(sibling_actions)}]),''')
                    else:
                        registry_entries.append(f'  {actual_page_id}: mergeWithCommonActions([...{actual_page_id}Actions.actions], []),')
            
            if action_imports and registry_entries:
                return {
                    'DYNAMIC_PAGE_ACTION_IMPORTS': '\n'.join(action_imports),
                    'DYNAMIC_PAGE_ACTION_ENTRIES': '\n'.join(registry_entries)
                }
            else:
                return {
                    'DYNAMIC_PAGE_ACTION_IMPORTS': '// No page actions available - add pages first',
                    'DYNAMIC_PAGE_ACTION_ENTRIES': '  // No page action entries available'
                }
            
        except Exception as e:
            print(f"Warning: Could not generate PAGE_ACTIONS registry variables: {e}")
            return {
                'DYNAMIC_PAGE_ACTION_IMPORTS': '// No page actions available - add pages first',
                'DYNAMIC_PAGE_ACTION_ENTRIES': '  // No page action entries available'
            }
    
    def _generate_parent_hook_imports(self, context: GenerationContext) -> str:
        """Generate imports for parent action hooks."""
        config = context.config
        children = self._get_existing_children(context, config.page_id)
        
        if children:
            return "import { useCallback } from 'react';\nimport { useAppStore } from '../../stores/appStore';"
        else:
            return "// Imports will be added here when children are created"
    
    def _generate_parent_hook_store_usage(self, context: GenerationContext) -> str:
        """Generate store usage for parent action hooks."""
        config = context.config
        children = self._get_existing_children(context, config.page_id)
        
        if children:
            return "  const setCurrentChildPage = useAppStore((state: any) => state.setCurrentChildPage);"
        else:
            return "  // Store usage will be added here when children are created"
    
    def _generate_sibling_navigation_methods(self, context: GenerationContext) -> str:
        """Generate navigation methods for sibling pages."""
        config = context.config
        
        # Get siblings (other children with same parent)
        siblings = self._get_existing_children(context, config.parent_id)
        siblings = [s for s in siblings if s.page_id != config.page_id]  # Exclude self
        
        if not siblings:
            return '  // No sibling navigation needed - single child'
        
        methods = []
        for sibling in siblings:
            method_name = f"goTo{sibling.base_name}"
            methods.append(f"""  const {method_name} = useCallback(() => {{
    // Small delay to prevent hover sound from triggering after menu transition
    setTimeout(() => {{
      setCurrentChildPage('{sibling.page_id}');
    }}, 100);
  }}, [setCurrentChildPage]);""")
        
        return '\n\n'.join(methods)
    
    def _generate_sibling_return_methods(self, context: GenerationContext) -> str:
        """Generate return object for sibling navigation."""
        config = context.config
        
        # Get siblings (other children with same parent)
        siblings = self._get_existing_children(context, config.parent_id)
        siblings = [s for s in siblings if s.page_id != config.page_id]  # Exclude self
        
        if not siblings:
            return '// No sibling navigation needed - single child'
        
        methods = [f"goTo{sibling.base_name}" for sibling in siblings]
        return ',\n    '.join(methods)