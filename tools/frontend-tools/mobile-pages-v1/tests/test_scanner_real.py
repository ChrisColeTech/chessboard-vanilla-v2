#!/usr/bin/env python3
"""
Test the dependency scanner with real template files
"""

from pathlib import Path
from modules.template_dependency_scanner import TemplateDependencyScanner

def test_with_real_templates():
    """Test scanner with actual template files."""
    
    # Set up paths to real template directories
    base_dir = Path(__file__).parent
    static_dir = base_dir / "templates" / "static"
    dynamic_dir = base_dir / "templates" / "dynamic"
    
    print(f"Static dir: {static_dir}")
    print(f"Dynamic dir: {dynamic_dir}")
    print(f"Static exists: {static_dir.exists()}")
    print(f"Dynamic exists: {dynamic_dir.exists()}")
    
    if not static_dir.exists() or not dynamic_dir.exists():
        print("Template directories not found!")
        return
    
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test parent page scanning
    print("\n=== SCANNING PARENT PAGE DEPENDENCIES ===")
    result = scanner.scan_dependencies("parent")
    
    print(f"\nFound {len(result.required_templates)} required templates:")
    for template in sorted(result.required_templates):
        print(f"  ✓ {template}")
    
    print(f"\nFound {len(result.missing_templates)} missing templates:")
    for template in sorted(result.missing_templates):
        print(f"  ❌ {template}")
    
    print("\n=== DEPENDENCY TREE ===")
    for template, deps in result.dependency_tree.items():
        if deps:  # Only show templates with dependencies
            print(f"\n{template}:")
            for dep in sorted(deps):
                print(f"  └── {dep}")

if __name__ == "__main__":
    test_with_real_templates()