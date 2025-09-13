"""
Export Generator Module
Generates TypeScript export statements with conflict resolution and aliasing
"""

import re
from typing import List, Dict, Set, Tuple, Any
from file_analyzer import ExportInfo


class ExportGenerator:
    """
    Generates TypeScript export statements with proper conflict resolution.
    """
    
    def __init__(self):
        pass
    
    def generate_export_statements(self, export_info: List[ExportInfo], 
                                 file_name: str, 
                                 export_name_tracker: Dict[str, List[str]] = None) -> Dict[str, List[str]]:
        """
        Generate modern export statements with deduplication and conflict resolution.
        
        Args:
            export_info: List of export information
            file_name: Name of the file (without extension)
            export_name_tracker: Map of export names to files that export them
            
        Returns:
            Dictionary with 'exports' and 'reexports' lists
        """
        if export_name_tracker is None:
            export_name_tracker = {}
            
        exports = []
        reexports = []
        
        # Deduplicate exports by name - prefer named over default
        exports_by_name = {}
        
        for export_item in export_info:
            existing = exports_by_name.get(export_item.name)
            
            if existing is None:
                exports_by_name[export_item.name] = export_item
            else:
                # Prefer named exports over default exports
                if export_item.is_named and existing.is_default:
                    exports_by_name[export_item.name] = export_item
        
        # Separate deduplicated exports
        unique_exports = list(exports_by_name.values())
        default_exports = [e for e in unique_exports if e.is_default]
        named_exports = [e for e in unique_exports if e.is_named]
        
        # Separate named exports by type vs value
        type_exports = [e for e in named_exports if e.is_type_only]
        value_exports = [e for e in named_exports if not e.is_type_only]
        
        # Create export statements
        named_names = {e.name for e in named_exports}
        
        # Handle default exports - only if no named export with same name
        for default_export in default_exports:
            if default_export.name not in named_names:
                if default_export.is_type_only:
                    reexports.append(f"export type {{ default as {default_export.name} }} from './{file_name}';")
                else:
                    reexports.append(f"export {{ default as {default_export.name} }} from './{file_name}';")
        
        # Handle type exports - use 'export type' syntax with conflict resolution
        if type_exports:
            type_export_statements = self.generate_export_statements_with_aliases(
                type_exports, file_name, export_name_tracker, True
            )
            reexports.extend(type_export_statements)
        
        # Handle value exports - use regular 'export' syntax with conflict resolution
        if value_exports:
            value_export_statements = self.generate_export_statements_with_aliases(
                value_exports, file_name, export_name_tracker, False
            )
            reexports.extend(value_export_statements)
        
        return {'exports': exports, 'reexports': reexports}
    
    def generate_export_statements_with_aliases(self, exports: List[ExportInfo], 
                                              file_name: str,
                                              export_name_tracker: Dict[str, List[str]],
                                              is_type_export: bool) -> List[str]:
        """
        Generate export statements with alias resolution for naming conflicts.
        
        Args:
            exports: List of export information
            file_name: Name of the file
            export_name_tracker: Map tracking which files export which names
            is_type_export: Whether these are type-only exports
            
        Returns:
            List of export statements
        """
        statements = []
        export_keyword = 'export type' if is_type_export else 'export'
        
        # Group exports by name for conflict resolution
        exports_by_name = {}
        for exp in exports:
            if exp.name not in exports_by_name:
                exports_by_name[exp.name] = []
            exports_by_name[exp.name].append(exp)
        
        for export_name, export_list in exports_by_name.items():
            conflicting_files = export_name_tracker.get(export_name, [])
            
            if len(conflicting_files) > 1:
                # Naming conflict detected - use alias
                alias = self.generate_alias(export_name, file_name)
                statements.append(f"{export_keyword} {{ {export_name} as {alias} }} from './{file_name}';")
                print(f"   🔄 Aliased conflicting export: {export_name} → {alias} (from {file_name})")
            else:
                # No conflict - use original name
                export_names = ', '.join(e.name for e in export_list)
                statements.append(f"{export_keyword} {{ {export_names} }} from './{file_name}';")
        
        return statements
    
    def generate_alias(self, export_name: str, file_name: str) -> str:
        """
        Generate a unique alias for conflicting export names.
        
        Args:
            export_name: Original export name
            file_name: File name to base alias on
            
        Returns:
            Generated alias name
        """
        # Convert filename to PascalCase, removing file extensions and invalid chars
        clean_file_name = (file_name
                          .replace('.ts', '').replace('.tsx', '').replace('.js', '').replace('.jsx', '')
                          .replace('-', '_').replace('.', '_'))
        
        # Split by various separators and convert to PascalCase
        parts = re.split(r'[-_.]', clean_file_name)
        parts = [part for part in parts if part]
        clean_file_name = ''.join(part.capitalize() for part in parts)
        
        # Special cases for common conflicts
        if export_name == 'useAuthStore' and file_name == 'authStore':
            return 'useAuthStore'  # Don't alias this one - it should be the primary export
        
        # For common names, create readable aliases
        if 'actions' in export_name.lower():
            return clean_file_name + 'Actions'
        elif 'config' in export_name.lower():
            return clean_file_name + 'Config'
        elif 'instructions' in export_name.lower():
            return clean_file_name + 'Instructions'
        else:
            return clean_file_name + export_name[0].upper() + export_name[1:]
    
    def generate_index_content(self, exports: List[str], reexports: List[str]) -> str:
        """
        Generate the final index.ts content - clean and simple.
        
        Args:
            exports: List of direct export statements
            reexports: List of re-export statements
            
        Returns:
            Complete index file content
        """
        lines = []
        
        # Add file header
        lines.append('// Auto-generated index file')
        lines.append('// Run `npm run generate:index` to regenerate')
        lines.append('')
        
        # Add re-exports (modern approach)
        if reexports:
            lines.extend(reexports)
        
        # Add direct exports if any
        if exports:
            lines.append('')
            lines.extend(exports)
        
        lines.append('')  # Final newline
        
        return '\n'.join(lines)
    
    def generate_barrel_content(self, exports: List[str]) -> str:
        """
        Generate the barrel index.ts content.
        
        Args:
            exports: List of export statements
            
        Returns:
            Barrel index file content
        """
        lines = []
        
        # Add file header
        lines.append('// Auto-generated barrel index file')
        lines.append('// Run `npm run generate:index` to regenerate')
        lines.append('')
        
        # Add exports
        lines.extend(exports)
        lines.append('')  # Final newline
        
        return '\n'.join(lines)
    
    def extract_export_key(self, export_line: str) -> str:
        """
        Extract export key for deduplication.
        
        Args:
            export_line: Export statement line
            
        Returns:
            Export key or None if not found
        """
        # Extract the exported name for deduplication
        matches = re.search(r'export\s+\{\s*([^}]+)\s*\}', export_line)
        if matches:
            return matches.group(1).split(',')[0].strip().split(' as ')[0].strip()
        
        type_match = re.search(r'export\s+(?:type|interface|enum|class|const|let|var|function)\s+(\w+)', export_line)
        if type_match:
            return type_match.group(1)
        
        return None