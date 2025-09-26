"""
Child Page Generator for creating child pages with adaptive wrappers.
"""

from pathlib import Path
from typing import Dict
import sys

try:
    from .config import GenerationContext, PageConfig
    from .template_engine import TemplateEngine
    from .file_writer import FileWriter
    from .variable_generator import VariableGenerator
    from .wrapper_selector import WrapperSelector
except ImportError:
    from config import GenerationContext, PageConfig
    from template_engine import TemplateEngine
    from file_writer import FileWriter
    from variable_generator import VariableGenerator
    from wrapper_selector import WrapperSelector

# Import config integration from shared
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
try:
    from config_integration import ConfigIntegration
except ImportError:
    print("Warning: Could not import config_integration. Navigation config will not be updated.")


class ChildPageGenerator:
    """Handles child page generation with adaptive wrapper selection."""
    
    def __init__(self, template_engine: TemplateEngine, file_writer: FileWriter, 
                 variable_generator: VariableGenerator, wrapper_selector: WrapperSelector):
        self.template_engine = template_engine
        self.file_writer = file_writer
        self.variable_generator = variable_generator
        self.wrapper_selector = wrapper_selector
        self.config_integration = None
    
    def create_child_page(self, context: GenerationContext) -> None:
        """Create complete child page structure with adaptive wrapper."""
        config = context.config
        
        if not config.parent:
            raise ValueError("Child pages must specify a parent")
        
        print(f"📝 Creating child page: {config.page_name} (parent: {config.parent})")
        
        # Initialize config integration
        self._init_config_integration(context)
        
        # Generate variables for templates
        variables = self.variable_generator.generate_child_variables(context)
        context.variables = variables
        
        # Create child page files
        self._generate_child_files(context)
        
        # Create mobile variant if requested
        if config.mobile:
            self._create_mobile_variant(context)
        
        # Create adaptive wrapper
        self._create_adaptive_wrapper(context)
        
        # Register child page in central config
        self._register_child_in_config(context)
        
        print(f"✅ Child page '{config.page_name}' created successfully!")
        if config.mobile:
            print(f"✅ Mobile variant 'Mobile{config.page_name}' created successfully!")
        print(f"✅ Adaptive wrapper created with {self._get_wrapper_description(context)}")
    
    def _generate_child_files(self, context: GenerationContext) -> None:
        """Generate all child page files."""
        config = context.config
        variables = context.variables
        
        # Get child templates
        templates = self.template_engine.get_child_templates(config)
        
        # Create parent directory for child pages
        parent_dir = context.pages_dir / config.parent_id
        self.file_writer.create_directory(parent_dir)
        
        # Create components directory for wrappers
        components_dir = context.components_dir / config.parent_id
        self.file_writer.create_directory(components_dir)
        
        # Create action/instruction directories
        self.file_writer.create_directory(context.actions_dir)
        self.file_writer.create_directory(context.instructions_dir)
        
        # Generate child page (desktop version)
        self._create_child_page_component(context, templates['child_page'], variables)
        
        # Generate child actions configuration
        self._create_child_actions_config(context, templates['child_actions'], variables)
        
        # Generate child instructions configuration
        self._create_child_instructions_config(context, templates['child_instructions'], variables)
    
    def _create_mobile_variant(self, context: GenerationContext) -> None:
        """Create mobile variant of the child page."""
        config = context.config
        variables = context.variables
        
        # Get mobile template
        templates = self.template_engine.get_child_templates(config)
        mobile_template = templates.get('mobile_child_page')
        
        if mobile_template:
            print(f"  📱 Creating mobile variant...")
            self._create_mobile_child_page_component(context, mobile_template, variables)
    
    def _create_adaptive_wrapper(self, context: GenerationContext) -> None:
        """Create adaptive wrapper based on project capabilities."""
        config = context.config
        capabilities = context.capabilities
        
        # Select appropriate wrapper template
        wrapper_template = self.wrapper_selector.select_wrapper_template(config, capabilities)
        
        # Validate wrapper selection
        validation_issues = self.wrapper_selector.validate_wrapper_selection(wrapper_template, config, capabilities)
        if validation_issues:
            print(f"  ⚠️  Wrapper validation warnings:")
            for issue in validation_issues:
                print(f"     - {issue}")
        
        # Generate wrapper-specific variables
        wrapper_variables = self.variable_generator.generate_wrapper_variables(context, wrapper_template)
        
        # Create wrapper component
        self._create_child_wrapper_component(context, wrapper_template, wrapper_variables)
        
        print(f"  🎯 Selected wrapper: {self.wrapper_selector.get_wrapper_description(wrapper_template)}")
    
    def _create_child_page_component(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create the main child page component."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.pages_dir / config.parent_id / f"{config.page_name}.tsx"
        self.file_writer.write_file(
            file_path,
            content,
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def _create_mobile_child_page_component(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create the mobile child page component."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.pages_dir / config.parent_id / f"Mobile{config.page_name}.tsx"
        self.file_writer.write_file(
            file_path,
            content,
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def _create_child_wrapper_component(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create the child wrapper component."""
        config = context.config
        
        # Use the full template path including components/ prefix
        full_template_path = f"components/{template_name}"
        content = self.template_engine.render_template(full_template_path, variables)
        
        file_path = context.components_dir / config.parent_id / f"{config.page_name}Wrapper.tsx"
        self.file_writer.write_file(
            file_path,
            content,
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def _create_child_actions_config(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create child actions configuration for action sheet."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.actions_dir / f"{config.page_id}.ts"
        self.file_writer.write_file(
            file_path,
            content,
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def _create_child_instructions_config(self, context: GenerationContext, template_name: str, variables: Dict[str, str]) -> None:
        """Create child instructions configuration."""
        config = context.config
        
        content = self.template_engine.render_template(template_name, variables)
        
        file_path = context.instructions_dir / f"{config.page_id}.ts"
        self.file_writer.write_file(
            file_path,
            content,
            "ChildPageGenerator",
            "/tools/frontend-tools/mobile-pages-v2/modules/child_generator.py"
        )
    
    def _get_wrapper_description(self, context: GenerationContext) -> str:
        """Get description of the selected wrapper."""
        wrapper_template = self.wrapper_selector.select_wrapper_template(context.config, context.capabilities)
        return self.wrapper_selector.get_wrapper_description(wrapper_template)
    
    def validate_child_creation(self, context: GenerationContext) -> Dict[str, bool]:
        """Validate that all child files were created successfully."""
        config = context.config
        validation_results = {}
        
        # Check main child page
        child_page_path = context.pages_dir / config.parent_id / f"{config.page_name}.tsx"
        validation_results['child_page'] = child_page_path.exists()
        
        # Check mobile variant if requested
        if config.mobile:
            mobile_page_path = context.pages_dir / config.parent_id / f"Mobile{config.page_name}.tsx"
            validation_results['mobile_child_page'] = mobile_page_path.exists()
        
        # Check wrapper
        wrapper_path = context.components_dir / config.parent_id / f"{config.page_name}Wrapper.tsx"
        validation_results['child_wrapper'] = wrapper_path.exists()
        
        # Check action/instruction files
        actions_path = context.actions_dir / f"{config.page_id}.ts"
        validation_results['child_actions'] = actions_path.exists()
        
        instructions_path = context.instructions_dir / f"{config.page_id}.ts"
        validation_results['child_instructions'] = instructions_path.exists()
        
        return validation_results
    
    def get_created_files(self, context: GenerationContext) -> list:
        """Get list of files that would be created for a child page."""
        config = context.config
        
        files = [
            context.pages_dir / config.parent_id / f"{config.page_name}.tsx",
            context.components_dir / config.parent_id / f"{config.page_name}Wrapper.tsx",
            context.actions_dir / f"{config.page_id}.ts",
            context.instructions_dir / f"{config.page_id}.ts"
        ]
        
        # Add mobile variant if requested
        if config.mobile:
            files.append(context.pages_dir / config.parent_id / f"Mobile{config.page_name}.tsx")
        
        return files
    
    def _init_config_integration(self, context: GenerationContext) -> None:
        """Initialize config integration if available."""
        try:
            if 'ConfigIntegration' in globals():
                self.config_integration = ConfigIntegration(context.frontend_root)
                self.config_integration.create_config_if_missing()
        except Exception as e:
            print(f"Warning: Could not initialize config integration: {e}")
    
    def _register_child_in_config(self, context: GenerationContext) -> None:
        """Register child page in central configuration."""
        if self.config_integration:
            try:
                self.config_integration.register_child_page(context.config)
            except Exception as e:
                print(f"Warning: Could not register child page in config: {e}")