"""
Export Generator - Generates TypeScript index file content from workflow context
Creates clean barrel exports with proper conflict resolution
"""

from typing import List, Dict, Set
from workflow_context import WorkflowContext, ExportInfo, DirectoryContext
from export_tracker import ExportTracker


class ExportGenerator:
    """
    Generates TypeScript export statements from workflow context.
    Uses the shared context to make informed decisions about exports.
    """
    
    def __init__(self, export_tracker: ExportTracker = None):
        self.export_tracker = export_tracker or ExportTracker()
    
    def generate_index_content(self, context: WorkflowContext, dir_path: str) -> str:
        """
        Generate complete index.ts content for a directory.
        This is the main entry point for the export generator workflow stage.
        """
        dir_context = context.get_directory_context(dir_path)
        
        if not dir_context.needs_index:
            return ""
        
        lines = []
        
        # Add header
        lines.extend(self._generate_header())
        
        # Generate file exports
        file_exports = self._generate_file_exports(context, dir_context)
        if file_exports:
            lines.extend(file_exports)
        
        # Generate directory exports
        dir_exports = self._generate_directory_exports(context, dir_context)
        if dir_exports:
            if file_exports:  # Add spacing if we have both file and directory exports
                lines.append("")
            lines.extend(dir_exports)
        
        # Add final newline
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_header(self) -> List[str]:
        """Generate file header"""
        return [
            "// Auto-generated index file",
            "// Run index generator to regenerate",
            ""
        ]
    
    def _generate_file_exports(self, context: WorkflowContext, dir_context: DirectoryContext) -> List[str]:
        """Generate exports for files in the current directory"""
        if not dir_context.files:
            return []
        
        exports = []
        
        # Group exports by file
        for file_context in dir_context.files:
            if not file_context.exports:
                continue
            
            file_name = file_context.file_name_without_ext
            
            # Separate exports into mutually exclusive categories
            type_exports = [e for e in file_context.exports if e.is_type_only and not e.is_default]
            value_exports = [e for e in file_context.exports if not e.is_type_only and not e.is_default]
            default_exports = [e for e in file_context.exports if e.is_default]
            
            # Generate type exports with smart aliasing
            if type_exports:
                type_exports_by_name = self._group_exports_by_name(type_exports)
                for original_name, export_list in type_exports_by_name.items():
                    if self._needs_smart_aliasing(context, dir_context, original_name):
                        # Apply smart aliasing based on filename
                        file_prefix = self._to_camel_case(file_name)  
                        alias_name = f"{file_prefix}{original_name[0].upper() + original_name[1:]}"
                        
                        # Debug logging for type-level alias generation
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"    🔧 Type alias: file='{file_name}' -> prefix='{file_prefix}' + export='{original_name}' = alias='{alias_name}'")
                        
                        exports.append(f"export type {{ {original_name} as {alias_name} }} from './{file_name}';")
                    else:
                        unique_names = [self._get_export_name(context, export) for export in export_list]
                        unique_names = list(dict.fromkeys(unique_names))
                        if len(unique_names) == 1:
                            exports.append(f"export type {{ {unique_names[0]} }} from './{file_name}';")
                        elif len(unique_names) > 1:
                            type_list = ", ".join(unique_names)
                            exports.append(f"export type {{ {type_list} }} from './{file_name}';")
            
            # Generate value exports with smart aliasing
            if value_exports:
                value_exports_by_name = self._group_exports_by_name(value_exports)
                for original_name, export_list in value_exports_by_name.items():
                    if self._needs_smart_aliasing(context, dir_context, original_name):
                        # Apply smart aliasing based on filename
                        file_prefix = self._to_camel_case(file_name)
                        alias_name = f"{file_prefix}{original_name[0].upper() + original_name[1:]}"
                        
                        # Debug logging for file-level alias generation
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"    🔧 File alias: file='{file_name}' -> prefix='{file_prefix}' + export='{original_name}' = alias='{alias_name}'")
                        
                        if context.should_use_export_type(file_context.file_path):
                            exports.append(f"export type {{ {original_name} as {alias_name} }} from './{file_name}';")
                        else:
                            exports.append(f"export {{ {original_name} as {alias_name} }} from './{file_name}';")
                    else:
                        unique_names = [self._get_export_name(context, export) for export in export_list]
                        unique_names = list(dict.fromkeys(unique_names))
                        if len(unique_names) == 1:
                            if context.should_use_export_type(file_context.file_path):
                                exports.append(f"export type {{ {unique_names[0]} }} from './{file_name}';")
                            else:
                                exports.append(f"export {{ {unique_names[0]} }} from './{file_name}';")
                        elif len(unique_names) > 1:
                            value_list = ", ".join(unique_names)
                            if context.should_use_export_type(file_context.file_path):
                                exports.append(f"export type {{ {value_list} }} from './{file_name}';")
                            else:
                                exports.append(f"export {{ {value_list} }} from './{file_name}';")
            
            # Generate default exports properly - preserve as re-exported defaults
            if default_exports:
                # Get names already exported to avoid conflicts
                exported_names = set()
                if type_exports:
                    exported_names.update(self._get_export_name(context, export) for export in type_exports)
                if value_exports:
                    exported_names.update(self._get_export_name(context, export) for export in value_exports)
                
                for default_export in default_exports:
                    export_name = self._get_export_name(context, default_export)
                    if export_name not in exported_names:
                        # For default exports, we need to use import/export pattern to preserve default nature
                        # This is better than export { default as name } because it maintains the default export semantics
                        if default_export.is_type_only or context.should_use_export_type(file_context.file_path):
                            exports.append(f"export type {{ default as {export_name} }} from './{file_name}';")
                        else:
                            exports.append(f"export {{ default as {export_name} }} from './{file_name}';")
        
        return exports
    
    def _collect_all_exports_recursively(self, context: WorkflowContext, dir_path: str, visited: set = None) -> set:
        """
        Collect all export names that would be available from a directory.
        Simplified non-recursive approach to avoid performance issues.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.debug(f"      📊 Collecting exports from: {dir_path}")
        
        all_exports = set()
        
        # Get directory context
        dir_context = context.directories.get(dir_path)
        if not dir_context:
            return all_exports
        
        # Add exports from direct files in this directory only
        for file_context in dir_context.files:
            for export in file_context.exports:
                all_exports.add(export.name)
        
        logger.debug(f"        📄 Found {len(all_exports)} direct file exports in {dir_path}")
        
        # For subdirectories, only collect their direct exports (no deep recursion)
        # This avoids exponential performance problems
        for subdir in dir_context.subdirectories:
            subdir_path = f"{dir_path}/{subdir}".replace("\\", "/")
            subdir_context = context.directories.get(subdir_path)
            
            # Include subdirectories that have index files or need them generated
            if subdir_context and (subdir_context.has_index or subdir_context.needs_index):
                logger.debug(f"        📁 Collecting direct exports from subdirectory: {subdir_path}")
                
                # Only collect direct file exports from subdirectory (no further recursion)
                for file_context in subdir_context.files:
                    for export in file_context.exports:
                        all_exports.add(export.name)
                
                logger.debug(f"        ✅ Added direct exports from {subdir_path}")
        
        logger.debug(f"      ✅ Total {len(all_exports)} exports collected from {dir_path}")
        return all_exports

    def _collect_export_objects_recursively(self, context: WorkflowContext, dir_path: str, visited: set = None) -> List:
        """
        Collect all export objects that would be available from a directory.
        Simplified non-recursive approach to avoid performance issues.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.debug(f"      📊 Collecting export objects from: {dir_path}")
        
        all_exports = []
        
        # Get directory context
        dir_context = context.directories.get(dir_path)
        if not dir_context:
            return all_exports
        
        # Add exports from direct files in this directory
        for file_context in dir_context.files:
            for export in file_context.exports:
                all_exports.append(export)
        
        logger.debug(f"        📄 Found {len(all_exports)} direct file export objects in {dir_path}")
        
        # For subdirectories, only collect their direct exports (no deep recursion)
        # This avoids exponential performance problems
        for subdir in dir_context.subdirectories:
            subdir_path = f"{dir_path}/{subdir}".replace("\\", "/")
            subdir_context = context.directories.get(subdir_path)
            if subdir_context and (subdir_context.has_index or subdir_context.needs_index):
                logger.debug(f"        📁 Collecting direct export objects from subdirectory: {subdir_path}")
                
                # Only collect direct file exports from subdirectory (no further recursion)
                for file_context in subdir_context.files:
                    for export in file_context.exports:
                        all_exports.append(export)
                
                logger.debug(f"        ✅ Added direct export objects from {subdir_path}")
        
        logger.debug(f"      ✅ Total {len(all_exports)} export objects collected from {dir_path}")
        return all_exports
    
    def _generate_directory_exports(self, context: WorkflowContext, dir_context: DirectoryContext) -> List[str]:
        """Generate exports for subdirectories with cross-directory conflict detection"""
        if not dir_context.subdirectories:
            return []
        
        exports = []
        
        # First, collect all exports from all subdirectories to detect cross-directory conflicts
        all_subdir_exports = {}
        subdir_export_map = {}
        
        for subdir in dir_context.subdirectories:
            subdir_path = f"{dir_context.dir_path}/{subdir}".replace("\\", "/")
            
            # Check if subdirectory has an index file
            subdir_context = context.directories.get(subdir_path)
            if not subdir_context or not subdir_context.has_index:
                continue
            
            # Collect all exports from this subdirectory (including nested)
            subdir_exports = self._collect_all_exports_recursively(context, subdir_path)
            
            subdir_export_map[subdir] = subdir_exports
            
            # Track which directories export which names
            for export_name in subdir_exports:
                if export_name not in all_subdir_exports:
                    all_subdir_exports[export_name] = []
                all_subdir_exports[export_name].append(subdir)
        
        # Find cross-directory conflicts
        conflicting_exports = {name: dirs for name, dirs in all_subdir_exports.items() if len(dirs) > 1}
        
        # Generate exports with smart handling of conflicts
        for subdir in dir_context.subdirectories:
            subdir_path = f"{dir_context.dir_path}/{subdir}".replace("\\", "/")
            
            # Check if subdirectory has an index file or needs one to be generated
            subdir_context = context.directories.get(subdir_path)
            if not subdir_context or (not subdir_context.has_index and not subdir_context.needs_index):
                continue
            
            # Check if this subdirectory has any conflicting exports
            subdir_exports = subdir_export_map.get(subdir, set())
            has_conflicts = any(export_name in conflicting_exports for export_name in subdir_exports)
            
            if has_conflicts:
                # Generate explicit exports with aliases for conflicting items
                subdir_exports = subdir_export_map.get(subdir, set())
                
                # Separate conflicting and non-conflicting exports
                conflicting_names = set()
                for export_name in subdir_exports:
                    if export_name in conflicting_exports:
                        conflicting_names.add(export_name)
                
                if conflicting_names:
                    # Import conflicting exports and re-export with aliases
                    import_statements = []
                    export_statements = []
                    
                    for export_name in conflicting_names:
                        # Create more readable alias by using PascalCase for subdirectory + PascalCase export name
                        subdir_prefix = self._to_pascal_case(subdir)
                        export_suffix = self._to_pascal_case(export_name)
                        alias_name = f"{subdir_prefix}{export_suffix}"
                        import_statements.append(f"{export_name} as {alias_name}")
                        export_statements.append(alias_name)
                    
                    # Add import/export pair
                    if context.should_use_export_type(subdir_path):
                        import_line = f"import type {{ {', '.join(import_statements)} }} from './{subdir}';"
                        export_line = f"export type {{ {', '.join(export_statements)} }};"
                    else:
                        import_line = f"import {{ {', '.join(import_statements)} }} from './{subdir}';"
                        export_line = f"export {{ {', '.join(export_statements)} }};"
                    
                    # Note: We'll need to handle this differently since we can't mix import/export in barrel files
                    # For now, just create aliased re-exports
                    exports.append(f"// Aliased exports from {subdir} to resolve conflicts")
                    for export_name in conflicting_names:
                        # Create more readable alias by using PascalCase for subdirectory + PascalCase export name
                        subdir_prefix = self._to_pascal_case(subdir)
                        export_suffix = self._to_pascal_case(export_name)
                        alias_name = f"{subdir_prefix}{export_suffix}"
                        
                        # Debug logging for alias generation
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.debug(f"    🔧 Generating alias: subdir='{subdir}' -> prefix='{subdir_prefix}' + export='{export_name}' -> suffix='{export_suffix}' = alias='{alias_name}'")
                        
                        if context.should_use_export_type(subdir_path):
                            exports.append(f"export type {{ {export_name} as {alias_name} }} from './{subdir}';")
                        else:
                            exports.append(f"export {{ {export_name} as {alias_name} }} from './{subdir}';")
                
                # Export non-conflicting items normally
                non_conflicting = subdir_exports - conflicting_names
                if non_conflicting:
                    # Export each non-conflicting item individually
                    # Need to check each export individually for type-only status
                    subdir_export_objects = self._collect_export_objects_recursively(context, subdir_path)
                    for export_name in sorted(non_conflicting):
                        # Find the export object to check if it's type-only
                        is_type_only = any(exp.is_type_only for exp in subdir_export_objects if exp.name == export_name)
                        if is_type_only or context.should_use_export_type(subdir_path):
                            exports.append(f"export type {{ {export_name} }} from './{subdir}';")
                        else:
                            exports.append(f"export {{ {export_name} }} from './{subdir}';")
                else:
                    # All exports from this directory are conflicting, so just use aliases
                    exports.append(f"// All exports from {subdir} have conflicts - using aliases above")
            else:
                # No conflicts, use normal barrel export
                if context.should_use_export_type(subdir_path):
                    exports.append(f"export type * from './{subdir}';")
                else:
                    exports.append(f"export * from './{subdir}';")
        
        return exports
    
    def _get_export_name(self, context: WorkflowContext, export_info: ExportInfo) -> str:
        """
        Get the final export name, handling conflicts if necessary.
        Uses context to make smart decisions about naming.
        """
        original_name = export_info.name
        
        # Check for conflicts
        if not context.has_conflict(original_name):
            return original_name
        
        # Handle conflicts - get all conflicting exports
        conflicts = context.get_export_conflicts(original_name)
        
        # If this export is from a well-known location, prefer it
        if self._is_primary_export(export_info, conflicts):
            return original_name
        
        # Generate alias for this export
        return self._generate_alias(export_info)
    
    def _is_primary_export(self, export_info: ExportInfo, all_conflicts: List[ExportInfo]) -> bool:
        """
        Determine if this export should get the primary name.
        Primary exports are typically from more specific or commonly used locations.
        """
        file_path = export_info.file_path.lower()
        
        # Prefer exports from files named after the export
        if export_info.name.lower() in file_path:
            return True
        
        # Prefer exports from main domain files over index re-exports
        if 'index' not in file_path:
            has_index_conflict = any('index' in conflict.file_path.lower() for conflict in all_conflicts)
            if has_index_conflict:
                return True
        
        # Prefer exports from more specific paths (deeper in hierarchy)
        path_depth = file_path.count('/')
        max_depth = max(conflict.file_path.lower().count('/') for conflict in all_conflicts)
        if path_depth == max_depth:
            return True
        
        return False
    
    def _generate_alias(self, export_info: ExportInfo) -> str:
        """Generate a meaningful alias for a conflicting export"""
        # Extract meaningful parts from the file path
        path_parts = export_info.file_path.replace('\\', '/').split('/')
        
        # Get the directory name (parent of the file)
        if len(path_parts) >= 2:
            dir_name = path_parts[-2]  # Parent directory
        else:
            dir_name = path_parts[-1].split('.')[0]  # File name without extension
        
        # Convert to PascalCase for alias
        clean_dir = self._to_pascal_case(dir_name)
        
        return f"{clean_dir}{export_info.name}"
    
    def _to_pascal_case(self, text: str) -> str:
        """Convert text to PascalCase"""
        import re
        
        # If already in CamelCase/PascalCase, return as-is
        if re.match(r'^[A-Z][a-zA-Z0-9]*$', text):
            return text
            
        # Handle kebab-case, snake_case, etc.
        parts = []
        for part in text.replace('-', '_').replace('.', '_').split('_'):
            if part:
                parts.append(part.capitalize())
        
        return ''.join(parts)
    
    def _to_camel_case(self, text: str) -> str:
        """Convert text to camelCase"""
        pascal = self._to_pascal_case(text)
        return pascal[0].lower() + pascal[1:] if pascal else ""
    
    def _group_exports_by_name(self, exports: List) -> Dict[str, List]:
        """Group exports by their original name"""
        groups = {}
        for export in exports:
            if export.name not in groups:
                groups[export.name] = []
            groups[export.name].append(export)
        return groups
    
    def _needs_smart_aliasing(self, context: WorkflowContext, dir_context: DirectoryContext, export_name: str) -> bool:
        """
        Determine if smart aliasing is needed for an export name.
        Returns True if multiple files in the same directory export the same name.
        """
        # Count how many files in this directory export this name
        files_with_export = 0
        conflicting_files = []
        for file_context in dir_context.files:
            if any(export.name == export_name for export in file_context.exports):
                files_with_export += 1
                conflicting_files.append(file_context.file_name_without_ext)
        
        needs_aliasing = files_with_export > 1
        if needs_aliasing:
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"    ⚠️  Smart aliasing needed for '{export_name}': found in {files_with_export} files: {conflicting_files}")
        
        return needs_aliasing
    
    def validate_generated_content(self, context: WorkflowContext, content: str, dir_path: str) -> bool:
        """
        Validate the generated content for common issues.
        Updates context with any validation errors.
        """
        lines = content.split('\n')
        export_lines = [line for line in lines if line.strip().startswith('export')]
        
        # Check for duplicate export lines
        seen_exports = set()
        for line in export_lines:
            if line in seen_exports:
                context.add_error(f"Duplicate export line: {line}", dir_path)
                return False
            seen_exports.add(line)
        
        # Check for empty export statements
        for line in export_lines:
            if 'export {  }' in line or 'export type {  }' in line:
                context.add_warning(f"Empty export statement: {line}", dir_path)
        
        # Check for undefined references
        if 'undefined' in content:
            context.add_error(f"Generated content contains 'undefined'", dir_path)
            return False
        
        return True