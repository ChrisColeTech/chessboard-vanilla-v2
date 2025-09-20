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
except ImportError:
    from config import ProjectCapabilities, GenerationContext
    from template_engine import TemplateEngine
    from file_writer import FileWriter
    from action_registry_manager import ActionRegistryManager
    from container_integrator import ContainerIntegrator
    from hook_integrator import HookIntegrator
    from integration_validator import IntegrationValidator
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
        
        for file_path, template_name in root_files.items():
            if isinstance(file_path, str):
                file_path = context.frontend_root / file_path
            
            # Skip if file exists and not forcing
            if file_path.exists() and not force:
                print(f"  ✅ Exists: {file_path.relative_to(context.frontend_root)}")
                continue
                
            if template_name:
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
        """Copy all styles from static templates to the project."""
        print(f"📂 Copying styles directory...")
        
        static_styles_dir = self.template_engine.static_dir / "styles"
        target_styles_dir = context.frontend_root / "src" / "styles"
        
        if not static_styles_dir.exists():
            print(f"  ⚠️  No styles directory found in static templates")
            return
        
        # Create target styles directory
        target_styles_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all files and subdirectories
        import shutil
        
        for item in static_styles_dir.rglob("*"):
            if item.is_file():
                # Calculate relative path from styles root
                relative_path = item.relative_to(static_styles_dir)
                target_file = target_styles_dir / relative_path
                
                # Create parent directories if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Skip if file exists and not forcing
                if target_file.exists() and not force:
                    print(f"  ✅ Exists: styles/{relative_path}")
                    continue
                
                try:
                    if item.suffix == '.template':
                        # Handle template files
                        template_rel_path = f"styles/{relative_path}"
                        template_variables = getattr(context, 'variables', {})
                        content = self.template_engine.render_template(template_rel_path, template_variables, is_static=True)
                        
                        # Remove .template extension from target
                        final_target = target_file.with_suffix('').with_suffix('.css' if '.css' in str(target_file) else '')
                        
                        self.file_writer.write_file(
                            final_target,
                            content,
                            "DependencyManager",
                            "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
                        )
                        print(f"  ✅ Created from template: styles/{relative_path}")
                    else:
                        # Copy non-template files directly
                        shutil.copy2(item, target_file)
                        print(f"  ✅ Copied: styles/{relative_path}")
                        
                except Exception as e:
                    print(f"  ⚠️  Failed to copy styles/{relative_path}: {e}")

    def validate_all_static_dependencies(self, context: GenerationContext) -> dict:
        """Validate that all required static dependencies exist BEFORE generation."""
        print(f"🔍 Validating static dependencies for templates to be used...")
        
        validation_results = {
            'all_valid': True,
            'missing_templates': [],
            'missing_dependencies': []
        }
        
        # Get all static templates that will be needed based on generation context
        required_templates = self._get_required_templates_for_generation(context)
        
        static_dir = self.template_engine.static_dir
        
        # Validate each required template exists
        for template_path in required_templates:
            full_template_path = static_dir / template_path
            if not full_template_path.exists():
                validation_results['missing_templates'].append(template_path)
                validation_results['all_valid'] = False
                print(f"  ❌ Missing template: {template_path}")
            else:
                print(f"  ✅ Found template: {template_path}")
        
        # Now validate the dependencies of all existing templates
        if validation_results['all_valid']:
            all_deps = self._analyze_generated_imports(context)
            for template_path, output_path in all_deps:
                full_template_path = static_dir / template_path
                if not full_template_path.exists():
                    validation_results['missing_dependencies'].append(template_path)
                    validation_results['all_valid'] = False
                    print(f"  ❌ Missing dependency template: {template_path}")
        
        return validation_results

    def ensure_all_dependencies(self, context: GenerationContext, required_templates: set = None) -> None:
        """Ensure all required dependencies exist."""
        print(f"🔍 Checking dependencies for: {context.frontend_root}")
        
        # Check and create usePageData hook (always create if missing)
        self.ensure_use_page_data_hook(context)
        
        # Check and create DataTable component (only if not detected)
        if not context.capabilities.has_data_table:
            self.ensure_data_table_component(context)
        
        # Create static components that templates expect
        self.ensure_static_components(context, required_templates)
        
        print(f"✅ All dependencies verified")
    
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
        """Create static components from scanner results."""
        print(f"  🔍 DEBUG: required_templates={required_templates is not None}, type={type(required_templates)}, len={len(required_templates) if required_templates else 0}")
        
        if required_templates is None or len(required_templates) == 0:
            print(f"  📦 Creating essential static components + proactive dependencies...")
            # Fall back to old method if no scanner results provided
            all_deps = self._analyze_generated_imports(context)
        else:
            print(f"  📦 Creating all {len(required_templates)} required templates from scanner...")
            all_deps = []
            for template_rel_path in required_templates:
                output_path = self._template_to_output_path(template_rel_path, context)
                if output_path:
                    all_deps.append((template_rel_path, output_path))
        
        # Phase 1: Detection Logic - Identify navigation files
        NAVIGATION_FILES = {
            'components/layout/types.ts.template',
            'components/layout/TabBar.tsx.template', 
            'components/layout/App.tsx.template',
            'App.tsx.template',  # Root App.tsx that gets replaced by NavigationGenerator
            'stores/appStore.ts.template'  # appStore with dynamic selectedTab
        }
        
        # Phase 2: Conditional Processing - Separate navigation from regular templates
        navigation_templates = [(t, p) for t, p in all_deps if t in NAVIGATION_FILES]
        regular_templates = [(t, p) for t, p in all_deps if t not in NAVIGATION_FILES]
        
        print(f"  📍 Found {len(navigation_templates)} navigation templates, {len(regular_templates)} regular templates")
        
        # Process regular static templates normally
        for template_path, output_path in regular_templates:
            if not output_path.exists():
                try:
                    # Create directory if it doesn't exist
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Render static template with context variables (for navigation variables)
                    template_variables = getattr(context, 'variables', {})
                    content = self.template_engine.render_template(template_path, template_variables, is_static=True)
                    
                    # Write the file
                    self.file_writer.write_file(
                        output_path,
                        content,
                        "DependencyManager",
                        "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
                    )
                    
                    print(f"    ✅ Created: {output_path.relative_to(context.frontend_root)}")
                    
                except Exception as e:
                    print(f"    ⚠️  Failed to create {template_path}: {e}")
            else:
                print(f"    ✅ Already exists: {output_path.relative_to(context.frontend_root)}")
        
        # Phase 3: Navigation Generation Integration - Process navigation templates via NavigationGenerator
        if navigation_templates:
            self._create_navigation_files_dynamically(context, navigation_templates)
    
    def _create_navigation_files_dynamically(self, context: GenerationContext, nav_templates: list) -> None:
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
                # Fallback to static templates
                self._fallback_to_static_navigation(context, nav_templates)
                
        except Exception as e:
            print(f"    ⚠️  Failed to generate navigation files dynamically: {e}")
            # Fallback to static templates if navigation generation fails
            self._fallback_to_static_navigation(context, nav_templates)
    
    def _fallback_to_static_navigation(self, context: GenerationContext, nav_templates: list) -> None:
        """Fallback to static navigation templates if dynamic generation fails."""
        print(f"    🔄 Falling back to static navigation templates...")
        
        for template_path, output_path in nav_templates:
            if not output_path.exists():
                try:
                    # Create directory if it doesn't exist
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Render static template with context variables
                    template_variables = getattr(context, 'variables', {})
                    content = self.template_engine.render_template(template_path, template_variables, is_static=True)
                    
                    # Write the file
                    self.file_writer.write_file(
                        output_path,
                        content,
                        "DependencyManager",
                        "/tools/frontend-tools/mobile-pages-v2/modules/dependency_manager.py"
                    )
                    
                    print(f"      ✅ Created (fallback): {output_path.relative_to(context.frontend_root)}")
                    
                except Exception as e:
                    print(f"      ⚠️  Failed to create {template_path}: {e}")
            else:
                print(f"      ✅ Already exists: {output_path.relative_to(context.frontend_root)}")

    def _template_to_output_path(self, template_rel_path: str, context: GenerationContext):
        """Convert template path to output path."""
        # Remove .template extension
        if template_rel_path.endswith('.template'):
            clean_path = template_rel_path[:-9]  # Remove '.template'
        else:
            clean_path = template_rel_path
            
        output_path = context.frontend_root / 'src' / clean_path
        return output_path

    def _analyze_generated_imports(self, context: GenerationContext) -> list:
        """Proactively analyze static template imports to find all needed dependencies."""
        import re
        
        static_deps = set()
        static_dir = self.template_engine.static_dir
        
        # Dynamically detect which static templates are referenced by dynamic templates
        essential_templates = self._detect_required_static_templates(context)
        
        # Process each essential template and recursively find its dependencies
        to_process = essential_templates.copy()
        processed = set()
        
        while to_process:
            template_rel_path = to_process.pop(0)
            
            if template_rel_path in processed:
                continue
                
            processed.add(template_rel_path)
            template_path = static_dir / template_rel_path
            
            if template_path.exists():
                # Add this template to dependencies
                output_path = context.frontend_root / "src" / template_rel_path.replace('.template', '')
                static_deps.add((template_rel_path, output_path))
                
                # Analyze its imports to find more dependencies
                try:
                    content = template_path.read_text(encoding='utf-8')
                    import_matches = re.findall(r'import.*?from\s+[\'"]([^\'"]+)[\'"]', content)
                    
                    for import_path in import_matches:
                        if import_path.startswith('../'):
                            # Find matching static template for this import
                            dep_template = self._find_template_for_import(import_path, template_rel_path, static_dir)
                            if dep_template and dep_template not in processed:
                                to_process.append(dep_template)
                                
                except Exception as e:
                    print(f"    ⚠️  Could not analyze template {template_rel_path}: {e}")
        
        return list(static_deps)
    
    def _resolve_import_path(self, from_file, import_path):
        """Resolve relative import path to absolute file path."""
        from pathlib import Path
        
        # Get the directory of the importing file
        base_dir = from_file.parent
        
        # Resolve the relative path
        resolved = (base_dir / import_path).resolve()
        
        # Add common extensions if not present
        if not resolved.suffix:
            for ext in ['.ts', '.tsx', '.js', '.jsx']:
                if (resolved.parent / (resolved.name + ext)).exists():
                    return resolved.parent / (resolved.name + ext)
        
        return resolved
    
    def _find_template_for_import(self, import_path, from_template_path, static_dir):
        """Find static template that matches an import path from another template."""
        from pathlib import Path
        
        try:
            # Get the directory of the importing template
            from_template = Path(from_template_path)
            base_dir = from_template.parent
            
            # Resolve the import relative to the template's location
            resolved_import = (base_dir / import_path).resolve()
            
            # Convert to template path
            template_candidate = str(resolved_import) + '.template'
            template_path = static_dir / template_candidate
            
            if template_path.exists():
                return template_candidate
                
            # Try with common extensions
            for ext in ['.ts', '.tsx', '.js', '.jsx']:
                template_candidate = str(resolved_import) + ext + '.template'
                template_path = static_dir / template_candidate
                if template_path.exists():
                    return template_candidate
                    
        except Exception:
            pass
            
        return None
    
    def _get_required_templates_for_generation(self, context: GenerationContext) -> list:
        """Determine which specific templates will be used for this generation."""
        required_templates = set()
        
        # Determine which dynamic templates will be used based on generation context
        if hasattr(context.config, 'parent') and context.config.parent:
            # Child page generation
            if context.config.mobile:
                # Mobile child templates
                dynamic_templates = [
                    'pages/mobile-child-page.tsx.template',
                    'wrappers/child-wrapper-basic-hooks.tsx.template'  # Or full-hooks based on capabilities
                ]
            else:
                # Regular child templates  
                dynamic_templates = [
                    'pages/child-page.tsx.template',
                    'wrappers/child-wrapper-basic-hooks.tsx.template'  # Or full-hooks based on capabilities
                ]
                
            # Upgrade to full wrapper if capabilities support it
            if context.capabilities.has_mobile_hook:
                dynamic_templates = [t.replace('basic-hooks', 'full-hooks') for t in dynamic_templates]
                
        else:
            # Parent page generation
            dynamic_templates = [
                'pages/parent-page.tsx.template',
                'pages/parent-main-page.tsx.template',
                'hooks/parent-actions-hook.ts.template',
                'constants/parent-actions.ts.template',
                'services/parent-instructions.ts.template'
            ]
        
        # For each dynamic template that will be used, find its static dependencies
        dynamic_dir = self.template_engine.dynamic_dir
        for template_rel_path in dynamic_templates:
            template_path = dynamic_dir / template_rel_path
            if template_path.exists():
                # Find static dependencies for this specific template
                template_deps = self._analyze_template_imports(template_path, context)
                required_templates.update(template_deps)
        
        return list(required_templates)
    
    def _analyze_template_imports(self, template_path: Path, context: GenerationContext) -> set:
        """Analyze a specific template file for static dependencies."""
        import re
        
        dependencies = set()
        
        try:
            content = template_path.read_text(encoding='utf-8')
            
            # Find import statements that reference static components
            import_patterns = [
                r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # Standard imports
                r'import\s+[\'"]([^\'"]+)[\'"]',        # Side-effect imports
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for import_path in matches:
                    # Convert import path to potential static template path
                    static_template = self._import_path_to_static_template(import_path, context)
                    if static_template:
                        dependencies.add(static_template)
                        
        except Exception as e:
            print(f"    ⚠️  Could not analyze template {template_path}: {e}")
        
        return dependencies

    def _detect_required_static_templates(self, context: GenerationContext) -> list:
        """Dynamically detect which static templates are referenced by dynamic templates AND core templates."""
        import re
        from pathlib import Path
        
        essential_templates = set()
        dynamic_dir = self.template_engine.dynamic_dir
        static_dir = self.template_engine.static_dir
        
        # Dynamically find all core template files in the static directory root
        core_templates = []
        if static_dir.exists():
            for template_file in static_dir.iterdir():
                if template_file.is_file() and template_file.suffix == '.template':
                    core_templates.append(template_file.name)
        
        # Analyze core templates first
        for core_template in core_templates:
            core_template_path = static_dir / core_template
            if core_template_path.exists():
                try:
                    content = core_template_path.read_text(encoding='utf-8')
                    
                    # Find import statements that reference static components
                    import_patterns = [
                        r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # Standard imports
                        r'import\s+[\'"]([^\'"]+)[\'"]',        # Side-effect imports
                    ]
                    
                    for pattern in import_patterns:
                        matches = re.findall(pattern, content)
                        for import_path in matches:
                            # Convert import path to potential static template path
                            static_template = self._import_path_to_static_template(import_path, context)
                            if static_template and (static_dir / static_template).exists():
                                essential_templates.add(static_template)
                                print(f"    📍 Found static dependency: {static_template} (from {core_template})")
                                
                except Exception as e:
                    print(f"    ⚠️  Could not analyze core template {core_template}: {e}")
        
        # Analyze all dynamic templates to find static template references
        if dynamic_dir.exists():
            for template_file in dynamic_dir.rglob('*.template'):
                try:
                    content = template_file.read_text(encoding='utf-8')
                    
                    # Find import statements that reference static components
                    import_patterns = [
                        r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # Standard imports
                        r'import\s+[\'"]([^\'"]+)[\'"]',        # Side-effect imports
                    ]
                    
                    for pattern in import_patterns:
                        matches = re.findall(pattern, content)
                        for import_path in matches:
                            # Convert import path to potential static template path
                            static_template = self._import_path_to_static_template(import_path, context)
                            if static_template and (static_dir / static_template).exists():
                                essential_templates.add(static_template)
                                print(f"    📍 Found static dependency: {static_template} (from {template_file.name})")
                                
                except Exception as e:
                    print(f"    ⚠️  Could not analyze dynamic template {template_file}: {e}")
        
        return list(essential_templates)
    
    def _import_path_to_static_template(self, import_path: str, context: GenerationContext) -> str:
        """Convert an import path to a static template path."""
        # Handle relative imports from component perspective
        if import_path.startswith('../'):
            # Remove leading '../' and convert to template path
            clean_path = import_path.lstrip('../')
            
            # Skip dynamic dependencies that are created by ensure_all_dependencies
            dynamic_dependencies = {
                'hooks/core/usePageData',  # Created by ensure_use_page_data_hook from dynamic template
                'components/ui/DataTable'   # Created by ensure_data_table_component from dynamic template
            }
            
            if clean_path in dynamic_dependencies:
                return None  # Don't validate as static template
            
            # Dynamically find matching template by checking all possible extensions and paths
            static_dir = self.template_engine.static_dir
            
            # Try direct path with various extensions
            for ext in ['.ts.template', '.tsx.template', '.js.template', '.jsx.template']:
                potential_template = clean_path + ext
                if (static_dir / potential_template).exists():
                    return potential_template
            
            # Try index file for directories (like components/layout -> components/layout/index.ts.template)
            for ext in ['.ts.template', '.tsx.template']:
                index_template = clean_path + '/index' + ext
                if (static_dir / index_template).exists():
                    return index_template
                    
        return None

    def _find_matching_static_template(self, file_path, static_dir):
        """Find static template that matches the needed file path."""
        # Convert file path to relative path from src/
        try:
            relative_to_src = file_path.relative_to(file_path.parts[0] if 'src' in str(file_path) else file_path)
            
            # Look for matching template
            template_path = static_dir / (str(relative_to_src) + '.template')
            
            if template_path.exists():
                return (str(relative_to_src) + '.template', file_path)
                
        except Exception:
            pass
            
        return None

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