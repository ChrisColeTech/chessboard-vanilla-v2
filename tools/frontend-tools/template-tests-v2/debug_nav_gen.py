#!/usr/bin/env python3
"""Debug NavigationGenerator directly"""

import sys
from pathlib import Path

# Add shared modules to path
sys.path.append('/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/shared')

from navigation_generator import NavigationGenerator

def debug_navigation_generation():
    project_root = Path('/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app')
    templates_dir = Path('/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/mobile-pages-v2/templates/dynamic/nav')
    
    print(f"🔍 Debugging NavigationGenerator")
    print(f"Project root: {project_root}")
    print(f"Templates dir: {templates_dir}")
    print(f"Templates dir exists: {templates_dir.exists()}")
    print()
    
    try:
        nav_gen = NavigationGenerator(project_root, templates_dir)
        
        # Check config
        config_path = project_root / 'pages.config.json'
        print(f"Config path: {config_path}")
        print(f"Config exists: {config_path.exists()}")
        
        # Force reload
        nav_gen.config_manager.reload_config()
        
        # Check pages
        pages = nav_gen.config_manager.get_pages_for_navigation()
        page_ids = [p.id for p in pages]
        print(f"Pages found: {page_ids}")
        print()
        
        # Try to generate
        output_dir = project_root / 'src' / 'components' / 'layout'
        print(f"Output dir: {output_dir}")
        print(f"Output dir exists: {output_dir.exists()}")
        
        generated = nav_gen.generate_all_files(output_dir)
        print(f"Generated files: {generated}")
        
        # Check the result
        types_file = output_dir / 'types.ts'
        if types_file.exists():
            content = types_file.read_text()
            print(f"\\nActual types.ts content:")
            print(repr(content))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_navigation_generation()