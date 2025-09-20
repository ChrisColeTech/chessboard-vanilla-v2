#!/usr/bin/env python3
"""
Comprehensive test to verify the dependency scanner fixes are working
"""

import sys
from pathlib import Path

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def test_dependency_scanner_comprehensive():
    """Comprehensive test of the dependency scanner after fixes"""
    
    print("=== COMPREHENSIVE DEPENDENCY SCANNER TEST ===")
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test scanning for parent page dependencies
    print("\n1. Testing parent page dependency scanning...")
    result = scanner.scan_dependencies('parent')
    
    # Check for all critical components that were previously missing
    critical_components = [
        'components/core/SettingsPanel.tsx.template',
        'components/core/InstructionsFAB.tsx.template', 
        'components/core/InstructionsModal.tsx.template',
        'components/action-sheet/ActionItem.tsx.template',
        'components/auth/AuthBackgroundEffects.tsx.template',
        'components/layout/AppLayout.tsx.template',
        'components/layout/TabBar.tsx.template',
        'components/action-sheet/ActionSheet.tsx.template',
    ]
    
    print(f"   Total templates found: {len(result.required_templates)}")
    
    all_found = True
    for component in critical_components:
        if component in result.required_templates:
            print(f"   ✅ {component}")
        else:
            print(f"   ❌ MISSING: {component}")
            all_found = False
    
    # Test specific import path resolutions
    print(f"\n2. Testing import path resolution...")
    
    test_cases = [
        # (import_path, from_file, expected_in_result)
        ('../core/SettingsPanel', 'components/layout/AppLayout.tsx.template', 'SettingsPanel'),
        ('../core/InstructionsFAB', 'components/layout/AppLayout.tsx.template', 'InstructionsFAB'),
        ('../core/InstructionsModal', 'components/layout/AppLayout.tsx.template', 'InstructionsModal'),
        ('./ActionItem', 'components/action-sheet/ActionSheet.tsx.template', 'ActionItem'),
        ('./AuthBackgroundEffects', 'components/auth/AuthLayout.tsx.template', 'AuthBackgroundEffects'),
        ('./BackgroundEffects', 'components/layout/AppLayout.tsx.template', 'BackgroundEffects'),
        ('./types.ts', 'components/layout/AppLayout.tsx.template', 'types.ts'),
    ]
    
    path_resolution_success = True
    for import_path, from_file, expected in test_cases:
        result_paths = scanner._convert_import_to_template_paths(import_path, from_file)
        
        found_expected = any(expected in str(r) for r in result_paths)
        if found_expected and result_paths:
            print(f"   ✅ '{import_path}' -> {result_paths}")
        else:
            print(f"   ❌ '{import_path}' -> {result_paths} (expected: {expected})")
            path_resolution_success = False
    
    # Test child page dependencies
    print(f"\n3. Testing child page dependency scanning...")
    child_result = scanner.scan_dependencies('child')
    print(f"   Child templates found: {len(child_result.required_templates)}")
    
    # Verify no chess.types pollution
    print(f"\n4. Verifying no chess.types pollution...")
    chess_pollution = [t for t in result.required_templates if 'chess.types' in t or 'component.types' in t or 'drag-testing' in t]
    if chess_pollution:
        print(f"   ❌ Found chess.types pollution: {chess_pollution}")
        all_found = False
    else:
        print(f"   ✅ No chess.types pollution found")
    
    print(f"\n=== TEST SUMMARY ===")
    
    if all_found and path_resolution_success:
        print(f"✅ ALL TESTS PASSED - Dependency scanner is working correctly")
        return True
    else:
        print(f"❌ SOME TESTS FAILED - Issues remain")
        return False

if __name__ == '__main__':
    success = test_dependency_scanner_comprehensive()
    sys.exit(0 if success else 1)