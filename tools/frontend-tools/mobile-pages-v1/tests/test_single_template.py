#!/usr/bin/env python3
"""Test single template path resolution"""

from modules.template_dependency_scanner import TemplateDependencyScanner
from pathlib import Path

def test_single_template():
    static_dir = Path("templates/static")
    dynamic_dir = Path("templates/dynamic")
    
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test specific path conversion
    print("=== TESTING PATH CONVERSION ===")
    
    # Test from AppLayout.tsx.template
    from_template = "components/layout/AppLayout.tsx.template"
    test_imports = [
        "../core/SettingsPanel",
        "../action-sheet", 
        "./BackgroundEffects",
        "../../stores/appStore"
    ]
    
    for import_path in test_imports:
        result = scanner._convert_import_to_template_paths(import_path, from_template)
        print(f"From {from_template}:")
        print(f"  Import: {import_path}")
        print(f"  Result: {result}")
        print()

if __name__ == "__main__":
    test_single_template()