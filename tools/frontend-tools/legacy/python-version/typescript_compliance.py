"""
TypeScript Compliance Module  
Handles TypeScript-specific compiler configurations and export syntax requirements
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class TypeScriptConfig:
    """TypeScript configuration settings relevant to export generation"""
    verbatim_module_syntax: bool = False
    isolated_modules: bool = False
    preserve_value_imports: bool = False
    import_helpers: bool = False
    es_module_interop: bool = False
    allow_synthetic_default_imports: bool = False
    strict: bool = False
    no_emit_on_error: bool = False
    
    # Module resolution settings
    module_resolution: str = 'node'
    base_url: Optional[str] = None
    paths: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.paths is None:
            self.paths = {}


class TypeScriptComplianceHandler:
    """
    Handles TypeScript compiler configuration and ensures generated exports comply
    with TypeScript compilation requirements
    """
    
    def __init__(self):
        self.config_cache = {}
    
    def read_typescript_config(self, project_root: str) -> TypeScriptConfig:
        """
        Read and parse TypeScript configuration from tsconfig.json
        
        Args:
            project_root: Root directory containing tsconfig.json
            
        Returns:
            Parsed TypeScript configuration
        """
        
        # Check cache first
        if project_root in self.config_cache:
            return self.config_cache[project_root]
        
        config = TypeScriptConfig()
        
        # Look for tsconfig files in order of preference
        config_files = [
            'tsconfig.json',
            'tsconfig.app.json', 
            'tsconfig.build.json'
        ]
        
        for config_file in config_files:
            config_path = os.path.join(project_root, config_file)
            if os.path.exists(config_path):
                try:
                    config = self._parse_config_file(config_path)
                    break
                except Exception as e:
                    print(f"Warning: Failed to parse {config_path}: {e}")
                    continue
        
        # Cache the result
        self.config_cache[project_root] = config
        return config
    
    def _parse_config_file(self, config_path: str) -> TypeScriptConfig:
        """Parse a specific TypeScript config file"""
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments for JSON parsing (basic approach)
        content = self._remove_json_comments(content)
        
        try:
            config_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
        
        # Parse compiler options
        compiler_options = config_data.get('compilerOptions', {})
        
        config = TypeScriptConfig(
            verbatim_module_syntax=compiler_options.get('verbatimModuleSyntax', False),
            isolated_modules=compiler_options.get('isolatedModules', False),
            preserve_value_imports=compiler_options.get('preserveValueImports', False),
            import_helpers=compiler_options.get('importHelpers', False),
            es_module_interop=compiler_options.get('esModuleInterop', False),
            allow_synthetic_default_imports=compiler_options.get('allowSyntheticDefaultImports', False),
            strict=compiler_options.get('strict', False),
            no_emit_on_error=compiler_options.get('noEmitOnError', False),
            module_resolution=compiler_options.get('moduleResolution', 'node'),
            base_url=compiler_options.get('baseUrl'),
            paths=compiler_options.get('paths', {})
        )
        
        return config
    
    def _remove_json_comments(self, content: str) -> str:
        """Remove JSON comments (// and /* */) for parsing"""
        import re
        
        # Remove single-line comments
        content = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments (basic approach)
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        
        return content
    
    def adjust_export_syntax(self, exports: List[str], config: TypeScriptConfig) -> List[str]:
        """
        Adjust export statements to comply with TypeScript configuration
        
        Args:
            exports: List of export statements
            config: TypeScript configuration
            
        Returns:
            Adjusted export statements
        """
        
        adjusted_exports = []
        
        for export_stmt in exports:
            adjusted_stmt = self._adjust_single_export(export_stmt, config)
            adjusted_exports.append(adjusted_stmt)
        
        return adjusted_exports
    
    def _adjust_single_export(self, export_stmt: str, config: TypeScriptConfig) -> str:
        """Adjust a single export statement for compliance"""
        
        # Handle verbatimModuleSyntax requirement
        if config.verbatim_module_syntax:
            export_stmt = self._enforce_verbatim_module_syntax(export_stmt)
        
        # Handle isolatedModules requirement  
        if config.isolated_modules:
            export_stmt = self._enforce_isolated_modules(export_stmt)
        
        return export_stmt
    
    def _enforce_verbatim_module_syntax(self, export_stmt: str) -> str:
        """
        Enforce verbatimModuleSyntax rules:
        - Type-only imports/exports must use 'type' keyword
        - Value imports/exports cannot use 'type' keyword
        """
        
        import re
        
        # Pattern to detect type-only re-exports that need 'type' keyword
        type_reexport_pattern = r'^export\s+\{\s*([^}]+)\s*\}\s+from\s+[\'"]([^\'"]+)[\'"];?\s*$'
        match = re.match(type_reexport_pattern, export_stmt)
        
        if match:
            export_names = match.group(1)
            module_path = match.group(2)
            
            # If this appears to be re-exporting types, ensure 'type' keyword is used
            if self._appears_to_be_types(export_names):
                # Check if 'type' keyword is already present
                if not re.match(r'export\s+type\s+\{', export_stmt):
                    return f"export type {{ {export_names} }} from '{module_path}';"
        
        # Pattern to detect star re-exports of types
        star_reexport_pattern = r'^export\s+\*\s+from\s+[\'"]([^\'"]+)[\'"];?\s*$'
        star_match = re.match(star_reexport_pattern, export_stmt)
        
        if star_match:
            module_path = star_match.group(1)
            # For star exports, we generally can't determine if they're type-only
            # The compiler will enforce this at compile time
            pass
        
        return export_stmt
    
    def _appears_to_be_types(self, export_names: str) -> bool:
        """Heuristic to determine if exports are likely types"""
        
        # Simple heuristics - can be enhanced
        type_indicators = [
            'Type', 'Interface', 'Props', 'Config', 'Options', 
            'Params', 'Response', 'Request', 'State', 'Schema'
        ]
        
        names = [name.strip().split(' as ')[0] for name in export_names.split(',')]
        
        for name in names:
            for indicator in type_indicators:
                if indicator.lower() in name.lower():
                    return True
                    
        return False
    
    def _enforce_isolated_modules(self, export_stmt: str) -> str:
        """
        Enforce isolatedModules rules:
        - Ensure re-exports are explicit enough for isolated compilation
        """
        
        # For isolatedModules, star exports can be problematic
        # but we'll leave them as-is since the specific requirements
        # depend on the actual module structure
        
        return export_stmt
    
    def validate_export_compliance(self, exports: List[str], 
                                 config: TypeScriptConfig) -> Dict[str, Any]:
        """
        Validate that exports comply with TypeScript configuration
        
        Args:
            exports: List of export statements to validate
            config: TypeScript configuration
            
        Returns:
            Validation results with issues and suggestions
        """
        
        issues = []
        warnings = []
        
        for i, export_stmt in enumerate(exports):
            # Check verbatimModuleSyntax compliance
            if config.verbatim_module_syntax:
                verbatim_issues = self._check_verbatim_compliance(export_stmt)
                issues.extend(verbatim_issues)
            
            # Check isolatedModules compliance
            if config.isolated_modules:
                isolation_warnings = self._check_isolation_compliance(export_stmt)
                warnings.extend(isolation_warnings)
        
        return {
            'is_compliant': len(issues) == 0,
            'total_exports': len(exports),
            'issues': issues,
            'warnings': warnings,
            'suggestions': self._generate_compliance_suggestions(issues, warnings)
        }
    
    def _check_verbatim_compliance(self, export_stmt: str) -> List[str]:
        """Check export statement for verbatimModuleSyntax compliance"""
        
        issues = []
        
        import re
        
        # Check for type re-exports without 'type' keyword
        if 'export {' in export_stmt and 'from' in export_stmt:
            if not 'export type {' in export_stmt:
                # This might be a type re-export that needs the 'type' keyword
                # We can't be 100% certain without more context, so this is a potential issue
                export_names_match = re.search(r'export\s+\{\s*([^}]+)\s*\}', export_stmt)
                if export_names_match and self._appears_to_be_types(export_names_match.group(1)):
                    issues.append(f"Potential verbatimModuleSyntax violation: '{export_stmt.strip()}' may need 'export type' keyword")
        
        return issues
    
    def _check_isolation_compliance(self, export_stmt: str) -> List[str]:
        """Check export statement for isolatedModules compliance"""
        
        warnings = []
        
        # Star exports can be problematic with isolatedModules
        if 'export *' in export_stmt:
            warnings.append(f"Star export may cause issues with isolatedModules: '{export_stmt.strip()}'")
        
        return warnings
    
    def _generate_compliance_suggestions(self, issues: List[str], warnings: List[str]) -> List[str]:
        """Generate suggestions for compliance issues"""
        
        suggestions = []
        
        if issues:
            suggestions.append("Consider adding 'type' keyword to type-only re-exports when verbatimModuleSyntax is enabled")
        
        if warnings:
            suggestions.append("Consider using explicit re-exports instead of star exports when isolatedModules is enabled")
        
        return suggestions
    
    def get_config_summary(self, project_root: str) -> Dict[str, Any]:
        """Get a summary of TypeScript configuration"""
        
        config = self.read_typescript_config(project_root)
        
        return {
            'project_root': project_root,
            'verbatim_module_syntax': config.verbatim_module_syntax,
            'isolated_modules': config.isolated_modules,
            'strict_mode': config.strict,
            'module_resolution': config.module_resolution,
            'has_path_mapping': bool(config.paths),
            'compliance_requirements': self._get_compliance_requirements(config)
        }
    
    def _get_compliance_requirements(self, config: TypeScriptConfig) -> List[str]:
        """Get list of compliance requirements based on config"""
        
        requirements = []
        
        if config.verbatim_module_syntax:
            requirements.append("Type-only re-exports must use 'export type' syntax")
        
        if config.isolated_modules:
            requirements.append("Each file must be compilable in isolation")
        
        if config.strict:
            requirements.append("Strict type checking enabled")
        
        if config.no_emit_on_error:
            requirements.append("No output generated if compilation errors exist")
        
        return requirements