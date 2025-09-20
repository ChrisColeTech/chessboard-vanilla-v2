#!/usr/bin/env python3
"""
Debug the path resolution logic
"""

import sys
from pathlib import Path

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def debug_path_resolution():
    """Debug the path resolution step by step"""
    
    print("=== DEBUGGING PATH RESOLUTION ===")
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test the path resolution directly
    test_cases = [
        ('../core/SettingsPanel', 'components/layout/AppLayout.tsx.template'),
        ('../core/InstructionsFAB', 'components/layout/AppLayout.tsx.template'),
        ('./ActionItem', 'components/action-sheet/ActionSheet.tsx.template'),
    ]
    
    for import_path, from_path in test_cases:
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
        
        # Show what conversion returns
        converted = scanner._convert_import_to_template_paths(import_path, from_path)
        print(f"Conversion result: {converted}")
    
    # Also show some sample template map entries for reference
    print(f"\n--- Sample template map entries ---")
    count = 0
    for key, value in scanner.template_map.items():
        if 'core' in key or 'action-sheet' in key:
            print(f"'{key}' -> '{value}'")
            count += 1
            if count > 10:
                break

if __name__ == '__main__':
    debug_path_resolution()