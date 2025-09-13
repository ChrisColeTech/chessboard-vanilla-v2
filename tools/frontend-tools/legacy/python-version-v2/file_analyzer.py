"""
File Analyzer - Analyzes TypeScript/JavaScript files and extracts export information
Updates workflow context with discovered exports
"""

import os
import re
from pathlib import Path
from typing import List, Optional
from workflow_context import WorkflowContext, ExportInfo, FileContext
from export_tracker import ExportTracker


class FileAnalyzer:
    """
    Analyzes TypeScript/JavaScript files to extract export information.
    Updates the workflow context with discovered exports.
    """
    
    def __init__(self, export_tracker: ExportTracker = None):
        self.supported_extensions = {'.ts', '.tsx', '.js', '.jsx'}
        self.exclude_patterns = [
            r'\.test\.',
            r'\.spec\.',
            r'\.d\.ts$',
            r'\.stories\.',
            r'\.config\.',
            # NOTE: Removed blanket index exclusion - we need to analyze source index files
            # Generated index files are now handled by export_tracker.should_skip_file()
        ]
        self.export_tracker = export_tracker or ExportTracker()
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns for export detection"""
        self.export_patterns = {
            # Named exports
            'export_declaration': re.compile(
                r'^export\s+(?:(interface|type|class|function|const|let|var|enum)\s+([A-Za-z_$][A-Za-z0-9_$]*)|(?:type\s+)?\{\s*([^}]+)\s*\})',
                re.MULTILINE
            ),
            
            # Default exports - handle multiple patterns
            'export_default_simple': re.compile(
                r'^export\s+default\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*;?\s*$',
                re.MULTILINE
            ),
            'export_default_function': re.compile(
                r'^export\s+default\s+function\s+([A-Za-z_$][A-Za-z0-9_$]*)',
                re.MULTILINE
            ),
            'export_default_class': re.compile(
                r'^export\s+default\s+class\s+([A-Za-z_$][A-Za-z0-9_$]*)',
                re.MULTILINE
            ),
            
            # Re-exports
            'export_from': re.compile(
                r'^export\s+(?:\*|(?:type\s+)?\{\s*([^}]+)\s*\})\s+from\s+[\'"]([^\'"]+)[\'"]',
                re.MULTILINE
            )
        }
    
    def is_valid_file(self, file_path: str) -> bool:
        """Check if file should be processed"""
        path = Path(file_path)
        
        # Check extension
        if path.suffix not in self.supported_extensions:
            return False
        
        # Check exclude patterns
        filename = path.name
        for pattern in self.exclude_patterns:
            if re.search(pattern, filename):
                return False
        
        return True
    
    def analyze_directory(self, context: WorkflowContext, dir_path: str) -> None:
        """
        Analyze all files in a directory and update workflow context.
        This is the main entry point for the file analyzer workflow stage.
        """
        if not os.path.exists(dir_path):
            context.add_error(f"Directory does not exist: {dir_path}")
            return
        
        try:
            entries = os.listdir(dir_path)
        except Exception as e:
            context.add_error(f"Cannot read directory: {e}", dir_path)
            return
        
        # Get directory context
        dir_context = context.get_directory_context(dir_path)
        
        # Process each file
        for entry in entries:
            entry_path = os.path.join(dir_path, entry)
            
            # Handle files
            if os.path.isfile(entry_path):
                if self.is_valid_file(entry):
                    file_context = self.analyze_file(context, entry_path)
                    if file_context:
                        dir_context.files.append(file_context)
            
            # Handle subdirectories
            elif (os.path.isdir(entry_path) and 
                  not entry.startswith('.') and 
                  entry != 'node_modules'):
                dir_context.subdirectories.append(entry)
        
        # Check if directory has existing index
        index_path = os.path.join(dir_path, 'index.ts')
        dir_context.has_index = os.path.exists(index_path)
        
        # Determine if directory needs an index
        dir_context.needs_index = (
            len(dir_context.files) > 0 or 
            len(dir_context.subdirectories) > 0
        )
    
    def analyze_file(self, context: WorkflowContext, file_path: str) -> Optional[FileContext]:
        """Analyze a single file and return file context"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            context.add_error(f"Cannot read file: {e}", file_path)
            return None

        # Check if file should be skipped using export tracker
        if self.export_tracker.should_skip_file(file_path, content):
            context.add_warning(f"Skipping generated/processed file", file_path)
            return None

        path = Path(file_path)
        file_context = FileContext(
            file_path=file_path,
            file_name=path.name,
            file_name_without_ext=path.stem
        )

        # Check if this is a source index file (contains actual definitions)
        is_source_index = self.export_tracker.is_source_index_file(file_path, content)

        # Extract exports
        exports = self.extract_exports(content, file_path)

        if not exports:
            context.add_warning(f"No exports found", file_path)
            # Still register as processed to avoid re-analyzing
            self.export_tracker.register_file_processed(file_path, set(), is_source_index)
            return file_context

        # Register exports in context and file context
        export_names = set()
        for export_info in exports:
            file_context.exports.append(export_info)
            context.register_export(export_info)
            export_names.add(export_info.name)

        # Register file as processed in export tracker
        self.export_tracker.register_file_processed(file_path, export_names, is_source_index)

        return file_context
    
    def extract_exports(self, content: str, file_path: str) -> List[ExportInfo]:
        """Extract all exports from file content"""
        import logging
        logger = logging.getLogger(__name__)
        
        exports = []
        lines = content.split('\n')
        
        # Remove comments and strings to avoid false matches
        cleaned_content = self._clean_content(content)
        
        logger.debug(f"    📄 Analyzing exports in: {file_path}")
        
        # Find named exports
        for match in self.export_patterns['export_declaration'].finditer(cleaned_content):
            exports.extend(self._handle_named_export(match, file_path, lines, cleaned_content))
        
        # Find default exports - try all patterns
        for pattern_name in ['export_default_simple', 'export_default_function', 'export_default_class']:
            for match in self.export_patterns[pattern_name].finditer(cleaned_content):
                exports.extend(self._handle_default_export(match, file_path, lines, cleaned_content))
        
        # Find re-exports (skip for now to avoid complexity)
        # Re-exports would be handled in the directory processing stage
        
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
    
    def _handle_named_export(self, match, file_path: str, lines: List[str], content: str) -> List[ExportInfo]:
        """Handle named export matches"""
        exports = []
        
        # Get line number for context
        line_start = content[:match.start()].count('\n')
        original_line = lines[line_start].strip() if line_start < len(lines) else ""
        
        if match.group(1) and match.group(2):
            # Direct export: export const/function/class/etc Name
            export_type = match.group(1)
            export_name = match.group(2)
            
            export_info = ExportInfo(
                name=export_name,
                is_default=False,
                is_named=True,
                is_type_only=export_type in ['interface', 'type', 'enum'],
                file_path=file_path,
                original_line=original_line
            )
            exports.append(export_info)
            
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"      📤 Found named export: '{export_name}' (type={export_type}, type_only={export_info.is_type_only})")
            
        elif match.group(3):
            # Export list: export { Name1, Name2 }
            export_list = match.group(3)
            is_type_export = 'export type {' in original_line
            
            names = self._parse_export_list(export_list)
            for name in names:
                exports.append(ExportInfo(
                    name=name,
                    is_default=False,
                    is_named=True,
                    is_type_only=is_type_export,
                    file_path=file_path,
                    original_line=original_line
                ))
        
        return exports
    
    def _handle_default_export(self, match, file_path: str, lines: List[str], content: str) -> List[ExportInfo]:
        """Handle default export matches"""
        exports = []
        
        # Get line number for context
        line_start = content[:match.start()].count('\n')
        original_line = lines[line_start].strip() if line_start < len(lines) else ""
        
        export_name = match.group(1)
        is_type_only = 'interface' in original_line or 'type' in original_line
        
        exports.append(ExportInfo(
            name=export_name,
            is_default=True,
            is_named=False,
            is_type_only=is_type_only,
            file_path=file_path,
            original_line=original_line
        ))
        
        return exports
    
    def _parse_export_list(self, export_list: str) -> List[str]:
        """Parse export list into individual names"""
        names = []
        
        for item in export_list.split(','):
            item = item.strip()
            if item:
                # Handle 'as' aliases - take the alias name
                if ' as ' in item:
                    item = item.split(' as ')[1].strip()
                
                # Remove type keyword if present
                if item.startswith('type '):
                    item = item[5:].strip()
                
                if item and item.isidentifier():
                    names.append(item)
        
        return names
    
    def _deduplicate_exports(self, exports: List[ExportInfo]) -> List[ExportInfo]:
        """Remove duplicate exports from the same file"""
        seen = set()
        unique_exports = []
        
        for export in exports:
            # Create unique key based on name, default status, and type
            key = (export.name, export.is_default, export.is_type_only)
            if key not in seen:
                seen.add(key)
                unique_exports.append(export)
            else:
                # Log duplicate detection for debugging
                print(f"DEBUG: Duplicate export detected: {export.name} in {export.file_path}")
        
        return unique_exports