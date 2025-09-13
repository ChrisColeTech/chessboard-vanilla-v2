"""
Validator - Validates workflow context and generated content
Simple validation focused on catching obvious errors
"""

import os
from typing import Dict, List
from workflow_context import WorkflowContext


class Validator:
    """
    Simple validator that checks the workflow context for obvious issues.
    Updates context with validation results.
    """
    
    def __init__(self):
        pass
    
    def validate_pre_generation(self, context: WorkflowContext) -> bool:
        """
        Validate context before generating index files.
        Returns True if generation should proceed.
        """
        initial_error_count = len(context.errors)
        
        # Validate directory structure
        self._validate_directory_structure(context)
        
        # Validate export registrations
        self._validate_export_registry(context)
        
        # Return True if no new errors were added
        return len(context.errors) == initial_error_count
    
    def validate_post_generation(self, context: WorkflowContext, generated_files: Dict[str, str]) -> bool:
        """
        Validate generated files.
        Returns True if all generated files are valid.
        """
        initial_error_count = len(context.errors)
        
        for file_path, content in generated_files.items():
            self._validate_generated_file(context, file_path, content)
        
        return len(context.errors) == initial_error_count
    
    def _validate_directory_structure(self, context: WorkflowContext) -> None:
        """Validate that the directory structure makes sense"""
        for dir_path, dir_context in context.directories.items():
            
            # Check if directory exists
            if not os.path.exists(dir_path):
                context.add_error(f"Directory does not exist: {dir_path}")
                continue
            
            # Warn about empty directories that need indexes
            if dir_context.needs_index and not dir_context.files and not dir_context.subdirectories:
                context.add_warning(f"Directory marked as needing index but is empty", dir_path)
            
            # Check for circular references (basic check)
            for subdir in dir_context.subdirectories:
                subdir_path = os.path.join(dir_path, subdir)
                if subdir_path == dir_path:
                    context.add_error(f"Circular directory reference detected", dir_path)
    
    def _validate_export_registry(self, context: WorkflowContext) -> None:
        """Validate the export registry for obvious issues"""
        
        for export_name, exports in context.export_registry.items():
            
            # Check for empty export names
            if not export_name or not export_name.strip():
                context.add_error(f"Empty export name found")
                continue
            
            # Check for invalid JavaScript identifiers
            if not export_name.isidentifier():
                context.add_warning(f"Export name may not be valid JavaScript identifier: {export_name}")
            
            # Report conflicts as informational warnings
            if len(exports) > 1:
                file_paths = [export.file_path for export in exports]
                context.add_warning(f"Export name '{export_name}' appears in {len(exports)} files: {', '.join(file_paths)}")
    
    def _validate_generated_file(self, context: WorkflowContext, file_path: str, content: str) -> None:
        """Validate a single generated file"""
        
        # Check for obvious syntax issues
        if 'undefined' in content:
            context.add_error(f"Generated file contains 'undefined'", file_path)
        
        if content.strip() == "":
            context.add_warning(f"Generated file is empty", file_path)
            return
        
        lines = content.split('\n')
        export_lines = [line.strip() for line in lines if line.strip().startswith('export')]
        
        # Check for duplicate export lines
        seen_lines = set()
        for line in export_lines:
            if line in seen_lines:
                context.add_error(f"Duplicate export statement: {line}", file_path)
            seen_lines.add(line)
        
        # Check for empty export statements
        for line in export_lines:
            if 'export {  }' in line or 'export type {  }' in line:
                context.add_warning(f"Empty export statement: {line}", file_path)
        
        # Check for malformed export statements
        for line in export_lines:
            if not self._is_valid_export_statement(line):
                context.add_error(f"Malformed export statement: {line}", file_path)
    
    def _is_valid_export_statement(self, line: str) -> bool:
        """Basic validation of export statement syntax"""
        line = line.strip()
        
        # Must start with export
        if not line.startswith('export '):
            return False
        
        # Must end with semicolon
        if not line.endswith(';'):
            return False
        
        # Check for basic patterns
        valid_patterns = [
            'export *',
            'export type *',
            'export {',
            'export type {',
            'export default',
            'export const',
            'export function',
            'export class',
            'export interface',
            'export type ',
            'export enum'
        ]
        
        return any(line.startswith(f'export {pattern}') for pattern in ['*', 'type *', '{', 'type {']) or \
               any(f'export {pattern}' in line for pattern in ['default', 'const', 'function', 'class', 'interface', 'enum']) or \
               line.startswith('export type ')
    
    def report_validation_results(self, context: WorkflowContext) -> None:
        """Report validation results to console"""
        
        if context.warnings:
            print(f"⚠️  {len(context.warnings)} warning(s):")
            for warning in context.warnings[:10]:  # Show first 10
                print(f"   {warning}")
            if len(context.warnings) > 10:
                print(f"   ... and {len(context.warnings) - 10} more warning(s)")
        
        if context.errors:
            print(f"❌ {len(context.errors)} error(s):")
            for error in context.errors[:10]:  # Show first 10
                print(f"   {error}")
            if len(context.errors) > 10:
                print(f"   ... and {len(context.errors) - 10} more error(s)")
        
        if not context.warnings and not context.errors:
            print("✅ Validation passed - no issues detected")