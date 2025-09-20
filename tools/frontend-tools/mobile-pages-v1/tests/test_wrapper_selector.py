"""
Tests for the Wrapper Selector module.
"""

import pytest
from pathlib import Path
import os
import sys

# Add the modules directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from wrapper_selector import WrapperSelector
from config import PageConfig, ProjectCapabilities, WrapperType


class TestWrapperSelector:
    """Test cases for WrapperSelector class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.wrapper_selector = WrapperSelector()
    
    def test_select_wrapper_template_full_hooks(self):
        """Test selection of full hooks wrapper template."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        result = self.wrapper_selector.select_wrapper_template(config, capabilities)
        
        assert result == WrapperType.FULL_HOOKS
    
    def test_select_wrapper_template_basic_hooks(self):
        """Test selection of basic hooks wrapper template."""
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        
        result = self.wrapper_selector.select_wrapper_template(config, capabilities)
        
        assert result == WrapperType.BASIC_HOOKS
    
    def test_select_wrapper_template_no_hooks(self):
        """Test selection of no hooks wrapper template."""
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        result = self.wrapper_selector.select_wrapper_template(config, capabilities)
        
        assert result == WrapperType.NO_HOOKS
    
    def test_select_wrapper_template_no_mobile(self):
        """Test selection of no mobile wrapper template (unusual case)."""
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=True,  # Has mobile but not page hooks
            has_data_table=False
        )
        
        result = self.wrapper_selector.select_wrapper_template(config, capabilities)
        
        assert result == WrapperType.NO_MOBILE
    
    def test_select_wrapper_template_mobile_request_no_mobile_hook(self):
        """Test mobile request when no mobile hook available falls back to basic hooks."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,  # No mobile hook available
            has_data_table=True
        )
        
        result = self.wrapper_selector.select_wrapper_template(config, capabilities)
        
        # Should fall back to basic hooks since mobile hook is not available
        assert result == WrapperType.BASIC_HOOKS
    
    def test_determine_wrapper_type_full_hooks(self):
        """Test wrapper type determination with full hooks."""
        result = self.wrapper_selector.determine_wrapper_type(
            has_page_hooks=True,
            has_mobile_hook=True,
            is_mobile=True
        )
        
        assert result == WrapperType.FULL_HOOKS
    
    def test_determine_wrapper_type_basic_hooks(self):
        """Test wrapper type determination with basic hooks."""
        result = self.wrapper_selector.determine_wrapper_type(
            has_page_hooks=True,
            has_mobile_hook=False,
            is_mobile=False
        )
        
        assert result == WrapperType.BASIC_HOOKS
    
    def test_determine_wrapper_type_no_hooks(self):
        """Test wrapper type determination with no hooks."""
        result = self.wrapper_selector.determine_wrapper_type(
            has_page_hooks=False,
            has_mobile_hook=False,
            is_mobile=False
        )
        
        assert result == WrapperType.NO_HOOKS
    
    def test_determine_wrapper_type_no_mobile(self):
        """Test wrapper type determination for no mobile case."""
        result = self.wrapper_selector.determine_wrapper_type(
            has_page_hooks=False,
            has_mobile_hook=True,
            is_mobile=False
        )
        
        assert result == WrapperType.NO_MOBILE
    
    def test_get_wrapper_requirements_full_hooks(self):
        """Test getting requirements for full hooks wrapper."""
        requirements = self.wrapper_selector.get_wrapper_requirements(WrapperType.FULL_HOOKS)
        
        expected = {
            'requires_page_hooks': True,
            'requires_mobile_hook': True,
            'supports_mobile_switching': True
        }
        assert requirements == expected
    
    def test_get_wrapper_requirements_basic_hooks(self):
        """Test getting requirements for basic hooks wrapper."""
        requirements = self.wrapper_selector.get_wrapper_requirements(WrapperType.BASIC_HOOKS)
        
        expected = {
            'requires_page_hooks': True,
            'requires_mobile_hook': False,
            'supports_mobile_switching': False
        }
        assert requirements == expected
    
    def test_get_wrapper_requirements_no_hooks(self):
        """Test getting requirements for no hooks wrapper."""
        requirements = self.wrapper_selector.get_wrapper_requirements(WrapperType.NO_HOOKS)
        
        expected = {
            'requires_page_hooks': False,
            'requires_mobile_hook': False,
            'supports_mobile_switching': False
        }
        assert requirements == expected
    
    def test_get_wrapper_requirements_no_mobile(self):
        """Test getting requirements for no mobile wrapper."""
        requirements = self.wrapper_selector.get_wrapper_requirements(WrapperType.NO_MOBILE)
        
        expected = {
            'requires_page_hooks': False,
            'requires_mobile_hook': True,
            'supports_mobile_switching': True
        }
        assert requirements == expected
    
    def test_get_wrapper_requirements_unknown_type(self):
        """Test getting requirements for unknown wrapper type."""
        requirements = self.wrapper_selector.get_wrapper_requirements("unknown-wrapper-type")
        
        assert requirements == {}
    
    def test_validate_wrapper_selection_valid(self):
        """Test validation of valid wrapper selection."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        issues = self.wrapper_selector.validate_wrapper_selection(
            WrapperType.FULL_HOOKS, config, capabilities
        )
        
        assert issues == []  # No issues should be found
    
    def test_validate_wrapper_selection_missing_page_hooks(self):
        """Test validation when page hooks are required but missing."""
        config = PageConfig(name="TestPage", mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,  # Missing page hooks
            has_mobile_hook=False,
            has_data_table=False
        )
        
        issues = self.wrapper_selector.validate_wrapper_selection(
            WrapperType.BASIC_HOOKS, config, capabilities  # Requires page hooks
        )
        
        assert len(issues) == 1
        assert "requires page hooks, but they are not available" in issues[0]
    
    def test_validate_wrapper_selection_missing_mobile_hook(self):
        """Test validation when mobile hook is required but missing."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,  # Missing mobile hook
            has_data_table=True
        )
        
        issues = self.wrapper_selector.validate_wrapper_selection(
            WrapperType.FULL_HOOKS, config, capabilities  # Requires mobile hook
        )
        
        assert len(issues) == 1
        assert "requires mobile hook, but it is not available" in issues[0]
    
    def test_validate_wrapper_selection_mobile_request_no_support(self):
        """Test validation when mobile is requested but wrapper doesn't support it."""
        config = PageConfig(name="TestPage", mobile=True)  # Mobile requested
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        
        issues = self.wrapper_selector.validate_wrapper_selection(
            WrapperType.BASIC_HOOKS, config, capabilities  # Doesn't support mobile switching
        )
        
        assert len(issues) == 1
        assert "doesn't support mobile switching" in issues[0]
    
    def test_validate_wrapper_selection_multiple_issues(self):
        """Test validation with multiple issues."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,  # Missing page hooks
            has_mobile_hook=False,  # Missing mobile hook
            has_data_table=False
        )
        
        issues = self.wrapper_selector.validate_wrapper_selection(
            WrapperType.FULL_HOOKS, config, capabilities  # Requires both
        )
        
        assert len(issues) == 3  # Two missing requirements + mobile support issue
        issue_text = ' '.join(issues)
        assert "requires page hooks" in issue_text
        assert "requires mobile hook" in issue_text
        assert "doesn't support mobile switching" in issue_text
    
    def test_get_wrapper_description_all_types(self):
        """Test getting descriptions for all wrapper types."""
        descriptions = {
            WrapperType.FULL_HOOKS: self.wrapper_selector.get_wrapper_description(WrapperType.FULL_HOOKS),
            WrapperType.BASIC_HOOKS: self.wrapper_selector.get_wrapper_description(WrapperType.BASIC_HOOKS),
            WrapperType.NO_HOOKS: self.wrapper_selector.get_wrapper_description(WrapperType.NO_HOOKS),
            WrapperType.NO_MOBILE: self.wrapper_selector.get_wrapper_description(WrapperType.NO_MOBILE)
        }
        
        # Verify all descriptions are non-empty and descriptive
        assert "Full hooks support with mobile/desktop switching" in descriptions[WrapperType.FULL_HOOKS]
        assert "Page hooks only" in descriptions[WrapperType.BASIC_HOOKS]
        assert "Minimal wrapper with no hooks" in descriptions[WrapperType.NO_HOOKS]
        assert "Mobile hook available but no page hooks" in descriptions[WrapperType.NO_MOBILE]
    
    def test_get_wrapper_description_unknown_type(self):
        """Test getting description for unknown wrapper type."""
        description = self.wrapper_selector.get_wrapper_description("unknown-type")
        
        assert description == "Unknown wrapper type"
    
    def test_recommend_wrapper_upgrades_no_capabilities(self):
        """Test upgrade recommendations when no capabilities are present."""
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        recommendations = self.wrapper_selector.recommend_wrapper_upgrades(capabilities)
        
        assert 'add_page_hooks' in recommendations
        assert 'add_mobile_hook' in recommendations
        assert 'add_data_table' in recommendations
        
        # Check that recommendations contain helpful guidance
        assert "usePageInstructions and usePageActions" in recommendations['add_page_hooks']
        assert "useIsMobile hook" in recommendations['add_mobile_hook']
        assert "DataTable component" in recommendations['add_data_table']
    
    def test_recommend_wrapper_upgrades_partial_capabilities(self):
        """Test upgrade recommendations when some capabilities are present."""
        capabilities = ProjectCapabilities(
            has_page_hooks=True,  # Has this
            has_mobile_hook=False,  # Missing this
            has_data_table=True   # Has this
        )
        
        recommendations = self.wrapper_selector.recommend_wrapper_upgrades(capabilities)
        
        # Should only recommend missing mobile hook
        assert 'add_page_hooks' not in recommendations  # Already has
        assert 'add_mobile_hook' in recommendations     # Missing
        assert 'add_data_table' not in recommendations  # Already has
    
    def test_recommend_wrapper_upgrades_all_capabilities(self):
        """Test upgrade recommendations when all capabilities are present."""
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        recommendations = self.wrapper_selector.recommend_wrapper_upgrades(capabilities)
        
        # Should have no recommendations
        assert recommendations == {}
    
    def test_get_all_wrapper_types(self):
        """Test getting all available wrapper types."""
        wrapper_types = self.wrapper_selector.get_all_wrapper_types()
        
        expected_types = [
            WrapperType.FULL_HOOKS,
            WrapperType.BASIC_HOOKS,
            WrapperType.NO_HOOKS,
            WrapperType.NO_MOBILE
        ]
        
        assert wrapper_types == expected_types
    
    def test_wrapper_selection_consistency(self):
        """Test that wrapper selection is consistent between methods."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        # Both methods should return the same result
        method1_result = self.wrapper_selector.select_wrapper_template(config, capabilities)
        method2_result = self.wrapper_selector.determine_wrapper_type(
            capabilities.has_page_hooks,
            capabilities.has_mobile_hook,
            config.mobile
        )
        
        assert method1_result == method2_result == WrapperType.FULL_HOOKS
    
    def test_edge_case_mobile_requested_only_mobile_hook(self):
        """Test edge case where mobile is requested but only mobile hook is available."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=True,  # Only mobile hook available
            has_data_table=False
        )
        
        wrapper_type = self.wrapper_selector.select_wrapper_template(config, capabilities)
        assert wrapper_type == WrapperType.NO_MOBILE
        
        # This should generate validation issues
        issues = self.wrapper_selector.validate_wrapper_selection(wrapper_type, config, capabilities)
        
        # Should have issue about mobile being requested but not supported by wrapper
        # (since NO_MOBILE wrapper supports switching but mobile was requested)
        assert len(issues) == 0  # Actually this case should be valid since NO_MOBILE supports mobile switching
    
    def test_wrapper_requirements_coverage(self):
        """Test that all wrapper types have requirement definitions."""
        all_types = self.wrapper_selector.get_all_wrapper_types()
        
        for wrapper_type in all_types:
            requirements = self.wrapper_selector.get_wrapper_requirements(wrapper_type)
            
            # Each wrapper should have requirement definitions
            assert isinstance(requirements, dict)
            assert len(requirements) > 0
            
            # Should have the standard requirement keys
            expected_keys = ['requires_page_hooks', 'requires_mobile_hook', 'supports_mobile_switching']
            for key in expected_keys:
                assert key in requirements
                assert isinstance(requirements[key], bool)