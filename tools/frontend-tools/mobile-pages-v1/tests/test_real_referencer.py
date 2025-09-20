#!/usr/bin/env python3
"""Test file referencer with real templates"""

from pathlib import Path
from modules.template_file_referencer import TemplateFileReferencer

def test_real_templates():
    templates_dir = Path("templates/static")
    referencer = TemplateFileReferencer(templates_dir)
    
    print(f"Found {len(referencer.available_templates)} templates")
    
    # Test with core templates
    core_templates = ["App.tsx.template", "main.tsx.template"]
    
    all_deps = referencer.get_all_dependencies(core_templates)
    
    print(f"\nStarting with: {core_templates}")
    print(f"Found {len(all_deps)} total dependencies:")
    
    for dep in sorted(all_deps):
        print(f"  ✓ {dep}")
    
    # Check if the missing components are found
    missing_components = [
        "components/core/SettingsPanel.tsx.template",
        "components/action-sheet/ActionSheetContainer.tsx.template",
        "components/core/InstructionsFAB.tsx.template"
    ]
    
    print(f"\nChecking for previously missing components:")
    for component in missing_components:
        if component in all_deps:
            print(f"  ✅ Found: {component}")
        else:
            print(f"  ❌ Missing: {component}")

if __name__ == "__main__":
    test_real_templates()