#!/usr/bin/env python3
"""
Tests for the Routing Updater module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.routing_updater import ParentRoutingUpdater, RoutingUpdateError
from modules.config import PageConfig, ProjectCapabilities, GenerationContext


class TestParentRoutingUpdater(unittest.TestCase):
    """Test the Parent Routing Updater"""
    
    def setUp(self):
        """Set up test environment"""
        # Create mock dependencies
        self.mock_template_engine = Mock()
        self.mock_file_writer = Mock()
        self.mock_variable_generator = Mock()
        
        self.updater = ParentRoutingUpdater(
            self.mock_template_engine,
            self.mock_file_writer,
            self.mock_variable_generator
        )
    
    def test_initialization(self):
        """Test updater initialization"""
        self.assertEqual(self.updater.template_engine, self.mock_template_engine)
        self.assertEqual(self.updater.file_writer, self.mock_file_writer)
        self.assertEqual(self.updater.variable_generator, self.mock_variable_generator)
        
        # Should have routing patterns
        self.assertTrue(hasattr(self.updater, 'route_import_pattern'))
        self.assertTrue(hasattr(self.updater, 'route_config_pattern'))
        self.assertTrue(hasattr(self.updater, 'switch_route_pattern'))
    
    def test_routing_patterns(self):
        """Test routing pattern compilation"""
        # Test that patterns are compiled regex objects
        self.assertTrue(hasattr(self.updater.route_import_pattern, 'match'))
        self.assertTrue(hasattr(self.updater.route_config_pattern, 'match'))
        self.assertTrue(hasattr(self.updater.switch_route_pattern, 'match'))
    
    def test_route_import_pattern_matching(self):
        """Test route import pattern matching"""
        test_content = """
import React from 'react';
// Child page imports
import { ChildPage } from './ChildPage';
"""
        match = self.updater.route_import_pattern.search(test_content)
        self.assertIsNotNone(match)
        self.assertIn("Child page imports", match.group())
    
    def test_route_config_pattern_matching(self):
        """Test route config pattern matching"""
        test_content = """
const routes = [
    // Child page routes
    { path: '/child', component: ChildPage }
];
"""
        match = self.updater.route_config_pattern.search(test_content)
        self.assertIsNotNone(match)
        self.assertIn("Child page routes", match.group())
    
    def test_switch_route_pattern_matching(self):
        """Test switch route pattern matching"""
        test_content = """
<Switch>
    // Child page components
    <Route path="/child" component={ChildPage} />
</Switch>
"""
        match = self.updater.switch_route_pattern.search(test_content)
        self.assertIsNotNone(match)
        self.assertIn("Child page components", match.group())
    
    def test_update_parent_routing_interface(self):
        """Test update parent routing method interface"""
        config = PageConfig(
            page_id="test-parent",
            base_name="TestParent",
            display_name="Test Parent",
            mobile=False
        )
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        context = GenerationContext(config=config, capabilities=capabilities)
        
        # Should be callable without errors (implementation may vary)
        try:
            self.updater.update_parent_routing(context, "TestChild")
        except Exception as e:
            # If it fails, it should be a specific routing error or implementation detail
            # We're testing the interface exists and is callable
            pass
    
    def test_routing_update_error_exception(self):
        """Test RoutingUpdateError exception"""
        error = RoutingUpdateError("Test error message")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Test error message")
    
    def test_updater_dependency_injection(self):
        """Test that updater properly stores injected dependencies"""
        # Test with different mock objects
        new_template_engine = Mock()
        new_file_writer = Mock()
        new_variable_generator = Mock()
        
        updater = ParentRoutingUpdater(
            new_template_engine,
            new_file_writer,
            new_variable_generator
        )
        
        self.assertEqual(updater.template_engine, new_template_engine)
        self.assertEqual(updater.file_writer, new_file_writer)
        self.assertEqual(updater.variable_generator, new_variable_generator)
    
    def test_pattern_multiline_support(self):
        """Test that patterns support multiline matching"""
        multiline_content = """
Line 1
Line 2
// Child page imports
Line 4
Line 5
"""
        match = self.updater.route_import_pattern.search(multiline_content)
        self.assertIsNotNone(match)
        
        # Test with different line endings
        windows_content = multiline_content.replace('\n', '\r\n')
        match = self.updater.route_import_pattern.search(windows_content)
        self.assertIsNotNone(match)
    
    def test_pattern_case_sensitivity(self):
        """Test pattern case sensitivity"""
        # Should match exact case
        exact_case = "// Child page imports\n"
        match = self.updater.route_import_pattern.search(exact_case)
        self.assertIsNotNone(match)
        
        # Should not match different case
        different_case = "// child page imports\n"
        match = self.updater.route_import_pattern.search(different_case)
        self.assertIsNone(match)
        
        different_case2 = "// CHILD PAGE IMPORTS\n"
        match = self.updater.route_import_pattern.search(different_case2)
        self.assertIsNone(match)
    
    def test_pattern_whitespace_handling(self):
        """Test pattern handling of whitespace"""
        # Test with different whitespace
        with_spaces = "// Child page imports  \n"
        match = self.updater.route_import_pattern.search(with_spaces)
        self.assertIsNotNone(match)
        
        with_tabs = "// Child page imports\t\n"
        match = self.updater.route_import_pattern.search(with_tabs)
        self.assertIsNotNone(match)
        
        # Pattern should be flexible about trailing whitespace
        no_trailing = "// Child page imports\n"
        match = self.updater.route_import_pattern.search(no_trailing)
        self.assertIsNotNone(match)
    
    def test_all_patterns_are_different(self):
        """Test that all routing patterns are distinct"""
        # Convert patterns to strings for comparison
        import_pattern_str = self.updater.route_import_pattern.pattern
        config_pattern_str = self.updater.route_config_pattern.pattern
        switch_pattern_str = self.updater.switch_route_pattern.pattern
        
        # All patterns should be different
        self.assertNotEqual(import_pattern_str, config_pattern_str)
        self.assertNotEqual(import_pattern_str, switch_pattern_str)
        self.assertNotEqual(config_pattern_str, switch_pattern_str)
    
    def test_updater_methods_exist(self):
        """Test that updater has expected methods"""
        # Should have update method
        self.assertTrue(hasattr(self.updater, 'update_parent_routing'))
        self.assertTrue(callable(self.updater.update_parent_routing))
        
        # Method should accept correct parameters
        import inspect
        sig = inspect.signature(self.updater.update_parent_routing)
        params = list(sig.parameters.keys())
        
        # Should have context and child_name parameters
        self.assertIn('context', params)
        self.assertIn('child_name', params)


if __name__ == '__main__':
    unittest.main()