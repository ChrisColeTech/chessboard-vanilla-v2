"""
Conflict Detection Engine Module
Advanced conflict detection and resolution with precise mapping
"""

import os
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
from ast_parser import TypeScriptASTParser, ExportInfo


@dataclass
class ExportConflict:
    """Represents a detailed export conflict"""
    export_name: str
    conflicting_sources: List[Tuple[str, ExportInfo]]  # (file_path, export_info)
    conflict_type: str  # 'name_collision', 'type_mismatch', 'default_collision'
    severity: str  # 'HIGH', 'MEDIUM', 'LOW'
    resolution_strategy: Optional[str] = None
    suggested_aliases: Optional[List[str]] = None


@dataclass
class ConflictResolution:
    """Represents a conflict resolution strategy"""
    strategy_type: str  # 'explicit_alias', 'namespace', 'skip', 'merge'
    exports: List[str]
    explanation: str
    conflicts_resolved: int
    remaining_conflicts: List[ExportConflict]
    success_rate: float


class ConflictDetectionEngine:
    """
    Advanced conflict detection engine with precise mapping and intelligent resolution
    """
    
    def __init__(self):
        self.ast_parser = TypeScriptASTParser()
        self.resolution_strategies = {
            'explicit_alias': self._resolve_with_explicit_aliases,
            'namespace': self._resolve_with_namespaces,
            'smart_merge': self._resolve_with_smart_merge,
            'skip_conflicts': self._resolve_by_skipping
        }
    
    def analyze_directory_conflicts(self, dir_path: str, subdirs: List[str], 
                                  file_exports: List[ExportInfo]) -> Dict[str, Any]:
        """
        Comprehensive conflict analysis for a directory
        
        Args:
            dir_path: Directory path
            subdirs: List of subdirectories
            file_exports: Exports from files in current directory
            
        Returns:
            Detailed conflict analysis
        """
        
        # Collect all exports with their sources
        all_exports = self._collect_all_exports(dir_path, subdirs, file_exports)
        
        # Detect conflicts
        conflicts = self._detect_conflicts(all_exports)
        
        # Analyze conflict patterns
        conflict_analysis = self._analyze_conflict_patterns(conflicts)
        
        # Recommend resolution strategy
        recommended_strategy = self._recommend_resolution_strategy(conflicts, conflict_analysis)
        
        return {
            'directory': dir_path,
            'total_exports': len(all_exports),
            'total_conflicts': len(conflicts),
            'conflicts': conflicts,
            'conflict_analysis': conflict_analysis,
            'recommended_strategy': recommended_strategy,
            'has_conflicts': len(conflicts) > 0
        }
    
    def resolve_conflicts(self, conflict_analysis: Dict[str, Any], 
                         subdirs: List[str]) -> ConflictResolution:
        """
        Resolve conflicts using the most appropriate strategy
        
        Args:
            conflict_analysis: Result from analyze_directory_conflicts
            subdirs: List of subdirectories
            
        Returns:
            Conflict resolution with generated exports
        """
        
        conflicts = conflict_analysis['conflicts']
        strategy_type = conflict_analysis['recommended_strategy']
        
        if strategy_type in self.resolution_strategies:
            resolution_func = self.resolution_strategies[strategy_type]
            return resolution_func(conflicts, subdirs, conflict_analysis['directory'])
        else:
            # Fallback to explicit aliases
            return self._resolve_with_explicit_aliases(conflicts, subdirs, conflict_analysis['directory'])
    
    def _collect_all_exports(self, dir_path: str, subdirs: List[str], 
                           file_exports: List[ExportInfo]) -> Dict[str, List[Tuple[str, ExportInfo]]]:
        """Collect all exports with their source files"""
        
        all_exports = defaultdict(list)
        
        # Add file exports from current directory
        for export in file_exports:
            all_exports[export.name].append(('current_directory', export))
        
        # Add exports from subdirectories
        for subdir in subdirs:
            subdir_path = os.path.join(dir_path, subdir)
            index_path = os.path.join(subdir_path, 'index.ts')
            
            if os.path.exists(index_path):
                subdir_exports = self.ast_parser.parse_file(index_path)
                
                for export in subdir_exports:
                    # For re-exports, we need to trace back to the original source
                    if export.is_re_export and not export.re_export_from:
                        # This is an `export * from './module'` - we need to expand it
                        expanded_exports = self._expand_star_exports(index_path, subdir_path)
                        for expanded_export in expanded_exports:
                            all_exports[expanded_export.name].append((subdir, expanded_export))
                    else:
                        all_exports[export.name].append((subdir, export))
        
        return all_exports
    
    def _expand_star_exports(self, barrel_file: str, barrel_dir: str) -> List[ExportInfo]:
        """Expand `export * from './module'` statements to individual exports"""
        
        expanded_exports = []
        
        try:
            with open(barrel_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all `export * from` statements
            import re
            star_export_pattern = re.compile(r'export\s*\*\s*from\s+[\'"]([^\'"]+)[\'"]')
            
            for match in star_export_pattern.finditer(content):
                module_path = match.group(1)
                resolved_path = self._resolve_module_path(module_path, barrel_dir)
                
                if resolved_path and os.path.exists(resolved_path):
                    module_exports = self.ast_parser.parse_file(resolved_path)
                    expanded_exports.extend(module_exports)
        
        except Exception as e:
            print(f"Error expanding star exports from {barrel_file}: {e}")
        
        return expanded_exports
    
    def _resolve_module_path(self, module_path: str, base_dir: str) -> Optional[str]:
        """Resolve module path to absolute file path"""
        
        if module_path.startswith('./'):
            relative_path = module_path[2:]
            
            # Try different file extensions
            for ext in ['.ts', '.tsx', '.js', '.jsx']:
                full_path = os.path.join(base_dir, relative_path + ext)
                if os.path.exists(full_path):
                    return full_path
            
            # Try index file
            index_path = os.path.join(base_dir, relative_path, 'index.ts')
            if os.path.exists(index_path):
                return index_path
        
        return None
    
    def _detect_conflicts(self, all_exports: Dict[str, List[Tuple[str, ExportInfo]]]) -> List[ExportConflict]:
        """Detect conflicts from collected exports"""
        
        conflicts = []
        
        for export_name, sources in all_exports.items():
            if len(sources) > 1:
                # Determine conflict type and severity
                conflict_type = self._determine_conflict_type(sources)
                severity = self._assess_conflict_severity(export_name, sources, conflict_type)
                
                conflict = ExportConflict(
                    export_name=export_name,
                    conflicting_sources=sources,
                    conflict_type=conflict_type,
                    severity=severity,
                    suggested_aliases=self._generate_suggested_aliases(export_name, sources)
                )
                
                conflicts.append(conflict)
        
        return conflicts
    
    def _determine_conflict_type(self, sources: List[Tuple[str, ExportInfo]]) -> str:
        """Determine the type of conflict"""
        
        export_types = [export.is_type_only for _, export in sources]
        default_types = [export.is_default for _, export in sources]
        
        if any(default_types):
            return 'default_collision'
        elif len(set(export_types)) > 1:
            return 'type_mismatch'
        else:
            return 'name_collision'
    
    def _assess_conflict_severity(self, export_name: str, sources: List[Tuple[str, ExportInfo]], 
                                conflict_type: str) -> str:
        """Assess conflict severity"""
        
        # High severity criteria
        common_names = ['User', 'Config', 'Props', 'State', 'Error', 'Response']
        if any(name in export_name for name in common_names):
            return 'HIGH'
        
        if conflict_type == 'default_collision':
            return 'HIGH'
        
        if len(sources) > 3:
            return 'HIGH'
        
        # Medium severity for type mismatches
        if conflict_type == 'type_mismatch':
            return 'MEDIUM'
        
        return 'LOW'
    
    def _generate_suggested_aliases(self, export_name: str, 
                                  sources: List[Tuple[str, ExportInfo]]) -> List[str]:
        """Generate suggested alias names for conflicts"""
        
        aliases = []
        
        for source_name, export_info in sources:
            if source_name == 'current_directory':
                continue
            
            # Generate meaningful alias
            alias = self._create_alias(export_name, source_name)
            aliases.append(alias)
        
        return aliases
    
    def _create_alias(self, export_name: str, module_name: str) -> str:
        """Create a meaningful alias name"""
        
        # Convert module name to PascalCase
        module_parts = module_name.replace('-', '_').replace('.', '_').split('_')
        module_prefix = ''.join(part.capitalize() for part in module_parts if part)
        
        # Handle different alias strategies
        if export_name.lower() in module_name.lower():
            return module_prefix + export_name.capitalize()
        elif any(prefix in export_name.lower() for prefix in ['use', 'create', 'get']):
            # Fix regex syntax for Python
            import re
            parts = re.split(r'(?=[A-Z])', export_name, 1)
            if len(parts) >= 2:
                return module_prefix + parts[0] + ''.join(parts[1:])
            else:
                return module_prefix + export_name
        else:
            return module_prefix + export_name
    
    def _analyze_conflict_patterns(self, conflicts: List[ExportConflict]) -> Dict[str, Any]:
        """Analyze patterns in conflicts to recommend strategy"""
        
        if not conflicts:
            return {
                'total_conflicts': 0,
                'high_severity_count': 0,
                'medium_severity_count': 0,
                'low_severity_count': 0,
                'conflict_types': {},
                'most_common_names': []
            }
        
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        conflict_type_counts = defaultdict(int)
        export_name_frequency = defaultdict(int)
        
        for conflict in conflicts:
            severity_counts[conflict.severity] += 1
            conflict_type_counts[conflict.conflict_type] += 1
            export_name_frequency[conflict.export_name] += 1
        
        most_common_names = sorted(export_name_frequency.items(), 
                                 key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_conflicts': len(conflicts),
            'high_severity_count': severity_counts['HIGH'],
            'medium_severity_count': severity_counts['MEDIUM'],
            'low_severity_count': severity_counts['LOW'],
            'conflict_types': dict(conflict_type_counts),
            'most_common_names': most_common_names,
            'average_sources_per_conflict': sum(len(c.conflicting_sources) for c in conflicts) / len(conflicts)
        }
    
    def _recommend_resolution_strategy(self, conflicts: List[ExportConflict], 
                                     analysis: Dict[str, Any]) -> str:
        """Recommend the best resolution strategy based on conflict analysis"""
        
        if not conflicts:
            return 'no_conflicts'
        
        high_severity = analysis['high_severity_count']
        total_conflicts = analysis['total_conflicts']
        avg_sources = analysis['average_sources_per_conflict']
        
        # Strategy decision tree
        if total_conflicts > 10:
            return 'namespace'  # Too many conflicts, use namespaces
        elif high_severity > 5:
            return 'explicit_alias'  # Many serious conflicts need careful handling
        elif avg_sources > 3:
            return 'smart_merge'  # Complex conflicts with many sources
        elif analysis['conflict_types'].get('type_mismatch', 0) > 0:
            return 'explicit_alias'  # Type mismatches need explicit handling
        else:
            return 'explicit_alias'  # Default to most precise strategy
    
    def _resolve_with_explicit_aliases(self, conflicts: List[ExportConflict], 
                                     subdirs: List[str], dir_path: str) -> ConflictResolution:
        """Resolve conflicts with explicit aliases"""
        
        exports = []
        resolved_conflicts = []
        conflicting_modules = set()
        
        # Collect all conflicting modules
        for conflict in conflicts:
            for source_name, _ in conflict.conflicting_sources:
                if source_name != 'current_directory':
                    conflicting_modules.add(source_name)
        
        # Add non-conflicting subdirectories as barrel exports
        for subdir in subdirs:
            if subdir not in conflicting_modules:
                exports.append(f"export * from './{subdir}';")
        
        # Add explicit aliases for conflicts
        for conflict in conflicts:
            aliases_added = []
            
            for source_name, export_info in conflict.conflicting_sources:
                if source_name != 'current_directory':
                    if conflict.suggested_aliases:
                        alias_idx = [s for s, _ in conflict.conflicting_sources if s != 'current_directory'].index(source_name)
                        if alias_idx < len(conflict.suggested_aliases):
                            alias = conflict.suggested_aliases[alias_idx]
                            
                            export_stmt = f"export type {{ {conflict.export_name} as {alias} }} from './{source_name}';" if export_info.is_type_only else f"export {{ {conflict.export_name} as {alias} }} from './{source_name}';"
                            exports.append(export_stmt)
                            aliases_added.append(alias)
            
            if aliases_added:
                resolved_conflicts.append(conflict)
        
        remaining_conflicts = [c for c in conflicts if c not in resolved_conflicts]
        success_rate = len(resolved_conflicts) / len(conflicts) if conflicts else 1.0
        
        return ConflictResolution(
            strategy_type='explicit_alias',
            exports=exports,
            explanation=f'Using explicit aliases to resolve {len(resolved_conflicts)} conflicts while preserving {len(subdirs) - len(conflicting_modules)} barrel exports',
            conflicts_resolved=len(resolved_conflicts),
            remaining_conflicts=remaining_conflicts,
            success_rate=success_rate
        )
    
    def _resolve_with_namespaces(self, conflicts: List[ExportConflict], 
                               subdirs: List[str], dir_path: str) -> ConflictResolution:
        """Resolve conflicts using namespace exports"""
        
        imports_re = re  # Ensure re is available
        exports = []
        
        for subdir in subdirs:
            # Convert to valid JavaScript identifier
            valid_identifier = imports_re.sub(r'[^a-zA-Z0-9_]', '', 
                                    ''.join(part.capitalize() for part in subdir.split('-')))
            
            if valid_identifier and valid_identifier[0].isalpha():
                exports.append(f"export * as {valid_identifier} from './{subdir}';")
            else:
                # Fallback for invalid identifiers
                exports.append(f"export * as {subdir.replace('-', '_')} from './{subdir}';")
        
        return ConflictResolution(
            strategy_type='namespace',
            exports=exports,
            explanation=f'Using namespaced exports to completely avoid all {len(conflicts)} conflicts',
            conflicts_resolved=len(conflicts),
            remaining_conflicts=[],
            success_rate=1.0
        )
    
    def _resolve_with_smart_merge(self, conflicts: List[ExportConflict], 
                                subdirs: List[str], dir_path: str) -> ConflictResolution:
        """Intelligent merge strategy combining different approaches"""
        
        # For now, delegate to explicit aliases (can be enhanced later)
        return self._resolve_with_explicit_aliases(conflicts, subdirs, dir_path)
    
    def _resolve_by_skipping(self, conflicts: List[ExportConflict], 
                           subdirs: List[str], dir_path: str) -> ConflictResolution:
        """Resolve by skipping conflicting modules entirely"""
        
        exports = []
        conflicting_modules = set()
        
        # Identify all conflicting modules
        for conflict in conflicts:
            for source_name, _ in conflict.conflicting_sources:
                if source_name != 'current_directory':
                    conflicting_modules.add(source_name)
        
        # Export only non-conflicting modules
        for subdir in subdirs:
            if subdir not in conflicting_modules:
                exports.append(f"export * from './{subdir}';")
        
        return ConflictResolution(
            strategy_type='skip_conflicts',
            exports=exports,
            explanation=f'Skipping {len(conflicting_modules)} conflicting modules to avoid all conflicts',
            conflicts_resolved=0,  # Conflicts avoided, not resolved
            remaining_conflicts=conflicts,  # All conflicts remain but are avoided
            success_rate=0.0  # No conflicts actually resolved
        )