#!/usr/bin/env python3
"""Test AppLayout template dependencies only"""

from modules.template_dependency_scanner import TemplateDependencyScanner
from pathlib import Path

def test_applayout():
    static_dir = Path("templates/static")
    dynamic_dir = Path("templates/dynamic")
    
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Test just AppLayout template scanning
    print("=== TESTING APPLAYOUT DEPENDENCIES ===")
    
    required_templates = set()
    dependency_tree = {}
    processed = set()
    
    # Scan just AppLayout
    scanner._scan_template_recursive(
        "components/layout/AppLayout.tsx.template",
        required_templates,
        dependency_tree,
        processed
    )
    
    print(f"Found {len(required_templates)} dependencies:")
    for template in sorted(required_templates):
        print(f"  ✓ {template}")
    
    print(f"\nDependency tree for AppLayout:")
    if "components/layout/AppLayout.tsx.template" in dependency_tree:
        for dep in sorted(dependency_tree["components/layout/AppLayout.tsx.template"]):
            print(f"  └── {dep}")

if __name__ == "__main__":
    test_applayout()