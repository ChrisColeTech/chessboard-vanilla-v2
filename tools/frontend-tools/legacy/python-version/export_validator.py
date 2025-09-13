"""
Export Cross-Reference Validator Module
Validates that barrel exports match actual source file exports
"""

import os
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from ast_parser import TypeScriptASTParser, ExportInfo


@dataclass
class ValidationIssue:
    """Represents an export validation issue"""
    severity: str  # 'ERROR', 'WARNING', 'INFO'
    type: str  # 'missing_export', 'phantom_export', 'type_mismatch', 'conflict'
    file_path: str
    export_name: str
    description: str
    suggested_fix: Optional[str] = None


@dataclass
class ExportMapping:
    """Maps exports between source files and barrel files"""
    source_file: str
    barrel_file: str
    export_name: str
    source_export: Optional[ExportInfo]
    barrel_export: Optional[ExportInfo]
    is_valid: bool
    issues: List[ValidationIssue]


class ExportCrossReferenceValidator:
    """
    Validates export consistency between source files and generated barrel files
    """
    
    def __init__(self):
        self.ast_parser = TypeScriptASTParser()
        self.validation_issues = []
    
    def validate_barrel_file(self, barrel_path: str, source_dir: str) -> Dict[str, Any]:
        """
        Validate a barrel file against its source directory
        
        Args:
            barrel_path: Path to the barrel index.ts file
            source_dir: Directory containing source files
            
        Returns:
            Comprehensive validation report
        """
        self.validation_issues = []
        
        # Parse barrel file exports
        barrel_exports = self.ast_parser.parse_file(barrel_path)
        
        # Get all source files in directory
        source_files = self._get_source_files(source_dir)
        
        # Create export mappings
        mappings = self._create_export_mappings(barrel_exports, source_files, source_dir)
        
        # Validate mappings
        validation_results = self._validate_mappings(mappings)
        
        # Check for missing exports
        missing_exports = self._find_missing_exports(source_files, barrel_exports)
        
        # Check for phantom exports
        phantom_exports = self._find_phantom_exports(barrel_exports, source_files, source_dir)
        
        return {
            'barrel_path': barrel_path,
            'source_dir': source_dir,
            'total_barrel_exports': len(barrel_exports),
            'total_source_files': len(source_files),
            'mappings': mappings,
            'validation_results': validation_results,
            'missing_exports': missing_exports,
            'phantom_exports': phantom_exports,
            'issues': self.validation_issues,
            'is_valid': len([i for i in self.validation_issues if i.severity == 'ERROR']) == 0
        }
    
    def validate_directory_recursively(self, root_dir: str) -> Dict[str, Any]:
        """
        Validate all barrel files in a directory tree
        
        Args:
            root_dir: Root directory to validate
            
        Returns:
            Comprehensive validation report for entire directory tree
        """
        all_reports = []
        total_issues = []
        
        for root, dirs, files in os.walk(root_dir):
            if 'index.ts' in files:
                barrel_path = os.path.join(root, 'index.ts')
                
                # Skip if barrel file is not auto-generated
                if not self._is_auto_generated_barrel(barrel_path):
                    continue
                
                report = self.validate_barrel_file(barrel_path, root)
                all_reports.append(report)
                total_issues.extend(report['issues'])
        
        return {
            'root_dir': root_dir,
            'barrel_reports': all_reports,
            'total_barrels_validated': len(all_reports),
            'total_issues': len(total_issues),
            'error_count': len([i for i in total_issues if i.severity == 'ERROR']),
            'warning_count': len([i for i in total_issues if i.severity == 'WARNING']),
            'all_issues': total_issues,
            'is_valid': len([i for i in total_issues if i.severity == 'ERROR']) == 0
        }
    
    def _get_source_files(self, source_dir: str) -> List[str]:
        """Get all TypeScript/JavaScript source files in directory"""
        source_files = []
        
        for file in os.listdir(source_dir):
            if file == 'index.ts':
                continue  # Skip barrel files
            
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path) and file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                # Skip test files and other excluded patterns
                if not self._should_exclude_file(file):
                    source_files.append(file_path)
        
        return source_files
    
    def _should_exclude_file(self, filename: str) -> bool:
        """Check if file should be excluded from validation"""
        exclude_patterns = [
            r'\.test\.',
            r'\.spec\.',
            r'\.d\.ts$',
            r'\.stories\.',
            r'\.config\.'
        ]
        
        import re
        for pattern in exclude_patterns:
            if re.search(pattern, filename):
                return True
        
        return False
    
    def _create_export_mappings(self, barrel_exports: List[ExportInfo], 
                              source_files: List[str], source_dir: str) -> List[ExportMapping]:
        """Create mappings between barrel exports and source exports"""
        mappings = []
        
        # Parse all source files
        source_exports_by_file = {}
        for source_file in source_files:
            source_exports_by_file[source_file] = self.ast_parser.parse_file(source_file)
        
        # Map each barrel export to its source
        for barrel_export in barrel_exports:
            if barrel_export.is_re_export and barrel_export.re_export_from:
                # Handle re-exports
                source_file_path = self._resolve_import_path(barrel_export.re_export_from, source_dir)
                source_export = self._find_matching_source_export(
                    barrel_export, source_exports_by_file.get(source_file_path, [])
                )
            else:
                # Find source file containing this export
                source_file_path, source_export = self._find_source_of_export(
                    barrel_export, source_exports_by_file
                )
            
            mapping = ExportMapping(
                source_file=source_file_path or "UNKNOWN",
                barrel_file=os.path.join(source_dir, 'index.ts'),
                export_name=barrel_export.name,
                source_export=source_export,
                barrel_export=barrel_export,
                is_valid=source_export is not None,
                issues=[]
            )
            
            if not mapping.is_valid:
                issue = ValidationIssue(
                    severity='ERROR',
                    type='phantom_export',
                    file_path=mapping.barrel_file,
                    export_name=barrel_export.name,
                    description=f"Barrel exports '{barrel_export.name}' but no source file contains this export",
                    suggested_fix=f"Remove export or create source export in appropriate file"
                )
                mapping.issues.append(issue)
                self.validation_issues.append(issue)
            
            mappings.append(mapping)
        
        return mappings
    
    def _find_source_of_export(self, barrel_export: ExportInfo, 
                             source_exports_by_file: Dict[str, List[ExportInfo]]) -> Tuple[Optional[str], Optional[ExportInfo]]:
        """Find which source file contains a specific export"""
        
        for source_file, source_exports in source_exports_by_file.items():
            matching_export = self._find_matching_source_export(barrel_export, source_exports)
            if matching_export:
                return source_file, matching_export
        
        return None, None
    
    def _find_matching_source_export(self, barrel_export: ExportInfo, 
                                   source_exports: List[ExportInfo]) -> Optional[ExportInfo]:
        """Find matching export in source file"""
        
        for source_export in source_exports:
            if (source_export.name == barrel_export.name and
                source_export.is_default == barrel_export.is_default and
                source_export.is_type_only == barrel_export.is_type_only):
                return source_export
        
        return None
    
    def _resolve_import_path(self, import_path: str, base_dir: str) -> Optional[str]:
        """Resolve relative import path to absolute file path"""
        
        if import_path.startswith('./'):
            # Relative import
            relative_path = import_path[2:]
            
            # Try common extensions
            for ext in ['.ts', '.tsx', '.js', '.jsx']:
                full_path = os.path.join(base_dir, relative_path + ext)
                if os.path.exists(full_path):
                    return full_path
            
            # Try index files
            index_path = os.path.join(base_dir, relative_path, 'index.ts')
            if os.path.exists(index_path):
                return index_path
        
        return None
    
    def _validate_mappings(self, mappings: List[ExportMapping]) -> Dict[str, Any]:
        """Validate all export mappings"""
        
        valid_mappings = [m for m in mappings if m.is_valid]
        invalid_mappings = [m for m in mappings if not m.is_valid]
        
        # Check for type mismatches
        type_mismatches = []
        for mapping in valid_mappings:
            if mapping.source_export and mapping.barrel_export:
                if mapping.source_export.is_type_only != mapping.barrel_export.is_type_only:
                    issue = ValidationIssue(
                        severity='WARNING',
                        type='type_mismatch',
                        file_path=mapping.barrel_file,
                        export_name=mapping.export_name,
                        description=f"Type mismatch for '{mapping.export_name}': source is {'type-only' if mapping.source_export.is_type_only else 'value'}, barrel treats as {'type-only' if mapping.barrel_export.is_type_only else 'value'}",
                        suggested_fix="Adjust barrel export to match source export type"
                    )
                    mapping.issues.append(issue)
                    type_mismatches.append(issue)
                    self.validation_issues.append(issue)
        
        return {
            'total_mappings': len(mappings),
            'valid_mappings': len(valid_mappings),
            'invalid_mappings': len(invalid_mappings),
            'type_mismatches': len(type_mismatches),
            'validation_success_rate': len(valid_mappings) / len(mappings) if mappings else 0
        }
    
    def _find_missing_exports(self, source_files: List[str], barrel_exports: List[ExportInfo]) -> List[ValidationIssue]:
        """Find exports that exist in source files but are missing from barrel"""
        
        missing_exports = []
        barrel_export_names = {e.name for e in barrel_exports}
        
        for source_file in source_files:
            source_exports = self.ast_parser.parse_file(source_file)
            
            for source_export in source_exports:
                if source_export.name not in barrel_export_names:
                    issue = ValidationIssue(
                        severity='WARNING',
                        type='missing_export',
                        file_path=source_file,
                        export_name=source_export.name,
                        description=f"Export '{source_export.name}' exists in source but missing from barrel",
                        suggested_fix=f"Add export to barrel file or verify if export should be public"
                    )
                    missing_exports.append(issue)
        
        self.validation_issues.extend(missing_exports)
        return missing_exports
    
    def _find_phantom_exports(self, barrel_exports: List[ExportInfo], 
                           source_files: List[str], source_dir: str) -> List[ValidationIssue]:
        """Find exports that exist in barrel but not in any source file"""
        
        phantom_exports = []
        
        # Collect all source export names
        all_source_exports = set()
        for source_file in source_files:
            source_exports = self.ast_parser.parse_file(source_file)
            for export in source_exports:
                all_source_exports.add(export.name)
        
        # Find barrel exports that don't exist in source
        for barrel_export in barrel_exports:
            if barrel_export.name not in all_source_exports:
                # Check if it's a re-export that might be valid
                if barrel_export.is_re_export and barrel_export.re_export_from:
                    resolved_path = self._resolve_import_path(barrel_export.re_export_from, source_dir)
                    if not resolved_path or not os.path.exists(resolved_path):
                        issue = ValidationIssue(
                            severity='ERROR',
                            type='phantom_export',
                            file_path=os.path.join(source_dir, 'index.ts'),
                            export_name=barrel_export.name,
                            description=f"Re-export '{barrel_export.name}' from '{barrel_export.re_export_from}' but source file not found",
                            suggested_fix="Fix import path or remove re-export"
                        )
                        phantom_exports.append(issue)
                else:
                    issue = ValidationIssue(
                        severity='ERROR',
                        type='phantom_export',
                        file_path=os.path.join(source_dir, 'index.ts'),
                        export_name=barrel_export.name,
                        description=f"Barrel exports '{barrel_export.name}' but no source file contains this export",
                        suggested_fix="Remove phantom export or add to appropriate source file"
                    )
                    phantom_exports.append(issue)
        
        self.validation_issues.extend(phantom_exports)
        return phantom_exports
    
    def _is_auto_generated_barrel(self, barrel_path: str) -> bool:
        """Check if barrel file is auto-generated"""
        try:
            with open(barrel_path, 'r', encoding='utf-8') as f:
                first_few_lines = f.read(200)
                return 'Auto-generated' in first_few_lines
        except:
            return False
    
    def generate_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate human-readable validation report"""
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("EXPORT VALIDATION REPORT")
        report_lines.append("=" * 60)
        
        if 'barrel_reports' in validation_result:
            # Directory-wide report
            report_lines.append(f"Root Directory: {validation_result['root_dir']}")
            report_lines.append(f"Barrels Validated: {validation_result['total_barrels_validated']}")
            report_lines.append(f"Total Issues: {validation_result['total_issues']}")
            report_lines.append(f"Errors: {validation_result['error_count']}")
            report_lines.append(f"Warnings: {validation_result['warning_count']}")
            report_lines.append(f"Overall Status: {'✅ VALID' if validation_result['is_valid'] else '❌ INVALID'}")
            
            # Individual barrel reports
            for barrel_report in validation_result['barrel_reports']:
                if barrel_report['issues']:
                    report_lines.append(f"\n📁 {barrel_report['barrel_path']}:")
                    for issue in barrel_report['issues']:
                        icon = "❌" if issue.severity == 'ERROR' else "⚠️" if issue.severity == 'WARNING' else "ℹ️"
                        report_lines.append(f"  {icon} {issue.description}")
                        if issue.suggested_fix:
                            report_lines.append(f"      💡 {issue.suggested_fix}")
        else:
            # Single barrel report
            report_lines.append(f"Barrel File: {validation_result['barrel_path']}")
            report_lines.append(f"Source Directory: {validation_result['source_dir']}")
            report_lines.append(f"Total Issues: {len(validation_result['issues'])}")
            report_lines.append(f"Status: {'✅ VALID' if validation_result['is_valid'] else '❌ INVALID'}")
            
            for issue in validation_result['issues']:
                icon = "❌" if issue.severity == 'ERROR' else "⚠️" if issue.severity == 'WARNING' else "ℹ️"
                report_lines.append(f"{icon} {issue.description}")
                if issue.suggested_fix:
                    report_lines.append(f"   💡 {issue.suggested_fix}")
        
        return "\n".join(report_lines)