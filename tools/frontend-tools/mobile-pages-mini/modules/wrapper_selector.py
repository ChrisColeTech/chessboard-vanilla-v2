"""
Wrapper Selector for choosing appropriate child wrapper templates based on capabilities.
"""

from typing import Dict
try:
    from .config import PageConfig, ProjectCapabilities, WrapperType
except ImportError:
    from config import PageConfig, ProjectCapabilities, WrapperType


class WrapperSelector:
    """Selects appropriate wrapper templates based on project capabilities."""
    
    def select_wrapper_template(self, config: PageConfig, capabilities: ProjectCapabilities) -> str:
        """
        Select appropriate child wrapper template based on project capabilities.
        
        Args:
            config: Page configuration
            capabilities: Detected project capabilities
            
        Returns:
            Template name for the wrapper
        """
        # Full hooks + mobile support
        if config.mobile and capabilities.has_page_hooks and capabilities.has_mobile_hook:
            return WrapperType.FULL_HOOKS
            
        # Page hooks only (no mobile)  
        elif capabilities.has_page_hooks and not capabilities.has_mobile_hook:
            return WrapperType.BASIC_HOOKS
            
        # No hooks, no mobile
        elif not capabilities.has_page_hooks and not capabilities.has_mobile_hook:
            return WrapperType.NO_HOOKS
            
        # Has mobile hook but not page hooks (unusual case)
        else:
            return WrapperType.NO_MOBILE
    
    def determine_wrapper_type(self, has_page_hooks: bool, has_mobile_hook: bool, is_mobile: bool) -> str:
        """
        Determine wrapper type based on individual capability flags.
        
        Args:
            has_page_hooks: Whether page hooks are available
            has_mobile_hook: Whether mobile hook is available
            is_mobile: Whether mobile variant is requested
            
        Returns:
            Wrapper type constant
        """
        if is_mobile and has_page_hooks and has_mobile_hook:
            return WrapperType.FULL_HOOKS
        elif has_page_hooks and not has_mobile_hook:
            return WrapperType.BASIC_HOOKS
        elif not has_page_hooks and not has_mobile_hook:
            return WrapperType.NO_HOOKS
        else:
            return WrapperType.NO_MOBILE
    
    def get_wrapper_requirements(self, wrapper_type: str) -> Dict[str, bool]:
        """
        Get the capability requirements for a wrapper type.
        
        Args:
            wrapper_type: Wrapper type constant
            
        Returns:
            Dictionary of capability requirements
        """
        requirements = {
            WrapperType.FULL_HOOKS: {
                'requires_page_hooks': True,
                'requires_mobile_hook': True,
                'supports_mobile_switching': True
            },
            WrapperType.BASIC_HOOKS: {
                'requires_page_hooks': True,
                'requires_mobile_hook': False,
                'supports_mobile_switching': False
            },
            WrapperType.NO_HOOKS: {
                'requires_page_hooks': False,
                'requires_mobile_hook': False,
                'supports_mobile_switching': False
            },
            WrapperType.NO_MOBILE: {
                'requires_page_hooks': False,
                'requires_mobile_hook': True,
                'supports_mobile_switching': True
            }
        }
        
        return requirements.get(wrapper_type, {})
    
    def validate_wrapper_selection(self, wrapper_type: str, config: PageConfig, capabilities: ProjectCapabilities) -> list:
        """
        Validate that the selected wrapper type is compatible with project capabilities.
        
        Args:
            wrapper_type: Selected wrapper type
            config: Page configuration
            capabilities: Project capabilities
            
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        requirements = self.get_wrapper_requirements(wrapper_type)
        
        # Check page hooks requirement
        if requirements.get('requires_page_hooks', False) and not capabilities.has_page_hooks:
            issues.append(f"Wrapper type {wrapper_type} requires page hooks, but they are not available")
        
        # Check mobile hook requirement
        if requirements.get('requires_mobile_hook', False) and not capabilities.has_mobile_hook:
            issues.append(f"Wrapper type {wrapper_type} requires mobile hook, but it is not available")
        
        # Check mobile support vs request
        if config.mobile and not requirements.get('supports_mobile_switching', False):
            issues.append(f"Mobile variant requested, but wrapper type {wrapper_type} doesn't support mobile switching")
        
        return issues
    
    def get_wrapper_description(self, wrapper_type: str) -> str:
        """Get human-readable description of wrapper type."""
        descriptions = {
            WrapperType.FULL_HOOKS: "Full hooks support with mobile/desktop switching",
            WrapperType.BASIC_HOOKS: "Page hooks only (usePageInstructions, usePageActions)",
            WrapperType.NO_HOOKS: "Minimal wrapper with no hooks",
            WrapperType.NO_MOBILE: "Mobile hook available but no page hooks (placeholder mobile detection)"
        }
        
        return descriptions.get(wrapper_type, "Unknown wrapper type")
    
    def recommend_wrapper_upgrades(self, current_capabilities: ProjectCapabilities) -> Dict[str, str]:
        """
        Recommend wrapper upgrades based on missing capabilities.
        
        Args:
            current_capabilities: Current project capabilities
            
        Returns:
            Dictionary of recommendations
        """
        recommendations = {}
        
        if not current_capabilities.has_page_hooks:
            recommendations['add_page_hooks'] = (
                "Add usePageInstructions and usePageActions hooks to enable automatic "
                "context switching for page instructions and action sheets"
            )
        
        if not current_capabilities.has_mobile_hook:
            recommendations['add_mobile_hook'] = (
                "Add useIsMobile hook to enable automatic mobile/desktop switching "
                "within child page wrappers"
            )
        
        if not current_capabilities.has_data_table:
            recommendations['add_data_table'] = (
                "Add DataTable component to enable data visualization in generated pages"
            )
        
        return recommendations
    
    def get_all_wrapper_types(self) -> list:
        """Get all available wrapper types."""
        return [
            WrapperType.FULL_HOOKS,
            WrapperType.BASIC_HOOKS, 
            WrapperType.NO_HOOKS,
            WrapperType.NO_MOBILE
        ]