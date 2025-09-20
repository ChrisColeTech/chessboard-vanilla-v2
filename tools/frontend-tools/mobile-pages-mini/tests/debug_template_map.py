#!/usr/bin/env python3

from pathlib import Path

def debug_template_map():
    static_dir = Path("templates/static")
    
    template_map = {}
    if static_dir.exists():
        for template_file in static_dir.rglob('*.template'):
            rel_path = template_file.relative_to(static_dir)
            # Remove .template extension for mapping
            import_name = str(rel_path)[:-9]  # Remove '.template'
            template_map[import_name] = str(rel_path)
    
    print("Template map:")
    for key, value in sorted(template_map.items()):
        print(f"  {key} -> {value}")
    
    print("\nLooking for:")
    searches = ["core/SettingsPanel", "action-sheet", "layout/BackgroundEffects", "stores/appStore"]
    for search in searches:
        if search in template_map:
            print(f"  ✓ Found: {search} -> {template_map[search]}")
        else:
            print(f"  ✗ Missing: {search}")

if __name__ == "__main__":
    debug_template_map()