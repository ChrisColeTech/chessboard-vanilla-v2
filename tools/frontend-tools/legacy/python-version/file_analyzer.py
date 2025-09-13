"""
File Analyzer Module
Handles analysis of TypeScript/JavaScript files to extract export information
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from ast_parser import TypeScriptASTParser, ExportInfo as ASTExportInfo


@dataclass
class ExportInfo:
    """Information about an exported symbol"""
    name: str
    is_default: bool
    is_named: bool
    is_type_only: bool
    original_line: str


class FileAnalyzer:
    """
    Analyzes TypeScript/JavaScript files to extract export information.
    """
    
    def __init__(self):
        self.ast_parser = TypeScriptASTParser()
        self.supported_extensions = ['.ts', '.tsx', '.js', '.jsx']
        self.exclude_patterns = [
            r'\.test\.',
            r'\.spec\.',
            r'\.d\.ts$',
            r'index\.',
            r'\.stories\.',
            r'\.config\.'
        ]
    
    def is_valid_file(self, filename: str) -> bool:
        """
        Check if file should be processed.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file should be processed, False otherwise
        """
        file_path = Path(filename)
        ext = file_path.suffix
        
        # Check extension
        if ext not in self.supported_extensions:
            return False
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if re.search(pattern, filename):
                return False
        
        return True
    
    async def analyze_file_exports(self, file_path: str) -> List[ExportInfo]:
        """
        Analyze a file to extract export information using AST parsing with regex fallback.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            List of export information objects
        """
        # Primary: Use AST parser for precise detection
        try:
            ast_exports = self.ast_parser.parse_file(file_path)
            
            # Convert AST exports to FileAnalyzer format
            exports = []
            for ast_export in ast_exports:
                exports.append(ExportInfo(
                    name=ast_export.name,
                    is_default=ast_export.is_default,
                    is_named=ast_export.is_named,
                    is_type_only=ast_export.is_type_only,
                    original_line=ast_export.original_line
                ))
            
            return exports
            
        except Exception as e:
            print(f"AST parsing failed for {file_path}: {e}")
            print("Falling back to regex-based parsing...")
            
            # Fallback: Use original regex-based parsing
            return self._fallback_regex_analysis(file_path)
    
    def _fallback_regex_analysis(self, file_path: str) -> List[ExportInfo]:
        """
        Fallback regex-based analysis for edge cases where AST parsing fails.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        exports = []
        lines = content.split('\n')
        
        for line in lines:
            trimmed_line = line.strip()
            
            # Skip comments and empty lines
            if (trimmed_line.startswith('//') or 
                trimmed_line.startswith('/*') or 
                not trimmed_line):
                continue
            
            # Basic export patterns for fallback
            if trimmed_line.startswith('export '):
                # Default exports
                if re.match(r'^export\s+default\s+', trimmed_line):
                    match = re.search(r'^export\s+default\s+(?:\w+\s+)?(\w+)', trimmed_line)
                    if match:
                        exports.append(ExportInfo(
                            name=match.group(1),
                            is_default=True,
                            is_named=False,
                            is_type_only='interface' in trimmed_line or 'type' in trimmed_line,
                            original_line=trimmed_line
                        ))
                
                # Named exports
                elif re.match(r'^export\s+(interface|type|class|function|const|let|var|enum)\s+(\w+)', trimmed_line):
                    match = re.match(r'^export\s+(\w+)\s+(\w+)', trimmed_line)
                    if match:
                        export_type = match.group(1)
                        export_name = match.group(2)
                        exports.append(ExportInfo(
                            name=export_name,
                            is_default=False,
                            is_named=True,
                            is_type_only=export_type in ['interface', 'type', 'enum'],
                            original_line=trimmed_line
                        ))
        
        return exports
    
    def remove_extension(self, filename: str) -> str:
        """
        Remove file extension from filename.
        
        Args:
            filename: Filename with extension
            
        Returns:
            Filename without extension
        """
        return re.sub(r'\.[^/.]+$', '', filename)
    
    def analyze_existing_index(self, index_path: str) -> Dict[str, Any]:
        """
        Analyze existing index.ts file to preserve custom content.
        
        Args:
            index_path: Path to existing index.ts file
            
        Returns:
            Dictionary with existing exports, custom content, and auto-generated flag
        """
        if not Path(index_path).exists():
            return {
                'existing_exports': [],
                'custom_content': [],
                'is_auto_generated': False
            }
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return {
                'existing_exports': [],
                'custom_content': [],
                'is_auto_generated': False
            }
        
        lines = content.split('\n')
        existing_exports = []
        custom_content = []
        is_auto_generated = False
        in_class = False
        brace_count = 0
        
        for line in lines:
            trimmed_line = line.strip()
            
            # Check if auto-generated
            if ('Auto-generated' in trimmed_line and 
                ('index' in trimmed_line or 'barrel' in trimmed_line)):
                is_auto_generated = True
                continue
            
            # Skip auto-generation comments
            if (trimmed_line.startswith('//') and 
                ('Run `npm run generate:index`' in trimmed_line or 
                 'Auto-generated' in trimmed_line)):
                continue
            
            # Track class blocks
            if 'export class' in trimmed_line or 'class ' in trimmed_line:
                in_class = True
                custom_content.append(line)
                brace_count += line.count('{') - line.count('}')
                continue
            
            if in_class:
                custom_content.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0:
                    in_class = False
                    brace_count = 0
                continue
            
            # Collect exports and other content
            if trimmed_line.startswith('export ') and 'Auto-generated' not in trimmed_line:
                existing_exports.append(line)
            # Collect custom content (imports, types, interfaces, etc.)
            elif trimmed_line and not trimmed_line.startswith('//'):
                custom_content.append(line)
        
        return {
            'existing_exports': existing_exports,
            'custom_content': custom_content,
            'is_auto_generated': is_auto_generated
        }