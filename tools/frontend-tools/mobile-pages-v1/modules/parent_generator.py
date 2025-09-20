"""
Parent Page Generator for creating complete parent page structures.
"""

from pathlib import Path
from typing import Dict, List
import sys

try:
    from .config import GenerationContext, PageConfig, ProjectCapabilities
    from .template_engine import TemplateEngine
    from .file_writer import FileWriter
    from .variable_generator import VariableGenerator
    from .dependency_manager import DependencyManager
except ImportError:
    from config import GenerationContext, PageConfig, ProjectCapabilities
    from template_engine import TemplateEngine
    from file_writer import FileWriter
    from variable_generator import VariableGenerator
    from dependency_manager import DependencyManager

# Import config integration from shared
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
try:
    from config_integration import ConfigIntegration
except ImportError:
    print("Warning: Could not import config_integration. Navigation config will not be updated.")


class ParentPageGenerator:
    """Handles parent page generation using templates."""
    
    def __init__(self, template_engine: TemplateEngine, file_writer: FileWriter, 
                 variable_generator: VariableGenerator, dependency_manager: DependencyManager):
        self.template_engine = template_engine
        self.file_writer = file_writer
        self.variable_generator = variable_generator
        self.dependency_manager = dependency_manager
        self.config_integration = None
    
    def create_parent_page(self, context: GenerationContext) -> None:
        """Create complete parent page structure."""
        config = context.config
        
        print(f"📝 Creating parent page: {config.page_name}")
        
        # Initialize config integration
        self._init_config_integration(context)
        
        # Generate variables for templates
        variables = self.variable_generator.generate_parent_variables(context)
        context.variables = variables
        
        # Create dependencies if needed (now navigation variables are available)
        self.dependency_manager.ensure_all_dependencies_with_integration(context)
        
        # Create all parent files
        self._generate_parent_files(context)
        
        # Register parent page in central config
        self._register_parent_in_config(context)
        
        # Regenerate index files
        self.dependency_manager.regenerate_index_files(context.frontend_root)
        
        print(f"✅ Parent page '{config.page_name}' created successfully!")
        print(f"  📁 Files created in: {context.pages_dir / config.page_id}")
        print(f"  🎯 Parent is now a direct tab target (no wrapper)")
        print(f"  🧭 Navigation system updated with new tab")
    
    def _generate_parent_files(self, context: GenerationContext) -> None:
        """Generate all parent page files."""
        config = context.config
        variables = context.variables
        
        # Get parent templates
        templates = self.template_engine.get_parent_templates()
        
        # Create parent page directory
        parent_dir = context.pages_dir / config.page_id
        self.file_writer.create_directory(parent_dir)
        
        # Create hooks directory
        hooks_dir = context.hooks_dir / config.page_id
        self.file_writer.create_directory(hooks_dir)
        
        # Create action/instruction directories
        self.file_writer.create_directory(context.actions_dir)
        self.file_writer.create_directory(context.instructions_dir)
        
        # Generate parent page (main routing page)
        self._create_parent_page(context, templates['parent_page'], variables)
        
        # Generate parent main page (landing page)
        self._create_parent_main_page(context, templates['parent_main'], variables)
        
        # Generate parent actions hook
        self._create_parent_actions_hook(context, templates['parent_hook'], variables)
        
        # Generate parent actions configuration
        self._create_parent_actions_config(context, templates['parent_actions'], variables)
        
        # Generate parent instructions configuration
        self._create_parent_instructions_config(context, templates['parent_instructions'], variables)
        
        # Generate mobile parent page if mobile flag is set
        if context.config.mobile:
            self._create_mobile_parent_page(context, variables)
    
    def _create_parent_page(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create the main parent page with routing logic."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.pages_dir / config.page_id / f"{config.page_name}.tsx"
        self.file_writer.write_file(
            file_path,
            content,
            "ParentPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/parent_generator.py"
        )
    
    def _create_parent_main_page(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create the parent landing page."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.pages_dir / config.page_id / f"{config.base_name.capitalize()}MainPage.tsx"
        self.file_writer.write_file(
            file_path,
            content,
            "ParentPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/parent_generator.py"
        )
    
    def _create_parent_actions_hook(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create the parent actions hook for navigation."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.hooks_dir / config.page_id / f"use{config.base_name.capitalize()}Actions.ts"
        self.file_writer.write_file(
            file_path,
            content,
            "ParentPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/parent_generator.py"
        )
    
    def _create_parent_actions_config(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create parent actions configuration for action sheet."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.actions_dir / f"{config.page_id}.ts"
        self.file_writer.write_file(
            file_path,
            content,
            "ParentPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/parent_generator.py"
        )
    
    def _create_parent_instructions_config(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create parent instructions configuration."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.instructions_dir / f"{config.page_id}.ts"
        self.file_writer.write_file(
            file_path,
            content,
            "ParentPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/parent_generator.py"
        )
    
    def _create_mobile_parent_page(self, context: GenerationContext, variables: Dict[str, str]) -> None:
        """Create the mobile parent page (simple mobile UI component)."""
        config = context.config
        
        content = self.template_engine.render_template('pages/mobile-parent-page.tsx.template', variables)
        
        file_path = context.pages_dir / config.page_id / f"Mobile{config.base_name.capitalize()}MainPage.tsx"
        self.file_writer.write_file(
            file_path,
            content,
            "ParentPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/parent_generator.py"
        )
        
        print(f"  📱 Mobile parent page created: Mobile{config.page_name}.tsx")
    
    def validate_parent_creation(self, context: GenerationContext) -> Dict[str, bool]:
        """Validate that all parent files were created successfully."""
        config = context.config
        validation_results = {}
        
        # Check main parent files
        parent_page_path = context.pages_dir / config.page_id / f"{config.page_name}.tsx"
        validation_results['parent_page'] = parent_page_path.exists()
        
        parent_main_path = context.pages_dir / config.page_id / f"{config.base_name.capitalize()}MainPage.tsx"
        validation_results['parent_main'] = parent_main_path.exists()
        
        # Check hook file
        hook_path = context.hooks_dir / config.page_id / f"use{config.base_name.capitalize()}Actions.ts"
        validation_results['parent_hook'] = hook_path.exists()
        
        # Check action/instruction files
        actions_path = context.actions_dir / f"{config.page_id}.ts"
        validation_results['parent_actions'] = actions_path.exists()
        
        instructions_path = context.instructions_dir / f"{config.page_id}.ts"
        validation_results['parent_instructions'] = instructions_path.exists()
        
        return validation_results
    
    def get_created_files(self, context: GenerationContext) -> list:
        """Get list of files that would be created for a parent page."""
        config = context.config
        
        return [
            context.pages_dir / config.page_id / f"{config.page_name}.tsx",
            context.pages_dir / config.page_id / f"{config.base_name.capitalize()}MainPage.tsx",
            context.hooks_dir / config.page_id / f"use{config.base_name.capitalize()}Actions.ts",
            context.actions_dir / f"{config.page_id}.ts",
            context.instructions_dir / f"{config.page_id}.ts"
        ]
    
    def update_parent_routing(self, context: GenerationContext, child_configs: List[PageConfig]) -> None:
        """Update parent page with new child routing when children are added."""
        config = context.config
        
        print(f"🔄 Regenerating parent page '{config.page_name}' with routing for {len(child_configs)} children")
        
        # Generate parent variables with current children
        parent_variables = self.variable_generator.generate_parent_variables(context)
        
        # Generate routing variables for all children
        routing_variables = self.variable_generator.generate_routing_variables(child_configs)
        
        # Merge all variables
        variables = {**parent_variables, **routing_variables}
        context.variables = variables
        
        # Regenerate only the parent page file (not all files to avoid overwriting)
        templates = self.template_engine.get_parent_templates()
        self._create_parent_page(context, templates['parent_page'], variables)
        
        print(f"✅ Parent page routing updated successfully!")
    
    def update_parent_actions_hook(self, context: GenerationContext) -> None:
        """Update parent actions hook when children are added.""" 
        config = context.config
        
        print(f"🔄 Regenerating parent actions hook for '{config.page_name}'")
        
        # Generate parent variables (includes navigation methods for existing children)
        variables = self.variable_generator.generate_parent_variables(context)
        context.variables = variables
        
        # Regenerate parent actions hook
        templates = self.template_engine.get_parent_templates()
        self._create_parent_actions_hook(context, templates['parent_hook'], variables)
        
        print(f"✅ Parent actions hook updated successfully!")
    
    def _init_config_integration(self, context: GenerationContext) -> None:
        """Initialize config integration if available."""
        try:
            if 'ConfigIntegration' in globals():
                self.config_integration = ConfigIntegration(context.frontend_root)
                self.config_integration.create_config_if_missing()
        except Exception as e:
            print(f"Warning: Could not initialize config integration: {e}")
    
    def _register_parent_in_config(self, context: GenerationContext) -> None:
        """Register parent page in central configuration."""
        if self.config_integration:
            try:
                self.config_integration.register_parent_page(context.config)
            except Exception as e:
                print(f"Warning: Could not register parent page in config: {e}")