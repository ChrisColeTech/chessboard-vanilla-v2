#!/usr/bin/env python3
"""
Debug the remaining import resolution issues
"""

import sys
from pathlib import Path

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def debug_remaining_issues():
    """Debug the specific import resolution issues that are still failing"""
    
    print("=== DEBUGGING REMAINING ISSUES ===")
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test the failing cases
    failing_cases = [
        ('./ActionItem', 'components/action-sheet/ActionSheet.tsx.template'),
        ('./AuthBackgroundEffects', 'components/auth/AuthLayout.tsx.template'),
    ]
    
    for import_path, from_path in failing_cases:
        print(f"\n--- Testing: '{import_path}' from '{from_path}' ---")
        
        # Test the resolution
        resolved = scanner._resolve_relative_import(import_path, from_path)
        print(f"Resolved path: '{resolved}'")
        
        # Check if it's in the template map
        if resolved in scanner.template_map:
            print(f"✅ Found in template map: {scanner.template_map[resolved]}")
        else:
            print(f"❌ Not found in template map")
            
            # Try with extensions
            for ext in ['.ts', '.tsx', '.js', '.jsx']:
                test_key = resolved + ext
                if test_key in scanner.template_map:
                    print(f"✅ Found with extension {ext}: {scanner.template_map[test_key]}")
                    break
            else:
                print(f"❌ Not found with any extension")
                
                # Show nearby matches
                print(f"Similar entries in template map:")
                for key in scanner.template_map.keys():
                    if 'ActionItem' in key or 'AuthBackground' in key:
                        print(f"  - {key}")
        
        # Show what conversion returns
        converted = scanner._convert_import_to_template_paths(import_path, from_path)
        print(f"Conversion result: {converted}")

if __name__ == '__main__':
    debug_remaining_issues()