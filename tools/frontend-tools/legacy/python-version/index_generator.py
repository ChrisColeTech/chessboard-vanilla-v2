#!/usr/bin/env python3

"""
Index Generator - Python Version
Generates TypeScript index files with modular architecture and separated concerns
"""

import os
import sys
import asyncio
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from export_strategy import ExportStrategy
from conflict_resolver import ConflictResolver
from file_analyzer import FileAnalyzer
from export_generator import ExportGenerator
from validator import Validator


class IndexGenerator:
    """
    Main class for generating TypeScript index files with conflict resolution and validation.
    """
    
    def __init__(self):
        # Initialize all modules
        self.export_strategy = ExportStrategy()
        self.conflict_resolver = ConflictResolver()
        self.file_analyzer = FileAnalyzer()
        self.export_generator = ExportGenerator()
        self.validator = Validator()
        
        # Set up logging
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging to file and console."""
        log_file = 'index_generator.log'
        
        # Create logger
        self.logger = logging.getLogger('IndexGenerator')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler (disabled to only log to file)
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # console_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Add handlers
        self.logger.addHandler(file_handler)
        # self.logger.addHandler(console_handler)
    
    def log_and_print(self, message: str, level: str = 'info'):
        """Log message to file and print to console."""
        getattr(self.logger, level)(message)
    
    def handle_special_cases(self, root_dir: str) -> None:
        """
        Handle special cases for missing directories that should have index files.
        
        Args:
            root_dir: Root directory to process
        """
        special_cases = [
            # Create missing service directories that are commonly imported
            {'path': 'services/chess', 'files': []},
            {'path': 'services/preloading', 'files': []},
            {'path': 'services/clients', 'files': []},
        ]
        
        for special_case in special_cases:
            full_path = os.path.join(root_dir, special_case['path'])
            if os.path.exists(full_path):
                index_path = os.path.join(full_path, 'index.ts')
                if not os.path.exists(index_path):
                    self.logger.info(f"   📁 Creating missing index for: {special_case['path']}")
                    # Create empty index file to prevent "Cannot find module" errors
                    empty_index = (
                        "// Auto-generated index file\n"
                        "// Run `npm run generate:index` to regenerate\n\n"
                        "// Directory exists but no exports found\n"
                        "// This prevents \"Cannot find module\" errors\n"
                    )
                    with open(index_path, 'w', encoding='utf-8') as f:
                        f.write(empty_index)
    
    async def generate_index_files(self, root_dir: str, options: Dict[str, Any] = None) -> None:
        """
        Main entry point - generates index.ts files recursively with validation.
        
        Args:
            root_dir: Root directory to process
            options: Generation options (recursive, dry_run)
        """
        if options is None:
            options = {}
        
        recursive = options.get('recursive', True)
        dry_run = options.get('dry_run', False)
        
        self.logger.info(f"🚀 Starting index.ts generation for: {root_dir}")
        self.logger.info(f"📋 Options: recursive={recursive}, dry_run={dry_run}")
        
        if not os.path.exists(root_dir):
            raise FileNotFoundError(f"Directory does not exist: {root_dir}")
        
        # Handle special cases for missing modules
        self.handle_special_cases(root_dir)
        
        # Pre-validation phase (always run)
        self.logger.info("🔍 Running pre-generation validation...")
        validation_results = await self.validator.validate_directory_structure(root_dir, recursive)
        self.validator.report_validation_results(validation_results)
        
        if validation_results['errors']:
            self.logger.error(f"❌ Validation failed with {len(validation_results['errors'])} error(s). "
                  "Cannot proceed with generation.")
            return
        
        await self.process_directory(root_dir, recursive, dry_run)
        
        # Post-validation phase (always run when files were written)
        if not dry_run:
            self.logger.info("🔍 Running post-generation validation...")
            await self.validator.validate_generated_files(root_dir, recursive)
        
        self.logger.info("✅ Index generation complete!")
    
    async def process_directory(self, dir_path: str, recursive: bool, dry_run: bool) -> None:
        """
        Process a single directory.
        
        Args:
            dir_path: Directory path to process
            recursive: Whether to process recursively
            dry_run: Whether to only show what would be generated
        """
        try:
            entries = os.listdir(dir_path)
        except Exception as e:
            self.logger.error(f"❌ Error reading directory {dir_path}: {e}")
            return
        
        files = []
        subdirs = []
        
        # Separate files and subdirectories
        for entry in entries:
            entry_path = os.path.join(dir_path, entry)
            if os.path.isfile(entry_path) and self.file_analyzer.is_valid_file(entry):
                files.append(entry)
            elif (os.path.isdir(entry_path) and 
                  not entry.startswith('.') and 
                  entry != 'node_modules'):
                subdirs.append(entry)
        
        # Always recursively process subdirectories first
        if recursive:
            for subdir in subdirs:
                subdir_path = os.path.join(dir_path, subdir)
                await self.process_directory(subdir_path, recursive, dry_run)
        
        # Generate combined index.ts for current directory (files + subdirectories)
        if files or subdirs:
            await self.generate_combined_index(dir_path, files, subdirs, dry_run)
    
    async def generate_combined_index(self, dir_path: str, files: List[str], 
                                    subdirs: List[str], dry_run: bool) -> None:
        """
        Generate combined index for directories with both files and subdirectories.
        
        Args:
            dir_path: Directory path
            files: List of files in the directory
            subdirs: List of subdirectories
            dry_run: Whether to only show what would be generated
        """
        exports = []
        reexports = []
        file_exports = {}
        export_name_tracker = {}
        
        self.logger.info(f"\n📁 Processing combined directory: {dir_path}")
        
        # Process files first (if any)
        if files:
            self.logger.info(f"   📄 Processing {len(files)} file(s)")
            
            # First pass: collect all exports to detect conflicts
            for file in files:
                file_path = os.path.join(dir_path, file)
                export_info = await self.file_analyzer.analyze_file_exports(file_path)
                
                if not export_info:
                    self.logger.warning(f"   ⚠️  No exports found in {file}")
                    continue
                
                file_without_ext = self.file_analyzer.remove_extension(file)
                file_exports[file_without_ext] = export_info
                
                # Track export names for conflict detection
                for exp in export_info:
                    if exp.name not in export_name_tracker:
                        export_name_tracker[exp.name] = []
                    export_name_tracker[exp.name].append(file_without_ext)
                
                self.logger.info(f"   ✨ {file}: {len(export_info)} export(s) found")
            
            # Second pass: generate exports with conflict resolution
            for file_without_ext, export_info in file_exports.items():
                statements = self.export_generator.generate_export_statements(
                    export_info, file_without_ext, export_name_tracker
                )
                
                exports.extend(statements['exports'])
                reexports.extend(statements['reexports'])
        
        # Process subdirectories (if any)
        if subdirs:
            self.logger.info(f"   📁 Processing {len(subdirs)} subdirectory(ies)")
            
            # Determine export strategy using the strategy module
            file_export_list = []
            for file_without_ext, export_info in file_exports.items():
                file_export_list.extend(export_info)
            
            strategy = self.export_strategy.determine_strategy(dir_path, subdirs, file_export_list)
            
            # Validate the strategy
            validation = self.export_strategy.validate_strategy(dir_path, strategy)
            if not validation['is_valid']:
                self.logger.error(f"   ❌ Strategy validation failed: {', '.join(validation['errors'])}")
                raise ValueError(f"Invalid export strategy: {', '.join(validation['errors'])}")
            
            if validation['warnings']:
                self.logger.warning(f"   ⚠️  Warnings: {', '.join(validation['warnings'])}")
            
            self.logger.info(f"   📋 {self.export_strategy.explain_strategy(strategy)}")
            
            if strategy['use_namespaced']:
                # Use namespaced exports to avoid conflicts
                for subdir in subdirs:
                    subdir_path = os.path.join(dir_path, subdir)
                    index_path = os.path.join(subdir_path, 'index.ts')
                    
                    if os.path.exists(index_path):
                        # Use explicit namespace import to avoid conflicts
                        # Convert hyphenated names to valid JavaScript identifiers
                        import re
                        valid_identifier = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), subdir)
                        exports.append(f"export * as {valid_identifier} from './{subdir}';")
                        self.logger.info(f"   ✨ {subdir}: namespaced export added")
                    else:
                        self.logger.warning(f"   ⚠️  {subdir}: no index.ts found, skipping export")
            else:
                # Use regular barrel exports with conflict detection
                conflict_result = await self.conflict_resolver.analyze_and_resolve_conflicts(
                    dir_path, subdirs, file_export_list
                )
                
                if conflict_result['has_conflicts']:
                    self.logger.info(f"   🔍 Detected {len(conflict_result['conflicts'])} export conflicts")
                    self.logger.info(f"   🛠️  {conflict_result['resolution']['explanation']}")
                    
                    # Validate the resolution
                    validation = self.conflict_resolver.validate_resolution(conflict_result['resolution'])
                    if not validation['is_valid']:
                        self.logger.error(f"   ❌ Resolution validation failed: {', '.join(validation['errors'])}")
                        raise ValueError(f"Conflict resolution failed: {', '.join(validation['errors'])}")
                    
                    if validation['warnings']:
                        self.logger.warning(f"   ⚠️  Resolution warnings: {', '.join(validation['warnings'])}")
                    
                    # Use resolved exports
                    exports.extend(conflict_result['resolution']['exports'])
                    self.logger.info(f"   ✅ Applied conflict resolution - "
                          f"{conflict_result['resolution']['conflicts_resolved']} conflicts resolved")
                else:
                    # No conflicts, use standard barrel exports
                    for subdir in subdirs:
                        subdir_path = os.path.join(dir_path, subdir)
                        index_path = os.path.join(subdir_path, 'index.ts')
                        
                        if os.path.exists(index_path):
                            exports.append(f"export * from './{subdir}';")
                            self.logger.info(f"   ✨ {subdir}: barrel export added")
                        else:
                            self.logger.warning(f"   ⚠️  {subdir}: no index.ts found, skipping barrel export")
        
        if not exports and not reexports:
            self.logger.warning("   ⚠️  No valid exports found, skipping index.ts generation")
            return
        
        index_path = os.path.join(dir_path, 'index.ts')
        index_content = self.export_generator.generate_index_content(exports, reexports)
        
        if dry_run:
            self.logger.info(f"   📄 Would generate {index_path}:")
            self.logger.info(index_content)
            return
        
        self.logger.info(f"   📝 Writing {index_path}")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        self.logger.info(f"   ✅ Generated index.ts with {len(exports) + len(reexports)} export(s)")


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("""
Usage: python index_generator.py <directory> [options]

Options:
  --no-recursive    Don't process subdirectories
  --dry-run        Show what would be generated without writing files

Examples:
  python index_generator.py ./src/components
  python index_generator.py ./src --dry-run
  python index_generator.py ./src/hooks --no-recursive
""")
        sys.exit(1)
    
    directory = sys.argv[1]
    options = {
        'recursive': '--no-recursive' not in sys.argv,
        'dry_run': '--dry-run' in sys.argv
    }
    
    generator = IndexGenerator()
    
    try:
        asyncio.run(generator.generate_index_files(directory, options))
    except Exception as error:
        print(f'❌ Error: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()