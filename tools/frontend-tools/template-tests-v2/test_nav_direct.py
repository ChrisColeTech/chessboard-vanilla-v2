#!/usr/bin/env python3
"""Direct test of navigation generation"""

import sys
from pathlib import Path

# Add shared modules to path
sys.path.append('/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/shared')

from navigation_generator import NavigationGenerator
from page_config_manager import PageConfigManager

def test_navigation_direct():
    project_root = Path('/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app')
    templates_dir = Path('/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/mobile-pages-v2/templates/dynamic/nav')
    output_dir = project_root / 'src' / 'components' / 'layout'
    
    print(f"🧪 Testing NavigationGenerator directly")
    print(f"Project root: {project_root}")
    print(f"Templates dir: {templates_dir}")
    print(f"Output dir: {output_dir}")
    print()
    
    # Check if config exists
    config_path = project_root / 'pages.config.json'
    print(f"Config exists: {config_path.exists()}")
    
    if config_path.exists():
        import json
        with open(config_path) as f:
            config = json.load(f)
        print(f"Config pages: {list(config.get('pages', {}).keys())}")
    print()
    
    # Test navigation generation
    try:
        nav_gen = NavigationGenerator(project_root, templates_dir)
        
        # Check what pages it sees
        pages = nav_gen.config_manager.get_pages_for_navigation()
        page_ids = [p.id for p in pages]
        print(f"Pages found: {page_ids}")
        
        # Generate files
        print(f"Generating files to: {output_dir}")
        generated = nav_gen.generate_all_files(output_dir)
        
        print(f"Generated: {list(generated.keys())}")
        
        # Check the actual file content
        types_file = output_dir / 'types.ts'
        if types_file.exists():
            content = types_file.read_text()
            print(f"\nActual types.ts content:")
            print(content)
        else:
            print("❌ types.ts not found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_navigation_direct()