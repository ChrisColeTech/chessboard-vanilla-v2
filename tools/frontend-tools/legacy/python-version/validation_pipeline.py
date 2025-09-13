"""
Pre/Post Generation Validation Pipeline
Orchestrates validation modules to ensure barrel file quality and correctness
"""

import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from ast_parser import TypeScriptASTParser, ExportInfo
from export_validator import ExportCrossReferenceValidator
from conflict_engine import ConflictDetectionEngine
from typescript_compliance import TypeScriptComplianceHandler


@dataclass
class ValidationResult:
    """Comprehensive validation result"""
    directory: str
    is_valid: bool
    pre_gen_issues: List[Dict[str, Any]]
    post_gen_issues: List[Dict[str, Any]]
    conflict_analysis: Dict[str, Any]
    compliance_report: Dict[str, Any]
    recommendations: List[str]
    success_rate: float


@dataclass
class PipelineConfig:
    """Configuration for validation pipeline"""
    enable_pre_generation: bool = True
    enable_post_generation: bool = True
    enable_conflict_detection: bool = True
    enable_compliance_check: bool = True
    strict_mode: bool = False
    auto_fix_issues: bool = False


class ValidationPipeline:
    """
    Comprehensive validation pipeline that orchestrates all validation modules
    to ensure barrel file quality before and after generation
    """
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        
        # Initialize validation modules
        self.ast_parser = TypeScriptASTParser()
        self.export_validator = ExportCrossReferenceValidator()
        self.conflict_engine = ConflictDetectionEngine()
        self.compliance_handler = TypeScriptComplianceHandler()
        
    def validate_directory_pre_generation(self, dir_path: str) -> Dict[str, Any]:
        """
        Run pre-generation validation to identify potential issues
        
        Args:
            dir_path: Directory to validate
            
        Returns:
            Pre-generation validation results
        """
        if not self.config.enable_pre_generation:
            return {'enabled': False, 'issues': []}
        
        issues = []
        
        # Check for source file accessibility
        source_files = self._get_source_files(dir_path)
        for source_file in source_files:
            if not os.access(source_file, os.R_OK):
                issues.append({
                    'type': 'accessibility',
                    'severity': 'HIGH',
                    'file': source_file,
                    'description': f'Source file is not readable: {source_file}'
                })
        
        # Validate source file exports
        for source_file in source_files:
            try:
                exports = self.ast_parser.parse_file(source_file)
                if not exports:
                    issues.append({
                        'type': 'no_exports',
                        'severity': 'MEDIUM',
                        'file': source_file,
                        'description': f'Source file has no exports: {source_file}'
                    })
            except Exception as e:
                issues.append({
                    'type': 'parse_error',
                    'severity': 'HIGH',
                    'file': source_file,
                    'description': f'Failed to parse source file: {e}'
                })
        
        # Check for potential naming conflicts
        subdirs = [d for d in os.listdir(dir_path) 
                  if os.path.isdir(os.path.join(dir_path, d)) and not d.startswith('.')]
        
        if subdirs:
            file_exports = []
            for source_file in source_files:
                try:
                    exports = self.ast_parser.parse_file(source_file)
                    file_exports.extend(exports)
                except:
                    continue
            
            conflict_analysis = self.conflict_engine.analyze_directory_conflicts(
                dir_path, subdirs, file_exports
            )
            
            if conflict_analysis['has_conflicts']:
                issues.append({
                    'type': 'potential_conflicts',
                    'severity': 'MEDIUM',
                    'file': dir_path,
                    'description': f'Detected {conflict_analysis["total_conflicts"]} potential conflicts',
                    'details': conflict_analysis
                })
        
        return {
            'enabled': True,
            'directory': dir_path,
            'total_source_files': len(source_files),
            'issues': issues,
            'is_valid': len([i for i in issues if i['severity'] == 'HIGH']) == 0
        }
    
    def validate_barrel_post_generation(self, barrel_path: str, source_dir: str) -> Dict[str, Any]:
        """
        Run post-generation validation to verify barrel file correctness
        
        Args:
            barrel_path: Path to generated barrel file
            source_dir: Source directory
            
        Returns:
            Post-generation validation results
        """
        if not self.config.enable_post_generation:
            return {'enabled': False, 'issues': []}
        
        issues = []
        
        # Validate barrel file existence and readability
        if not os.path.exists(barrel_path):
            issues.append({
                'type': 'missing_barrel',
                'severity': 'HIGH',
                'file': barrel_path,
                'description': 'Barrel file was not generated'
            })
            return {
                'enabled': True,
                'barrel_path': barrel_path,
                'issues': issues,
                'is_valid': False
            }
        
        # Cross-reference validation
        try:
            validation_report = self.export_validator.validate_barrel_file(barrel_path, source_dir)
            
            # Extract high-severity issues
            for issue in validation_report['issues']:
                if issue.severity == 'ERROR':
                    issues.append({
                        'type': issue.type,
                        'severity': 'HIGH',
                        'file': issue.file_path,
                        'export_name': issue.export_name,
                        'description': issue.description,
                        'suggested_fix': issue.suggested_fix
                    })
                elif issue.severity == 'WARNING':
                    issues.append({
                        'type': issue.type,
                        'severity': 'MEDIUM',
                        'file': issue.file_path,
                        'export_name': issue.export_name,
                        'description': issue.description,
                        'suggested_fix': issue.suggested_fix
                    })
        except Exception as e:
            issues.append({
                'type': 'validation_error',
                'severity': 'HIGH',
                'file': barrel_path,
                'description': f'Cross-reference validation failed: {e}'
            })
        
        # TypeScript compliance check
        if self.config.enable_compliance_check:
            try:
                project_root = self._find_project_root(source_dir)
                compliance_summary = self.compliance_handler.get_config_summary(project_root)
                
                # Read barrel exports for compliance check
                barrel_exports = self.ast_parser.parse_file(barrel_path)
                export_statements = [export.original_line for export in barrel_exports]
                
                config = self.compliance_handler.read_typescript_config(project_root)
                compliance_result = self.compliance_handler.validate_export_compliance(
                    export_statements, config
                )
                
                # Add compliance issues
                for issue in compliance_result['issues']:
                    issues.append({
                        'type': 'compliance',
                        'severity': 'MEDIUM',
                        'file': barrel_path,
                        'description': issue
                    })
                    
            except Exception as e:
                issues.append({
                    'type': 'compliance_check_error',
                    'severity': 'LOW',
                    'file': barrel_path,
                    'description': f'TypeScript compliance check failed: {e}'
                })
        
        return {
            'enabled': True,
            'barrel_path': barrel_path,
            'source_dir': source_dir,
            'issues': issues,
            'is_valid': len([i for i in issues if i['severity'] == 'HIGH']) == 0,
            'validation_report': validation_report if 'validation_report' in locals() else None
        }
    
    def run_full_validation(self, dir_path: str, subdirs: List[str], 
                          file_exports: List[ExportInfo]) -> ValidationResult:
        """
        Run complete validation pipeline including conflict analysis
        
        Args:
            dir_path: Directory to validate
            subdirs: List of subdirectories
            file_exports: Exports from files in directory
            
        Returns:
            Complete validation result
        """
        # Pre-generation validation
        pre_gen_result = self.validate_directory_pre_generation(dir_path)
        
        # Conflict analysis
        conflict_analysis = {}
        if self.config.enable_conflict_detection:
            try:
                conflict_analysis = self.conflict_engine.analyze_directory_conflicts(
                    dir_path, subdirs, file_exports
                )
            except Exception as e:
                conflict_analysis = {
                    'error': f'Conflict analysis failed: {e}',
                    'has_conflicts': False
                }
        
        # TypeScript compliance check
        compliance_report = {}
        if self.config.enable_compliance_check:
            try:
                project_root = self._find_project_root(dir_path)
                compliance_report = self.compliance_handler.get_config_summary(project_root)
            except Exception as e:
                compliance_report = {
                    'error': f'Compliance check failed: {e}'
                }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            pre_gen_result, conflict_analysis, compliance_report
        )
        
        # Calculate success rate
        total_issues = len(pre_gen_result.get('issues', []))
        high_severity_issues = len([i for i in pre_gen_result.get('issues', []) 
                                  if i.get('severity') == 'HIGH'])
        success_rate = max(0, 1.0 - (high_severity_issues * 0.5 + total_issues * 0.1))
        
        return ValidationResult(
            directory=dir_path,
            is_valid=pre_gen_result.get('is_valid', False) and not conflict_analysis.get('has_conflicts', False),
            pre_gen_issues=pre_gen_result.get('issues', []),
            post_gen_issues=[],  # Will be filled by post-generation validation
            conflict_analysis=conflict_analysis,
            compliance_report=compliance_report,
            recommendations=recommendations,
            success_rate=success_rate
        )
    
    def _get_source_files(self, dir_path: str) -> List[str]:
        """Get all source files in directory"""
        source_files = []
        
        try:
            for file in os.listdir(dir_path):
                if file == 'index.ts':
                    continue  # Skip existing barrel files
                
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path) and file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    # Skip test files and other excluded patterns
                    exclude_patterns = [r'\.test\.', r'\.spec\.', r'\.d\.ts$', r'\.stories\.', r'\.config\.']
                    import re
                    should_exclude = any(re.search(pattern, file) for pattern in exclude_patterns)
                    
                    if not should_exclude:
                        source_files.append(file_path)
        except OSError as e:
            print(f"Error reading directory {dir_path}: {e}")
        
        return source_files
    
    def _find_project_root(self, start_dir: str) -> str:
        """Find project root by looking for tsconfig.json"""
        current_dir = Path(start_dir).resolve()
        
        while current_dir.parent != current_dir:
            if (current_dir / 'tsconfig.json').exists():
                return str(current_dir)
            current_dir = current_dir.parent
        
        # Fallback to start directory
        return start_dir
    
    def _generate_recommendations(self, pre_gen_result: Dict[str, Any],
                                conflict_analysis: Dict[str, Any],
                                compliance_report: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []
        
        # Pre-generation issues
        high_issues = [i for i in pre_gen_result.get('issues', []) if i.get('severity') == 'HIGH']
        if high_issues:
            recommendations.append(f"Fix {len(high_issues)} high-severity issues before barrel generation")
        
        # Conflict resolution
        if conflict_analysis.get('has_conflicts'):
            total_conflicts = conflict_analysis.get('total_conflicts', 0)
            strategy = conflict_analysis.get('recommended_strategy', 'explicit_alias')
            recommendations.append(f"Resolve {total_conflicts} export conflicts using {strategy} strategy")
        
        # Compliance improvements
        if 'compliance_requirements' in compliance_report:
            requirements = compliance_report['compliance_requirements']
            if requirements:
                recommendations.append(f"Ensure compliance with {len(requirements)} TypeScript requirements")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Validation passed - ready for barrel generation")
        
        return recommendations
    
    def generate_validation_report(self, result: ValidationResult) -> str:
        """Generate human-readable validation report"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("VALIDATION PIPELINE REPORT")
        report_lines.append("=" * 60)
        
        report_lines.append(f"Directory: {result.directory}")
        report_lines.append(f"Overall Status: {'✅ VALID' if result.is_valid else '❌ INVALID'}")
        report_lines.append(f"Success Rate: {result.success_rate:.1%}")
        report_lines.append("")
        
        # Pre-generation issues
        if result.pre_gen_issues:
            report_lines.append("PRE-GENERATION ISSUES:")
            for issue in result.pre_gen_issues:
                icon = "❌" if issue['severity'] == 'HIGH' else "⚠️" if issue['severity'] == 'MEDIUM' else "ℹ️"
                report_lines.append(f"  {icon} {issue['description']}")
        
        # Conflict analysis
        if result.conflict_analysis.get('has_conflicts'):
            report_lines.append("\nCONFLICT ANALYSIS:")
            report_lines.append(f"  Total Conflicts: {result.conflict_analysis.get('total_conflicts', 0)}")
            report_lines.append(f"  Recommended Strategy: {result.conflict_analysis.get('recommended_strategy', 'N/A')}")
        
        # Recommendations
        if result.recommendations:
            report_lines.append("\nRECOMMENDATIONS:")
            for rec in result.recommendations:
                report_lines.append(f"  💡 {rec}")
        
        return "\n".join(report_lines)