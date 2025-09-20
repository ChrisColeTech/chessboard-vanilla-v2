#!/usr/bin/env python3
"""
Test to reproduce the dependency scanning issue where core components are missing
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def test_missing_core_components():
    """Test that reproduces the issue of missing core components in dependency scan"""
    
    print("=== REPRODUCING DEPENDENCY SCANNING ISSUE ===")
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test scanning for parent page dependencies
    print("\n1. Scanning parent page dependencies...")
    result = scanner.scan_dependencies('parent')
    
    # Check for specific missing components that we know should be included
    required_core_components = [
        'components/core/SettingsPanel.tsx.template',
        'components/core/InstructionsFAB.tsx.template', 
        'components/core/InstructionsModal.tsx.template',
        'components/action-sheet/ActionItem.tsx.template',
        'components/auth/AuthBackgroundEffects.tsx.template'
    ]
    
    print(f"\n2. Checking for required core components...")
    print(f"   Total templates found: {len(result.required_templates)}")
    
    missing_components = []
    found_components = []
    
    for component in required_core_components:
        if component in result.required_templates:
            found_components.append(component)
            print(f"   ✅ FOUND: {component}")
        else:
            missing_components.append(component)
            print(f"   ❌ MISSING: {component}")
    
    # Check if AppLayout is in the scan and what it depends on
    app_layout = 'components/layout/AppLayout.tsx.template'
    if app_layout in result.dependency_tree:
        print(f"\n3. AppLayout dependencies:")
        deps = result.dependency_tree[app_layout]
        for dep in sorted(deps):
            print(f"   - {dep}")
    else:
        print(f"\n3. ❌ AppLayout not found in dependency tree!")
    
    # Test the conversion logic directly
    print(f"\n4. Testing import conversion logic...")
    test_imports = [
        '../core/SettingsPanel',
        '../core/InstructionsFAB', 
        '../core/InstructionsModal',
        './ActionItem',
        './AuthBackgroundEffects'
    ]
    
    for test_import in test_imports:
        converted = scanner._convert_import_to_template_paths(test_import, 'components/layout/AppLayout.tsx.template')
        print(f"   '{test_import}' -> {converted}")
    
    print(f"\n=== ISSUE REPRODUCTION SUMMARY ===")
    print(f"Found {len(found_components)}/{len(required_core_components)} required core components")
    print(f"Missing components: {missing_components}")
    
    if missing_components:
        print(f"❌ ISSUE REPRODUCED: Core components are missing from dependency scan")
        return False
    else:
        print(f"✅ All core components found - issue may be fixed")
        return True

def test_import_path_resolution():
    """Test the import path resolution logic specifically"""
    
    print(f"\n=== TESTING IMPORT PATH RESOLUTION ===")
    
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test cases for import resolution
    test_cases = [
        # (import_path, from_file, expected_result_should_contain)
        ('../core/SettingsPanel', 'components/layout/AppLayout.tsx.template', 'SettingsPanel'),
        ('../core/InstructionsFAB', 'components/layout/AppLayout.tsx.template', 'InstructionsFAB'),
        ('./ActionItem', 'components/action-sheet/ActionSheet.tsx.template', 'ActionItem'),
        ('./BackgroundEffects', 'components/layout/AppLayout.tsx.template', 'BackgroundEffects'),
    ]
    
    for import_path, from_file, expected in test_cases:
        result = scanner._convert_import_to_template_paths(import_path, from_file)
        print(f"Import: '{import_path}' from '{from_file}'")
        print(f"  Result: {result}")
        
        found_expected = any(expected in str(r) for r in result)
        if found_expected:
            print(f"  ✅ Contains expected '{expected}'")
        else:
            print(f"  ❌ Missing expected '{expected}'")
        print()

if __name__ == '__main__':
    print("Testing dependency scanning for missing core components...")
    
    # Run the reproduction test
    success = test_missing_core_components()
    
    # Run detailed import resolution test
    test_import_path_resolution()
    
    if not success:
        print(f"\n🔧 Issue confirmed - need to fix dependency scanner")
        sys.exit(1)
    else:
        print(f"\n✅ No issues found")
        sys.exit(0)