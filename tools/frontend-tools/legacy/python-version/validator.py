"""
Validator Module
Handles validation of directory structure and generated files
"""

import os
import re
from typing import Dict, List, Any, Set
from file_analyzer import FileAnalyzer


class Validator:
    """
    Validates directory structure and generated index files.
    """
    
    def __init__(self):
        self.file_analyzer = FileAnalyzer()
    
    async def validate_directory_structure(self, root_dir: str, recursive: bool) -> Dict[str, List[str]]:
        """
        Validate directory structure before generation.
        
        Args:
            root_dir: Root directory to validate
            recursive: Whether to validate recursively
            
        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        errors = []
        warnings = []
        processed_dirs: Set[str] = set()
        
        await self._validate_directory(root_dir, recursive, errors, warnings, processed_dirs)
        
        return {'errors': errors, 'warnings': warnings}
    
    async def _validate_directory(self, dir_path: str, recursive: bool, 
                                errors: List[str], warnings: List[str], 
                                processed_dirs: Set[str]) -> None:
        """
        Validate a single directory.
        
        Args:
            dir_path: Directory path to validate
            recursive: Whether to validate recursively
            errors: List to collect errors
            warnings: List to collect warnings
            processed_dirs: Set of already processed directories
        """
        if dir_path in processed_dirs:
            warnings.append(f"Circular directory reference detected: {dir_path}")
            return
        
        processed_dirs.add(dir_path)
        
        try:
            entries = os.listdir(dir_path)
            files = []
            subdirs = []
            export_names: Dict[str, List[str]] = {}
            
            # Separate files and subdirectories
            for entry in entries:
                entry_path = os.path.join(dir_path, entry)
                if os.path.isfile(entry_path) and self.file_analyzer.is_valid_file(entry):
                    files.append(entry)
                elif (os.path.isdir(entry_path) and 
                      not entry.startswith('.') and 
                      entry != 'node_modules'):
                    subdirs.append(entry)
            
            # Validate files in current directory
            for file in files:
                file_path = os.path.join(dir_path, file)
                try:
                    export_info = await self.file_analyzer.analyze_file_exports(file_path)
                    
                    if not export_info:
                        warnings.append(f"No exports found in {file_path}")
                    else:
                        # Check for export conflicts
                        for exp in export_info:
                            if exp.name not in export_names:
                                export_names[exp.name] = []
                            export_names[exp.name].append(file)
                            
                except Exception as error:
                    errors.append(f"Failed to analyze exports in {file_path}: {error}")
            
            # Report conflicts as warnings (they'll be auto-resolved)
            for export_name, file_list in export_names.items():
                if len(file_list) > 1:
                    warnings.append(
                        f"Export name conflict '{export_name}' in {dir_path}: "
                        f"{', '.join(file_list)} (will be auto-resolved with aliases)"
                    )
            
            # Recursively validate subdirectories
            if recursive:
                for subdir in subdirs:
                    subdir_path = os.path.join(dir_path, subdir)
                    await self._validate_directory(subdir_path, recursive, errors, warnings, processed_dirs)
                    
        except Exception as error:
            errors.append(f"Failed to read directory {dir_path}: {error}")
    
    def report_validation_results(self, results: Dict[str, List[str]]) -> None:
        """
        Report validation results to console.
        
        Args:
            results: Dictionary with 'errors' and 'warnings' lists
        """
        if results['warnings']:
            print(f"⚠️  {len(results['warnings'])} warning(s):")
            for warning in results['warnings'][:10]:  # Limit to first 10
                print(f"   {warning}")
            if len(results['warnings']) > 10:
                print(f"   ... and {len(results['warnings']) - 10} more warning(s)")
        
        if results['errors']:
            print(f"❌ {len(results['errors'])} error(s):")
            for error in results['errors'][:10]:  # Limit to first 10
                print(f"   {error}")
            if len(results['errors']) > 10:
                print(f"   ... and {len(results['errors']) - 10} more error(s)")
        
        if not results['warnings'] and not results['errors']:
            print("✅ Pre-validation passed - no issues detected")
    
    async def validate_generated_files(self, root_dir: str, recursive: bool) -> None:
        """
        Validate generated index files.
        
        Args:
            root_dir: Root directory containing generated files
            recursive: Whether to validate recursively
        """
        errors = []
        warnings = []
        
        await self._validate_generated_directory(root_dir, recursive, errors, warnings)
        
        if errors:
            print(f"❌ Post-validation found {len(errors)} error(s):")
            for error in errors[:5]:
                print(f"   {error}")
        
        if warnings:
            print(f"⚠️  Post-validation found {len(warnings)} warning(s):")
            for warning in warnings[:5]:
                print(f"   {warning}")
        
        if not errors and not warnings:
            print("✅ Post-validation passed - generated files are valid")
    
    async def _validate_generated_directory(self, dir_path: str, recursive: bool,
                                          errors: List[str], warnings: List[str]) -> None:
        """
        Validate generated files in a directory.
        
        Args:
            dir_path: Directory path to validate
            recursive: Whether to validate recursively
            errors: List to collect errors
            warnings: List to collect warnings
        """
        index_path = os.path.join(dir_path, 'index.ts')
        
        if os.path.exists(index_path):
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic syntax validation
                if 'undefined' in content:
                    errors.append(f"Generated index contains 'undefined': {index_path}")
                
                # Check for duplicate export lines
                lines = [line for line in content.split('\n') if line.strip().startswith('export')]
                export_set: Set[str] = set()
                for line in lines:
                    if line in export_set:
                        errors.append(f"Duplicate export line in {index_path}: {line}")
                    export_set.add(line)
                
                # Check for empty exports
                if any('export {  }' in line for line in lines):
                    warnings.append(f"Empty export statement in {index_path}")
                    
            except Exception as error:
                errors.append(f"Failed to validate {index_path}: {error}")
        
        # Recursively validate subdirectories
        if recursive:
            try:
                for entry in os.listdir(dir_path):
                    entry_path = os.path.join(dir_path, entry)
                    if (os.path.isdir(entry_path) and 
                        not entry.startswith('.') and 
                        entry != 'node_modules'):
                        await self._validate_generated_directory(entry_path, recursive, errors, warnings)
            except Exception as error:
                errors.append(f"Failed to read directory for validation {dir_path}: {error}")