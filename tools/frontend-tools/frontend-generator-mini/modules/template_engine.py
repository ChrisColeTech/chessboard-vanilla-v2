"""
Template Engine for loading and rendering page generation templates.
"""

from pathlib import Path
from typing import Dict, Optional, List
try:
    from .config import PageConfig, ProjectCapabilities, WrapperType
except ImportError:
    from config import PageConfig, ProjectCapabilities, WrapperType


class TemplateValidationError(Exception):
    """Raised when template validation fails."""
    pass


class TemplateEngine:
    """Handles template loading, variable substitution, and template selection."""
    
    def __init__(self, templates_root: Path):
        self.templates_root = templates_root
        self.dynamic_dir = self.templates_root / "dynamic"
        self.static_dir = self.templates_root / "static"
        self._validate_templates_root()
        
    def load_template(self, template_name: str, is_static: bool = False) -> str:
        """Load template content from file."""
        if is_static:
            template_path = self.static_dir / template_name
        else:
            template_path = self.dynamic_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        return template_path.read_text(encoding='utf-8')
    
    def render_template(self, template_name: str, variables: Dict[str, str], is_static: bool = False) -> str:
        """Load template and substitute variables."""
        template_content = self.load_template(template_name, is_static)
        
        # Simple variable substitution using {{VARIABLE_NAME}} format
        for var_name, var_value in variables.items():
            placeholder = f'{{{{{var_name}}}}}'
            template_content = template_content.replace(placeholder, var_value)
            
        return template_content
    
    def select_child_wrapper_template(self, config: PageConfig, capabilities: ProjectCapabilities) -> str:
        """Select appropriate child wrapper template based on project capabilities."""
        
        # Full hooks + mobile support
        if config.mobile and capabilities.has_page_hooks and capabilities.has_mobile_hook:
            return WrapperType.FULL_HOOKS
            
        # Page hooks only (no mobile)  
        elif capabilities.has_page_hooks and not capabilities.has_mobile_hook:
            return WrapperType.BASIC_HOOKS
            
        # No hooks, no mobile
        elif not capabilities.has_page_hooks and not capabilities.has_mobile_hook:
            return WrapperType.NO_HOOKS
            
        # Has mobile hook but not page hooks (unusual case)
        else:
            return WrapperType.NO_MOBILE
    
    def get_parent_templates(self) -> Dict[str, str]:
        """Get template names for parent page generation."""
        return {
            'parent_page': 'pages/parent-page.tsx.template',
            'parent_main': 'pages/parent-main-page.tsx.template', 
            'parent_actions': 'actions/parent-actions.ts.template',
            'parent_instructions': 'instructions/parent-instructions.ts.template',
            'parent_hook': 'hooks/parent-actions-hook.ts.template'
        }
    
    def get_child_templates(self, config: PageConfig) -> Dict[str, str]:
        """Get template names for child page generation."""
        templates = {
            'child_page': 'pages/child-page.tsx.template',
            'child_actions': 'actions/child-actions.ts.template',
            'child_instructions': 'instructions/child-instructions.ts.template'
        }
        
        # Add mobile variant if requested
        if config.mobile:
            templates['mobile_child_page'] = 'pages/mobile-child-page.tsx.template'
            
        return templates
    
    def get_dependency_templates(self) -> Dict[str, str]:
        """Get template names for dependency creation."""
        return {
            'use_page_data': 'dependencies/use-page-data-hook.ts.template',
            'data_table': 'dependencies/data-table-component.tsx.template'
        }
    
    def validate_template_exists(self, template_name: str) -> bool:
        """Check if a template file exists."""
        template_path = self.templates_root / template_name
        return template_path.exists()
    
    def list_available_templates(self) -> list:
        """List all available template files."""
        templates = []
        for template_file in self.templates_root.rglob('*.template'):
            # Get relative path from templates root
            relative_path = template_file.relative_to(self.templates_root)
            templates.append(str(relative_path))
        return sorted(templates)
    
    def _validate_templates_root(self) -> None:
        """Validate that templates root exists and is accessible."""
        if not self.templates_root.exists():
            raise TemplateValidationError(f"Templates root directory not found: {self.templates_root}")
        
        if not self.templates_root.is_dir():
            raise TemplateValidationError(f"Templates root is not a directory: {self.templates_root}")
    
    def validate_all_required_templates(self) -> List[str]:
        """Validate that all required templates exist. Returns list of missing templates."""
        missing_templates = []
        
        # Check parent templates
        parent_templates = self.get_parent_templates()
        for template_name in parent_templates.values():
            if not self.validate_template_exists(template_name):
                missing_templates.append(template_name)
        
        # Check child templates (without mobile)
        child_config = PageConfig(name="Test", mobile=False)
        child_templates = self.get_child_templates(child_config)
        for template_name in child_templates.values():
            if not self.validate_template_exists(template_name):
                missing_templates.append(template_name)
        
        # Check mobile child template
        mobile_child_config = PageConfig(name="Test", mobile=True)
        mobile_templates = self.get_child_templates(mobile_child_config)
        for template_name in mobile_templates.values():
            if template_name not in child_templates.values() and not self.validate_template_exists(template_name):
                missing_templates.append(template_name)
        
        # Check wrapper templates
        wrapper_templates = [
            WrapperType.FULL_HOOKS,
            WrapperType.BASIC_HOOKS,
            WrapperType.NO_HOOKS,
            WrapperType.NO_MOBILE
        ]
        for template_name in wrapper_templates:
            if not self.validate_template_exists(f"components/{template_name}"):
                missing_templates.append(f"components/{template_name}")
        
        # Check dependency templates
        dependency_templates = self.get_dependency_templates()
        for template_name in dependency_templates.values():
            if not self.validate_template_exists(template_name):
                missing_templates.append(template_name)
        
        return list(set(missing_templates))  # Remove duplicates
    
    def validate_template_content(self, template_name: str) -> List[str]:
        """Validate template content for common issues. Returns list of issues found."""
        issues = []
        
        try:
            content = self.load_template(template_name)
            
            # Check for common template issues
            if not content.strip():
                issues.append(f"Template {template_name} is empty")
            
            # Check for unmatched braces
            open_braces = content.count('{{')
            close_braces = content.count('}}')
            if open_braces != close_braces:
                issues.append(f"Template {template_name} has unmatched braces ({open_braces} open, {close_braces} close)")
            
            # Check for nested braces (not supported)
            if '{{{' in content or '}}}' in content:
                issues.append(f"Template {template_name} contains nested braces (not supported)")
            
        except FileNotFoundError:
            issues.append(f"Template {template_name} not found")
        except Exception as e:
            issues.append(f"Error reading template {template_name}: {str(e)}")
        
        return issues