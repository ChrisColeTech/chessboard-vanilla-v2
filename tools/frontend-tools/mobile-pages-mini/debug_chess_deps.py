#!/usr/bin/env python3
"""
Debug script to trace which templates are importing chess-specific dependencies.
"""

import re
from pathlib import Path
from collections import defaultdict

def read_template_content(template_path, static_dir, dynamic_dir):
    """Read content from a template file."""
    # Try static directory first
    static_path = static_dir / template_path
    if static_path.exists():
        try:
            return static_path.read_text(encoding='utf-8')
        except Exception:
            return None
    
    # Try dynamic directory
    dynamic_path = dynamic_dir / template_path
    if dynamic_path.exists():
        try:
            return dynamic_path.read_text(encoding='utf-8')
        except Exception:
            return None
    
    return None

def extract_imports_from_content(content):
    """Extract import paths from template content."""
    import_patterns = [
        r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # import ... from "path"
        r'import\s+[\'"]([^\'"]+)[\'"]',        # import "path"
        r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',  # require("path")
    ]
    
    imports = set()
    for pattern in import_patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        imports.update(matches)
    
    return imports

def is_chess_specific(import_path):
    """Check if an import path is chess-specific."""
    chess_patterns = [
        r'.*chess.*', r'.*piece.*', r'.*board.*', r'.*stockfish.*',
        r'.*computer.*difficulty.*', r'.*game.*result.*'
    ]
    
    for pattern in chess_patterns:
        if re.match(pattern, import_path, re.IGNORECASE):
            return True
    return False

def main():
    static_dir = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/mobile-pages-mini/templates/static")
    dynamic_dir = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/mobile-pages-mini/templates/dynamic")
    
    # Get all template files
    all_templates = []
    if static_dir.exists():
        all_templates.extend(static_dir.rglob('*.template'))
    if dynamic_dir.exists():
        all_templates.extend(dynamic_dir.rglob('*.template'))
    
    chess_imports_by_source = defaultdict(list)
    
    print("🔍 Scanning all templates for chess-specific imports...")
    print("=" * 80)
    
    for template_file in all_templates:
        # Determine relative path
        if static_dir in template_file.parents:
            rel_path = template_file.relative_to(static_dir)
        else:
            rel_path = template_file.relative_to(dynamic_dir)
        
        content = read_template_content(str(rel_path), static_dir, dynamic_dir)
        if content:
            imports = extract_imports_from_content(content)
            
            for import_path in imports:
                if is_chess_specific(import_path):
                    chess_imports_by_source[str(rel_path)].append(import_path)
    
    # Report results
    if chess_imports_by_source:
        print(f"🚨 Found chess-specific imports in {len(chess_imports_by_source)} templates:")
        print()
        
        for template_path, chess_imports in sorted(chess_imports_by_source.items()):
            print(f"📄 {template_path}")
            for imp in sorted(chess_imports):
                print(f"    ❌ {imp}")
            print()
    else:
        print("✅ No chess-specific imports found!")
    
    print(f"📊 Summary:")
    print(f"  - Templates scanned: {len(all_templates)}")
    print(f"  - Templates with chess imports: {len(chess_imports_by_source)}")
    total_chess_imports = sum(len(imports) for imports in chess_imports_by_source.values())
    print(f"  - Total chess-specific imports: {total_chess_imports}")

if __name__ == "__main__":
    main()