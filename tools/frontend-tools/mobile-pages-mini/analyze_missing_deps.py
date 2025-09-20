#!/usr/bin/env python3
"""
Analyze missing dependencies from build output.
"""

import re
import subprocess
from pathlib import Path

def get_build_errors(project_dir):
    """Get build errors from the project."""
    result = subprocess.run(
        ["npm", "run", "build"], 
        cwd=project_dir, 
        capture_output=True, 
        text=True
    )
    return result.stdout + result.stderr

def extract_missing_imports(build_output):
    """Extract missing import information from build output."""
    missing_modules = set()
    missing_exports = set()
    
    lines = build_output.split('\n')
    
    for line in lines:
        # Pattern: Cannot find module 'xyz'
        module_match = re.search(r"Cannot find module '([^']+)'", line)
        if module_match:
            module = module_match.group(1)
            missing_modules.add(module)
        
        # Pattern: Module '"xyz"' has no exported member 'abc'
        export_match = re.search(r"Module '\"([^\"]+)\"' has no exported member '([^']+)'", line)
        if export_match:
            module, member = export_match.groups()
            missing_exports.add(f"{module}#{member}")
    
    return missing_modules, missing_exports

def get_essential_templates():
    """Get the current essential templates list."""
    dep_manager_path = Path(__file__).parent / "modules" / "dependency_manager.py"
    
    with open(dep_manager_path, 'r') as f:
        content = f.read()
    
    # Find the essential_templates list
    start_marker = "essential_templates = ["
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        return []
    
    # Extract lines between the brackets
    lines = content[start_idx:].split('\n')
    templates = []
    
    for line in lines[1:]:  # Skip the opening line
        if line.strip() == ']':
            break
        
        # Extract template path from tuples like ('path/file.template', 'output/path')
        match = re.search(r"'([^']+\.template)'", line)
        if match:
            templates.append(match.group(1))
    
    return templates

def suggest_additional_templates(missing_modules):
    """Suggest additional templates needed."""
    suggestions = []
    
    # Map common missing imports to template files
    template_mapping = {
        './components/layout': 'components/layout/AppLayout.tsx.template',
        './hooks/audio/useGlobalUIAudio': 'hooks/audio/useGlobalUIAudio.ts.template',
        './contexts/InstructionsContext': 'contexts/InstructionsContext.tsx.template',
        './components/splash/SplashModal': 'components/splash/SplashModal.tsx.template',
        './components/auth/AuthRouter': 'components/auth/AuthRouter.tsx.template',
        './components/action-sheet/ActionItem': 'components/action-sheet/ActionItem.tsx.template',
        './services/audio/audioService': 'services/audio/audioService.ts.template',
        './services/core/backgroundEffectsRegistry': 'services/core/backgroundEffectsRegistry.ts.template',
        './components/splash/withSplashScreen': 'components/splash/withSplashScreen.tsx.template',
        './components/layout/types': 'types/core/layout.types.ts.template',
        './components/core/ThemeSwitcher': 'components/core/ThemeSwitcher.tsx.template',
        './types/core/backgroundEffects': 'types/core/backgroundEffects.types.ts.template',
        './constants/pieces.constants': 'constants/pieces.constants.ts.template',
        './data/boardColorConfig': 'data/boardColorConfig.ts.template',
        './services/instructions/InstructionsService': 'services/instructions/InstructionsService.ts.template',
        './utils': 'utils/index.ts.template',
        './services': 'services/index.ts.template',
        './types': 'types/index.ts.template',
    }
    
    for module in missing_modules:
        if module in template_mapping:
            suggestions.append(template_mapping[module])
        elif module.startswith('./'):
            # Try to infer template path
            path = module[2:]  # Remove './'
            if not path.endswith('.ts') and not path.endswith('.tsx'):
                # Try both .ts and .tsx
                suggestions.append(f"{path}.ts.template")
                suggestions.append(f"{path}.tsx.template")
            else:
                suggestions.append(f"{path}.template")
    
    return suggestions

def main():
    """Main analysis function."""
    project_dir = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/mini-test-app")
    
    if not project_dir.exists():
        print(f"❌ Test project not found: {project_dir}")
        return 1
    
    print("🔍 Analyzing missing dependencies in generated project...")
    print("=" * 60)
    
    # Get build errors
    build_output = get_build_errors(project_dir)
    
    # Extract missing imports
    missing_modules, missing_exports = extract_missing_imports(build_output)
    
    print(f"📊 Found {len(missing_modules)} missing modules:")
    for module in sorted(missing_modules):
        print(f"  ❌ {module}")
    
    print(f"\n📊 Found {len(missing_exports)} missing exports:")
    for export in sorted(missing_exports):
        print(f"  ❌ {export}")
    
    # Get current essential templates
    essential_templates = get_essential_templates()
    print(f"\n📦 Current essential templates ({len(essential_templates)}):")
    for template in essential_templates:
        print(f"  ✅ {template}")
    
    # Suggest additional templates
    suggestions = suggest_additional_templates(missing_modules)
    
    print(f"\n💡 Suggested additional templates to add:")
    for suggestion in sorted(set(suggestions)):
        print(f"  + {suggestion}")
    
    print(f"\n📋 SUMMARY:")
    print(f"  - Missing modules: {len(missing_modules)}")
    print(f"  - Missing exports: {len(missing_exports)}")
    print(f"  - Current essential templates: {len(essential_templates)}")
    print(f"  - Suggested additional templates: {len(set(suggestions))}")
    
    return 0

if __name__ == "__main__":
    main()