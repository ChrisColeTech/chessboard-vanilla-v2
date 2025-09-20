#!/usr/bin/env python3
"""Debug import extraction for AppLayout template"""

from pathlib import Path
import re

def extract_imports(content):
    """Extract import paths from template content."""
    import_patterns = [
        r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # import ... from "path"
        r'import\s+[\'"]([^\'"]+)[\'"]',        # import "path"
    ]
    
    imports = set()
    for pattern in import_patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        for match in matches:
            # Only process relative imports that start with ./ or ../
            if match.startswith('./') or match.startswith('../'):
                imports.add(match)
    
    return imports

def convert_import_to_template_path(import_path):
    """Convert an import path to a template file path."""
    # Remove leading ./ or ../
    clean_path = import_path
    if clean_path.startswith('./'):
        clean_path = clean_path[2:]
    elif clean_path.startswith('../'):
        clean_path = clean_path[3:]
    
    print(f"  {import_path} -> {clean_path}")
    
    # Skip dynamic dependencies
    dynamic_dependencies = {
        'hooks/core/usePageData',
        'components/ui/DataTable'
    }
    
    if clean_path in dynamic_dependencies:
        return None
    
    # Try direct file match first
    extensions = ['.ts.template', '.tsx.template', '.js.template', '.jsx.template']
    
    static_dir = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/mobile-pages-v2/templates/static")
    
    for ext in extensions:
        potential_template = clean_path + ext
        if (static_dir / potential_template).exists():
            print(f"    Found: {potential_template}")
            return potential_template
    
    # Try directory imports
    directory_path = static_dir / clean_path
    if directory_path.exists() and directory_path.is_dir():
        print(f"    Directory found: {clean_path}")
        templates = []
        for file in directory_path.iterdir():
            if file.is_file() and file.suffix == '.template':
                rel_path = file.relative_to(static_dir)
                templates.append(str(rel_path))
        print(f"    Directory templates: {templates}")
        return templates
    
    print(f"    Not found: {clean_path}")
    return None

if __name__ == "__main__":
    template_path = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/mobile-pages-v2/templates/static/components/layout/AppLayout.tsx.template")
    
    content = template_path.read_text(encoding='utf-8')
    print("=== APPLAYOUT TEMPLATE CONTENT (first 20 lines) ===")
    lines = content.split('\n')[:20]
    for i, line in enumerate(lines, 1):
        print(f"{i:2}: {line}")
    
    print("\n=== EXTRACTED IMPORTS ===")
    imports = extract_imports(content)
    for imp in sorted(imports):
        print(f"Import: {imp}")
    
    print("\n=== IMPORT CONVERSION ===")
    for imp in sorted(imports):
        result = convert_import_to_template_path(imp)
        if result:
            print(f"✓ {imp} -> {result}")
        else:
            print(f"✗ {imp} -> None")