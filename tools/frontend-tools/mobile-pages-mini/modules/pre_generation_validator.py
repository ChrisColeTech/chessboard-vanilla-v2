"""
Pre-Generation Dependency Validator

Validates ALL dependencies BEFORE generating any files to prevent broken projects.
Fails fast with clear error messages about what needs to be fixed.
"""

import re
import json
from pathlib import Path
from typing import Set, Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from .template_dependency_scanner import TemplateDependencyScanner
    from .config import GenerationContext
except ImportError:
    from template_dependency_scanner import TemplateDependencyScanner
    from config import GenerationContext


class DependencyType(Enum):
    NPM_PACKAGE = "npm_package"
    TEMPLATE_FILE = "template_file"
    GENERATED_FILE = "generated_file"
    PROJECT_FILE = "project_file"
    CHESS_SPECIFIC = "chess_specific"
    UNKNOWN = "unknown"


@dataclass
class DependencyInfo:
    """Information about a single dependency."""
    import_path: str
    dependency_type: DependencyType
    exists: bool
    source_template: str
    error_message: Optional[str] = None
    remediation: Optional[str] = None


@dataclass
class ValidationResults:
    """Results of pre-generation validation."""
    dependencies: List[DependencyInfo]
    npm_packages_missing: List[str]
    templates_missing: List[str]
    chess_dependencies: List[str]
    critical_failures: List[str]
    warnings: List[str]
    can_proceed: bool
    
    @property
    def has_critical_failures(self) -> bool:
        return len(self.critical_failures) > 0


class PreGenerationValidator:
    """Validates all dependencies before generating any files."""
    
    def __init__(self, static_templates_dir: Path, dynamic_templates_dir: Path):
        self.static_dir = static_templates_dir
        self.dynamic_dir = dynamic_templates_dir
        self.scanner = TemplateDependencyScanner(static_templates_dir, dynamic_templates_dir)
        
        # Known NPM packages that need to be installed
        self.known_npm_packages = {
            '@radix-ui/react-slot', '@radix-ui/react-label', 'class-variance-authority',
            'howler', 'react-hook-form', 'react-icons/hi', 'react-icons/vsc', 
            'tailwind-merge', 'lucide-react', '@headlessui/react'
        }
        
        # Known chess-specific dependencies that should be flagged
        self.chess_specific_patterns = [
            r'.*chess.*', r'.*piece.*', r'.*board.*', r'.*stockfish.*',
            r'.*computer.*difficulty.*', r'.*game.*result.*'
        ]
    
    def validate_before_generation(self, context: GenerationContext, page_type: str) -> ValidationResults:
        """
        Comprehensive validation before generating any files.
        
        Args:
            context: Generation context
            page_type: "parent" or "child"
            
        Returns:
            ValidationResults with all dependency validation info
            
        Raises:
            ValidationError: If critical dependencies are missing
        """
        print(f"🔍 Running comprehensive pre-generation validation...")
        
        # 1. Scan all templates that will be used
        scan_result = self.scanner.scan_dependencies(page_type)
        
        # 2. Extract all dependencies from templates
        all_dependencies = self._extract_all_dependencies_from_templates(scan_result.required_templates)
        
        # 3. Categorize and validate each dependency
        dependency_info = self._categorize_and_validate_dependencies(all_dependencies, context)
        
        # 4. Analyze results and determine if we can proceed
        results = self._analyze_validation_results(dependency_info)
        
        # 5. Report results
        self._report_validation_results(results)
        
        return results
    
    def _extract_all_dependencies_from_templates(self, template_paths: Set[str]) -> Dict[str, Set[str]]:
        """Extract all import dependencies from the given templates."""
        all_dependencies = {}
        
        for template_path in template_paths:
            dependencies = set()
            
            # Read template content
            content = self._read_template_content(template_path)
            if content:
                # Extract import statements
                imports = self._extract_imports_from_content(content)
                dependencies.update(imports)
            
            all_dependencies[template_path] = dependencies
        
        return all_dependencies
    
    def _read_template_content(self, template_path: str) -> Optional[str]:
        """Read content from a template file."""
        # Try static directory first
        static_path = self.static_dir / template_path
        if static_path.exists():
            try:
                return static_path.read_text(encoding='utf-8')
            except Exception:
                return None
        
        # Try dynamic directory
        dynamic_path = self.dynamic_dir / template_path
        if dynamic_path.exists():
            try:
                return dynamic_path.read_text(encoding='utf-8')
            except Exception:
                return None
        
        return None
    
    def _extract_imports_from_content(self, content: str) -> Set[str]:
        """Extract import paths from template content."""
        import_patterns = [
            r'import.*?from\s+[\'"]([^\'"]+)[\'"]',  # import ... from "path"
            r'import\s+[\'"]([^\'"]+)[\'"]',        # import "path"
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',  # require("path")
        ]
        
        imports = set()
        for pattern in import_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.update(matches)
        
        return imports
    
    def _categorize_and_validate_dependencies(self, all_dependencies: Dict[str, Set[str]], context: GenerationContext) -> List[DependencyInfo]:
        """Categorize each dependency and validate its existence."""
        dependency_info = []
        
        for template_path, dependencies in all_dependencies.items():
            for dep_path in dependencies:
                dep_info = self._analyze_single_dependency(dep_path, template_path, context)
                dependency_info.append(dep_info)
        
        return dependency_info
    
    def _analyze_single_dependency(self, import_path: str, source_template: str, context: GenerationContext) -> DependencyInfo:
        """Analyze a single dependency and determine its type and existence."""
        # Determine dependency type
        dep_type = self._determine_dependency_type(import_path)
        
        # Check if it exists
        exists = False
        error_message = None
        remediation = None
        
        if dep_type == DependencyType.NPM_PACKAGE:
            exists = self._check_npm_package_exists(import_path, context)
            if not exists:
                error_message = f"NPM package '{import_path}' not installed"
                remediation = f"Run: npm install {import_path}"
        
        elif dep_type == DependencyType.TEMPLATE_FILE:
            exists = self._check_template_exists(import_path)
            if not exists:
                error_message = f"Template file '{import_path}' not found"
                remediation = "This template should exist in the static templates directory"
        
        elif dep_type == DependencyType.GENERATED_FILE:
            # Generated files don't exist yet, but will be created
            exists = True
        
        elif dep_type == DependencyType.PROJECT_FILE:
            exists = self._check_project_file_exists(import_path, context)
            if not exists:
                error_message = f"Project file '{import_path}' not found"
                remediation = "This file should exist in your project or be created manually"
        
        elif dep_type == DependencyType.CHESS_SPECIFIC:
            exists = False
            error_message = f"Chess-specific dependency '{import_path}' not available for generic projects"
            remediation = "Consider using a chess-specific project template or removing chess dependencies"
        
        return DependencyInfo(
            import_path=import_path,
            dependency_type=dep_type,
            exists=exists,
            source_template=source_template,
            error_message=error_message,
            remediation=remediation
        )
    
    def _determine_dependency_type(self, import_path: str) -> DependencyType:
        """Determine the type of dependency based on the import path."""
        # NPM packages (don't start with ./ or ../)
        if not import_path.startswith('./') and not import_path.startswith('../'):
            if import_path in self.known_npm_packages:
                return DependencyType.NPM_PACKAGE
            # Check if it matches chess-specific patterns
            for pattern in self.chess_specific_patterns:
                if re.match(pattern, import_path):
                    return DependencyType.CHESS_SPECIFIC
            return DependencyType.NPM_PACKAGE
        
        # Relative imports
        clean_path = import_path.lstrip('./')
        
        # Check for chess-specific patterns
        for pattern in self.chess_specific_patterns:
            if re.match(pattern, clean_path):
                return DependencyType.CHESS_SPECIFIC
        
        # Check if it's a template file
        if self._check_template_exists(import_path):
            return DependencyType.TEMPLATE_FILE
        
        # Check common generated file patterns
        generated_patterns = [
            r'hooks/.*Actions', r'pages/.*', r'constants/actions/pages/.*'
        ]
        for pattern in generated_patterns:
            if re.match(pattern, clean_path):
                return DependencyType.GENERATED_FILE
        
        return DependencyType.PROJECT_FILE
    
    def _check_npm_package_exists(self, package_name: str, context: GenerationContext) -> bool:
        """Check if an NPM package is installed."""
        package_json_path = context.frontend_root / "package.json"
        if not package_json_path.exists():
            return False
        
        try:
            with open(package_json_path, 'r') as f:
                package_json = json.load(f)
            
            dependencies = package_json.get('dependencies', {})
            dev_dependencies = package_json.get('devDependencies', {})
            all_packages = {**dependencies, **dev_dependencies}
            
            # Handle submodule imports like 'react-icons/hi' or 'zustand/middleware'
            root_package = self._extract_root_package_name(package_name)
            
            # Check if the root package exists
            return root_package in all_packages
        except Exception:
            return False
    
    def _extract_root_package_name(self, package_name: str) -> str:
        """Extract root package name from submodule imports."""
        # Handle scoped packages like '@hookform/resolvers/zod'
        if package_name.startswith('@'):
            parts = package_name.split('/')
            if len(parts) >= 2:
                # For scoped packages, take scope + package name: '@hookform/resolvers'
                return f"{parts[0]}/{parts[1]}"
            else:
                # Malformed scoped package, return as-is
                return package_name
        
        # For regular packages, split on '/' and take the first part
        # Examples: 'react-icons/hi' -> 'react-icons', 'zustand/middleware' -> 'zustand'
        return package_name.split('/')[0]
    
    def _check_template_exists(self, import_path: str) -> bool:
        """Check if a template file exists."""
        clean_path = import_path.lstrip('./')
        
        # Try different extensions
        possible_paths = [
            f"{clean_path}.template",
            f"{clean_path}.ts.template",
            f"{clean_path}.tsx.template"
        ]
        
        for path in possible_paths:
            if (self.static_dir / path).exists() or (self.dynamic_dir / path).exists():
                return True
        
        return False
    
    def _check_project_file_exists(self, import_path: str, context: GenerationContext) -> bool:
        """Check if a project file exists."""
        clean_path = import_path.lstrip('./')
        
        # Try different extensions and paths
        possible_paths = [
            f"src/{clean_path}",
            f"src/{clean_path}.ts",
            f"src/{clean_path}.tsx",
            f"src/{clean_path}/index.ts",
            f"src/{clean_path}/index.tsx"
        ]
        
        for path in possible_paths:
            if (context.frontend_root / path).exists():
                return True
        
        return False
    
    def _analyze_validation_results(self, dependency_info: List[DependencyInfo]) -> ValidationResults:
        """Analyze validation results and determine if generation can proceed."""
        npm_packages_missing = []
        templates_missing = []
        chess_dependencies = []
        critical_failures = []
        warnings = []
        
        for dep in dependency_info:
            if not dep.exists:
                if dep.dependency_type == DependencyType.NPM_PACKAGE:
                    npm_packages_missing.append(dep.import_path)
                    critical_failures.append(dep.error_message)
                elif dep.dependency_type == DependencyType.TEMPLATE_FILE:
                    templates_missing.append(dep.import_path)
                    critical_failures.append(dep.error_message)
                elif dep.dependency_type == DependencyType.CHESS_SPECIFIC:
                    chess_dependencies.append(dep.import_path)
                    warnings.append(dep.error_message)
                elif dep.dependency_type == DependencyType.PROJECT_FILE:
                    warnings.append(dep.error_message)
        
        # Can proceed if no critical failures
        can_proceed = len(critical_failures) == 0
        
        return ValidationResults(
            dependencies=dependency_info,
            npm_packages_missing=list(set(npm_packages_missing)),
            templates_missing=list(set(templates_missing)),
            chess_dependencies=list(set(chess_dependencies)),
            critical_failures=critical_failures,
            warnings=warnings,
            can_proceed=can_proceed
        )
    
    def _report_validation_results(self, results: ValidationResults) -> None:
        """Report validation results to the user."""
        print(f"\n📊 Pre-Generation Validation Results:")
        print(f"  📦 Dependencies analyzed: {len(results.dependencies)}")
        
        if results.npm_packages_missing:
            print(f"\n❌ Missing NPM packages ({len(results.npm_packages_missing)}):")
            for pkg in results.npm_packages_missing:
                print(f"    - {pkg}")
            print(f"\n💡 To fix: npm install {' '.join(results.npm_packages_missing)}")
        
        if results.templates_missing:
            print(f"\n❌ Missing template files ({len(results.templates_missing)}):")
            for template in results.templates_missing:
                print(f"    - {template}")
        
        if results.chess_dependencies:
            print(f"\n⚠️  Chess-specific dependencies found ({len(results.chess_dependencies)}):")
            for dep in results.chess_dependencies:
                print(f"    - {dep}")
            print(f"💡 These may need to be removed for generic projects")
        
        if results.critical_failures:
            print(f"\n🚨 CRITICAL FAILURES - Cannot proceed:")
            for failure in results.critical_failures[:5]:  # Show first 5
                print(f"    ❌ {failure}")
            if len(results.critical_failures) > 5:
                print(f"    ... and {len(results.critical_failures) - 5} more")
        
        if results.warnings and not results.critical_failures:
            print(f"\n⚠️  Warnings ({len(results.warnings)}):")
            for warning in results.warnings[:3]:  # Show first 3
                print(f"    ⚠️  {warning}")
        
        if results.can_proceed:
            print(f"\n✅ Validation passed - safe to proceed with generation")
        else:
            print(f"\n❌ Validation failed - fix critical issues before proceeding")


class ValidationError(Exception):
    """Raised when pre-generation validation fails."""
    pass