"""
Conflict Resolver Module
Handles duplicate export conflicts in barrel files
"""

import os
import re
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum


class ConflictStrategy(Enum):
    """Available conflict resolution strategies"""
    PREFIX_MODULE = "prefix_module"
    EXPLICIT_ALIAS = "explicit_alias"  
    NAMESPACE = "namespace"
    SKIP = "skip"


@dataclass
class ConflictSource:
    """Represents a source of export conflict"""
    module: str
    type: str  # 'subdir' or 'file'
    export_name: str


@dataclass
class ExportConflict:
    """Represents an export naming conflict"""
    export_name: str
    sources: List[ConflictSource]
    severity: str  # 'HIGH', 'MEDIUM', 'LOW'


class ConflictResolver:
    """
    Handles detection and resolution of export naming conflicts.
    """
    
    def __init__(self):
        self.conflict_strategies = ConflictStrategy
        self.common_type_names = ['User', 'GameResult', 'UpdateRequest', 'Config', 'Props', 'State']
    
    async def analyze_and_resolve_conflicts(self, dir_path: str, subdirs: List[str], 
                                          file_exports: List[Any]) -> Dict[str, Any]:
        """
        Analyze and resolve export conflicts.
        
        Args:
            dir_path: Directory path
            subdirs: List of subdirectories
            file_exports: List of file exports
            
        Returns:
            Resolution result with conflicts and strategy
        """
        conflicts = self.detect_conflicts(dir_path, subdirs, file_exports)
        
        if not conflicts:
            return {
                'has_conflicts': False,
                'conflicts': [],
                'resolution': None
            }
        
        resolution = await self.resolve_conflicts(dir_path, conflicts, subdirs)
        
        return {
            'has_conflicts': True,
            'conflicts': conflicts,
            'resolution': resolution
        }
    
    def detect_conflicts(self, dir_path: str, subdirs: List[str], 
                        file_exports: List[Any]) -> List[ExportConflict]:
        """
        Detect export conflicts between modules.
        
        Args:
            dir_path: Directory path
            subdirs: List of subdirectories
            file_exports: List of file exports
            
        Returns:
            List of detected conflicts
        """
        export_map: Dict[str, List[ConflictSource]] = {}
        conflicts = []
        
        # Track exports from subdirectories
        for subdir in subdirs:
            index_path = os.path.join(dir_path, subdir, 'index.ts')
            
            if os.path.exists(index_path):
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    exports = self.extract_exports_from_content(content)
                    
                    for export_name in exports:
                        if export_name not in export_map:
                            export_map[export_name] = []
                        
                        export_map[export_name].append(ConflictSource(
                            module=subdir,
                            type='subdir',
                            export_name=export_name
                        ))
                        
                except Exception as e:
                    print(f"⚠️  Could not analyze {index_path}: {e}")
        
        # Track exports from files in current directory
        for export_info in file_exports:
            export_name = self._extract_export_name(export_info)
            if export_name:
                if export_name not in export_map:
                    export_map[export_name] = []
                
                export_map[export_name].append(ConflictSource(
                    module='current',
                    type='file',
                    export_name=export_name
                ))
        
        # Find conflicts (exports that appear in multiple modules)
        for export_name, sources in export_map.items():
            if len(sources) > 1:
                conflicts.append(ExportConflict(
                    export_name=export_name,
                    sources=sources,
                    severity=self.assess_conflict_severity(export_name, sources)
                ))
        
        return conflicts
    
    def extract_exports_from_content(self, content: str) -> List[str]:
        """
        Extract export names from TypeScript content.
        
        Args:
            content: File content
            
        Returns:
            List of export names
        """
        exports = []
        
        # Match export patterns
        patterns = [
            # export interface/type/class/function Name
            r'export\s+(?:interface|type|class|function|const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)',
            # export { Name }
            r'export\s*\{\s*([^}]+)\s*\}',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                if '{' in pattern:
                    # Handle export { Name1, Name2 } pattern
                    export_list = match.group(1)
                    names = [
                        name.strip().split(' as ')[0].strip()
                        for name in export_list.split(',')
                        if name.strip() and '*' not in name
                    ]
                    exports.extend(names)
                else:
                    # Handle direct export pattern
                    exports.append(match.group(1))
        
        return list(set(exports))  # Remove duplicates
    
    def assess_conflict_severity(self, export_name: str, sources: List[ConflictSource]) -> str:
        """
        Assess conflict severity.
        
        Args:
            export_name: Export name
            sources: List of conflict sources
            
        Returns:
            Severity level ('HIGH', 'MEDIUM', 'LOW')
        """
        # High severity for common type names
        if any(common_name in export_name for common_name in self.common_type_names):
            return 'HIGH'
        
        # Medium severity for multiple subdirectories
        if len([s for s in sources if s.type == 'subdir']) > 1:
            return 'MEDIUM'
        
        return 'LOW'
    
    async def resolve_conflicts(self, dir_path: str, conflicts: List[ExportConflict], 
                              subdirs: List[str]) -> Dict[str, Any]:
        """
        Resolve conflicts using appropriate strategy.
        
        Args:
            dir_path: Directory path
            conflicts: List of detected conflicts
            subdirs: List of subdirectories
            
        Returns:
            Resolution strategy and exports
        """
        strategy = self.select_resolution_strategy(dir_path, conflicts)
        
        if strategy == ConflictStrategy.EXPLICIT_ALIAS:
            return self.create_explicit_alias_resolution(conflicts, subdirs)
        elif strategy == ConflictStrategy.NAMESPACE:
            return self.create_namespace_resolution(conflicts, subdirs)
        elif strategy == ConflictStrategy.PREFIX_MODULE:
            return self.create_prefix_resolution(conflicts, subdirs)
        else:
            return self.create_skip_resolution(conflicts, subdirs)
    
    def select_resolution_strategy(self, dir_path: str, conflicts: List[ExportConflict]) -> ConflictStrategy:
        """
        Select appropriate resolution strategy.
        
        Args:
            dir_path: Directory path
            conflicts: List of conflicts
            
        Returns:
            Selected strategy
        """
        high_severity_count = len([c for c in conflicts if c.severity == 'HIGH'])
        total_conflicts = len(conflicts)
        
        # For types directory with many high-severity conflicts, use explicit aliases
        if '/types' in dir_path and high_severity_count > 2:
            return ConflictStrategy.EXPLICIT_ALIAS
        
        # For many conflicts, use namespacing
        if total_conflicts > 5:
            return ConflictStrategy.NAMESPACE
        
        # Default to explicit aliases for precise control
        return ConflictStrategy.EXPLICIT_ALIAS
    
    def create_explicit_alias_resolution(self, conflicts: List[ExportConflict], 
                                       subdirs: List[str]) -> Dict[str, Any]:
        """
        Create explicit alias resolution.
        
        Args:
            conflicts: List of conflicts
            subdirs: List of subdirectories
            
        Returns:
            Resolution with explicit aliases
        """
        exports = []
        used_names: Set[str] = set()
        conflicting_modules: Set[str] = set()
        
        # Identify modules that have conflicts
        for conflict in conflicts:
            for source in conflict.sources:
                if source.type == 'subdir':
                    conflicting_modules.add(source.module)
        
        # Handle non-conflicting subdirectories first - use barrel exports
        for subdir in subdirs:
            if subdir not in conflicting_modules:
                exports.append(f"export * from './{subdir}';")
        
        # Handle conflicting exports with aliases
        for conflict in conflicts:
            for source in conflict.sources:
                if source.type == 'subdir':
                    alias_name = self.generate_alias(conflict.export_name, source.module)
                    if alias_name not in used_names:
                        exports.append(f"export {{ {conflict.export_name} as {alias_name} }} from './{source.module}';")
                        used_names.add(alias_name)
        
        return {
            'strategy': ConflictStrategy.EXPLICIT_ALIAS.value,
            'exports': exports,
            'explanation': 'Using explicit aliases to resolve naming conflicts while preserving barrel exports',
            'conflicts_resolved': len(conflicts)
        }
    
    def create_namespace_resolution(self, conflicts: List[ExportConflict], 
                                  subdirs: List[str]) -> Dict[str, Any]:
        """
        Create namespace resolution.
        
        Args:
            conflicts: List of conflicts
            subdirs: List of subdirectories
            
        Returns:
            Resolution with namespaced exports
        """
        exports = []
        for subdir in subdirs:
            valid_identifier = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), subdir)
            exports.append(f"export * as {valid_identifier} from './{subdir}';")
        
        return {
            'strategy': ConflictStrategy.NAMESPACE.value,
            'exports': exports,
            'explanation': 'Using namespaced exports to avoid all conflicts',
            'conflicts_resolved': len(conflicts)
        }
    
    def create_prefix_resolution(self, conflicts: List[ExportConflict], 
                               subdirs: List[str]) -> Dict[str, Any]:
        """
        Create prefix resolution.
        
        Args:
            conflicts: List of conflicts
            subdirs: List of subdirectories
            
        Returns:
            Resolution with module prefixes
        """
        # This would require modifying source files, which is complex
        # For now, fallback to explicit alias
        return self.create_explicit_alias_resolution(conflicts, subdirs)
    
    def create_skip_resolution(self, conflicts: List[ExportConflict], 
                             subdirs: List[str]) -> Dict[str, Any]:
        """
        Create skip resolution.
        
        Args:
            conflicts: List of conflicts
            subdirs: List of subdirectories
            
        Returns:
            Resolution that skips conflicting modules
        """
        exports = []
        conflicting_modules: Set[str] = set()
        
        # Identify modules with conflicts
        for conflict in conflicts:
            for source in conflict.sources:
                if source.type == 'subdir':
                    conflicting_modules.add(source.module)
        
        # Export non-conflicting modules only
        for subdir in subdirs:
            if subdir not in conflicting_modules:
                exports.append(f"export * from './{subdir}';")
        
        return {
            'strategy': ConflictStrategy.SKIP.value,
            'exports': exports,
            'explanation': 'Skipping conflicting modules to avoid errors',
            'conflicts_resolved': 0,
            'skipped_modules': list(conflicting_modules)
        }
    
    def generate_alias(self, export_name: str, module_name: str) -> str:
        """
        Generate alias name for conflicting export.
        
        Args:
            export_name: Original export name
            module_name: Module name
            
        Returns:
            Generated alias name
        """
        # Convert module name to PascalCase
        module_prefix = ''.join(
            part.capitalize() for part in module_name.split('-')
        )
        
        return f"{module_prefix}{export_name}"
    
    def validate_resolution(self, resolution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate resolution result.
        
        Args:
            resolution: Resolution result to validate
            
        Returns:
            Validation result with warnings and errors
        """
        warnings = []
        errors = []
        
        # Check for duplicate exports in resolution
        export_names: Set[str] = set()
        for export_line in resolution['exports']:
            match = re.search(r'export\s+(?:\*\s+as\s+(\w+)|\{\s*\w+\s+as\s+(\w+)\s*\})', export_line)
            if match:
                export_name = match.group(1) or match.group(2)
                if export_name in export_names:
                    errors.append(f"Duplicate export name in resolution: {export_name}")
                export_names.add(export_name)
        
        return {
            'is_valid': len(errors) == 0,
            'warnings': warnings,
            'errors': errors
        }
    
    def _extract_export_name(self, export_info: Any) -> Optional[str]:
        """
        Extract export name from export info object.
        
        Args:
            export_info: Export information object or string
            
        Returns:
            Export name if found, None otherwise
        """
        if isinstance(export_info, str):
            return export_info
        elif hasattr(export_info, 'name'):
            return export_info.name
        elif hasattr(export_info, 'export_name'):
            return export_info.export_name
        elif isinstance(export_info, dict):
            return export_info.get('name') or export_info.get('export_name')
        return None