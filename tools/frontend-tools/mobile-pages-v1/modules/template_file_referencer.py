"""
Simple Template File Referencer

Reads imports from template files and finds all required template dependencies.
"""

import re
from pathlib import Path
from typing import Set, List


class TemplateFileReferencer:
    """Simple file referencer that reads template imports."""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        # Build map of all available templates
        self.available_templates = self._scan_all_templates()
    
    def _scan_all_templates(self) -> Set[str]:
        """Get all available template files."""
        templates = set()
        if self.templates_dir.exists():
            for template_file in self.templates_dir.rglob('*.template'):
                rel_path = template_file.relative_to(self.templates_dir)
                templates.add(str(rel_path))
        return templates
    
    def get_imports_from_template(self, template_path: str) -> List[str]:
        """Read all imports from a template file."""
        full_path = self.templates_dir / template_path
        if not full_path.exists():
            return []
        
        content = full_path.read_text(encoding='utf-8')
        
        # Extract import statements
        import_pattern = r'import.*?from\s+[\'"]([^\'"]+)[\'"]'
        matches = re.findall(import_pattern, content)
        
        # Only return relative imports
        relative_imports = []
        for match in matches:
            if match.startswith('./') or match.startswith('../'):
                relative_imports.append(match)
        
        return relative_imports
    
    def find_referenced_templates(self, template_path: str) -> List[str]:
        """Find all template files referenced by imports."""
        imports = self.get_imports_from_template(template_path)
        referenced_templates = []
        
        for import_path in imports:
            # Try to find matching templates with context of current template
            matches = self._find_template_matches(import_path, template_path)
            referenced_templates.extend(matches)
        
        return referenced_templates
    
    def _find_template_matches(self, import_path: str, from_template: str = "") -> List[str]:
        """Find template files that match an import path."""
        # Resolve relative path based on importing template location
        if import_path.startswith('./') or import_path.startswith('../'):
            resolved_path = self._resolve_relative_import(import_path, from_template)
        else:
            resolved_path = import_path
        
        matches = []
        
        # Try exact matches with different extensions
        for ext in ['.ts.template', '.tsx.template', '.js.template', '.jsx.template']:
            potential = resolved_path + ext
            if potential in self.available_templates:
                matches.append(potential)
        
        # Try directory matches (import from directory gets all files)
        for template in self.available_templates:
            template_without_ext = template.replace('.template', '')
            if template_without_ext.startswith(resolved_path + '/'):
                matches.append(template)
        
        return matches
    
    def _resolve_relative_import(self, import_path: str, from_template: str) -> str:
        """Resolve relative import path based on importing template's location."""
        if not from_template:
            # Fallback to simple resolution
            return import_path.lstrip('./')
        
        # Get directory of importing template
        from_dir = str(Path(from_template).parent)
        
        # Start with the importing template's directory
        current_parts = from_dir.split('/') if from_dir != '.' else []
        
        # Process the import path
        import_parts = import_path.split('/')
        
        for part in import_parts:
            if part == '..':
                # Go up one directory
                if current_parts:
                    current_parts.pop()
            elif part == '.':
                # Stay in current directory
                continue
            elif part:  # Non-empty part
                current_parts.append(part)
        
        return '/'.join(current_parts)
    
    def get_all_dependencies(self, start_templates: List[str]) -> Set[str]:
        """Get all template dependencies recursively."""
        all_deps = set()
        to_process = start_templates.copy()
        processed = set()
        
        while to_process:
            current = to_process.pop(0)
            
            if current in processed:
                continue
                
            processed.add(current)
            
            if current in self.available_templates:
                all_deps.add(current)
                # Get dependencies of this template
                deps = self.find_referenced_templates(current)
                for dep in deps:
                    if dep not in processed:
                        to_process.append(dep)
        
        return all_deps