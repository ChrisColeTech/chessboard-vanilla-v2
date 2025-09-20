#!/usr/bin/env python3
"""
Script to find directory imports in template files.
Looks for imports that might be importing entire directories instead of specific files.
"""

import re
from pathlib import Path


def find_directory_imports():
    """Find potential directory imports in template files."""
    static_dir = Path("templates/static")
    
    # Pattern to match imports like:
    # from '../../components'  (no file extension)
    # from '../utils'          (no file extension)
    import_pattern = r"from\s+['\"]([^'\"]+)['\"]"
    
    directory_imports = []
    
    for template_file in static_dir.rglob("*.template"):
        try:
            content = template_file.read_text(encoding='utf-8')
            matches = re.findall(import_pattern, content)
            
            for match in matches:
                # Skip if it has a file extension
                if any(match.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx', '.css', '.json']):
                    continue
                
                # Skip if it's an npm package (doesn't start with . or /)
                if not (match.startswith('./') or match.startswith('../') or match.startswith('/')):
                    continue
                
                # Check if it's likely a directory import
                # (doesn't end with a specific filename)
                path_parts = match.split('/')
                last_part = path_parts[-1] if path_parts else ""
                
                # If last part looks like a directory name (no extension)
                if last_part and '.' not in last_part:
                    rel_template = template_file.relative_to(static_dir)
                    directory_imports.append({
                        'file': str(rel_template),
                        'import': match,
                        'line_content': None
                    })
                    
                    # Find the actual line for context
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if match in line:
                            directory_imports[-1]['line_content'] = line.strip()
                            directory_imports[-1]['line_num'] = line_num
                            break
                            
        except Exception as e:
            print(f"Error reading {template_file}: {e}")
    
    return directory_imports


def main():
    print("🔍 Scanning for directory imports in templates...\n")
    
    directory_imports = find_directory_imports()
    
    if not directory_imports:
        print("✅ No directory imports found!")
        return
    
    print(f"⚠️  Found {len(directory_imports)} potential directory imports:\n")
    
    # Group by import path for easier review
    by_import = {}
    for item in directory_imports:
        import_path = item['import']
        if import_path not in by_import:
            by_import[import_path] = []
        by_import[import_path].append(item)
    
    for import_path, items in sorted(by_import.items()):
        print(f"📁 Import: {import_path}")
        print(f"   Used in {len(items)} file(s):")
        
        for item in items:
            print(f"   • {item['file']}:{item.get('line_num', '?')}")
            if item['line_content']:
                print(f"     {item['line_content']}")
        print()
    
    print("💡 Review these imports to ensure they're specific enough.")
    print("   Consider changing directory imports to specific file imports.")


if __name__ == "__main__":
    main()