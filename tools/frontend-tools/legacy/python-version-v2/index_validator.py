"""
Index File Validator - Specialized validator for source index files
Handles validation of index files that contain actual type definitions
"""

import os
import re
from typing import List, Dict, Set, Optional
from pathlib import Path
from workflow_context import WorkflowContext, ExportInfo, FileContext


class IndexFileValidator:
    """
    Specialized validator for index files that contain source definitions.
    This runs as a separate step to analyze source index files without 
    interfering with the main file analysis workflow.
    """
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns for export detection in index files"""
        self.export_patterns = {
            # Interface definitions
            'interface': re.compile(
                r'^export\s+interface\s+([A-Za-z_$][A-Za-z0-9_$]*)',
                re.MULTILINE
            ),
            
            # Type aliases
            'type_alias': re.compile(
                r'^export\s+type\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=',
                re.MULTILINE
            ),
            
            # Enum definitions
            'enum': re.compile(
                r'^export\s+enum\s+([A-Za-z_$][A-Za-z0-9_$]*)',
                re.MULTILINE
            ),
            
            # Class definitions
            'class': re.compile(
                r'^export\s+class\s+([A-Za-z_$][A-Za-z0-9_$]*)',
                re.MULTILINE
            ),
            
            # Const/function definitions
            'const_function': re.compile(
                r'^export\s+(?:const|function)\s+([A-Za-z_$][A-Za-z0-9_$]*)',
                re.MULTILINE
            )
        }
    
    def is_source_index_file(self, file_path: str, content: str) -> bool:
        """
        Determine if an index file contains actual source definitions.
        
        Args:
            file_path: Path to the index file
            content: Content of the file
            
        Returns:
            True if the file contains actual type/interface definitions
        """
        # Must be an index file
        if not (file_path.endswith('/index.ts') or file_path.endswith('\\index.ts')):
            return False
        
        # Check for auto-generated header (indicates generated file)
        if "// Auto-generated index file" in content:
            return False
        
        # Look for actual definitions (not just re-exports)
        for pattern_name, pattern in self.export_patterns.items():
            if pattern.search(content):
                return True
        
        return False
    
    def identify_source_index_directories(self, context: WorkflowContext, root_dir: str) -> List[str]:
        """
        Identify directories that contain source index files and mark them in workflow context.
        This runs BEFORE file analysis to prevent overwriting source index files.
        
        Args:
            context: Workflow context to update
            root_dir: Root directory to search
            
        Returns:
            List of directory paths that contain source index files
        """
        source_index_files = self._find_source_index_files(root_dir)
        source_dirs = []
        
        for file_path in source_index_files:
            # Get directory path for this source index file
            dir_path = os.path.dirname(file_path)
            source_dirs.append(dir_path)
            
            # Mark directory as having a source index file in workflow context
            dir_context = context.get_directory_context(dir_path)
            dir_context.has_source_index = True
            dir_context.needs_index = False  # Don't generate a new index for this directory
            
            print(f"INFO: Marked directory as having source index: {dir_path}")
        
        return source_dirs
    
    def analyze_source_index_files(self, context: WorkflowContext, root_dir: str) -> None:
        """
        Find and analyze all source index files in the directory tree.
        
        Args:
            context: Workflow context to update
            root_dir: Root directory to search
        """
        source_index_files = self._find_source_index_files(root_dir)
        
        for file_path in source_index_files:
            self._analyze_source_index_file(context, file_path)
    
    def _find_source_index_files(self, root_dir: str) -> List[str]:
        """Find all source index files (not generated ones) in directory tree"""
        source_index_files = []
        
        for root, dirs, files in os.walk(root_dir):
            # Skip node_modules and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                if file == 'index.ts':
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if self.is_source_index_file(file_path, content):
                            source_index_files.append(file_path)
                            
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")
        
        return source_index_files
    
    def _analyze_source_index_file(self, context: WorkflowContext, file_path: str) -> None:
        """Analyze a single source index file and update context"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            context.add_error(f"Cannot read source index file: {e}", file_path)
            return
        
        # Get directory path for this index file
        dir_path = os.path.dirname(file_path)
        dir_context = context.get_directory_context(dir_path)
        
        # Create file context
        path = Path(file_path)
        file_context = FileContext(
            file_path=file_path,
            file_name=path.name,
            file_name_without_ext=path.stem
        )
        
        # Extract exports from source index file
        exports = self._extract_exports_from_source_index(content, file_path)
        
        if exports:
            # Add exports to file context and workflow context
            for export_info in exports:
                file_context.exports.append(export_info)
                context.register_export(export_info)
            
            # Add file context to directory context if not already present
            if not any(fc.file_path == file_path for fc in dir_context.files):
                dir_context.files.append(file_context)
                
            print(f"INFO: Analyzed source index file: {file_path} ({len(exports)} exports)")
        else:
            context.add_warning("No exports found in source index file", file_path)
    
    def _extract_exports_from_source_index(self, content: str, file_path: str) -> List[ExportInfo]:
        """Extract exports from source index file content"""
        exports = []
        lines = content.split('\n')
        
        # Remove comments and strings to avoid false matches
        cleaned_content = self._clean_content(content)
        
        # Find all pattern matches
        for pattern_name, pattern in self.export_patterns.items():
            for match in pattern.finditer(cleaned_content):
                export_name = match.group(1)
                
                # Get line number for context
                line_start = cleaned_content[:match.start()].count('\n')
                original_line = lines[line_start].strip() if line_start < len(lines) else ""
                
                # Determine if it's a type-only export
                is_type_only = pattern_name in ['interface', 'type_alias', 'enum']
                
                exports.append(ExportInfo(
                    name=export_name,
                    is_default=False,
                    is_named=True,
                    is_type_only=is_type_only,
                    file_path=file_path,
                    original_line=original_line
                ))
        
        return self._deduplicate_exports(exports)
    
    def _clean_content(self, content: str) -> str:
        """Remove comments and string literals to avoid false matches"""
        # Remove single line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        
        # Remove string literals (basic approach)
        content = re.sub(r'[\'"`]([^\'"`\\]|\\.)*[\'"`]', '""', content)
        
        return content
    
    def _deduplicate_exports(self, exports: List[ExportInfo]) -> List[ExportInfo]:
        """Remove duplicate exports"""
        seen = set()
        unique_exports = []
        
        for export in exports:
            key = (export.name, export.is_default, export.is_type_only)
            if key not in seen:
                seen.add(key)
                unique_exports.append(export)
        
        return unique_exports