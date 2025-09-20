#!/usr/bin/env python3
"""
Debug the chess.types dependency chain
"""

import sys
from pathlib import Path
import re

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def debug_dependency_chain():
    """Debug the dependency chain to see why chess.types is being pulled in"""
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Check what templates actually exist that import chess.types
    chess_types_files = [
        'types/core/component.types.ts.template',
        'types/ui/drag-testing.types.ts.template'
    ]
    
    print("=== Checking actual imports of chess.types files ===")
    
    for chess_file in chess_types_files:
        print(f"\n--- {chess_file} ---")
        
        # Check if any template actually imports this file
        importers = []
        
        # Scan all templates for imports of this file
        for template_dir in [static_dir, dynamic_dir]:
            if template_dir.exists():
                for template_file in template_dir.rglob('*.template'):
                    try:
                        content = template_file.read_text(encoding='utf-8')
                        
                        # Look for imports of this specific file
                        import_patterns = [
                            rf"from\s+['\"].*{chess_file.replace('.template', '').replace('.ts', '').replace('.tsx', '')}['\"]",
                            rf"import.*from\s+['\"].*{chess_file.replace('.template', '').replace('.ts', '').replace('.tsx', '')}['\"]",
                        ]
                        
                        for pattern in import_patterns:
                            if re.search(pattern, content):
                                if template_dir == static_dir:
                                    rel_path = template_file.relative_to(static_dir)
                                else:
                                    rel_path = template_file.relative_to(dynamic_dir)
                                importers.append(str(rel_path))
                                break
                                
                    except Exception as e:
                        print(f"Warning: Could not read {template_file}: {e}")
        
        if importers:
            print(f"Actually imported by: {importers}")
        else:
            print("NOT actually imported by any template!")
    
    # Let's also check what the dependency scanner thinks
    print(f"\n=== Scanner Dependency Analysis ===")
    result = scanner.scan_dependencies('parent')
    
    print(f"All required templates ({len(result.required_templates)}):")
    for template in sorted(result.required_templates):
        if 'chess' in template.lower() or 'component.types' in template or 'drag-testing' in template:
            print(f"  CHESS-RELATED: {template}")
    
    print(f"\nDependency tree involving chess-related files:")
    for parent, deps in result.dependency_tree.items():
        chess_deps = [d for d in deps if 'chess' in d.lower() or 'component.types' in d or 'drag-testing' in d]
        if chess_deps:
            print(f"  {parent} -> {chess_deps}")

if __name__ == '__main__':
    debug_dependency_chain()