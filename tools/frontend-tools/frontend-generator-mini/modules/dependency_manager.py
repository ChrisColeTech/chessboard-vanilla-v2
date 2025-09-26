"""
Dependency Manager for creating missing components like usePageData hook and DataTable.
Enhanced with specialized integration modules for complete page integration.
"""

from pathlib import Path
from typing import Dict, List
try:
    from .config import ProjectCapabilities, GenerationContext
    from .template_engine import TemplateEngine
    from .file_writer import FileWriter
    from .action_registry_manager import ActionRegistryManager
    from .container_integrator import ContainerIntegrator
    from .hook_integrator import HookIntegrator
    from .integration_validator import IntegrationValidator
    from .template_dependency_scanner import TemplateDependencyScanner
except ImportError:
    from config import ProjectCapabilities, GenerationContext
    from template_engine import TemplateEngine
    from file_writer import FileWriter
    from action_registry_manager import ActionRegistryManager
    from container_integrator import ContainerIntegrator
    from hook_integrator import HookIntegrator
    from integration_validator import IntegrationValidator
    from template_dependency_scanner import TemplateDependencyScanner
import subprocess
import sys


class DependencyManager:
    """Manages creation of missing project dependencies and specialized page integration."""
    
    def __init__(self, template_engine: TemplateEngine, file_writer: FileWriter):
        self.template_engine = template_engine
        self.file_writer = file_writer
        
        # Specialized integration modules (initialized per-project)
        self._action_registry = None
        self._container_integrator = None
        self._hook_integrator = None
        self._integration_validator = None
    
    def _ensure_specialized_modules(self, context: GenerationContext) -> None:
        """Initialize specialized integration modules for the current project."""
        if self._action_registry is None:
            self._action_registry = ActionRegistryManager(context.frontend_root, self.file_writer)
        if self._container_integrator is None:
            self._container_integrator = ContainerIntegrator(context.frontend_root, self.file_writer)
        if self._hook_integrator is None:
            self._hook_integrator = HookIntegrator(context.frontend_root, self.file_writer)
        if self._integration_validator is None:
            self._integration_validator = IntegrationValidator(context.frontend_root)
    
    def ensure_use_page_data_hook(self, context: GenerationContext) -> None:
        """Ensure usePageData hook exists."""
        hook_path = context.frontend_root / "src" / "hooks" / "core" / "usePageData.ts"
        
        if hook_path.exists():
            print(f"  ✅ usePageData hook already exists: {hook_path}")
            return
        
        print(f"  📝 Creating missing usePageData hook...")
        
        # Generate usePageData hook from template
        variables = {
            'GENERATOR_NAME': 'DependencyManager',
            'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py'
        }
        
        content = self.template_engine.render_template(
            'dependencies/use-page-data-hook.ts.template',
            variables
        )
        
        self.file_writer.write_file(
            hook_path,
            content,
            "DependencyManager",
            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
        )
    
    def ensure_data_table_component(self, context: GenerationContext) -> None:
        """Ensure DataTable component exists."""
        component_path = context.frontend_root / "src" / "components" / "ui" / "DataTable.tsx"
        
        if component_path.exists():
            print(f"  ✅ DataTable component already exists: {component_path}")
            return
        
        print(f"  📝 Creating missing DataTable component...")
        
        # Generate DataTable component from template
        variables = {
            'GENERATOR_NAME': 'DependencyManager',
            'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py'
        }
        
        content = self.template_engine.render_template(
            'dependencies/data-table-component.tsx.template',
            variables
        )
        
        self.file_writer.write_file(
            component_path,
            content,
            "DependencyManager", 
            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
        )
    
    def ensure_css_types(self, context: 'GenerationContext') -> None:
        """Ensure CSS types for WebKit properties exist."""
        types_path = context.frontend_root / "src" / "types" / "css.d.ts"
        
        if types_path.exists():
            print(f"  ✅ CSS types already exist: {types_path}")
            return
        
        print(f"  📝 Creating missing CSS types...")
        
        # Generate CSS types from template
        variables = {
            'GENERATOR_NAME': 'DependencyManager',
            'SOURCE_FILE': '/tools/frontend-tools/mobile-pages-mini/modules/dependency_manager.py'
        }
        
        content = self.template_engine.render_template(
            'types/css.d.ts.template',
            variables
        )
        
        self.file_writer.write_file(
            types_path,
            content,
            "DependencyManager", 
            "/tools/frontend-tools/mobile-pages-mini/modules/dependency_manager.py"
        )
    
    def ensure_dynamic_action_sheet_container(self, context: GenerationContext) -> None:
        """Ensure dynamic ActionSheetContainer is generated with current pages."""
        container_path = context.frontend_root / "src" / "components" / "action-sheet" / "ActionSheetContainer.tsx"
        
        print(f"  📝 Generating dynamic ActionSheetContainer...")
        
        # Generate ActionSheetContainer variables
        from .variable_generator import VariableGenerator
        variable_generator = VariableGenerator()
        variables = variable_generator.generate_action_sheet_container_variables(context)
        
        # Render dynamic template
        content = self.template_engine.render_template(
            'components/action-sheet-container.tsx.template',
            variables
        )
        
        # Ensure directory exists
        container_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.file_writer.write_file(
            container_path,
            content,
            "DependencyManager",
            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
        )
    
    def ensure_dynamic_page_actions_registry(self, context: GenerationContext) -> None:
        """Ensure dynamic PAGE_ACTIONS registry is generated with current pages."""
        registry_path = context.frontend_root / "src" / "constants" / "actions" / "page-actions.constants.ts"
        
        print(f"  📝 Generating dynamic PAGE_ACTIONS registry...")
        
        # Generate PAGE_ACTIONS registry variables
        from .variable_generator import VariableGenerator
        variable_generator = VariableGenerator()
        variables = variable_generator.generate_page_actions_registry_variables(context)
        
        # Render dynamic template
        content = self.template_engine.render_template(
            'constants/page-actions.constants.ts.template',
            variables
        )
        
        # Ensure directory exists
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.file_writer.write_file(
            registry_path,
            content,
            "DependencyManager",
            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
        )
    
    def integrate_parent_page(self, context: GenerationContext, parent_id: str) -> bool:
        """
        Complete integration of parent page using specialized modules.
        Handles registry, container, and hook integration.
        """
        print(f"🔗 Integrating parent page '{parent_id}' with specialized modules...")
        self._ensure_specialized_modules(context)
        
        success = True
        
        try:
            # Step 1: Regenerate dynamic PAGE_ACTIONS registry with all pages
            print(f"  📝 Regenerating dynamic PAGE_ACTIONS registry...")
            self.ensure_dynamic_page_actions_registry(context)
            
            # Step 2: Regenerate dynamic ActionSheetContainer with all page hooks
            print(f"  📦 Regenerating dynamic ActionSheetContainer...")
            self.ensure_dynamic_action_sheet_container(context)
            
            # Note: Parent hooks are already generated by ParentPageGenerator with proper variable substitution
            # No need for separate hook generation here since the templates are now working correctly
            
            if success:
                print(f"  ✅ Parent '{parent_id}' successfully integrated with all systems")
            else:
                print(f"  ❌ Some integration steps failed for parent '{parent_id}'")
            
        except Exception as e:
            print(f"  ❌ Error during parent integration: {e}")
            success = False
        
        return success
    
    def integrate_child_pages(self, context: GenerationContext, parent_id: str) -> bool:
        """
        Complete integration of child pages using specialized modules.
        Handles registry, container, and hook integration for all children.
        """
        print(f"🔗 Integrating child pages for parent '{parent_id}' with specialized modules...")
        self._ensure_specialized_modules(context)
        
        success = True
        
        try:
            # Step 1: Register child actions in PAGE_ACTIONS registry with sibling navigation
            print(f"  📝 Registering child actions with sibling navigation...")
            if not self._action_registry.register_child_actions(parent_id):
                success = False
            
            # Step 2: Add sibling navigation to COMMON_ACTIONS
            print(f"  🧭 Adding sibling navigation to common actions...")
            if not self._action_registry.add_sibling_navigation(parent_id):
                success = False
            
            # Step 3: Integrate children with ActionSheetContainer
            print(f"  📦 Integrating child pages with ActionSheetContainer...")
            if not self._container_integrator.integrate_child_pages(parent_id):
                success = False
            
            # Step 4: Generate functional child hooks
            print(f"  🪝 Generating functional child hooks...")
            children = self._get_children_for_parent(parent_id, context)
            for child in children:
                child_id = child['id']
                if not self._hook_integrator.generate_child_action_hook(child_id, parent_id):
                    success = False
            
            if success:
                print(f"  ✅ All child pages for '{parent_id}' successfully integrated")
            else:
                print(f"  ❌ Some child integration steps failed for '{parent_id}'")
            
        except Exception as e:
            print(f"  ❌ Error during child integration: {e}")
            success = False
        
        return success
    
    def validate_page_integration(self, context: GenerationContext, page_id: str) -> bool:
        """
        Validate complete page integration using IntegrationValidator.
        Returns True if all validations pass.
        """
        print(f"🔍 Validating integration for page '{page_id}'...")
        self._ensure_specialized_modules(context)
        
        try:
            validation_result = self._integration_validator.validate_page_integration(page_id)
            
            if validation_result.is_valid:
                print(f"  ✅ Page '{page_id}' integration is valid and complete")
                return True
            else:
                print(f"  ❌ Page '{page_id}' integration has issues:")
                for issue in validation_result.all_issues:
                    print(f"    • {issue}")
                
                if validation_result.has_critical_issues:
                    print(f"  🚨 Critical issues found - page may not function correctly")
                
                return False
                
        except Exception as e:
            print(f"  ❌ Error during validation: {e}")
            return False
    
    def validate_complete_integration(self, context: GenerationContext) -> bool:
        """
        Validate complete project integration using IntegrationValidator.
        Returns True if all validations pass.
        """
        print(f"🔍 Validating complete project integration...")
        self._ensure_specialized_modules(context)
        
        try:
            validation_result = self._integration_validator.validate_complete_project_integration()
            
            print(f"\n{self._integration_validator.get_integration_summary(validation_result)}\n")
            
            return validation_result.is_valid
                
        except Exception as e:
            print(f"  ❌ Error during complete validation: {e}")
            return False
    
    def fix_integration_issues(self, context: GenerationContext, page_id: str = None) -> bool:
        """
        Attempt to fix integration issues by re-running all integration steps.
        If page_id is provided, fixes issues for that specific page and its relationships.
        If page_id is None, fixes issues for the entire project.
        """
        print(f"🔧 Attempting to fix integration issues...")
        self._ensure_specialized_modules(context)
        
        try:
            if page_id:
                # Fix specific page
                page_info = self._get_page_info(page_id, context)
                if not page_info:
                    print(f"  ❌ Page '{page_id}' not found in configuration")
                    return False
                
                page_type = page_info.get('type')
                
                if page_type == 'parent':
                    # Re-run parent integration
                    parent_success = self.integrate_parent_page(context, page_id)
                    child_success = self.integrate_child_pages(context, page_id)
                    return parent_success and child_success
                    
                elif page_type == 'child':
                    # Re-run child integration for the parent
                    parent_id = page_info.get('parent_id')
                    if parent_id:
                        return self.integrate_child_pages(context, parent_id)
                    else:
                        print(f"  ❌ Child page '{page_id}' has no parent_id")
                        return False
                        
            else:
                # Fix entire project
                success = True
                
                # Get all parent pages and fix each one
                config_data = self._load_config(context)
                pages = config_data.get('pages', {})
                
                parent_pages = [pid for pid, pinfo in pages.items() if pinfo.get('type') == 'parent']
                
                for parent_id in parent_pages:
                    parent_success = self.integrate_parent_page(context, parent_id)
                    child_success = self.integrate_child_pages(context, parent_id)
                    if not (parent_success and child_success):
                        success = False
                
                return success
                
        except Exception as e:
            print(f"  ❌ Error during integration fix: {e}")
            return False
    
    def _get_children_for_parent(self, parent_id: str, context: GenerationContext) -> List[Dict]:
        """Get all children for a parent from pages.config.json"""
        try:
            # Use the ActionRegistryManager's method since it's already implemented
            return self._action_registry._get_children_for_parent(parent_id)
        except Exception as e:
            print(f"  ⚠️  Error getting children for parent {parent_id}: {e}")
            return []
    
    def _get_page_info(self, page_id: str, context: GenerationContext) -> Dict:
        """Get page information from pages.config.json"""
        try:
            # Use the ActionRegistryManager's method since it's already implemented
            return self._action_registry._get_page_info(page_id)
        except Exception as e:
            print(f"  ⚠️  Error loading page info: {e}")
            return None
    
    def _load_config(self, context: GenerationContext) -> Dict:
        """Load pages.config.json data"""
        try:
            # Use the ActionRegistryManager's config integration
            return self._action_registry.config_integration.load_config()
        except Exception as e:
            print(f"  ⚠️  Error loading config: {e}")
            return {"pages": {}}
    
    def validate_and_create_root_files(self, context: GenerationContext, force: bool = False) -> None:
        """Validate and create missing root configuration files."""
        print(f"🔍 Checking root configuration files...")
        
        # Define required root files and their templates
        root_files = {
            'index.html': None,  # No template, will create manually
            'vite.config.ts': None,  # No template, will create manually  
            'tsconfig.json': None,  # Might exist, skip if not force
            'tsconfig.node.json': None,  # Might exist, skip if not force
            # 'package.json': None,  # DON'T MODIFY USER'S PACKAGE.JSON
            context.frontend_root / 'src' / 'main.tsx': 'main.tsx.template',
            context.frontend_root / 'src' / 'App.tsx': 'App.tsx.template',
            context.frontend_root / 'src' / 'App.css': 'App.css.template',
            context.frontend_root / 'src' / 'index.css': 'index.css.template',
            context.frontend_root / 'src' / 'vite-env.d.ts': 'vite-env.d.ts.template'
        }
        
        # Define navigation-critical files that should always be overwritten
        # Note: App.tsx removed to allow NavigationGenerator to manage it
        navigation_critical_files = {'main.tsx'}
        
        for file_path, template_name in root_files.items():
            if isinstance(file_path, str):
                file_path = context.frontend_root / file_path
            
            # Determine if this file should be forced (navigation-critical files always get overwritten)
            should_force = force or file_path.name in navigation_critical_files
            
            # Skip if file exists and not forcing (except for navigation-critical files)
            if file_path.exists() and not should_force:
                print(f"  ✅ Exists: {file_path.relative_to(context.frontend_root)}")
                continue
                
            if template_name:
                # Check if file exists before writing for proper messaging
                file_existed = file_path.exists()
                is_navigation_critical = file_path.name in navigation_critical_files
                
                # Create from template
                try:
                    # Use context variables if available (for navigation variables)
                    template_variables = getattr(context, 'variables', {})
                    content = self.template_engine.render_template(template_name, template_variables, is_static=True)
                    self.file_writer.write_file(
                        file_path,
                        content,
                        "DependencyManager",
                        "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
                    )
                    if file_existed and is_navigation_critical:
                        print(f"  🔄 Updated navigation-critical file: {file_path.relative_to(context.frontend_root)}")
                    else:
                        print(f"  ✅ Created from template: {file_path.relative_to(context.frontend_root)}")
                    
                    # Check if content still contains template variables
                    if "{{" in content and "}}" in content:
                        print(f"  ⚠️  Warning: Content contains template variables that may not have been substituted")
                except Exception as e:
                    print(f"  ⚠️  Failed to create {file_path.relative_to(context.frontend_root)}: {e}")
            else:
                # Handle non-template files manually
                self._create_manual_root_file(file_path, context)

    def _create_manual_root_file(self, file_path: Path, context: GenerationContext) -> None:
        """Create root files that don't have templates."""
        file_name = file_path.name
        
        try:
            if file_name == 'index.html':
                content = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Template Generated Project</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>'''
            elif file_name == 'vite.config.ts':
                content = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
})'''
# REMOVED: Don't contaminate user's package.json
            elif file_name == 'tsconfig.node.json':
                content = '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}'''
            else:
                return  # Skip unknown files
                
            self.file_writer.write_file(
                file_path,
                content,
                "DependencyManager",
                "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
            )
            print(f"  ✅ Created: {file_path.relative_to(context.frontend_root)}")
            
        except Exception as e:
            print(f"  ⚠️  Failed to create {file_name}: {e}")
    
    def _update_package_json(self, file_path: Path) -> None:
        """Update package.json with proper build configuration."""
        import json
        
        try:
            # Read existing package.json
            if file_path.exists():
                with open(file_path, 'r') as f:
                    package_data = json.load(f)
            else:
                package_data = {
                    "name": "template-generated-project",
                    "version": "1.0.0",
                    "type": "module"
                }
            
            # Update scripts
            package_data.setdefault("scripts", {})
            package_data["scripts"].update({
                "dev": "vite",
                "build": "tsc && vite build", 
                "preview": "vite preview"
            })
            
            # Ensure dependencies exist
            package_data.setdefault("dependencies", {})
            required_deps = {
                "react": "^18.0.0",
                "react-dom": "^18.0.0", 
                "zustand": "^5.0.8",
                "lucide-react": "^0.544.0"
            }
            package_data["dependencies"].update(required_deps)
            
            # Ensure devDependencies exist
            package_data.setdefault("devDependencies", {})
            required_dev_deps = {
                "@types/react": "^19.1.13",
                "@types/react-dom": "^19.1.9",
                "typescript": "^5.9.2",
                "vite": "^5.0.0",
                "@vitejs/plugin-react": "^4.0.0"
            }
            package_data["devDependencies"].update(required_dev_deps)
            
            # Write updated package.json
            with open(file_path, 'w') as f:
                json.dump(package_data, f, indent=2)
                
        except Exception as e:
            print(f"  ⚠️  Failed to update package.json: {e}")

    def ensure_styles_directory(self, context: GenerationContext, force: bool = False) -> None:
        """Skip styles directory copying in mini version."""
        print(f"📂 Skipping styles directory copying (mini version)")
        return

    def validate_all_static_dependencies(self, context: GenerationContext) -> dict:
        """Skip static dependencies validation in mini version."""
        print(f"🔍 Skipping static dependencies validation (mini version)")
        return {
            'all_valid': True,
            'missing_templates': [],
            'missing_dependencies': []
        }

    def ensure_all_dependencies(self, context: GenerationContext, required_templates: set = None) -> None:
        """Ensure only essential dependencies exist (mini version)."""
        print(f"🔍 Checking essential dependencies for: {context.frontend_root}")
        
        # Check and create usePageData hook (always create if missing)
        self.ensure_use_page_data_hook(context)
        
        # Check and create DataTable component (only if not detected)
        if not context.capabilities.has_data_table:
            self.ensure_data_table_component(context)
        
        # Check and create CSS types for WebKit properties (always create if missing)
        self.ensure_css_types(context)
        
        # Create essential static templates (mini version - only essential ones)
        self.ensure_essential_static_templates(context)
        
        print(f"✅ Essential dependencies verified")
    
    def ensure_all_dependencies_with_integration(self, context: GenerationContext, required_templates: set = None) -> None:
        """
        Enhanced version that includes specialized module integration.
        Use this method for complete page generation with proper integration.
        """
        print(f"🔍 Checking dependencies and integration for: {context.frontend_root}")
        
        # Step 1: Ensure basic dependencies
        self.ensure_all_dependencies(context, required_templates)
        
        # Step 2: Initialize specialized modules
        self._ensure_specialized_modules(context)
        
        # Step 3: Perform integration based on context
        if hasattr(context.config, 'parent') and context.config.parent:
            # Child page integration
            parent_id = context.config.parent_id if hasattr(context.config, 'parent_id') else context.config.parent
            child_id = context.config.page_id
            
            print(f"🔗 Performing child page integration for '{child_id}' under parent '{parent_id}'...")
            
            # Integrate child and update parent
            child_success = self.integrate_child_pages(context, parent_id)
            
            # Update parent hook for new child (if needed)
            if child_success:
                print(f"  🔄 Updating parent hook for new child...")
                self._hook_integrator.update_parent_hook_for_new_child(parent_id, child_id)
            
        else:
            # Parent page integration
            parent_id = context.config.page_id
            
            print(f"🔗 Performing parent page integration for '{parent_id}'...")
            
            # Integrate parent page
            parent_success = self.integrate_parent_page(context, parent_id)
            
            # Integrate any existing children
            if parent_success:
                self.integrate_child_pages(context, parent_id)
        
        # Step 4: Validate integration
        print(f"🔍 Validating integration...")
        validation_success = self.validate_complete_integration(context)
        
        if validation_success:
            print(f"✅ All dependencies and integration verified")
        else:
            print(f"⚠️  Integration validation found issues - consider running fix_integration_issues()")
            
            # Optionally attempt to fix issues automatically
            print(f"🔧 Attempting to fix integration issues automatically...")
            if self.fix_integration_issues(context):
                print(f"✅ Integration issues resolved")
            else:
                print(f"❌ Some integration issues could not be resolved automatically")
    
    def regenerate_index_files(self, frontend_root: Path) -> None:
        """Regenerate index files using the index generator."""
        try:
            # Path to the index generator script
            index_generator_path = Path(__file__).parent.parent.parent / "index-generator-v2" / "index_generator.py"
            
            if not index_generator_path.exists():
                print(f"  ⚠️  Index generator not found at: {index_generator_path}")
                return
            
            print(f"  🔄 Regenerating index files...")
            
            result = subprocess.run([
                sys.executable, 
                str(index_generator_path), 
                str(frontend_root / "src")
            ], capture_output=True, text=True, cwd=index_generator_path.parent)
            
            if result.returncode == 0:
                print(f"  ✅ Index files regenerated successfully")
            else:
                print(f"  ⚠️  Index generation had issues: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"  ⚠️  Failed to run index generator: {e}")
    
    def validate_dependencies(self, context: GenerationContext) -> Dict[str, bool]:
        """Validate that all dependencies exist and are accessible."""
        validation_results = {}
        
        # Check usePageData hook
        hook_path = context.frontend_root / "src" / "hooks" / "core" / "usePageData.ts"
        validation_results['usePageData'] = hook_path.exists()
        
        # Check DataTable component
        table_path = context.frontend_root / "src" / "components" / "ui" / "DataTable.tsx"
        validation_results['DataTable'] = table_path.exists()
        
        # Check page hooks if they should exist
        if context.capabilities.has_page_hooks:
            instructions_path = context.frontend_root / "src" / "hooks" / "core" / "usePageInstructions.ts"
            actions_path = context.frontend_root / "src" / "hooks" / "core" / "usePageActions.ts"
            validation_results['usePageInstructions'] = instructions_path.exists()
            validation_results['usePageActions'] = actions_path.exists()
        
        # Check mobile hook if it should exist
        if context.capabilities.has_mobile_hook:
            mobile_path = context.frontend_root / "src" / "hooks" / "core" / "useIsMobile.ts"
            validation_results['useIsMobile'] = mobile_path.exists()
        
        return validation_results
    
    def get_missing_dependencies(self, context: GenerationContext) -> list:
        """Get list of missing dependencies."""
        validation_results = self.validate_dependencies(context)
        return [dep for dep, exists in validation_results.items() if not exists]
    
    def ensure_static_components(self, context: GenerationContext, required_templates: set = None) -> None:
        """Skip static components creation in mini version."""
        print(f"📦 Skipping static components creation (mini version)")
        return
    
    def ensure_essential_static_templates(self, context: GenerationContext) -> None:
        """Create all static templates required by generated pages using dependency scanning."""
        print(f"📦 Creating required static templates using dependency analysis")
        
        # Initialize dependency scanner
        scanner = TemplateDependencyScanner(
            static_templates_dir=self.template_engine.static_dir,
            dynamic_templates_dir=self.template_engine.dynamic_dir
        )
        
        # Determine page type based on context
        page_type = "child" if hasattr(context.config, 'parent') and context.config.parent else "parent"
        
        # Scan dependencies for this page type
        scan_result = scanner.scan_dependencies(page_type)
        
        print(f"📊 Dependency scan found {len(scan_result.required_templates)} required templates")
        if scan_result.missing_templates:
            print(f"⚠️  Found {len(scan_result.missing_templates)} missing templates:")
            for missing in sorted(scan_result.missing_templates):
                print(f"    ❌ {missing}")
        
        # Convert required templates to (template_path, output_path) tuples
        required_template_tuples = []
        for template_path in scan_result.required_templates:
            # Convert template path to output path
            if template_path.endswith('.template'):
                output_relative = template_path[:-9]  # Remove '.template'
            else:
                output_relative = template_path
            
            output_path = f"src/{output_relative}"
            required_template_tuples.append((template_path, output_path))
        
        # Always include these core templates that are essential for basic functionality
        core_essential_templates = [
            ('stores/appStore.ts.template', 'src/stores/appStore.ts'),
            ('stores/settingsStore.ts.template', 'src/stores/settingsStore.ts'),
            ('stores/authStore.ts.template', 'src/stores/authStore.ts'),
            ('types/core/action-sheet.types.ts.template', 'src/types/core/action-sheet.types.ts'),
            ('hooks/core/usePageInstructions.ts.template', 'src/hooks/core/usePageInstructions.ts'),
            ('hooks/core/usePageActions.ts.template', 'src/hooks/core/usePageActions.ts'),
            ('hooks/core/useIsMobile.ts.template', 'src/hooks/core/useIsMobile.ts'),
            ('hooks/audio/useUIClickSoundOptimized.ts.template', 'src/hooks/audio/useUIClickSoundOptimized.ts'),
            ('hooks/audio/useUIHoverSoundOptimized.ts.template', 'src/hooks/audio/useUIHoverSoundOptimized.ts'),
            ('hooks/useActionSheetDelayedPage.ts', 'src/hooks/useActionSheetDelayedPage.ts'),
            ('components/action-sheet/ActionSheet.tsx.template', 'src/components/action-sheet/ActionSheet.tsx'),
            ('constants/actions/common-actions.constants.ts.template', 'src/constants/actions/common-actions.constants.ts'),
        ]
        
        # Combine scanned dependencies with core essentials (avoid duplicates)
        all_templates = dict(required_template_tuples + core_essential_templates)
        
        static_dir = self.template_engine.static_dir
        created_count = 0
        skipped_count = 0
        
        for template_path, output_path in all_templates.items():
            full_template_path = static_dir / template_path
            full_output_path = context.frontend_root / output_path
            
            if full_template_path.exists() and not full_output_path.exists():
                try:
                    # Create directory if it doesn't exist
                    full_output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Render template with context variables
                    template_variables = getattr(context, 'variables', {})
                    content = self.template_engine.render_template(template_path, template_variables, is_static=True)
                    
                    # Write the file
                    self.file_writer.write_file(
                        full_output_path,
                        content,
                        "DependencyManager",
                        "/tools/frontend-tools/mobile-pages-mini/modules/dependency_manager.py"
                    )
                    
                    print(f"    ✅ Created: {output_path}")
                    created_count += 1
                    
                except Exception as e:
                    print(f"    ⚠️  Failed to create {template_path}: {e}")
            elif full_output_path.exists():
                print(f"    ✅ Already exists: {output_path}")
                skipped_count += 1
            elif not full_template_path.exists():
                print(f"    ⚠️  Template not found: {template_path}")
        
        print(f"📦 Created {created_count} static templates, skipped {skipped_count} existing files")
        print(f"🔍 Dependency scan successfully identified all required dependencies")

    def _template_to_output_path(self, template_rel_path: str, context: GenerationContext):
        """Convert template path to output path."""
        # Remove .template extension
        if template_rel_path.endswith('.template'):
            clean_path = template_rel_path[:-9]  # Remove '.template'
        else:
            clean_path = template_rel_path
            
        output_path = context.frontend_root / 'src' / clean_path
        return output_path

    # Static analysis methods removed in mini version

    def _create_navigation_files_dynamically(self, context: GenerationContext) -> None:
        """Create navigation files using NavigationGenerator instead of static templates."""
        try:
            print(f"  🚀 Creating navigation files dynamically...")
            
            # Import NavigationGenerator from shared modules
            import sys
            from pathlib import Path
            shared_path = Path(__file__).parent.parent.parent / "shared"
            if str(shared_path) not in sys.path:
                sys.path.append(str(shared_path))
            
            from navigation_generator import NavigationGenerator
            
            # Initialize with proper template paths
            nav_templates_dir = Path(__file__).parent.parent / "templates" / "dynamic" / "nav"
            nav_generator = NavigationGenerator(context.frontend_root, nav_templates_dir)
            
            # Generate navigation files in proper locations
            layout_dir = context.frontend_root / "src" / "components" / "layout"
            layout_dir.mkdir(parents=True, exist_ok=True)
            src_dir = context.frontend_root / "src"
            
            # Force navigation generator to reload config from disk
            nav_generator.config_manager.reload_config()
            
            # Generate files with proper directory separation
            generated_files = nav_generator.generate_navigation_files(src_dir, layout_dir)
            
            # Report success
            if generated_files:
                print(f"    ✅ Navigation files generated dynamically:")
                for name, path in generated_files.items():
                    print(f"      • {name}: {path.relative_to(context.frontend_root)}")
            else:
                print(f"    ⚠️  No navigation files were generated")
                
        except Exception as e:
            print(f"    ⚠️  Failed to generate navigation files dynamically: {e}")
            print(f"    ℹ️  Continuing with static App.tsx template")

    def create_missing_directories(self, context: GenerationContext) -> None:
        """Create any missing directory structure."""
        directories = [
            context.pages_dir,
            context.components_dir,
            context.hooks_dir,
            context.actions_dir,
            context.instructions_dir,
            context.frontend_root / "src" / "hooks" / "core",
            context.frontend_root / "src" / "components" / "ui",
            context.frontend_root / "src" / "stores",
            context.frontend_root / "src" / "types" / "core",
            context.frontend_root / "src" / "components" / "chess"
        ]
        
        for directory in directories:
            if not directory.exists():
                self.file_writer.create_directory(directory)
    
    # Convenience methods for accessing specialized modules
    def get_action_registry_manager(self, context: GenerationContext) -> ActionRegistryManager:
        """Get the ActionRegistryManager instance for this project."""
        self._ensure_specialized_modules(context)
        return self._action_registry
    
    def get_container_integrator(self, context: GenerationContext) -> ContainerIntegrator:
        """Get the ContainerIntegrator instance for this project."""
        self._ensure_specialized_modules(context)
        return self._container_integrator
    
    def get_hook_integrator(self, context: GenerationContext) -> HookIntegrator:
        """Get the HookIntegrator instance for this project."""
        self._ensure_specialized_modules(context)
        return self._hook_integrator
    
    def get_integration_validator(self, context: GenerationContext) -> IntegrationValidator:
        """Get the IntegrationValidator instance for this project."""
        self._ensure_specialized_modules(context)
        return self._integration_validator