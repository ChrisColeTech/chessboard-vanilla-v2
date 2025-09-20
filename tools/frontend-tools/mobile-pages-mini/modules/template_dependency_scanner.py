"""
Template Dependency Scanner

Scans template files and recursively finds all their dependencies.
This module reads template files, extracts import statements, and builds
a complete dependency tree of all required template files.
"""

import re
from pathlib import Path
from typing import Set, Dict, List, Tuple
from dataclasses import dataclass


@dataclass 
class ScanResult:
    """Result of dependency scanning."""
    required_templates: Set[str]
    dependency_tree: Dict[str, Set[str]]
    missing_templates: Set[str]


class TemplateDependencyScanner:
    """Scans template files and finds all their dependencies recursively."""
    
    def __init__(self, static_templates_dir: Path, dynamic_templates_dir: Path):
        self.static_dir = static_templates_dir
        self.dynamic_dir = dynamic_templates_dir
        # Build a simple template map for fast lookup
        self.template_map = self._build_template_map()
    
    def _build_template_map(self) -> dict:
        """Build a map of import names to template paths for fast lookup."""
        template_map = {}
        
        # Scan static templates
        if self.static_dir.exists():
            for template_file in self.static_dir.rglob('*.template'):
                rel_path = template_file.relative_to(self.static_dir)
                # Remove .template extension for mapping
                import_name = str(rel_path)[:-9]  # Remove '.template'
                template_map[import_name] = str(rel_path)
        
        return template_map
        
    def scan_dependencies(self, page_type: str) -> ScanResult:
        """
        Scan all dependencies for a given page type.
        
        Args:
            page_type: "parent" or "child"
            
        Returns:
            ScanResult with all required templates and dependency tree
        """
        # Find core templates that will be generated
        core_templates = self._get_core_templates()
        
        # Find dynamic templates based on page type
        dynamic_templates = self._get_dynamic_templates(page_type)
        
        # Start with all templates that will be processed
        all_start_templates = core_templates | dynamic_templates
        
        # Recursively scan dependencies
        dependency_tree = {}
        required_templates = set()
        processed = set()
        
        for template in all_start_templates:
            self._scan_template_recursive(
                template, 
                required_templates, 
                dependency_tree, 
                processed
            )
        
        # Find missing templates
        missing_templates = self._find_missing_templates(required_templates)
        
        return ScanResult(
            required_templates=required_templates,
            dependency_tree=dependency_tree,
            missing_templates=missing_templates
        )
    
    def _get_core_templates(self) -> Set[str]:
        """Get core entry point template files."""
        # Only include true entry points, not all templates
        entry_points = {
            'App.tsx.template',
            'main.tsx.template', 
            'index.html.template',
            'package.json.template',
            'vite.config.ts.template',
            'tsconfig.json.template',
            'tsconfig.node.json.template',
            'index.css.template',
            'stores/appStore.ts.template'  # Add appStore as entry point so its dependencies get scanned
        }
        
        core_templates = set()
        if self.static_dir.exists():
            for entry_point in entry_points:
                entry_path = self.static_dir / entry_point
                if entry_path.exists():
                    core_templates.add(entry_point)
        
        return core_templates
    
    def _get_dynamic_templates(self, page_type: str) -> Set[str]:
        """Get dynamic template files for the given page type."""
        dynamic_templates = set()
        
        # Map page types to template patterns
        type_patterns = {
            'parent': ['parent-*.template', 'child-wrapper-*.template'],
            'child': ['child-*.template', 'child-wrapper-*.template']
        }
        
        patterns = type_patterns.get(page_type, [])
        
        if self.dynamic_dir.exists():
            for pattern in patterns:
                for file in self.dynamic_dir.rglob(pattern):
                    if file.is_file():
                        rel_path = file.relative_to(self.dynamic_dir)
                        dynamic_templates.add(str(rel_path))
        
        return dynamic_templates
    
    def _scan_template_recursive(
        self, 
        template_path: str, 
        required_templates: Set[str], 
        dependency_tree: Dict[str, Set[str]], 
        processed: Set[str]
    ) -> None:
        """Recursively scan a template and all its dependencies."""
        if template_path in processed:
            return
            
        processed.add(template_path)
        
        # Read template content
        content = self._read_template_content(template_path)
        if content is None:
            return
            
        # Extract imports from content
        imports = self._extract_imports(content)
        
        # Convert imports to template paths
        template_dependencies = set()
        for import_path in imports:
            template_deps = self._convert_import_to_template_paths(import_path, template_path)
            for template_dep in template_deps:
                template_dependencies.add(template_dep)
                required_templates.add(template_dep)
        
        # Store dependency tree
        dependency_tree[template_path] = template_dependencies
        
        # Recursively scan dependencies
        for dep in template_dependencies:
            self._scan_template_recursive(
                dep, 
                required_templates, 
                dependency_tree, 
                processed
            )
    
    def _read_template_content(self, template_path: str) -> str:
        """Read content of a template file."""
        # Try static directory first
        static_path = self.static_dir / template_path
        if static_path.exists():
            try:
                return static_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Warning: Could not read {static_path}: {e}")
                return None
        
        # Try dynamic directory
        dynamic_path = self.dynamic_dir / template_path
        if dynamic_path.exists():
            try:
                return dynamic_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Warning: Could not read {dynamic_path}: {e}")
                return None
        
        return None
    
    def _extract_imports(self, content: str) -> Set[str]:
        """Extract import paths from template content."""
        import_patterns = [
            r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # import ... from "path"
            r'import\s+[\'"]([^\'"]+)[\'"]',        # import "path"
        ]
        
        imports = set()
        for pattern in import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                # Only process relative imports that start with ./ or ../
                if match.startswith('./') or match.startswith('../'):
                    imports.add(match)
        
        return imports
    
    def _convert_import_to_template_paths(self, import_path: str, from_template_path: str = "") -> List[str]:
        """Convert an import path to template file paths using template map."""
        # Resolve relative path properly
        resolved_path = self._resolve_relative_import(import_path, from_template_path)
        
        # Skip dynamic dependencies
        if resolved_path in {'hooks/core/usePageData', 'components/ui/DataTable'}:
            return []
        
        # Direct lookup in template map
        if resolved_path in self.template_map:
            return [self.template_map[resolved_path]]
        
        # Try with different extensions
        for ext in ['.ts', '.tsx', '.js', '.jsx']:
            if resolved_path + ext in self.template_map:
                return [self.template_map[resolved_path + ext]]
        
        # For directory imports, find all templates in that directory
        directory_templates = []
        for import_name, template_path in self.template_map.items():
            if import_name.startswith(resolved_path + '/'):
                directory_templates.append(template_path)
        
        return directory_templates
    
    def _resolve_relative_import(self, import_path: str, from_template_path: str) -> str:
        """Resolve relative import paths like '../core/SettingsPanel' to relative paths."""
        if not import_path.startswith('.'):
            # Not a relative import, return as-is
            return import_path
        
        if not from_template_path:
            # No context, just strip leading dots
            return import_path.lstrip('./')
        
        # Use string manipulation to resolve relative paths
        return self._resolve_relative_import_fallback(import_path, from_template_path)
    
    def _resolve_relative_import_fallback(self, import_path: str, from_template_path: str) -> str:
        """Fallback method for resolving relative imports using string manipulation."""
        # Split paths into parts
        from_parts = from_template_path.split('/')
        import_parts = import_path.split('/')
        
        # Start from the directory containing the from_template
        current_parts = from_parts[:-1]  # Remove filename, keep directory parts
        
        # Process each part of the import path
        for part in import_parts:
            if part == '..':
                # Go up one directory
                if current_parts:
                    current_parts.pop()
            elif part == '.':
                # Stay in current directory
                continue
            elif part:
                # Add this part to the path
                current_parts.append(part)
        
        return '/'.join(current_parts)
    
    def _find_directory_templates(self, directory_path: str) -> List[str]:
        """Find all template files in a directory."""
        templates = []
        
        # Check static directory
        static_dir_path = self.static_dir / directory_path
        if static_dir_path.exists() and static_dir_path.is_dir():
            for file in static_dir_path.iterdir():
                if file.is_file() and file.suffix == '.template':
                    rel_path = file.relative_to(self.static_dir)
                    templates.append(str(rel_path))
        
        # Check dynamic directory
        dynamic_dir_path = self.dynamic_dir / directory_path
        if dynamic_dir_path.exists() and dynamic_dir_path.is_dir():
            for file in dynamic_dir_path.iterdir():
                if file.is_file() and file.suffix == '.template':
                    rel_path = file.relative_to(self.dynamic_dir)
                    templates.append(str(rel_path))
        
        return templates
    
    def _template_exists(self, template_path: str) -> bool:
        """Check if a template file exists in static or dynamic directories."""
        static_path = self.static_dir / template_path
        dynamic_path = self.dynamic_dir / template_path
        
        return static_path.exists() or dynamic_path.exists()
    
    def _find_missing_templates(self, required_templates: Set[str]) -> Set[str]:
        """Find templates that are required but don't exist."""
        missing = set()
        
        for template in required_templates:
            if not self._template_exists(template):
                missing.add(template)
        
        return missing