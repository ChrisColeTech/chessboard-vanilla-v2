#!/usr/bin/env python3
"""
Debug the scanner's logic to see why it's finding false dependencies
"""

import sys
from pathlib import Path
import re

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def debug_scanner_logic():
    """Debug the scanner's logic step by step"""
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Check what the template map contains
    print("=== Template Map (chess-related entries) ===")
    for import_name, template_path in scanner.template_map.items():
        if 'chess' in import_name.lower() or 'component.types' in import_name or 'drag-testing' in import_name:
            print(f"  '{import_name}' -> '{template_path}'")
    
    # Check what imports AppLayout actually has
    print(f"\n=== AppLayout.tsx Actual Imports ===")
    app_layout_path = static_dir / 'components' / 'layout' / 'AppLayout.tsx.template'
    if app_layout_path.exists():
        content = app_layout_path.read_text()
        imports = scanner._extract_imports(content)
        print(f"Raw imports found: {imports}")
        
        for import_path in imports:
            template_deps = scanner._convert_import_to_template_paths(import_path, 'components/layout/AppLayout.tsx.template')
            if template_deps:
                print(f"  '{import_path}' -> {template_deps}")
    
    # Check what imports TabBar actually has  
    print(f"\n=== TabBar.tsx Actual Imports ===")
    tab_bar_path = static_dir / 'components' / 'layout' / 'TabBar.tsx.template'
    if tab_bar_path.exists():
        content = tab_bar_path.read_text()
        imports = scanner._extract_imports(content)
        print(f"Raw imports found: {imports}")
        
        for import_path in imports:
            template_deps = scanner._convert_import_to_template_paths(import_path, 'components/layout/TabBar.tsx.template')
            if template_deps:
                print(f"  '{import_path}' -> {template_deps}")
    
    # Debug the conversion logic for a specific import
    print(f"\n=== Debug Import Conversion ===")
    test_import = './types'
    print(f"Testing import: '{test_import}'")
    
    clean_path = test_import.lstrip('./')
    print(f"Clean path: '{clean_path}'")
    
    # Check direct lookup
    if clean_path in scanner.template_map:
        print(f"Direct lookup found: {scanner.template_map[clean_path]}")
    
    # Check with extensions
    for ext in ['.ts', '.tsx', '.js', '.jsx']:
        if clean_path + ext in scanner.template_map:
            print(f"Extension lookup ({ext}) found: {scanner.template_map[clean_path + ext]}")
    
    # Check directory lookup
    directory_templates = []
    for import_name, template_path in scanner.template_map.items():
        if import_name.startswith(clean_path + '/'):
            directory_templates.append(template_path)
            print(f"Directory match: '{import_name}' -> '{template_path}'")
    
    print(f"Directory templates for '{clean_path}': {directory_templates}")

if __name__ == '__main__':
    debug_scanner_logic()