"""
Export Strategy Module
Handles special cases and validation for different directory types
"""

from typing import Dict, List, Any, Optional
import os


class ExportStrategy:
    """
    Determines export strategies for different directory types to avoid naming conflicts.
    """
    
    def __init__(self):
        # Special directory configurations
        self.special_directories = {
            'types': {
                'use_namespaced': False,
                'reason': 'Types directories must use barrel exports for existing import compatibility'
            },
            'components': {
                'use_namespaced': False,
                'reason': 'Component directories typically use barrel exports'
            }
        }
        
        # Conflict threshold settings
        self.conflict_thresholds = {
            'subdirectory_count': 10,
            'export_count': 50
        }
    
    def determine_strategy(self, dir_path: str, subdirs: List[str], exports: List[Any]) -> Dict[str, Any]:
        """
        Determine export strategy for a directory.
        
        Args:
            dir_path: Directory path
            subdirs: List of subdirectories
            exports: List of file exports
            
        Returns:
            Strategy object with decision and reasoning
        """
        analysis = self.analyze_directory(dir_path, subdirs, exports)
        
        # Check special directory rules first
        special_rule = self.get_special_directory_rule(dir_path)
        if special_rule:
            return {
                'use_namespaced': special_rule['use_namespaced'],
                'reason': special_rule['reason'],
                'analysis': analysis
            }
        
        # Apply general conflict detection rules
        conflict_analysis = self.analyze_conflict_potential(dir_path, subdirs, exports)
        
        return {
            'use_namespaced': conflict_analysis['has_high_conflict'],
            'reason': conflict_analysis['reason'],
            'analysis': analysis
        }
    
    def analyze_directory(self, dir_path: str, subdirs: List[str], exports: List[Any]) -> Dict[str, Any]:
        """
        Analyze directory characteristics.
        
        Args:
            dir_path: Directory path
            subdirs: List of subdirectories
            exports: List of exports
            
        Returns:
            Analysis dictionary
        """
        is_root_src = dir_path.endswith('/src') or dir_path.endswith('\\src')
        path_segments = dir_path.replace('\\', '/').split('/')
        directory_name = path_segments[-1] if path_segments else ''
        
        return {
            'is_root_src': is_root_src,
            'directory_name': directory_name,
            'path_segments': path_segments,
            'subdirectory_count': len(subdirs),
            'export_count': len(exports),
            'depth': len(path_segments)
        }
    
    def get_special_directory_rule(self, dir_path: str) -> Optional[Dict[str, Any]]:
        """
        Check for special directory rules.
        
        Args:
            dir_path: Directory path
            
        Returns:
            Special rule configuration or None
        """
        normalized_path = dir_path.replace('\\', '/')
        
        # Types directories - never use namespaced exports
        if '/types' in normalized_path:
            return self.special_directories['types']
        
        # Add other special cases here
        # if '/components' in normalized_path:
        #     return self.special_directories['components']
        
        return None
    
    def analyze_conflict_potential(self, dir_path: str, subdirs: List[str], exports: List[Any]) -> Dict[str, Any]:
        """
        Analyze conflict potential using heuristics.
        
        Args:
            dir_path: Directory path
            subdirs: List of subdirectories
            exports: List of exports
            
        Returns:
            Conflict analysis with decision and reasoning
        """
        analysis = self.analyze_directory(dir_path, subdirs, exports)
        reasons = []
        has_high_conflict = False
        
        # Root src directory typically has many modules
        if analysis['is_root_src']:
            has_high_conflict = True
            reasons.append('Root src directory with multiple modules')
        
        # Many subdirectories indicate potential naming conflicts
        if len(subdirs) > self.conflict_thresholds['subdirectory_count']:
            has_high_conflict = True
            reasons.append(f"{len(subdirs)} subdirectories exceeds threshold of {self.conflict_thresholds['subdirectory_count']}")
        
        # Many exports indicate potential conflicts
        if len(exports) > self.conflict_thresholds['export_count']:
            has_high_conflict = True
            reasons.append(f"{len(exports)} exports exceeds threshold of {self.conflict_thresholds['export_count']}")
        
        return {
            'has_high_conflict': has_high_conflict,
            'reason': ('High conflict potential: ' + ', '.join(reasons)) if has_high_conflict 
                     else 'Low conflict potential - using barrel exports'
        }
    
    def validate_strategy(self, dir_path: str, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate export strategy decision.
        
        Args:
            dir_path: Directory path
            strategy: Strategy object to validate
            
        Returns:
            Validation result with warnings and errors
        """
        warnings = []
        errors = []
        
        # Validate types directory usage
        if '/types' in dir_path and strategy['use_namespaced']:
            errors.append('Types directories should not use namespaced exports - breaks existing imports')
        
        # Validate root directory usage
        analysis = strategy.get('analysis', {})
        if (analysis.get('is_root_src') and 
            not strategy['use_namespaced'] and 
            analysis.get('subdirectory_count', 0) > 5):
            warnings.append('Root src directory with many modules might benefit from namespaced exports')
        
        return {
            'is_valid': len(errors) == 0,
            'warnings': warnings,
            'errors': errors
        }
    
    def explain_strategy(self, strategy: Dict[str, Any]) -> str:
        """
        Get human-readable strategy explanation.
        
        Args:
            strategy: Strategy object
            
        Returns:
            Human-readable explanation string
        """
        export_type = 'namespaced exports' if strategy['use_namespaced'] else 'barrel exports'
        return f"Using {export_type}: {strategy['reason']}"