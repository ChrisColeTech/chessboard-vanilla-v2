"""
Comprehensive validation module for template-based page generator.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import re

try:
    from .config import GenerationContext, PageConfig, ProjectCapabilities
    from .template_engine import TemplateEngine
    from .project_detector import ProjectCapabilityDetector
    from .dependency_manager import DependencyManager
    from .routing_updater import ParentRoutingUpdater
except ImportError:
    from config import GenerationContext, PageConfig, ProjectCapabilities
    from template_engine import TemplateEngine
    from project_detector import ProjectCapabilityDetector
    from dependency_manager import DependencyManager
    from routing_updater import ParentRoutingUpdater


@dataclass
class ValidationResult:
    """Result of a validation check."""
    category: str
    item: str
    status: bool
    message: str = ""
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationReport:
    """Complete validation report."""
    results: List[ValidationResult]
    summary: Dict[str, int]
    passed: bool


class ValidationError(Exception):
    """Raised when validation fails critically."""
    pass


class ProjectValidator:
    """Comprehensive validator for template-based page generator."""
    
    def __init__(self, frontend_root: Path, templates_dir: Path):
        self.frontend_root = frontend_root
        self.templates_dir = templates_dir
        
        # Initialize components for validation
        self.project_detector = ProjectCapabilityDetector(frontend_root)
        
        try:
            # These might fail if templates don't exist, handle gracefully
            from template_engine import TemplateEngine
            from dependency_manager import DependencyManager
            from file_writer import FileWriter
            from routing_updater import ParentRoutingUpdater
            from variable_generator import VariableGenerator
            
            self.template_engine = TemplateEngine(templates_dir)
            file_writer = FileWriter()
            variable_generator = VariableGenerator()
            
            self.dependency_manager = DependencyManager(self.template_engine, file_writer)
            self.routing_updater = ParentRoutingUpdater(
                self.template_engine, file_writer, variable_generator
            )
        except Exception as e:
            # If initialization fails, we can still do basic validation
            self.template_engine = None
            self.dependency_manager = None
            self.routing_updater = None
    
    def validate_project_structure(self) -> ValidationReport:
        """Validate basic project structure."""
        results = []
        
        # Check frontend root exists
        results.append(ValidationResult(
            category="Project Structure",
            item="Frontend Root",
            status=self.frontend_root.exists(),
            message=f"Path: {self.frontend_root}"
        ))
        
        # Check required directories
        required_dirs = [
            ("src", "src"),
            ("src/pages", "src/pages"),
            ("src/components", "src/components"),
            ("src/hooks", "src/hooks"),
            ("src/constants", "src/constants"),
            ("src/services", "src/services")
        ]
        
        for dir_name, dir_path in required_dirs:
            full_path = self.frontend_root / dir_path
            results.append(ValidationResult(
                category="Project Structure",
                item=f"Directory: {dir_name}",
                status=full_path.exists(),
                message=f"Path: {full_path}",
                severity="warning" if dir_name != "src" else "error"
            ))
        
        # Check package.json
        package_json = self.frontend_root / "package.json"
        results.append(ValidationResult(
            category="Project Structure", 
            item="package.json",
            status=package_json.exists(),
            message="Node.js project configuration",
            severity="warning"
        ))
        
        return self._create_report("Project Structure", results)
    
    def validate_templates(self) -> ValidationReport:
        """Validate template files and structure."""
        results = []
        
        # Check templates directory
        results.append(ValidationResult(
            category="Templates",
            item="Templates Directory",
            status=self.templates_dir.exists(),
            message=f"Path: {self.templates_dir}"
        ))
        
        if not self.templates_dir.exists():
            return self._create_report("Templates", results)
        
        # Check template subdirectories
        expected_template_dirs = [
            "pages", "components", "actions", "instructions", 
            "hooks", "dependencies", "routing"
        ]
        
        for template_dir in expected_template_dirs:
            dir_path = self.templates_dir / template_dir
            results.append(ValidationResult(
                category="Templates",
                item=f"Template Dir: {template_dir}",
                status=dir_path.exists(),
                message=f"Path: {dir_path}",
                severity="warning"
            ))
        
        # Validate individual templates if template engine is available
        if self.template_engine:
            try:
                missing_templates = self.template_engine.validate_all_required_templates()
                
                if not missing_templates:
                    results.append(ValidationResult(
                        category="Templates",
                        item="All Required Templates",
                        status=True,
                        message="All templates found"
                    ))
                else:
                    for template in missing_templates:
                        results.append(ValidationResult(
                            category="Templates",
                            item=f"Template: {template}",
                            status=False,
                            message="Template file missing"
                        ))
                
            except Exception as e:
                results.append(ValidationResult(
                    category="Templates",
                    item="Template Validation",
                    status=False,
                    message=f"Validation error: {e}",
                    severity="warning"
                ))
        
        return self._create_report("Templates", results)
    
    def validate_project_capabilities(self) -> ValidationReport:
        """Validate detected project capabilities."""
        results = []
        
        try:
            capabilities = self.project_detector.detect_capabilities()
            
            # Report capability detection
            capability_checks = [
                ("Page Hooks", capabilities.has_page_hooks, "usePageInstructions & usePageActions"),
                ("Mobile Hook", capabilities.has_mobile_hook, "useIsMobile hook"),
                ("DataTable", capabilities.has_data_table, "DataTable component")
            ]
            
            for name, status, description in capability_checks:
                results.append(ValidationResult(
                    category="Capabilities",
                    item=name,
                    status=status,
                    message=description,
                    severity="info"
                ))
            
            # Report existing structure
            results.append(ValidationResult(
                category="Capabilities",
                item="Existing Parents",
                status=len(capabilities.existing_parents) > 0,
                message=f"Found {len(capabilities.existing_parents)} parent pages",
                severity="info"
            ))
            
            total_children = sum(len(children) for children in capabilities.existing_children.values())
            results.append(ValidationResult(
                category="Capabilities",
                item="Existing Children",
                status=total_children > 0,
                message=f"Found {total_children} child pages",
                severity="info"
            ))
            
        except Exception as e:
            results.append(ValidationResult(
                category="Capabilities",
                item="Capability Detection",
                status=False,
                message=f"Detection failed: {e}"
            ))
        
        return self._create_report("Capabilities", results)
    
    def validate_dependencies(self) -> ValidationReport:
        """Validate project dependencies."""
        results = []
        
        if not self.dependency_manager:
            results.append(ValidationResult(
                category="Dependencies",
                item="Dependency Manager",
                status=False,
                message="Dependency manager not initialized"
            ))
            return self._create_report("Dependencies", results)
        
        try:
            capabilities = self.project_detector.detect_capabilities()
            
            # Create dummy context for dependency validation
            context = GenerationContext(
                config=PageConfig("DummyPage"),
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                templates_dir=self.templates_dir
            )
            
            dependency_validation = self.dependency_manager.validate_dependencies(context)
            
            for dep_name, exists in dependency_validation.items():
                results.append(ValidationResult(
                    category="Dependencies",
                    item=dep_name,
                    status=exists,
                    message="Dependency available" if exists else "Dependency missing",
                    severity="warning" if not exists else "info"
                ))
            
            # Check for missing dependencies
            missing = self.dependency_manager.get_missing_dependencies(context)
            if missing:
                results.append(ValidationResult(
                    category="Dependencies",
                    item="Missing Dependencies",
                    status=False,
                    message=f"Missing: {', '.join(missing)}",
                    severity="warning"
                ))
            else:
                results.append(ValidationResult(
                    category="Dependencies",
                    item="All Dependencies",
                    status=True,
                    message="All dependencies available"
                ))
                
        except Exception as e:
            results.append(ValidationResult(
                category="Dependencies",
                item="Dependency Validation",
                status=False,
                message=f"Validation error: {e}"
            ))
        
        return self._create_report("Dependencies", results)
    
    def validate_routing_sync(self) -> ValidationReport:
        """Validate parent-child routing synchronization."""
        results = []
        
        if not self.routing_updater:
            results.append(ValidationResult(
                category="Routing",
                item="Routing Updater",
                status=False,
                message="Routing updater not initialized"
            ))
            return self._create_report("Routing", results)
        
        try:
            capabilities = self.project_detector.detect_capabilities()
            
            # Create dummy context for routing validation
            context = GenerationContext(
                config=PageConfig("DummyPage"),
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                templates_dir=self.templates_dir
            )
            
            # Validate each parent's routing
            for parent in capabilities.existing_parents:
                sync_result = self.routing_updater.sync_routing_with_filesystem(context, parent)
                
                in_sync = sync_result['in_sync']
                results.append(ValidationResult(
                    category="Routing",
                    item=f"Parent: {parent}",
                    status=in_sync,
                    message=f"Routing {'synchronized' if in_sync else 'out of sync'}",
                    severity="info" if in_sync else "warning"
                ))
                
                # Report specific sync issues
                if sync_result['missing_in_routing']:
                    results.append(ValidationResult(
                        category="Routing",
                        item=f"{parent} - Missing in Routing",
                        status=False,
                        message=f"Files not in routing: {', '.join(sync_result['missing_in_routing'])}",
                        severity="warning"
                    ))
                
                if sync_result['missing_in_filesystem']:
                    results.append(ValidationResult(
                        category="Routing",
                        item=f"{parent} - Missing Files",
                        status=False,
                        message=f"Routes without files: {', '.join(sync_result['missing_in_filesystem'])}",
                        severity="warning"
                    ))
            
            if not capabilities.existing_parents:
                results.append(ValidationResult(
                    category="Routing",
                    item="Parent Pages",
                    status=True,
                    message="No parent pages found to validate",
                    severity="info"
                ))
                
        except Exception as e:
            results.append(ValidationResult(
                category="Routing",
                item="Routing Validation",
                status=False,
                message=f"Validation error: {e}"
            ))
        
        return self._create_report("Routing", results)
    
    def validate_generated_files(self, config: PageConfig) -> ValidationReport:
        """Validate files generated for a specific page configuration."""
        results = []
        
        try:
            capabilities = self.project_detector.detect_capabilities()
            context = GenerationContext(
                config=config,
                capabilities=capabilities,
                frontend_root=self.frontend_root,
                templates_dir=self.templates_dir
            )
            
            if config.parent:
                # Child page validation
                from child_generator import ChildPageGenerator
                from wrapper_selector import WrapperSelector
                from variable_generator import VariableGenerator
                from file_writer import FileWriter
                
                child_generator = ChildPageGenerator(
                    self.template_engine,
                    FileWriter(),
                    VariableGenerator(),
                    WrapperSelector()
                )
                
                validation = child_generator.validate_child_creation(context)
                
                for item, status in validation.items():
                    results.append(ValidationResult(
                        category="Generated Files",
                        item=f"Child {item}",
                        status=status,
                        message=f"File {'exists' if status else 'missing'}"
                    ))
            else:
                # Parent page validation
                from parent_generator import ParentPageGenerator
                from variable_generator import VariableGenerator
                
                parent_generator = ParentPageGenerator(
                    self.template_engine,
                    FileWriter(),
                    VariableGenerator(),
                    self.dependency_manager
                )
                
                validation = parent_generator.validate_parent_creation(context)
                
                for item, status in validation.items():
                    results.append(ValidationResult(
                        category="Generated Files",
                        item=f"Parent {item}",
                        status=status,
                        message=f"File {'exists' if status else 'missing'}"
                    ))
                    
        except Exception as e:
            results.append(ValidationResult(
                category="Generated Files",
                item="File Validation",
                status=False,
                message=f"Validation error: {e}"
            ))
        
        return self._create_report("Generated Files", results)
    
    def run_comprehensive_validation(self) -> ValidationReport:
        """Run all validation checks and return comprehensive report."""
        all_results = []
        
        # Run all validation checks
        validation_methods = [
            self.validate_project_structure,
            self.validate_templates,
            self.validate_project_capabilities,
            self.validate_dependencies,
            self.validate_routing_sync
        ]
        
        for validation_method in validation_methods:
            try:
                report = validation_method()
                all_results.extend(report.results)
            except Exception as e:
                all_results.append(ValidationResult(
                    category="Validation System",
                    item=validation_method.__name__,
                    status=False,
                    message=f"Validation method failed: {e}"
                ))
        
        return self._create_report("Comprehensive Validation", all_results)
    
    def _create_report(self, category: str, results: List[ValidationResult]) -> ValidationReport:
        """Create validation report from results."""
        # Calculate summary
        summary = {
            "total": len(results),
            "passed": len([r for r in results if r.status]),
            "failed": len([r for r in results if not r.status]),
            "errors": len([r for r in results if not r.status and r.severity == "error"]),
            "warnings": len([r for r in results if not r.status and r.severity == "warning"]),
            "info": len([r for r in results if r.severity == "info"])
        }
        
        # Determine overall pass/fail
        critical_failures = [r for r in results if not r.status and r.severity == "error"]
        passed = len(critical_failures) == 0
        
        return ValidationReport(
            results=results,
            summary=summary,
            passed=passed
        )
    
    def print_validation_report(self, report: ValidationReport, show_details: bool = True) -> None:
        """Print validation report in formatted way."""
        print(f"\n📋 Validation Summary:")
        print(f"  Total Checks: {report.summary['total']}")
        print(f"  ✅ Passed: {report.summary['passed']}")
        print(f"  ❌ Failed: {report.summary['failed']}")
        
        if report.summary['errors'] > 0:
            print(f"  🚨 Errors: {report.summary['errors']}")
        if report.summary['warnings'] > 0:
            print(f"  ⚠️  Warnings: {report.summary['warnings']}")
        if report.summary['info'] > 0:
            print(f"  ℹ️  Info: {report.summary['info']}")
        
        overall_status = "✅ PASSED" if report.passed else "❌ FAILED"
        print(f"  Overall: {overall_status}")
        
        if show_details:
            print(f"\n📋 Detailed Results:")
            
            current_category = None
            for result in report.results:
                if result.category != current_category:
                    print(f"\n  {result.category}:")
                    current_category = result.category
                
                status_icon = "✅" if result.status else {
                    "error": "❌",
                    "warning": "⚠️",
                    "info": "ℹ️"
                }.get(result.severity, "❌")
                
                print(f"    {status_icon} {result.item}")
                if result.message:
                    print(f"        {result.message}")
    
    def get_validation_issues(self, report: ValidationReport, severity: str = "error") -> List[ValidationResult]:
        """Get validation issues of specific severity."""
        return [r for r in report.results if not r.status and r.severity == severity]
    
    def has_critical_issues(self, report: ValidationReport) -> bool:
        """Check if report has critical issues that prevent operation."""
        return len(self.get_validation_issues(report, "error")) > 0