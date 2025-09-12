#!/usr/bin/env python3
"""
ID Setter CLI Tool
Automatically adds meaningful IDs to React components and interactive elements
"""

import argparse
import sys
from pathlib import Path

from modules.file_processor import FileProcessor
from modules.id_generator import IDGenerator
from modules.html_parser import HTMLParser


def main():
    parser = argparse.ArgumentParser(description="Add IDs to React components and interactive elements")
    parser.add_argument("--src", type=str, default="../../frontend/src", 
                       help="Source directory to process (default: ../../frontend/src)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be changed without making changes")
    parser.add_argument("--component", type=str, 
                       help="Process only a specific component file")
    parser.add_argument("--page", type=str, 
                       help="Page context for ID generation (e.g., 'game', 'settings', 'menu')")
    parser.add_argument("--skip-existing", action="store_true", 
                       help="Skip elements that already have IDs (default: false - will update existing IDs)")
    
    args = parser.parse_args()
    
    src_path = Path(args.src).resolve()
    if not src_path.exists():
        print(f"Error: Source directory {src_path} does not exist")
        sys.exit(1)
    
    processor = FileProcessor(
        html_parser=HTMLParser(skip_existing=args.skip_existing),
        id_generator=IDGenerator(),
        dry_run=args.dry_run
    )
    
    if args.component:
        # Process single component
        component_path = src_path / args.component
        if not component_path.exists():
            print(f"Error: Component file {component_path} does not exist")
            sys.exit(1)
        
        processor.process_file(component_path, page_context=args.page)
    else:
        # Process all components
        processor.process_directory(src_path, page_context=args.page)
    
    print("ID setting complete!")


if __name__ == "__main__":
    main()