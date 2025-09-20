#!/usr/bin/env python3
"""
Test script to identify missing dependencies in mobile-pages-mini generated projects.
"""

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
import re
import json

def run_command(cmd, cwd=None, capture_output=True):
    """Run a command and return the result."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=capture_output, text=True)
    return result

def create_test_project():
    """Create a temporary test project and generate pages."""
    # Create a temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="mini_test_"))
    print(f"📁 Created test directory: {temp_dir}")
    
    try:
        # Create a basic Vite React TypeScript project
        print("🏗️  Creating Vite React TypeScript project...")
        result = run_command(f"npm create vite@latest {temp_dir / 'test-app'} -- --template react-ts")
        if result.returncode != 0:
            print(f"❌ Failed to create Vite project: {result.stderr}")
            return None
            
        project_dir = temp_dir / "test-app"
        
        # Install dependencies
        print("📦 Installing dependencies...")
        result = run_command("npm install", cwd=project_dir)
        if result.returncode != 0:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return None
            
        # Install additional dependencies that mini-pages needs
        print("📦 Installing additional dependencies...")
        result = run_command("npm install zustand @headlessui/react lucide-react", cwd=project_dir)
        if result.returncode != 0:
            print(f"❌ Failed to install additional dependencies: {result.stderr}")
            return None
        
        # Remove src directory and pages.config to start fresh
        if (project_dir / "src").exists():
            shutil.rmtree(project_dir / "src")
        if (project_dir / "pages.config.json").exists():
            (project_dir / "pages.config.json").unlink()
            
        return project_dir
        
    except Exception as e:
        print(f"❌ Error creating test project: {e}")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        return None

def generate_pages(project_dir):
    """Generate pages using mobile-pages-mini."""
    print("🚀 Generating pages with mobile-pages-mini...")
    
    # Path to mobile-pages-mini
    mini_tool_path = Path(__file__).parent / "main.py"
    
    # Generate Dashboard with Analytics and Reports children
    cmd = f'python "{mini_tool_path}" create Dashboard --children Analytics Reports --mobile'
    result = run_command(cmd, cwd=project_dir)
    
    if result.returncode != 0:
        print(f"❌ Failed to generate pages: {result.stderr}")
        return False
        
    print("✅ Pages generated successfully")
    return True

def extract_typescript_errors(build_output):
    """Extract TypeScript errors from build output."""
    errors = []
    
    # Pattern to match TypeScript errors
    error_pattern = r'src/([^(]+)\((\d+),(\d+)\): error (TS\d+): (.+)'
    
    for line in build_output.split('\n'):
        match = re.match(error_pattern, line)
        if match:
            file_path, line_num, col_num, error_code, message = match.groups()
            errors.append({
                'file': file_path,
                'line': int(line_num),
                'column': int(col_num),
                'error_code': error_code,
                'message': message
            })
    
    return errors

def categorize_missing_imports(errors):
    """Categorize missing import errors by the module being imported."""
    import_errors = []
    module_errors = {}
    
    for error in errors:
        message = error['message']
        
        # Check for "Cannot find module" errors
        if "Cannot find module" in message:
            # Extract the module name
            module_match = re.search(r"Cannot find module '([^']+)'", message)
            if module_match:
                module = module_match.group(1)
                if module not in module_errors:
                    module_errors[module] = []
                module_errors[module].append(error)
                import_errors.append(error)
        
        # Check for "has no exported member" errors  
        elif "has no exported member" in message:
            member_match = re.search(r"Module '\"([^\"]+)\"' has no exported member '([^']+)'", message)
            if member_match:
                module, member = member_match.groups()
                key = f"{module}#{member}"
                if key not in module_errors:
                    module_errors[key] = []
                module_errors[key].append(error)
                import_errors.append(error)
    
    return import_errors, module_errors

def analyze_missing_dependencies(project_dir):
    """Analyze what dependencies are missing by attempting to build."""
    print("🔍 Analyzing missing dependencies...")
    
    # Attempt to build the project
    result = run_command("npm run build", cwd=project_dir)
    
    if result.returncode == 0:
        print("✅ Project builds successfully - no missing dependencies!")
        return []
    
    print("❌ Build failed - analyzing errors...")
    
    # Extract TypeScript errors
    errors = extract_typescript_errors(result.stdout + result.stderr)
    import_errors, module_errors = categorize_missing_imports(errors)
    
    print(f"\n📊 Found {len(errors)} total TypeScript errors")
    print(f"📊 Found {len(import_errors)} import-related errors")
    print(f"📊 Missing {len(module_errors)} unique modules/members")
    
    print(f"\n🔍 Missing modules/members:")
    for module, errs in sorted(module_errors.items()):
        print(f"  ❌ {module} (referenced in {len(errs)} places)")
        for err in errs[:2]:  # Show first 2 examples
            print(f"     - {err['file']}:{err['line']}")
        if len(errs) > 2:
            print(f"     - ... and {len(errs) - 2} more")
    
    return module_errors

def get_essential_templates():
    """Get the list of essential templates from dependency_manager.py."""
    dependency_manager_path = Path(__file__).parent / "modules" / "dependency_manager.py"
    
    with open(dependency_manager_path, 'r') as f:
        content = f.read()
    
    # Extract the essential_templates list
    start_marker = "essential_templates = ["
    end_marker = "]"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return []
    
    # Find the closing bracket for this list
    bracket_count = 0
    current_idx = start_idx + len(start_marker)
    
    while current_idx < len(content):
        char = content[current_idx]
        if char == '[':
            bracket_count += 1
        elif char == ']':
            if bracket_count == 0:
                break
            bracket_count -= 1
        current_idx += 1
    
    if current_idx >= len(content):
        return []
    
    list_content = content[start_idx:current_idx + 1]
    
    # Extract template paths using regex
    template_pattern = r"'([^']+\.template)'"
    templates = re.findall(template_pattern, list_content)
    
    return templates

def suggest_missing_templates(module_errors, essential_templates):
    """Suggest which templates should be added to fix the missing dependencies."""
    print(f"\n💡 ANALYSIS:")
    print(f"Essential templates currently included: {len(essential_templates)}")
    
    # Map missing modules to likely template paths
    missing_templates = []
    
    for module in module_errors.keys():
        # Remove the export member part if present
        if '#' in module:
            module = module.split('#')[0]
            
        # Skip external npm packages
        if not module.startswith('./') and not module.startswith('../'):
            continue
            
        # Convert import path to likely template path
        if module.startswith('./'):
            # Remove the ./ prefix and convert to template path
            template_path = module[2:] + ".tsx.template"
        elif module.startswith('../'):
            # Handle relative imports
            parts = module.split('/')
            template_path = '/'.join(parts[1:]) + ".tsx.template"
        else:
            continue
            
        # Check if this template exists in the static templates
        missing_templates.append(template_path)
    
    print(f"\n🔧 RECOMMENDED FIXES:")
    print(f"Add these templates to the essential_templates list in dependency_manager.py:")
    
    for template in sorted(set(missing_templates)):
        print(f"  + '{template}'")
    
    return missing_templates

def main():
    """Main test function."""
    print("🧪 Testing mobile-pages-mini dependency completeness")
    print("=" * 60)
    
    # Create test project
    project_dir = create_test_project()
    if not project_dir:
        return 1
    
    try:
        # Generate pages
        if not generate_pages(project_dir):
            return 1
        
        # Analyze missing dependencies
        module_errors = analyze_missing_dependencies(project_dir)
        
        if not module_errors:
            print("✅ No missing dependencies found!")
            return 0
        
        # Get current essential templates
        essential_templates = get_essential_templates()
        
        # Suggest fixes
        suggest_missing_templates(module_errors, essential_templates)
        
        print(f"\n📋 SUMMARY:")
        print(f"  - Generated project at: {project_dir}")
        print(f"  - Found {len(module_errors)} missing dependencies")
        print(f"  - Currently includes {len(essential_templates)} essential templates")
        print(f"  - Build FAILED due to missing imports")
        
        return 1
        
    finally:
        # Clean up
        print(f"\n🧹 Cleaning up test directory: {project_dir.parent}")
        shutil.rmtree(project_dir.parent)

if __name__ == "__main__":
    sys.exit(main())