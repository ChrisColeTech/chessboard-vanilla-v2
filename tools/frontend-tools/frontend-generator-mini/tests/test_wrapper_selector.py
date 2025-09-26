#!/usr/bin/env python3
"""
Tests for the Wrapper Selector module
"""

import unittest
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.wrapper_selector import WrapperSelector
from modules.config import PageConfig, ProjectCapabilities, WrapperType


class TestWrapperSelector(unittest.TestCase):
    """Test the Wrapper Selector"""
    
    def setUp(self):
        """Set up test environment"""
        self.selector = WrapperSelector()
    
    def test_select_wrapper_full_hooks(self):
        """Test selecting full hooks wrapper"""
        config = PageConfig(mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        wrapper_type = self.selector.select_wrapper_template(config, capabilities)
        self.assertEqual(wrapper_type, WrapperType.FULL_HOOKS)
    
    def test_select_wrapper_basic_hooks(self):
        """Test selecting basic hooks wrapper"""
        config = PageConfig(mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        
        wrapper_type = self.selector.select_wrapper_template(config, capabilities)
        self.assertEqual(wrapper_type, WrapperType.BASIC_HOOKS)
    
    def test_select_wrapper_no_hooks(self):
        """Test selecting no hooks wrapper"""
        config = PageConfig(mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        wrapper_type = self.selector.select_wrapper_template(config, capabilities)
        self.assertEqual(wrapper_type, WrapperType.NO_HOOKS)
    
    def test_select_wrapper_no_mobile(self):
        """Test selecting no mobile wrapper (edge case)"""
        config = PageConfig(mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=True,
            has_data_table=False
        )
        
        wrapper_type = self.selector.select_wrapper_template(config, capabilities)
        self.assertEqual(wrapper_type, WrapperType.NO_MOBILE)
    
    def test_determine_wrapper_type_full_hooks(self):
        """Test determining wrapper type with full capabilities"""
        wrapper_type = self.selector.determine_wrapper_type(
            has_page_hooks=True,
            has_mobile_hook=True,
            is_mobile=True
        )
        self.assertEqual(wrapper_type, WrapperType.FULL_HOOKS)
    
    def test_determine_wrapper_type_basic_hooks(self):
        """Test determining wrapper type with basic hooks only"""
        wrapper_type = self.selector.determine_wrapper_type(
            has_page_hooks=True,
            has_mobile_hook=False,
            is_mobile=False
        )
        self.assertEqual(wrapper_type, WrapperType.BASIC_HOOKS)
    
    def test_determine_wrapper_type_no_hooks(self):
        """Test determining wrapper type with no hooks"""
        wrapper_type = self.selector.determine_wrapper_type(
            has_page_hooks=False,
            has_mobile_hook=False,
            is_mobile=False
        )
        self.assertEqual(wrapper_type, WrapperType.NO_HOOKS)
    
    def test_get_wrapper_requirements(self):
        """Test getting wrapper requirements"""
        # Test full hooks requirements
        requirements = self.selector.get_wrapper_requirements(WrapperType.FULL_HOOKS)
        self.assertTrue(requirements['requires_page_hooks'])
        self.assertTrue(requirements['requires_mobile_hook'])
        self.assertTrue(requirements['supports_mobile_switching'])
        
        # Test basic hooks requirements
        requirements = self.selector.get_wrapper_requirements(WrapperType.BASIC_HOOKS)
        self.assertTrue(requirements['requires_page_hooks'])
        self.assertFalse(requirements['requires_mobile_hook'])
        self.assertFalse(requirements['supports_mobile_switching'])
        
        # Test no hooks requirements
        requirements = self.selector.get_wrapper_requirements(WrapperType.NO_HOOKS)
        self.assertFalse(requirements['requires_page_hooks'])
        self.assertFalse(requirements['requires_mobile_hook'])
        self.assertFalse(requirements['supports_mobile_switching'])
    
    def test_validate_wrapper_selection_valid(self):
        """Test validation of valid wrapper selection"""
        config = PageConfig(mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        issues = self.selector.validate_wrapper_selection(
            WrapperType.FULL_HOOKS, config, capabilities
        )
        self.assertEqual(len(issues), 0)
    
    def test_validate_wrapper_selection_missing_page_hooks(self):
        """Test validation when page hooks are missing"""
        config = PageConfig(mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        issues = self.selector.validate_wrapper_selection(
            WrapperType.BASIC_HOOKS, config, capabilities
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("requires page hooks", issues[0])
    
    def test_validate_wrapper_selection_missing_mobile_hook(self):
        """Test validation when mobile hook is missing"""
        config = PageConfig(mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        issues = self.selector.validate_wrapper_selection(
            WrapperType.FULL_HOOKS, config, capabilities
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("requires mobile hook", issues[0])
    
    def test_validate_wrapper_selection_mobile_not_supported(self):
        """Test validation when mobile is requested but not supported"""
        config = PageConfig(mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        issues = self.selector.validate_wrapper_selection(
            WrapperType.NO_HOOKS, config, capabilities
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("doesn't support mobile switching", issues[0])
    
    def test_get_wrapper_description(self):
        """Test getting wrapper descriptions"""
        description = self.selector.get_wrapper_description(WrapperType.FULL_HOOKS)
        self.assertIn("Full hooks support", description)
        self.assertIn("mobile/desktop switching", description)
        
        description = self.selector.get_wrapper_description(WrapperType.BASIC_HOOKS)
        self.assertIn("Page hooks only", description)
        
        description = self.selector.get_wrapper_description(WrapperType.NO_HOOKS)
        self.assertIn("Minimal wrapper", description)
        
        description = self.selector.get_wrapper_description("unknown")
        self.assertEqual(description, "Unknown wrapper type")
    
    def test_recommend_wrapper_upgrades(self):
        """Test wrapper upgrade recommendations"""
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        
        recommendations = self.selector.recommend_wrapper_upgrades(capabilities)
        self.assertIn('add_page_hooks', recommendations)
        self.assertIn('add_mobile_hook', recommendations)
        self.assertIn('add_data_table', recommendations)
        
        # Test partial capabilities
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        
        recommendations = self.selector.recommend_wrapper_upgrades(capabilities)
        self.assertNotIn('add_page_hooks', recommendations)
        self.assertIn('add_mobile_hook', recommendations)
        self.assertNotIn('add_data_table', recommendations)
    
    def test_get_all_wrapper_types(self):
        """Test getting all wrapper types"""
        wrapper_types = self.selector.get_all_wrapper_types()
        self.assertEqual(len(wrapper_types), 4)
        self.assertIn(WrapperType.FULL_HOOKS, wrapper_types)
        self.assertIn(WrapperType.BASIC_HOOKS, wrapper_types)
        self.assertIn(WrapperType.NO_HOOKS, wrapper_types)
        self.assertIn(WrapperType.NO_MOBILE, wrapper_types)


if __name__ == '__main__':
    unittest.main()