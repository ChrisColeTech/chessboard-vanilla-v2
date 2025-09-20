#!/usr/bin/env python3
"""
Find what templates are using chess.types
"""

import sys
from pathlib import Path
import re

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from template_dependency_scanner import TemplateDependencyScanner

def find_chess_types_usage():
    """Find all templates that depend on chess.types"""
    
    # Set up paths
    base_dir = Path(__file__).parent
    static_dir = base_dir / 'templates' / 'static'
    dynamic_dir = base_dir / 'templates' / 'dynamic'
    
    # Create scanner
    scanner = TemplateDependencyScanner(static_dir, dynamic_dir)
    
    # Find all templates that directly import chess.types
    direct_importers = []
    
    # Scan all static templates
    if static_dir.exists():
        for template_file in static_dir.rglob('*.template'):
            try:
                content = template_file.read_text(encoding='utf-8')
                if 'chess.types' in content:
                    rel_path = template_file.relative_to(static_dir)
                    direct_importers.append(str(rel_path))
            except Exception as e:
                print(f"Warning: Could not read {template_file}: {e}")
    
    # Scan all dynamic templates
    if dynamic_dir.exists():
        for template_file in dynamic_dir.rglob('*.template'):
            try:
                content = template_file.read_text(encoding='utf-8')
                if 'chess.types' in content:
                    rel_path = template_file.relative_to(dynamic_dir)
                    direct_importers.append(str(rel_path))
            except Exception as e:
                print(f"Warning: Could not read {template_file}: {e}")
    
    print("=== Direct importers of chess.types ===")
    for importer in sorted(direct_importers):
        print(f"  {importer}")
    
    # Now scan dependencies to find what depends on these templates
    print("\n=== Dependency Analysis ===")
    
    # Scan for parent and child dependencies
    for page_type in ['parent', 'child']:
        print(f"\n--- {page_type.upper()} page dependencies ---")
        result = scanner.scan_dependencies(page_type)
        
        # Find which templates in the dependency tree use chess.types
        chess_related = set()
        for template in direct_importers:
            if template in result.required_templates:
                chess_related.add(template)
        
        if chess_related:
            print(f"Chess.types templates required for {page_type} pages:")
            for template in sorted(chess_related):
                print(f"  {template}")
                
                # Find what depends on this template
                dependents = []
                for parent, deps in result.dependency_tree.items():
                    if template in deps:
                        dependents.append(parent)
                
                if dependents:
                    print(f"    Used by: {', '.join(sorted(dependents))}")
        else:
            print(f"No chess.types dependencies for {page_type} pages")
    
    print(f"\n=== Summary ===")
    print(f"Direct chess.types importers: {len(direct_importers)}")
    print("Templates:")
    for template in sorted(direct_importers):
        print(f"  - {template}")

if __name__ == '__main__':
    find_chess_types_usage()