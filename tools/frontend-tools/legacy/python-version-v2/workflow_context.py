"""
Workflow Context - Shared state management for the index generation pipeline
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from pathlib import Path


@dataclass
class ExportInfo:
    """Information about an exported symbol"""
    name: str
    is_default: bool
    is_named: bool
    is_type_only: bool
    file_path: str
    original_line: str


@dataclass
class FileContext:
    """Context for a single file being processed"""
    file_path: str
    file_name: str
    file_name_without_ext: str
    exports: List[ExportInfo] = field(default_factory=list)
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)


@dataclass
class DirectoryContext:
    """Context for a directory being processed"""
    dir_path: str
    files: List[FileContext] = field(default_factory=list)
    subdirectories: List[str] = field(default_factory=list)
    has_index: bool = False
    has_source_index: bool = False  # True if directory contains a source index file with actual definitions
    needs_index: bool = True


class WorkflowContext:
    """
    Shared context that flows through the entire workflow pipeline.
    Each stage updates the context and passes it to the next stage.
    """
    
    def __init__(self, root_dir: str, options: Dict[str, Any] = None):
        self.root_dir = Path(root_dir)
        self.options = options or {}
        
        # Global registry of all exports across the project
        self.export_registry: Dict[str, List[ExportInfo]] = {}
        
        # Directory contexts keyed by path
        self.directories: Dict[str, DirectoryContext] = {}
        
        # Validation results
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
        # Generation options
        self.dry_run = self.options.get('dry_run', False)
        self.recursive = self.options.get('recursive', True)
        self.verbatim_module_syntax = self.options.get('verbatim_module_syntax', True)
    
    def register_export(self, export_info: ExportInfo) -> None:
        """Register an export in the global registry"""
        if export_info.name not in self.export_registry:
            self.export_registry[export_info.name] = []
        
        # Avoid duplicate entries from the same file
        existing = [e for e in self.export_registry[export_info.name] 
                   if e.file_path == export_info.file_path]
        
        if not existing:
            self.export_registry[export_info.name].append(export_info)
    
    def get_export_conflicts(self, export_name: str) -> List[ExportInfo]:
        """Get all exports that conflict with the given name"""
        return self.export_registry.get(export_name, [])
    
    def has_conflict(self, export_name: str) -> bool:
        """Check if an export name has conflicts"""
        return len(self.export_registry.get(export_name, [])) > 1
    
    def get_directory_context(self, dir_path: str) -> DirectoryContext:
        """Get or create directory context"""
        if dir_path not in self.directories:
            self.directories[dir_path] = DirectoryContext(dir_path=dir_path)
        return self.directories[dir_path]
    
    def add_error(self, message: str, context: str = "") -> None:
        """Add an error to the global error list"""
        full_message = f"{context}: {message}" if context else message
        self.errors.append(full_message)
    
    def add_warning(self, message: str, context: str = "") -> None:
        """Add a warning to the global warning list"""
        full_message = f"{context}: {message}" if context else message
        self.warnings.append(full_message)
    
    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return len(self.errors) > 0
    
    def get_type_only_directories(self) -> Set[str]:
        """
        Get directories that should use 'export type *' syntax.
        
        IMPORTANT: Interfaces with function signatures (like AuthActions) should NOT use 'export type *'
        because TypeScript's export type syntax excludes function signatures from interfaces.
        
        Only use 'export type *' for directories that contain PURE type definitions:
        - Type aliases (type X = Y)
        - Simple interfaces without methods
        - Enums
        
        Do NOT use 'export type *' for:
        - Interfaces with function signatures (methods)
        - Mixed content directories
        """
        type_only_dirs = set()
        
        for dir_path, dir_context in self.directories.items():
            if dir_context.files:
                # Check if directory contains any interfaces with function signatures
                has_interface_with_methods = False
                for file_ctx in dir_context.files:
                    if file_ctx.exports:
                        # Read file content to check for function signatures in interfaces
                        try:
                            with open(file_ctx.file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            # Check for interface definitions with function signatures
                            # Look for patterns like: methodName: (...) => ...
                            import re
                            interface_with_methods_pattern = re.compile(
                                r'interface\s+\w+\s*\{[^}]*\w+\s*:\s*\([^)]*\)\s*=>\s*[^;]+[;}]',
                                re.DOTALL | re.MULTILINE
                            )
                            
                            if interface_with_methods_pattern.search(content):
                                has_interface_with_methods = True
                                break
                                
                        except Exception:
                            # If we can't read the file, be conservative and don't use export type
                            has_interface_with_methods = True
                            break
                
                # Only use export type * if:
                # 1. All exports are type-only AND
                # 2. No interfaces have function signatures
                if not has_interface_with_methods:
                    all_type_only = all(
                        all(export.is_type_only for export in file_ctx.exports)
                        for file_ctx in dir_context.files
                        if file_ctx.exports
                    )
                    if all_type_only:
                        type_only_dirs.add(dir_path)
        
        return type_only_dirs
    
    def should_use_export_type(self, dir_path: str) -> bool:
        """Determine if directory should use 'export type' syntax"""
        if not self.verbatim_module_syntax:
            return False
        
        return dir_path in self.get_type_only_directories()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the workflow context"""
        total_files = sum(len(dir_ctx.files) for dir_ctx in self.directories.values())
        total_exports = sum(len(exports) for exports in self.export_registry.values())
        conflicts = sum(1 for exports in self.export_registry.values() if len(exports) > 1)
        
        return {
            'directories_processed': len(self.directories),
            'files_processed': total_files,
            'total_exports': total_exports,
            'export_conflicts': conflicts,
            'errors': len(self.errors),
            'warnings': len(self.warnings)
        }