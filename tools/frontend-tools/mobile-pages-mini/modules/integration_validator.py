"""
IntegrationValidator - Comprehensive validation of page generation and integration.

This module handles:
- Validating ActionRegistryManager integration (PAGE_ACTIONS, COMMON_ACTIONS)
- Validating ContainerIntegrator setup (ActionSheetContainer connections)
- Validating HookIntegrator implementation (functional hooks, no placeholders)
- Cross-module validation (ensuring all pieces work together)
- Using pages.config.json as source of truth for validation rules

Follows Single Responsibility Principle (SRP) - only handles validation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add parent directory to path so we can import shared modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from shared.name_standardizer import NameStandardizer

try:
    from .config import PageConfig
    from .action_registry_manager import ActionRegistryManager
    from .container_integrator import ContainerIntegrator
    from .hook_integrator import HookIntegrator
    from .config_integration import ConfigIntegration
except ImportError:
    # For standalone testing
    import sys
    sys.path.append(str(Path(__file__).parent))
    from config import PageConfig
    from action_registry_manager import ActionRegistryManager
    from container_integrator import ContainerIntegrator
    from hook_integrator import HookIntegrator
    
    sys.path.append(str(Path(__file__).parent.parent / "shared"))
    from config_integration import ConfigIntegration


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self):
        self.registry_issues: List[str] = []
        self.container_issues: List[str] = []
        self.hook_issues: List[str] = []
        self.cross_module_issues: List[str] = []
        self.critical_issues: List[str] = []
        
    @property
    def all_issues(self) -> List[str]:
        """Get all issues from all categories."""
        return (self.registry_issues + self.container_issues + 
                self.hook_issues + self.cross_module_issues + self.critical_issues)
    
    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no issues found)."""
        return len(self.all_issues) == 0
    
    @property
    def has_critical_issues(self) -> bool:
        """Check if there are critical issues that prevent functionality."""
        return len(self.critical_issues) > 0
    
    def add_registry_issue(self, issue: str):
        """Add registry-related issue."""
        self.registry_issues.append(f"Registry: {issue}")
        
    def add_container_issue(self, issue: str):
        """Add container-related issue."""
        self.container_issues.append(f"Container: {issue}")
        
    def add_hook_issue(self, issue: str):
        """Add hook-related issue."""
        self.hook_issues.append(f"Hook: {issue}")
        
    def add_cross_module_issue(self, issue: str):
        """Add cross-module issue."""
        self.cross_module_issues.append(f"Cross-Module: {issue}")
        
    def add_critical_issue(self, issue: str):
        """Add critical issue."""
        self.critical_issues.append(f"CRITICAL: {issue}")
    
    def get_summary(self) -> str:
        """Get validation summary."""
        total_issues = len(self.all_issues)
        
        if total_issues == 0:
            return "✅ All validations passed - integration is complete and functional"
        
        summary = f"❌ Found {total_issues} integration issues:\n"
        
        if self.critical_issues:
            summary += f"  🚨 Critical: {len(self.critical_issues)}\n"
        if self.registry_issues:
            summary += f"  📝 Registry: {len(self.registry_issues)}\n"
        if self.container_issues:
            summary += f"  📦 Container: {len(self.container_issues)}\n"
        if self.hook_issues:
            summary += f"  🪝 Hooks: {len(self.hook_issues)}\n"
        if self.cross_module_issues:
            summary += f"  🔗 Cross-Module: {len(self.cross_module_issues)}\n"
            
        return summary.rstrip()


class IntegrationValidator:
    """Comprehensive validator for page generation and integration."""
    
    def __init__(self, frontend_root: Path):
        self.frontend_root = frontend_root
        
        # Initialize specialized validators
        self.action_registry = ActionRegistryManager(frontend_root)
        self.container_integrator = ContainerIntegrator(frontend_root)
        self.hook_integrator = HookIntegrator(frontend_root)
        
        # Config integration
        self.config_integration = ConfigIntegration(frontend_root)
        
    def validate_page_integration(self, page_id: str) -> ValidationResult:
        """
        Comprehensive validation of a single page's integration.
        Uses pages.config.json to determine validation rules.
        """
        result = ValidationResult()
        
        try:
            # Get page info from config
            page_info = self._get_page_info(page_id)
            if not page_info:
                result.add_critical_issue(f"Page '{page_id}' not found in pages.config.json")
                return result
            
            page_type = page_info.get('type')
            
            if page_type == 'parent':
                self._validate_parent_page(page_id, page_info, result)
            elif page_type == 'child':
                self._validate_child_page(page_id, page_info, result)
            else:
                result.add_critical_issue(f"Page '{page_id}' has invalid type: {page_type}")
            
        except Exception as e:
            result.add_critical_issue(f"Error validating page '{page_id}': {e}")
        
        return result
    
    def validate_parent_integration(self, parent_id: str) -> ValidationResult:
        """
        Comprehensive validation of parent page and all its children.
        Uses pages.config.json to get accurate child relationships.
        """
        result = ValidationResult()
        
        try:
            # Validate parent page itself
            parent_result = self.validate_page_integration(parent_id)
            result.registry_issues.extend(parent_result.registry_issues)
            result.container_issues.extend(parent_result.container_issues)
            result.hook_issues.extend(parent_result.hook_issues)
            result.critical_issues.extend(parent_result.critical_issues)
            
            # Get and validate all children
            children = self._get_children_for_parent(parent_id)
            
            for child in children:
                child_result = self.validate_page_integration(child['id'])
                result.registry_issues.extend(child_result.registry_issues)
                result.container_issues.extend(child_result.container_issues)
                result.hook_issues.extend(child_result.hook_issues)
                result.critical_issues.extend(child_result.critical_issues)
            
            # Cross-module validation for parent-child relationships
            self._validate_parent_child_integration(parent_id, children, result)
            
        except Exception as e:
            result.add_critical_issue(f"Error validating parent integration '{parent_id}': {e}")
        
        return result
    
    def validate_complete_project_integration(self) -> ValidationResult:
        """
        Validate integration of entire project based on pages.config.json.
        """
        result = ValidationResult()
        
        try:
            config_data = self.config_integration.load_config()
            pages = config_data.get('pages', {})
            
            # Get all parent pages
            parent_pages = [page_id for page_id, page_info in pages.items() 
                          if page_info.get('type') == 'parent']
            
            if not parent_pages:
                result.add_critical_issue("No parent pages found in configuration")
                return result
            
            # Validate each parent and its children
            for parent_id in parent_pages:
                parent_result = self.validate_parent_integration(parent_id)
                result.registry_issues.extend(parent_result.registry_issues)
                result.container_issues.extend(parent_result.container_issues)
                result.hook_issues.extend(parent_result.hook_issues)
                result.cross_module_issues.extend(parent_result.cross_module_issues)
                result.critical_issues.extend(parent_result.critical_issues)
            
            # Project-wide cross-validation
            self._validate_project_wide_integration(pages, result)
            
        except Exception as e:
            result.add_critical_issue(f"Error validating complete project integration: {e}")
        
        return result
    
    def _validate_parent_page(self, parent_id: str, parent_info: Dict, result: ValidationResult):
        """Validate parent page integration across all modules."""
        
        # ActionRegistryManager validation
        registry_issues = self.action_registry.validate_registry_integration(parent_id)
        for issue in registry_issues:
            result.add_registry_issue(issue)
        
        # ContainerIntegrator validation
        container_issues = self.container_integrator.validate_container_integration(parent_id)
        for issue in container_issues:
            result.add_container_issue(issue)
        
        # HookIntegrator validation
        hook_issues = self.hook_integrator.validate_hook_integration(parent_id)
        for issue in hook_issues:
            result.add_hook_issue(issue)
        
        # Parent-specific cross-module validation
        self._validate_parent_cross_module(parent_id, parent_info, result)
    
    def _validate_child_page(self, child_id: str, child_info: Dict, result: ValidationResult):
        """Validate child page integration across all modules."""
        
        # ActionRegistryManager validation (child should be in registry)
        registry_issues = self.action_registry.validate_registry_integration(child_id)
        for issue in registry_issues:
            result.add_registry_issue(issue)
        
        # ContainerIntegrator validation
        container_issues = self.container_integrator.validate_container_integration(child_id)
        for issue in container_issues:
            result.add_container_issue(issue)
        
        # HookIntegrator validation  
        hook_issues = self.hook_integrator.validate_hook_integration(child_id)
        for issue in hook_issues:
            result.add_hook_issue(issue)
        
        # Child-specific cross-module validation
        self._validate_child_cross_module(child_id, child_info, result)
    
    def _validate_parent_cross_module(self, parent_id: str, parent_info: Dict, result: ValidationResult):
        """Cross-module validation specific to parent pages."""
        
        # Check that parent hook methods match registered children in PAGE_ACTIONS
        try:
            children = self._get_children_for_parent(parent_id)
            
            # Verify hook has navigation methods for all registered children
            hook_path = self.hook_integrator._get_parent_hook_path(parent_id)
            if hook_path.exists():
                hook_content = hook_path.read_text(encoding='utf-8')
                
                for child in children:
                    method_name = f"goTo{NameStandardizer.to_pascal_case(child['name'])}"
                    if method_name not in hook_content:
                        result.add_cross_module_issue(
                            f"Parent hook '{parent_id}' missing navigation method '{method_name}' for registered child '{child['id']}'")
            
            # Verify PAGE_ACTIONS registry has entries for all children with hooks
            if self.action_registry.page_actions_path.exists():
                page_actions_content = self.action_registry.page_actions_path.read_text(encoding='utf-8')
                
                for child in children:
                    if f"{child['id']}:" not in page_actions_content:
                        result.add_cross_module_issue(
                            f"Child '{child['id']}' has hook but not registered in PAGE_ACTIONS")
                            
        except Exception as e:
            result.add_cross_module_issue(f"Error in parent cross-module validation for '{parent_id}': {e}")
    
    def _validate_child_cross_module(self, child_id: str, child_info: Dict, result: ValidationResult):
        """Cross-module validation specific to child pages."""
        
        parent_id = child_info.get('parent_id')
        if not parent_id:
            result.add_cross_module_issue(f"Child '{child_id}' has no parent_id in config")
            return
        
        try:
            # Verify child is registered in parent's navigation
            parent_hook_path = self.hook_integrator._get_parent_hook_path(parent_id)
            if parent_hook_path.exists():
                parent_hook_content = parent_hook_path.read_text(encoding='utf-8')
                child_method = f"goTo{NameStandardizer.to_pascal_case(child_info['name'])}"
                
                if child_method not in parent_hook_content:
                    result.add_cross_module_issue(
                        f"Child '{child_id}' not included in parent '{parent_id}' navigation methods")
            
            # Verify sibling navigation in child hook matches actual siblings in config
            siblings = self._get_sibling_pages(child_id, parent_id)
            child_hook_path = self.hook_integrator._get_child_hook_path(child_id, parent_id)
            
            if child_hook_path.exists() and siblings:
                child_hook_content = child_hook_path.read_text(encoding='utf-8')
                
                for sibling in siblings:
                    sibling_method = f"goTo{NameStandardizer.to_pascal_case(sibling['name'])}"
                    if sibling_method not in child_hook_content:
                        result.add_cross_module_issue(
                            f"Child '{child_id}' missing sibling navigation to '{sibling['id']}'")
                            
        except Exception as e:
            result.add_cross_module_issue(f"Error in child cross-module validation for '{child_id}': {e}")
    
    def _validate_parent_child_integration(self, parent_id: str, children: List[Dict], result: ValidationResult):
        """Validate integration between parent and all its children."""
        
        try:
            # Verify parent hook has methods for all children
            parent_hook_path = self.hook_integrator._get_parent_hook_path(parent_id)
            if parent_hook_path.exists():
                parent_hook_content = parent_hook_path.read_text(encoding='utf-8')
                
                expected_methods = len(children)
                actual_methods = parent_hook_content.count('setCurrentChildPage(')
                
                if expected_methods != actual_methods:
                    result.add_cross_module_issue(
                        f"Parent '{parent_id}' hook has {actual_methods} navigation methods but {expected_methods} children")
            
            # Verify COMMON_ACTIONS has navigation actions for all children
            if self.action_registry.common_actions_path.exists():
                common_actions_content = self.action_registry.common_actions_path.read_text(encoding='utf-8')
                
                for child in children:
                    expected_action = f'"go-to-{child["id"]}"'
                    if expected_action not in common_actions_content:
                        result.add_cross_module_issue(
                            f"Missing common action '{expected_action}' for child '{child['id']}'")
            
            # Verify sibling groups are properly formed
            if len(children) > 1:
                sibling_group_name = f"{parent_id}Siblings"
                if sibling_group_name not in common_actions_content:
                    result.add_cross_module_issue(
                        f"Missing sibling group '{sibling_group_name}' for parent '{parent_id}' with {len(children)} children")
                        
        except Exception as e:
            result.add_cross_module_issue(f"Error validating parent-child integration for '{parent_id}': {e}")
    
    def _validate_project_wide_integration(self, pages: Dict, result: ValidationResult):
        """Project-wide integration validation."""
        
        try:
            # Verify all pages in config have corresponding files
            for page_id, page_info in pages.items():
                page_type = page_info.get('type')
                
                if page_type == 'parent':
                    # Check parent page file exists
                    parent_page_path = self.frontend_root / f"src/pages/{page_id}/{page_info['component_name']}.tsx"
                    if not parent_page_path.exists():
                        result.add_critical_issue(f"Parent page file missing: {parent_page_path}")
                        
                elif page_type == 'child':
                    # Check child page file exists
                    parent_id = page_info.get('parent_id')
                    child_page_path = self.frontend_root / f"src/pages/{parent_id}/{page_info['component_name'].replace('Page', '')}.tsx"
                    if not child_page_path.exists():
                        result.add_critical_issue(f"Child page file missing: {child_page_path}")
            
            # Verify configuration consistency
            parent_count = sum(1 for page in pages.values() if page.get('type') == 'parent')
            child_count = sum(1 for page in pages.values() if page.get('type') == 'child')
            
            metadata = self.config_integration.load_config().get('metadata', {})
            if metadata.get('parent_pages', 0) != parent_count:
                result.add_cross_module_issue(f"Metadata parent count ({metadata.get('parent_pages', 0)}) doesn't match actual count ({parent_count})")
                
            if metadata.get('child_pages', 0) != child_count:
                result.add_cross_module_issue(f"Metadata child count ({metadata.get('child_pages', 0)}) doesn't match actual count ({child_count})")
                
        except Exception as e:
            result.add_cross_module_issue(f"Error in project-wide validation: {e}")
    
    def _get_page_info(self, page_id: str) -> Optional[Dict]:
        """Get page information from pages.config.json"""
        try:
            config_data = self.config_integration.load_config()
            return config_data.get('pages', {}).get(page_id)
        except Exception as e:
            print(f"  ⚠️  Error loading page config: {e}")
            return None
    
    def _get_children_for_parent(self, parent_id: str) -> List[Dict]:
        """Get all children for a parent from pages.config.json"""
        try:
            config_data = self.config_integration.load_config()
            pages = config_data.get('pages', {})
            
            children = []
            for page_id, page_info in pages.items():
                if page_info.get('type') == 'child' and page_info.get('parent_id') == parent_id:
                    children.append(page_info)
            
            # Sort by creation date for consistent ordering
            children.sort(key=lambda x: x.get('created_at', ''))
            return children
            
        except Exception as e:
            print(f"  ⚠️  Error getting children for parent {parent_id}: {e}")
            return []
    
    def _get_sibling_pages(self, child_id: str, parent_id: str) -> List[Dict]:
        """Get sibling pages for a child (all other children of the same parent)."""
        children = self._get_children_for_parent(parent_id)
        return [child for child in children if child['id'] != child_id]
    
    def check_critical_files_exist(self) -> List[str]:
        """Check that critical integration files exist."""
        issues = []
        
        critical_files = [
            self.action_registry.page_actions_path,
            self.action_registry.common_actions_path,
            self.container_integrator.action_sheet_container_path,
            self.frontend_root / "pages.config.json"
        ]
        
        for file_path in critical_files:
            if not file_path.exists():
                issues.append(f"Critical file missing: {file_path}")
        
        return issues
    
    def get_integration_summary(self, result: ValidationResult) -> str:
        """Get detailed integration summary with specific recommendations."""
        summary = result.get_summary() + "\n\n"
        
        if result.is_valid:
            summary += "🎉 Integration Status: COMPLETE AND FUNCTIONAL\n"
            summary += "All modules are properly integrated and working together."
            return summary
        
        summary += "🔧 Integration Status: NEEDS ATTENTION\n\n"
        
        if result.critical_issues:
            summary += "🚨 CRITICAL ISSUES (Must Fix First):\n"
            for issue in result.critical_issues:
                summary += f"   • {issue}\n"
            summary += "\n"
        
        if result.registry_issues:
            summary += "📝 Registry Integration Issues:\n"
            for issue in result.registry_issues:
                summary += f"   • {issue}\n"
            summary += "   Recommendation: Run ActionRegistryManager integration\n\n"
        
        if result.container_issues:
            summary += "📦 Container Integration Issues:\n"
            for issue in result.container_issues:
                summary += f"   • {issue}\n"
            summary += "   Recommendation: Run ContainerIntegrator setup\n\n"
        
        if result.hook_issues:
            summary += "🪝 Hook Integration Issues:\n"
            for issue in result.hook_issues:
                summary += f"   • {issue}\n"
            summary += "   Recommendation: Run HookIntegrator generation\n\n"
        
        if result.cross_module_issues:
            summary += "🔗 Cross-Module Integration Issues:\n"
            for issue in result.cross_module_issues:
                summary += f"   • {issue}\n"
            summary += "   Recommendation: Re-run all integration modules in sequence\n\n"
        
        return summary.rstrip()


# Convenience functions for direct usage
def validate_page(frontend_root: Path, page_id: str) -> ValidationResult:
    """Convenience function to validate single page integration."""
    validator = IntegrationValidator(frontend_root)
    return validator.validate_page_integration(page_id)


def validate_parent_with_children(frontend_root: Path, parent_id: str) -> ValidationResult:
    """Convenience function to validate parent and all its children."""
    validator = IntegrationValidator(frontend_root)
    return validator.validate_parent_integration(parent_id)


def validate_complete_project(frontend_root: Path) -> ValidationResult:
    """Convenience function to validate entire project integration."""
    validator = IntegrationValidator(frontend_root)
    return validator.validate_complete_project_integration()


