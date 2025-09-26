#!/usr/bin/env python3
"""
Template-Based Page Generator v2

A comprehensive page generator that creates React pages using templates
with adaptive wrapper selection based on project capabilities.

Usage:
    python main.py <command> [options]

Commands:
    parent <name>              Create parent page
    child <name> --parent <p>  Create child page
    analyze                    Analyze project structure
    validate                   Validate generated files
    migrate                    Migrate from old generators

Examples:
    python main.py parent Settings
    python main.py child UserProfile --parent Settings --mobile
    python main.py analyze
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add current directory to path for module imports
sys.path.insert(0, str(Path(__file__).parent))

from modules.config import PageConfig, GenerationContext, ProjectCapabilities
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter
from modules.project_detector import ProjectCapabilityDetector, ProjectDetectionError
from modules.variable_generator import VariableGenerator
from modules.dependency_manager import DependencyManager
from modules.template_file_referencer import TemplateFileReferencer
from modules.parent_generator import ParentPageGenerator
from modules.child_generator import ChildPageGenerator
from modules.wrapper_selector import WrapperSelector
from modules.routing_updater import ParentRoutingUpdater

# Import shared modules for config management and logging
sys.path.append(str(Path(__file__).parent.parent / "shared"))
from config_integration import ConfigIntegration
from unified_logger import create_logger, LogMode


def get_env_file_path():
    """Get the path to the .env file in the same directory as main.py"""
    return Path(__file__).parent / '.env'


def load_last_frontend_root():
    """Load the last used frontend root from .env file"""
    env_file = get_env_file_path()
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('LAST_FRONTEND_ROOT='):
                        path = line.split('=', 1)[1].strip()
                        # Remove quotes if present
                        if path.startswith('"') and path.endswith('"'):
                            path = path[1:-1]
                        if path.startswith("'") and path.endswith("'"):
                            path = path[1:-1]
                        return path
        except Exception as e:
            print(f"⚠️  Warning: Could not read .env file: {e}")
    return None


def save_last_frontend_root(frontend_root):
    """Save the frontend root to .env file"""
    env_file = get_env_file_path()
    try:
        # Convert to absolute path for storage
        abs_path = str(Path(frontend_root).resolve())
        with open(env_file, 'w') as f:
            f.write(f'LAST_FRONTEND_ROOT="{abs_path}"\n')
    except Exception as e:
        print(f"⚠️  Warning: Could not save frontend root to .env file: {e}")


class TemplateBasedGeneratorCLI:
    """Main CLI interface for the template-based page generator."""
    
    def __init__(self, frontend_root: str, force: bool = False, log_mode: str = "minimal", log_file: Optional[Path] = None):
        self.frontend_root = Path(frontend_root).resolve()
        self.force = force
        self.templates_dir = Path(__file__).parent / "templates"
        
        # Initialize logger
        self.logger = create_logger("page_generator", log_mode, log_file)
        
        # Validate paths
        if not self.frontend_root.exists():
            raise ValueError(f"Frontend root directory not found: {self.frontend_root}")
        
        if not self.templates_dir.exists():
            raise ValueError(f"Templates directory not found: {self.templates_dir}")
        
        # Initialize core components
        self.template_engine = TemplateEngine(self.templates_dir)
        self.file_writer = FileWriter(self.logger)
        self.project_detector = ProjectCapabilityDetector(self.frontend_root)
        self.variable_generator = VariableGenerator()
        self.dependency_manager = DependencyManager(self.template_engine, self.file_writer)
        self.wrapper_selector = WrapperSelector()
        self.routing_updater = ParentRoutingUpdater(
            self.template_engine, 
            self.file_writer, 
            self.variable_generator
        )
        
        # Initialize generators
        self.parent_generator = ParentPageGenerator(
            self.template_engine,
            self.file_writer,
            self.variable_generator,
            self.dependency_manager
        )
        
        self.child_generator = ChildPageGenerator(
            self.template_engine,
            self.file_writer,
            self.variable_generator,
            self.wrapper_selector
        )
        
        # Initialize shared modules for config management
        self.config_integration = ConfigIntegration(self.frontend_root)
    
    def create_parent_page(self, name: str, mobile: bool = True) -> None:
        """Create a parent page with all required files."""
        self.logger.operation(f"Creating parent page: {name}")
        
        try:
            # Detect project capabilities
            capabilities = self.project_detector.detect_capabilities()
            
            # Create page configuration
            config = PageConfig(name=name, mobile=mobile)
            
            # Create generation context
            context = GenerationContext(
                config=config,
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                variables={}
            )
            
            # FIND ALL TEMPLATE DEPENDENCIES
            referencer = TemplateFileReferencer(self.template_engine.static_dir)
            
            # Get core templates that will be generated
            core_templates = ["App.tsx.template", "main.tsx.template"]
            all_dependencies = referencer.get_all_dependencies(core_templates)
            
            self.logger.success("Found all template dependencies!")
            self.logger.verbose(f"Starting from: {core_templates}")
            self.logger.verbose(f"Found {len(all_dependencies)} total dependencies")
            
            # Validate and create missing root files  
            self.dependency_manager.validate_and_create_root_files(context, self.force)
            
            # Copy all styles files
            self.dependency_manager.ensure_styles_directory(context, self.force)
            
            # Ensure dependencies exist
            self.dependency_manager.ensure_all_dependencies_with_integration(context, all_dependencies)
            
            # Generate parent page
            self.parent_generator.create_parent_page(context)
            
            # Integrate parent page (create hooks, update registries, etc.)  
            self.logger.info("Integrating parent page with specialized modules...")
            integration_success = self.dependency_manager.integrate_parent_page(context, config.page_id)
            if not integration_success:
                self.logger.warning("Parent integration had some issues, but continuing...")
            
            # Validate creation
            validation = self.parent_generator.validate_parent_creation(context)
            self._print_validation_results("Parent Page", validation)
            
            # Navigation files are now generated by DependencyManager during ensure_static_components()
            self.logger.success("Parent page creation completed with integrated navigation generation")
            
        except Exception as e:
            self.logger.error(f"Error creating parent page: {e}")
            sys.exit(1)
    
    def create_child_page(self, name: str, parent: str, mobile: bool = True) -> None:
        """Create a child page with adaptive wrapper."""
        self.logger.operation(f"Creating child page: {name} (parent: {parent})")
        
        try:
            # Detect project capabilities
            capabilities = self.project_detector.detect_capabilities()
            
            # Auto-create parent if it doesn't exist
            if not self.project_detector.check_parent_exists(parent):
                print(f"🔄 Parent page '{parent}' not found. Creating it automatically...")
                self.create_parent_page(parent)
            
            # Create page configuration
            config = PageConfig(name=name, parent=parent, mobile=mobile)
            
            # Create generation context
            context = GenerationContext(
                config=config,
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                variables={}
            )
            
            # FIND ALL TEMPLATE DEPENDENCIES
            referencer = TemplateFileReferencer(self.template_engine.static_dir)
            
            # Get core templates that will be generated
            core_templates = ["App.tsx.template", "main.tsx.template"]
            all_dependencies = referencer.get_all_dependencies(core_templates)
            
            self.logger.success("Found all template dependencies!")
            self.logger.verbose(f"Starting from: {core_templates}")
            self.logger.verbose(f"Found {len(all_dependencies)} total dependencies")
            
            # Validate and create missing root files
            self.dependency_manager.validate_and_create_root_files(context, self.force)
            
            # Copy all styles files
            self.dependency_manager.ensure_styles_directory(context, self.force)
            
            # Ensure dependencies exist
            self.dependency_manager.ensure_all_dependencies_with_integration(context, all_dependencies)
            
            # Generate child page
            self.child_generator.create_child_page(context)
            
            # Integrate child page (create hooks, update registries, etc.)
            self.logger.info("Integrating child page with specialized modules...")
            integration_success = self.dependency_manager.integrate_child_pages(context, config.parent_id)
            if not integration_success:
                self.logger.warning("Child integration had some issues, but continuing...")
            
            # Update parent routing using parent generator
            self._update_parent_for_new_child(context, name)
            
            # Regenerate index files
            self.dependency_manager.regenerate_index_files(self.frontend_root)
            
            # Validate creation
            validation = self.child_generator.validate_child_creation(context)
            self._print_validation_results("Child Page", validation)
            
            # Navigation files are now generated by DependencyManager during ensure_static_components()
            self.logger.success("Child page creation completed with integrated navigation generation")
            
        except Exception as e:
            self.logger.error(f"Error creating child page: {e}")
            sys.exit(1)
    
    def _update_parent_for_new_child(self, context: GenerationContext, child_name: str) -> None:
        """Update parent page routing and actions when a new child is added."""
        config = context.config
        
        # Get all existing children for this parent
        capabilities = self.project_detector.detect_capabilities()
        existing_children_list = capabilities.existing_children.get(config.parent_id, [])
        
        # Use a set to automatically handle duplicates
        existing_children_set = set(existing_children_list)
        existing_children_set.add(child_name.lower())  # Ensure lowercase consistency
        
        # Convert back to sorted list for consistent ordering
        existing_children = sorted(list(existing_children_set))
        
        self.logger.debug(f"Final existing_children for {config.parent_id}: {existing_children}")
        
        # Create child configs for routing variables
        child_configs = []
        for child_id in existing_children:
            # Create a temporary config for each child (capitalize the name properly)
            child_name_proper = child_id.capitalize()
            child_config = PageConfig(name=child_name_proper, parent=config.parent)
            child_configs.append(child_config)
        
        # Create parent context for updating
        parent_config = PageConfig(name=config.parent, parent=None)
        parent_context = GenerationContext(
            config=parent_config,
            capabilities=capabilities,
            frontend_root=context.frontend_root,
            variables={}
        )
        
        # Update parent page with routing
        self.parent_generator.update_parent_routing(parent_context, child_configs)
        
        # Update parent actions hook
        self.parent_generator.update_parent_actions_hook(parent_context)
    
    def analyze_project(self) -> None:
        """Analyze project structure and capabilities."""
        self.logger.info("Analyzing project structure...")
        
        try:
            # Get project summary
            summary = self.project_detector.get_project_summary()
            
            print(f"\n📁 Frontend Root: {summary['frontend_root']}")
            print(f"\n🎯 Project Capabilities:")
            for capability, status in summary['capabilities'].items():
                status_icon = "✅" if status else "❌"
                print(f"  {status_icon} {capability}: {status}")
            
            print(f"\n📊 Project Structure:")
            print(f"  📄 Total Parents: {summary['structure']['total_parents']}")
            print(f"  📄 Total Children: {summary['structure']['total_children']}")
            
            if summary['structure']['parents']:
                print(f"\n👥 Parent Pages:")
                for parent in summary['structure']['parents']:
                    children = summary['structure']['children'].get(parent, [])
                    children_count = len(children)
                    print(f"  📁 {parent} ({children_count} children)")
                    for child in children:
                        print(f"    📄 {child}")
            
            # Check for validation issues
            issues = self.project_detector.validate_project_structure()
            if issues:
                print(f"\n⚠️  Project Structure Issues:")
                for issue in issues:
                    print(f"  - {issue}")
            else:
                print(f"\n✅ Project structure looks good!")
            
            # Get wrapper recommendations
            capabilities = self.project_detector.detect_capabilities()
            recommendations = self.wrapper_selector.recommend_wrapper_upgrades(capabilities)
            if recommendations:
                print(f"\n💡 Recommendations:")
                for upgrade, description in recommendations.items():
                    print(f"  🔧 {upgrade}: {description}")
            
        except ProjectDetectionError as e:
            self.logger.error(f"Project detection error: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Error analyzing project: {e}")
            sys.exit(1)
    
    def validate_generated_files(self) -> None:
        """Validate all generated files in the project."""
        print("🔍 Validating generated files...")
        
        try:
            capabilities = self.project_detector.detect_capabilities()
            
            # Validate dependencies
            context = GenerationContext(
                config=PageConfig("dummy"),  # Dummy config for validation
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                variables={}
            )
            
            dependency_validation = self.dependency_manager.validate_dependencies(context)
            self._print_validation_results("Dependencies", dependency_validation)
            
            # Check missing dependencies
            missing = self.dependency_manager.get_missing_dependencies(context)
            if missing:
                print(f"\n⚠️  Missing Dependencies:")
                for dep in missing:
                    print(f"  - {dep}")
            else:
                print(f"\n✅ All dependencies are available!")
            
            # Validate parent-child routing sync
            for parent in capabilities.existing_parents:
                sync_result = self.routing_updater.sync_routing_with_filesystem(context, parent)
                
                if not sync_result['in_sync']:
                    print(f"\n⚠️  Routing sync issues for {parent}:")
                    
                    if sync_result['missing_in_routing']:
                        print(f"  📄 Files missing from routing:")
                        for child in sync_result['missing_in_routing']:
                            print(f"    - {child}")
                    
                    if sync_result['missing_in_filesystem']:
                        print(f"  🔗 Routes missing files:")
                        for child in sync_result['missing_in_filesystem']:
                            print(f"    - {child}")
                else:
                    print(f"\n✅ {parent} routing is in sync!")
            
        except Exception as e:
            print(f"❌ Error validating files: {e}")
            sys.exit(1)
    
    def create_pages(self, parent: str, children: list = None, mobile: bool = True) -> None:
        """Create parent and children in one command."""
        if children is None:
            children = []
            
        print(f"🚀 Creating page structure: {parent} with {len(children)} children")
        
        try:
            # BUGFIX: Pre-register all children in config before creating parent
            # so that parent actions can find them immediately
            if children:
                print(f"📋 Pre-registering {len(children)} children in config...")
                self._preregister_children_in_config(parent, children, mobile)
            
            # Create the parent (now children are already in config)
            self.create_parent_page(parent)
            
            # Create all children (files only, config already done)
            for child_name in children:
                print(f"\n📝 Adding child: {child_name}")
                self.create_child_page(child_name, parent, mobile)
            
            print(f"\n✅ Successfully created {parent} with {len(children)} children!")
            
        except Exception as e:
            print(f"❌ Error creating page structure: {e}")
            sys.exit(1)
    
    def _preregister_children_in_config(self, parent: str, children: list, mobile: bool = True) -> None:
        """Pre-register children in config so parent can find them during generation."""
        try:
            # Import the PageConfigManager from shared 
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent / "shared"))
            from page_config_manager import PageConfigManager, PageInfo
            
            # Initialize page config manager
            config_manager = PageConfigManager(self.frontend_root)
            
            # Register each child in the config
            for child_name in children:
                child_info = PageInfo(
                    id=child_name.lower(),
                    name=child_name,
                    type="child",
                    parent_id=parent.lower(),
                    has_mobile=mobile
                )
                config_manager.add_page(child_info)
                print(f"  ✅ Pre-registered: {child_name}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not pre-register children: {e}")
            print("   Parent actions may not include child navigation")

    def migrate_from_old_generators(self) -> None:
        """Migrate pages from old generator formats."""
        print("🔄 Migration from old generators...")
        print("⚠️  Migration functionality not yet implemented.")
        print("    This would scan for old generator patterns and convert them to new templates.")
        
        # TODO: Implement migration logic
        # - Scan for old generator comments
        # - Identify page patterns
        # - Convert to new template-based structure
        # - Update routing patterns
    
    def regenerate_dependencies(self, target: str = 'all') -> None:
        """Regenerate dynamic dependencies like ActionSheetContainer and PAGE_ACTIONS."""
        print(f"🔄 Regenerating dependencies (target: {target})...")
        
        try:
            # Get current project capabilities
            capabilities = self.project_detector.detect_capabilities()
            
            # Create a dummy context for dependency generation
            dummy_config = PageConfig("dummy")
            context = GenerationContext(
                config=dummy_config,
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                variables={}  # Empty variables for dependency regeneration
            )
            
            # Initialize dependency manager
            dependency_manager = DependencyManager(
                template_engine=self.template_engine,
                file_writer=self.file_writer
            )
            
            success = True
            
            if target in ['all', 'container']:
                print("  📦 Regenerating ActionSheetContainer...")
                try:
                    dependency_manager.ensure_dynamic_action_sheet_container(context)
                    print("  ✅ ActionSheetContainer regenerated successfully")
                except Exception as e:
                    print(f"  ❌ Failed to regenerate ActionSheetContainer: {e}")
                    success = False
            
            if target in ['all', 'actions']:
                print("  📋 Regenerating PAGE_ACTIONS registry...")
                try:
                    dependency_manager.ensure_dynamic_page_actions_registry(context)
                    print("  ✅ PAGE_ACTIONS registry regenerated successfully")
                except Exception as e:
                    print(f"  ❌ Failed to regenerate PAGE_ACTIONS registry: {e}")
                    success = False
            
            if success:
                print(f"\n✅ Dependency regeneration completed successfully!")
                print("📝 The fix for child page action mappings has been applied.")
                print("🎯 Child pages should now have working go-to navigation links.")
            else:
                print(f"\n❌ Some dependencies failed to regenerate.")
                
        except Exception as e:
            self.logger.error(f"Failed to regenerate dependencies: {e}")
            print(f"❌ Error regenerating dependencies: {e}")
            raise
    
    def _print_validation_results(self, category: str, results: dict) -> None:
        """Print validation results in a formatted way."""
        print(f"\n📋 {category} Validation:")
        
        for item, status in results.items():
            if isinstance(status, bool):
                status_icon = "✅" if status else "❌"
                print(f"  {status_icon} {item}")
            else:
                print(f"  ℹ️  {item}: {status}")




def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Template-Based Page Generator v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s parent Settings
  %(prog)s child UserProfile --parent Settings --mobile
  %(prog)s create Dashboard --children Analytics Reports --mobile
  %(prog)s analyze
  %(prog)s validate
        """
    )
    
    # Load last frontend root from .env file
    last_frontend_root = load_last_frontend_root()
    
    parser.add_argument(
        '--frontend-root',
        help='Path to frontend root directory (required on first run, optional afterwards - uses saved location)'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force overwrite existing root configuration files'
    )
    
    # Logging configuration
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (shows all operation details)'
    )
    logging_group.add_argument(
        '--silent', '-s',
        action='store_true',
        help='Enable silent mode (only warnings and errors)'
    )
    parser.add_argument(
        '--log-file',
        type=Path,
        help='Log to file (includes timestamps and all log levels)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Parent command
    parent_parser = subparsers.add_parser('parent', help='Create parent page')
    parent_parser.add_argument('name', help='Parent page name')
    parent_parser.add_argument('--mobile', action='store_true', help='Create mobile variant of parent page (default)')
    
    # Child command
    child_parser = subparsers.add_parser('child', help='Create child page')
    child_parser.add_argument('name', help='Child page name')
    child_parser.add_argument('--parent', required=True, help='Parent page name')
    child_parser.add_argument('--mobile', action='store_true', help='Create mobile variant (default)')
    
    # Create command (one-shot parent + children)
    create_parser = subparsers.add_parser('create', help='Create parent and children in one command')
    create_parser.add_argument('parent', help='Parent page name')
    create_parser.add_argument('--children', nargs='+', help='Child page names', default=[])
    create_parser.add_argument('--mobile', action='store_true', help='Create mobile variants for all children (default)')
    
    # Analyze command
    subparsers.add_parser('analyze', help='Analyze project structure')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate generated files')
    
    # Migrate command
    subparsers.add_parser('migrate', help='Migrate from old generators')
    
    # Regenerate command
    regenerate_parser = subparsers.add_parser('regenerate', help='Regenerate dynamic dependencies (ActionSheetContainer, PAGE_ACTIONS)')
    regenerate_parser.add_argument('--target', choices=['all', 'container', 'actions'], default='all', 
                                 help='What to regenerate (default: all)')
    
    # Custom parsing to handle flexible argument order
    import sys
    raw_args = sys.argv[1:]
    
    # Global flag patterns that need to be moved before command
    global_flags = ['--frontend-root', '--force', '-f', '--verbose', '-v', '--silent', '-s', '--log-file']
    
    # Find the command (non-flag argument)
    command_candidates = ['parent', 'child', 'create', 'analyze', 'validate', 'migrate', 'regenerate']
    found_command = None
    command_index = -1
    
    for i, arg in enumerate(raw_args):
        if arg in command_candidates:
            found_command = arg
            command_index = i
            break
    
    if found_command:
        # Separate global flags and command-specific args
        global_args = []
        command_args = [found_command]
        
        # Process args before command
        i = 0
        while i < command_index:
            arg = raw_args[i]
            if arg in global_flags:
                global_args.append(arg)
                # Check if this flag takes a value
                if arg in ['--frontend-root', '--log-file'] and i + 1 < command_index:
                    i += 1
                    global_args.append(raw_args[i])
            else:
                command_args.append(arg)
            i += 1
        
        # Process args after command
        i = command_index + 1
        while i < len(raw_args):
            arg = raw_args[i]
            if arg in global_flags:
                global_args.append(arg)
                # Check if this flag takes a value
                if arg in ['--frontend-root', '--log-file'] and i + 1 < len(raw_args):
                    i += 1
                    global_args.append(raw_args[i])
            else:
                command_args.append(arg)
            i += 1
        
        # Reconstruct with proper order: global flags + command + command args
        reordered_args = global_args + command_args
        args = parser.parse_args(reordered_args)
    else:
        # No command found, parse normally
        args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Determine frontend root with environment file logic
    if args.frontend_root:
        # Use the provided frontend root
        frontend_root = args.frontend_root
        print(f"📁 Using specified frontend root: {frontend_root}")
    elif last_frontend_root:
        # Use saved location and show info
        frontend_root = last_frontend_root
        print(f"📁 Using saved frontend location: {frontend_root}")
        print("   (Use --frontend-root to specify a different location)")
    else:
        # No saved location and no flag provided - require explicit flag
        print("❌ No frontend root specified and no saved location found.")
        print("   Please provide --frontend-root to specify the frontend directory")
        sys.exit(1)
    
    try:
        # Determine log mode from CLI args
        if args.verbose:
            log_mode = "verbose"
        elif args.silent:
            log_mode = "silent"
        else:
            log_mode = "minimal"
        
        # Initialize CLI with logging configuration
        cli = TemplateBasedGeneratorCLI(frontend_root, args.force, log_mode, args.log_file)
        
        # Save the frontend root for next time
        save_last_frontend_root(frontend_root)
        if args.frontend_root:
            # Show save confirmation when explicitly provided
            env_file_path = get_env_file_path()
            print(f"💾 Frontend location saved to: {env_file_path}")
            print("   (Will be used automatically in future runs)")
        
        # Execute command
        if args.command == 'parent':
            cli.create_parent_page(args.name)  # Use method default (True)
        elif args.command == 'child':
            cli.create_child_page(args.name, args.parent)  # Use method default (True)
        elif args.command == 'create':
            cli.create_pages(args.parent, args.children)  # Use method default (True)
        elif args.command == 'analyze':
            cli.analyze_project()
        elif args.command == 'validate':
            cli.validate_generated_files()
        elif args.command == 'migrate':
            cli.migrate_from_old_generators()
        elif args.command == 'regenerate':
            cli.regenerate_dependencies(args.target)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()