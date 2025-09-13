#!/usr/bin/env python3

"""
Index Generator V2 - Clean workflow pipeline approach
Main orchestrator that runs the workflow stages in sequence
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from workflow_context import WorkflowContext
from file_analyzer import FileAnalyzer
from export_generator import ExportGenerator
from validator import Validator
from export_tracker import ExportTracker
from index_validator import IndexFileValidator


class IndexGenerator:
    """
    Main index generator using clean workflow pipeline.
    Each stage processes and updates the shared workflow context.
    """
    
    def __init__(self):
        # Initialize export tracker first
        self.export_tracker = ExportTracker()
        
        # Pass export tracker to components that need it
        self.file_analyzer = FileAnalyzer(self.export_tracker)
        self.export_generator = ExportGenerator(self.export_tracker)
        self.validator = Validator()
        self.index_validator = IndexFileValidator()
        
        # Set up logging
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging to file"""
        log_file = 'index_generator_v2.log'
        
        logging.basicConfig(
            level=logging.INFO,  # Back to INFO logging
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='w'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('IndexGeneratorV2')
    
    def generate_index_files(self, root_dir: str, options: Dict[str, Any] = None) -> bool:
        """
        Main entry point - generate index files using workflow pipeline.
        Returns True if generation completed successfully.
        """
        if options is None:
            options = {}
        
        self.logger.info(f"🚀 Starting index generation for: {root_dir}")
        self.logger.info(f"📋 Options: {options}")
        
        # Initialize workflow context
        context = WorkflowContext(root_dir, options)
        
        try:
            # Stage 0.5: Identify source index files first (before analysis)
            self.logger.info("📋 Stage 0.5: Identifying source index files...")
            self._identify_source_index_files_stage(context)
            
            # Stage 1: Analyze files and build export registry
            self.logger.info("📁 Stage 1: Analyzing files...")
            if not self._analyze_files_stage(context):
                return False
            
            # Stage 2: Pre-generation validation
            self.logger.info("🔍 Stage 2: Pre-generation validation...")
            if not self._validation_stage(context, pre_generation=True):
                return False
            
            # Stage 3: Generate index files
            self.logger.info("📝 Stage 3: Generating index files...")
            generated_files = self._generation_stage(context)
            if generated_files is None:
                return False
            
            # Stage 4: Write files (if not dry run)
            if not context.dry_run:
                self.logger.info("💾 Stage 4: Writing files...")
                if not self._write_files_stage(context, generated_files):
                    return False
            
            # Stage 5: Post-generation validation
            self.logger.info("✅ Stage 5: Post-generation validation...")
            if not self._validation_stage(context, pre_generation=False, generated_files=generated_files):
                return False
            
            # Report summary
            self._report_summary(context)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline failed: {e}")
            context.add_error(f"Pipeline execution failed: {e}")
            return False
    
    def _analyze_files_stage(self, context: WorkflowContext) -> bool:
        """Stage 1: Analyze all files and build export registry"""
        
        # Safety limits to prevent infinite loops
        MAX_DIRECTORIES = 1000  # Maximum number of directories to process
        MAX_DEPTH = 20  # Maximum directory depth from root
        
        # Process root directory and all subdirectories
        root_resolved = Path(context.root_dir).resolve()
        directories_to_process = [(root_resolved, 0)]  # (path, depth)
        processed_directories = set()
        queued_directories = {str(root_resolved)}  # Track queued directories
        
        directories_processed = 0
        
        while directories_to_process and directories_processed < MAX_DIRECTORIES:
            current_dir, depth = directories_to_process.pop(0)
            current_dir_str = str(current_dir)
            current_dir_resolved = str(current_dir.resolve())
            
            # Use resolved path for deduplication to handle symlinks and relative paths
            if current_dir_resolved in processed_directories:
                continue
            
            # Check depth limit
            if depth > MAX_DEPTH:
                self.logger.warning(f"   ⚠️  Skipping deep directory (depth {depth}): {current_dir_resolved}")
                continue
            
            processed_directories.add(current_dir_resolved)
            directories_processed += 1
            self.logger.info(f"   📁 Analyzing {current_dir_str} (depth: {depth})")
            
            # Analyze current directory
            self.file_analyzer.analyze_directory(context, current_dir_str)
            
            # Add subdirectories to processing queue if recursive
            if context.recursive:
                dir_context = context.get_directory_context(current_dir_str)
                for subdir in dir_context.subdirectories:
                    subdir_path = current_dir / subdir
                    subdir_resolved = subdir_path.resolve()
                    subdir_resolved_str = str(subdir_resolved)
                    
                    # Additional safety check: prevent adding parent directories
                    if not subdir_resolved_str.startswith(str(root_resolved)):
                        self.logger.warning(f"   ⚠️  Skipping subdirectory outside root: {subdir_resolved}")
                        continue
                    
                    # Prevent adding already processed or queued directories
                    if (subdir_resolved_str not in processed_directories and 
                        subdir_resolved_str not in queued_directories):
                        directories_to_process.append((subdir_path, depth + 1))
                        queued_directories.add(subdir_resolved_str)
        
        # Check for potential infinite loop situation
        if directories_processed >= MAX_DIRECTORIES:
            context.add_error(f"Hit directory processing limit ({MAX_DIRECTORIES}). Possible infinite loop or very large directory structure.")
            return False
        
        # Check if we found anything to process
        if not context.directories:
            context.add_error("No directories found to process")
            return False
        
        self.logger.info(f"   ✅ Analyzed {len(context.directories)} directories")
        return True
    
    def _identify_source_index_files_stage(self, context: WorkflowContext) -> None:
        """Stage 0.5: Identify directories with source index files before analysis"""
        source_dirs = self.index_validator.identify_source_index_directories(context, str(context.root_dir))
        self.logger.info(f"   ✅ Identified {len(source_dirs)} directories with source index files")
    
    def _validation_stage(self, context: WorkflowContext, pre_generation: bool, generated_files: Dict[str, str] = None) -> bool:
        """Stage 2/5: Validation"""
        
        if pre_generation:
            if not self.validator.validate_pre_generation(context):
                self.logger.error("❌ Pre-generation validation failed")
                self.validator.report_validation_results(context)
                return False
        else:
            if generated_files and not self.validator.validate_post_generation(context, generated_files):
                self.logger.error("❌ Post-generation validation failed")
                self.validator.report_validation_results(context)
                return False
        
        self.validator.report_validation_results(context)
        return True
    
    def _generation_stage(self, context: WorkflowContext) -> Optional[Dict[str, str]]:
        """Stage 3: Generate index file content"""
        
        generated_files = {}
        
        for dir_path, dir_context in context.directories.items():
            if not dir_context.needs_index:
                continue
            
            if dir_context.has_source_index:
                self.logger.info(f"   📋 Skipping {dir_path} - has source index file")
                continue
            
            self.logger.info(f"   📝 Generating index for {dir_path}")
            
            # Generate content
            self.logger.debug(f"   🎯 Generating index content for: {dir_path}")
            content = self.export_generator.generate_index_content(context, dir_path)
            
            if not content:
                self.logger.warning(f"   ⚠️  No content generated for {dir_path}")
                continue
            else:
                self.logger.debug(f"   ✅ Generated content for {dir_path} ({len(content)} chars)")
            
            # Validate generated content
            if not self.export_generator.validate_generated_content(context, content, dir_path):
                self.logger.error(f"   ❌ Generated content validation failed for {dir_path}")
                return None
            
            # Store generated content
            index_path = os.path.join(dir_path, 'index.ts')
            generated_files[index_path] = content
            
            if context.dry_run:
                self.logger.info(f"   📄 [DRY RUN] Would generate {index_path}:")
                for i, line in enumerate(content.split('\n')[:10], 1):
                    self.logger.info(f"   {i:2}: {line}")
                if len(content.split('\n')) > 10:
                    self.logger.info(f"   ... ({len(content.split('\n')) - 10} more lines)")
        
        self.logger.info(f"   ✅ Generated {len(generated_files)} index files")
        return generated_files
    
    def _write_files_stage(self, context: WorkflowContext, generated_files: Dict[str, str]) -> bool:
        """Stage 4: Write generated files to disk"""
        
        files_written = 0
        
        for file_path, content in generated_files.items():
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_written += 1
                self.logger.info(f"   💾 Wrote {file_path}")
                
            except Exception as e:
                context.add_error(f"Failed to write {file_path}: {e}")
                return False
        
        self.logger.info(f"   ✅ Wrote {files_written} files")
        return True
    
    def _report_summary(self, context: WorkflowContext) -> None:
        """Report final summary"""
        summary = context.get_summary()
        tracker_stats = self.export_tracker.get_stats()
        
        self.logger.info("\n📊 Generation Summary:")
        self.logger.info(f"   Directories processed: {summary['directories_processed']}")
        self.logger.info(f"   Files analyzed: {summary['files_processed']}")
        self.logger.info(f"   Files processed by tracker: {tracker_stats['total_processed']}")
        self.logger.info(f"   Source index files: {tracker_stats['source_files']}")
        self.logger.info(f"   Generated files skipped: {tracker_stats['generated_files']}")
        self.logger.info(f"   Total exports found: {summary['total_exports']}")
        self.logger.info(f"   Export conflicts: {summary['export_conflicts']}")
        self.logger.info(f"   Warnings: {summary['warnings']}")
        self.logger.info(f"   Errors: {summary['errors']}")
        
        if summary['errors'] == 0:
            self.logger.info("✅ Generation completed successfully!")
        else:
            self.logger.error(f"❌ Generation completed with {summary['errors']} error(s)")


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("""
Usage: python index_generator.py <directory> [options]

Options:
  --no-recursive        Don't process subdirectories
  --dry-run            Show what would be generated without writing files
  --no-verbatim        Don't use 'export type' syntax

Examples:
  python index_generator.py ./src/components
  python index_generator.py ./src --dry-run
  python index_generator.py ./src/types --no-recursive
""")
        sys.exit(1)
    
    directory = sys.argv[1]
    options = {
        'recursive': '--no-recursive' not in sys.argv,
        'dry_run': '--dry-run' in sys.argv,
        'verbatim_module_syntax': '--no-verbatim' not in sys.argv
    }
    
    generator = IndexGenerator()
    
    if generator.generate_index_files(directory, options):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()