"""
AST Parser Module
Provides precise TypeScript/JavaScript export detection using AST parsing
"""

import re
import json
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExportInfo:
    """Precise export information with source location"""
    name: str
    is_default: bool
    is_named: bool
    is_type_only: bool
    export_type: str  # 'interface', 'type', 'class', 'function', 'const', 'enum', etc.
    source_line: int
    original_line: str
    is_re_export: bool = False
    re_export_from: Optional[str] = None


class TypeScriptASTParser:
    """
    Advanced TypeScript/JavaScript parser for precise export detection
    Uses regex patterns optimized for TypeScript syntax
    """
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup comprehensive regex patterns for TypeScript exports"""
        
        # Export declaration patterns
        self.export_patterns = {
            # Default exports
            'default_class': re.compile(r'^export\s+default\s+class\s+(\w+)', re.MULTILINE),
            'default_function': re.compile(r'^export\s+default\s+function\s+(\w+)', re.MULTILINE),
            'default_const': re.compile(r'^export\s+default\s+const\s+(\w+)', re.MULTILINE),
            'default_interface': re.compile(r'^export\s+default\s+interface\s+(\w+)', re.MULTILINE),
            'default_type': re.compile(r'^export\s+default\s+type\s+(\w+)', re.MULTILINE),
            'default_expression': re.compile(r'^export\s+default\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*;?\s*$', re.MULTILINE),
            
            # Named exports - declarations
            'export_interface': re.compile(r'^export\s+interface\s+(\w+)', re.MULTILINE),
            'export_type': re.compile(r'^export\s+type\s+(\w+)', re.MULTILINE),
            'export_class': re.compile(r'^export\s+class\s+(\w+)', re.MULTILINE),
            'export_function': re.compile(r'^export\s+function\s+(\w+)', re.MULTILINE),
            'export_const': re.compile(r'^export\s+const\s+(\w+)', re.MULTILINE),
            'export_let': re.compile(r'^export\s+let\s+(\w+)', re.MULTILINE),
            'export_var': re.compile(r'^export\s+var\s+(\w+)', re.MULTILINE),
            'export_enum': re.compile(r'^export\s+enum\s+(\w+)', re.MULTILINE),
            
            # Export lists - single line
            'export_list': re.compile(r'^export\s*\{\s*([^}]+)\s*\}\s*(?:from\s+[\'"]([^\'"]+)[\'"])?\s*;?\s*$', re.MULTILINE),
            'export_type_list': re.compile(r'^export\s+type\s*\{\s*([^}]+)\s*\}\s*(?:from\s+[\'"]([^\'"]+)[\'"])?\s*;?\s*$', re.MULTILINE),
            
            # Re-exports
            'export_star': re.compile(r'^export\s*\*\s*from\s+[\'"]([^\'"]+)[\'"]', re.MULTILINE),
            'export_star_as': re.compile(r'^export\s*\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', re.MULTILINE),
        }
        
        # Multiline export patterns
        self.multiline_patterns = {
            'multiline_export_list': re.compile(r'export\s*\{\s*([\s\S]*?)\s*\}\s*(?:from\s+[\'"]([^\'"]+)[\'"])?\s*;?\s*$', re.MULTILINE),
            'multiline_type_export_list': re.compile(r'export\s+type\s*\{\s*([\s\S]*?)\s*\}\s*(?:from\s+[\'"]([^\'"]+)[\'"])?\s*;?\s*$', re.MULTILINE),
        }
    
    def parse_file(self, file_path: str) -> List[ExportInfo]:
        """
        Parse a TypeScript/JavaScript file and extract all exports with high precision
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            List of ExportInfo objects with precise export information
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        exports = []
        lines = content.split('\n')
        
        # Remove comments and strings to avoid false matches
        cleaned_content = self._remove_comments_and_strings(content)
        
        # Track processed lines to prevent duplicates
        processed_lines = set()
        
        # Parse single-line exports first
        single_line_exports = self._parse_single_line_exports(cleaned_content, lines)
        exports.extend(single_line_exports)
        
        # Track which lines were processed by single-line patterns
        for export in single_line_exports:
            processed_lines.add(export.source_line)
        
        # Parse multiline exports, excluding already processed lines
        multiline_exports = self._parse_multiline_exports(cleaned_content, lines, processed_lines)
        exports.extend(multiline_exports)
        
        # Validate and deduplicate
        exports = self._validate_and_deduplicate(exports)
        
        return exports
    
    def _remove_comments_and_strings(self, content: str) -> str:
        """Remove comments and string literals to avoid false matches"""
        # Remove single line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        
        # Remove string literals (basic approach)
        content = re.sub(r'[\'"`]([^\'"`\\]|\\.)*[\'"`]', '""', content)
        
        return content
    
    def _parse_single_line_exports(self, content: str, lines: List[str]) -> List[ExportInfo]:
        """Parse single-line export statements"""
        exports = []
        
        for pattern_name, pattern in self.export_patterns.items():
            for match in pattern.finditer(content):
                export_info = self._create_export_info_from_match(
                    pattern_name, match, lines, content
                )
                if export_info:
                    exports.extend(export_info)
        
        return exports
    
    def _parse_multiline_exports(self, content: str, lines: List[str], processed_lines: set = None) -> List[ExportInfo]:
        """Parse multiline export statements, excluding already processed lines"""
        if processed_lines is None:
            processed_lines = set()
            
        exports = []
        
        for pattern_name, pattern in self.multiline_patterns.items():
            for match in pattern.finditer(content):
                # Get line number to check if already processed
                line_start = content[:match.start()].count('\n') + 1
                
                # Skip if this line was already processed by single-line patterns
                if line_start in processed_lines:
                    continue
                    
                export_info = self._create_multiline_export_info(
                    pattern_name, match, lines, content
                )
                if export_info:
                    exports.extend(export_info)
        
        return exports
    
    def _create_export_info_from_match(self, pattern_name: str, match, lines: List[str], content: str) -> List[ExportInfo]:
        """Create ExportInfo objects from regex matches"""
        exports = []
        
        # Get line number
        line_start = content[:match.start()].count('\n')
        original_line = lines[line_start].strip() if line_start < len(lines) else ""
        
        if pattern_name.startswith('default_'):
            # Default exports
            export_name = match.group(1)
            export_type = pattern_name.replace('default_', '')
            
            exports.append(ExportInfo(
                name=export_name,
                is_default=True,
                is_named=False,
                is_type_only=export_type in ['interface', 'type'],
                export_type=export_type,
                source_line=line_start + 1,
                original_line=original_line
            ))
            
        elif pattern_name.startswith('export_'):
            # Named exports
            export_name = match.group(1)
            export_type = pattern_name.replace('export_', '')
            
            exports.append(ExportInfo(
                name=export_name,
                is_default=False,
                is_named=True,
                is_type_only=export_type in ['interface', 'type', 'enum'],
                export_type=export_type,
                source_line=line_start + 1,
                original_line=original_line
            ))
            
        elif pattern_name in ['export_list', 'export_type_list']:
            # Export lists
            is_type_only = pattern_name == 'export_type_list'
            export_names_str = match.group(1)
            re_export_from = match.group(2) if match.lastindex >= 2 else None
            
            # Parse individual export names
            export_names = self._parse_export_names(export_names_str)
            
            for export_name in export_names:
                exports.append(ExportInfo(
                    name=export_name,
                    is_default=False,
                    is_named=True,
                    is_type_only=is_type_only,
                    export_type='list',
                    source_line=line_start + 1,
                    original_line=original_line,
                    is_re_export=re_export_from is not None,
                    re_export_from=re_export_from
                ))
                
        elif pattern_name.startswith('export_star'):
            # Star exports
            if pattern_name == 'export_star_as':
                namespace_name = match.group(1)
                re_export_from = match.group(2)
                
                exports.append(ExportInfo(
                    name=namespace_name,
                    is_default=False,
                    is_named=True,
                    is_type_only=False,
                    export_type='namespace',
                    source_line=line_start + 1,
                    original_line=original_line,
                    is_re_export=True,
                    re_export_from=re_export_from
                ))
        
        return exports
    
    def _create_multiline_export_info(self, pattern_name: str, match, lines: List[str], content: str) -> List[ExportInfo]:
        """Create ExportInfo objects from multiline export matches"""
        exports = []
        
        # Get line number
        line_start = content[:match.start()].count('\n')
        original_line = lines[line_start].strip() if line_start < len(lines) else ""
        
        is_type_only = 'type' in pattern_name
        export_names_str = match.group(1)
        re_export_from = match.group(2) if match.lastindex >= 2 else None
        
        # Parse individual export names from multiline content
        export_names = self._parse_multiline_export_names(export_names_str)
        
        for export_name in export_names:
            exports.append(ExportInfo(
                name=export_name,
                is_default=False,
                is_named=True,
                is_type_only=is_type_only,
                export_type='multiline_list',
                source_line=line_start + 1,
                original_line=original_line,
                is_re_export=re_export_from is not None,
                re_export_from=re_export_from
            ))
        
        return exports
    
    def _parse_export_names(self, export_names_str: str) -> List[str]:
        """Parse export names from a comma-separated string"""
        names = []
        
        # Split by comma and clean up
        for name in export_names_str.split(','):
            name = name.strip()
            if name:
                # Handle 'as' aliases - take alias name (the exported name)
                if ' as ' in name:
                    name = name.split(' as ')[1].strip()
                
                # Remove type keyword if present
                if name.startswith('type '):
                    name = name[5:].strip()
                
                names.append(name)
        
        return [name for name in names if name and name.isidentifier()]
    
    def _parse_multiline_export_names(self, export_names_str: str) -> List[str]:
        """Parse export names from multiline export content"""
        # Remove newlines and extra whitespace
        cleaned = re.sub(r'\s+', ' ', export_names_str.strip())
        return self._parse_export_names(cleaned)
    
    def _validate_and_deduplicate(self, exports: List[ExportInfo]) -> List[ExportInfo]:
        """Validate exports and remove duplicates"""
        seen = set()
        validated = []
        
        for export in exports:
            # Create unique key that includes source line to prevent duplicates from same line
            key = (export.name, export.is_default, export.is_type_only, export.source_line, export.original_line)
            
            if key not in seen:
                seen.add(key)
                validated.append(export)
        
        return validated
    
    def get_export_summary(self, file_path: str) -> Dict[str, Any]:
        """Get a comprehensive summary of exports in a file"""
        exports = self.parse_file(file_path)
        
        return {
            'file_path': file_path,
            'total_exports': len(exports),
            'default_exports': len([e for e in exports if e.is_default]),
            'named_exports': len([e for e in exports if e.is_named]),
            'type_exports': len([e for e in exports if e.is_type_only]),
            're_exports': len([e for e in exports if e.is_re_export]),
            'export_names': [e.name for e in exports],
            'exports': exports
        }