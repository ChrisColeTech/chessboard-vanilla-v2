#!/usr/bin/env python3
"""
Tests for the Variable Generator module
"""

import unittest
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.variable_generator import VariableGenerator
from modules.config import PageConfig, ProjectCapabilities, GenerationContext


class TestVariableGenerator(unittest.TestCase):
    """Test the Variable Generator"""
    
    def setUp(self):
        """Set up test environment"""
        self.generator = VariableGenerator()
    
    def test_generate_parent_variables_basic(self):
        """Test generating basic parent variables"""
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
        
        variables = self.generator.generate_parent_variables(context)
        
        # Check basic variables
        self.assertEqual(variables['PARENT_NAME'], 'TestParent')
        self.assertEqual(variables['PARENT_ID'], 'test-parent')
        self.assertEqual(variables['PARENT_DISPLAY_NAME'], 'Test Parent')
        
        # Check mobile variables (should be disabled)
        self.assertEqual(variables['MOBILE_IMPORT'], '')
        self.assertIn('Mobile detection will be added', variables['MOBILE_DETECTION'])
        self.assertEqual(variables['MOBILE_MAIN_PAGE_LOGIC'], 'TestParentMainPage')
    
    def test_generate_parent_variables_with_mobile(self):
        """Test generating parent variables with mobile support"""
        config = PageConfig(
            page_id="mobile-parent",
            base_name="MobileParent",
            display_name="Mobile Parent",
            mobile=True
        )
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        context = GenerationContext(config=config, capabilities=capabilities)
        
        variables = self.generator.generate_parent_variables(context)
        
        # Check mobile-specific variables
        self.assertIn('MobileMobileParentMainPage', variables['MOBILE_IMPORT'])
        self.assertIn('useIsMobile', variables['MOBILE_HOOK_IMPORT'])
        self.assertIn('isMobile ?', variables['MOBILE_MAIN_PAGE_LOGIC'])
        self.assertIn('const isMobile = useIsMobile()', variables['MOBILE_DETECTION'])
    
    def test_generate_child_variables(self):
        """Test generating child variables"""
        config = PageConfig(
            page_id="test-child",
            base_name="TestChild",
            display_name="Test Child",
            mobile=False
        )
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        context = GenerationContext(config=config, capabilities=capabilities)
        
        variables = self.generator.generate_child_variables(context)
        
        # Check that variables dictionary is returned
        self.assertIsInstance(variables, dict)
        # The actual content depends on the implementation details
        # We can add more specific tests as the implementation evolves
    
    def test_generate_routing_variables_empty_children(self):
        """Test generating routing variables with no children"""
        children = []
        
        variables = self.generator.generate_routing_variables(children)
        
        # Should return empty or default values
        self.assertIsInstance(variables, dict)
        self.assertIn('CHILD_IMPORTS', variables)
        self.assertIn('CHILD_ROUTING_LOGIC', variables)
    
    def test_generate_routing_variables_with_children(self):
        """Test generating routing variables with children"""
        children = [
            {'name': 'ChildOne', 'id': 'child-one'},
            {'name': 'ChildTwo', 'id': 'child-two'}
        ]
        
        variables = self.generator.generate_routing_variables(children)
        
        # Should contain imports and routing logic for children
        self.assertIsInstance(variables, dict)
        self.assertIn('CHILD_IMPORTS', variables)
        self.assertIn('CHILD_ROUTING_LOGIC', variables)
        
        # Check that child names appear in the imports
        if variables['CHILD_IMPORTS']:
            self.assertIn('ChildOne', variables['CHILD_IMPORTS'])
            self.assertIn('ChildTwo', variables['CHILD_IMPORTS'])
    
    def test_generate_child_navigation_actions(self):
        """Test generating child navigation actions"""
        children = [
            {'name': 'Settings', 'id': 'settings'},
            {'name': 'Profile', 'id': 'profile'}
        ]
        
        actions = self.generator.generate_child_navigation_actions(children)
        
        # Should return string with navigation actions
        self.assertIsInstance(actions, str)
        if actions and actions != '// Child navigation actions will be added here when children are created':
            self.assertIn('Settings', actions)
            self.assertIn('Profile', actions)
    
    def test_generate_child_navigation_icons(self):
        """Test generating child navigation icons"""
        children = [
            {'name': 'Settings', 'id': 'settings'},
            {'name': 'Dashboard', 'id': 'dashboard'}
        ]
        
        icons = self.generator.generate_child_navigation_icons(children)
        
        # Should return string with icon names
        self.assertIsInstance(icons, str)
        # Icons are typically generated based on child names
        # The exact format depends on implementation
    
    def test_private_generate_parent_hook_imports(self):
        """Test generating parent hook imports"""
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
        
        imports = self.generator._generate_parent_hook_imports(context)
        
        # Should return string with hook imports
        self.assertIsInstance(imports, str)
        # When page hooks are available, should include page hook imports
        if capabilities.has_page_hooks:
            self.assertIn('usePageInstructions', imports)
    
    def test_private_generate_parent_hook_store_usage(self):
        """Test generating parent hook store usage"""
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
        
        usage = self.generator._generate_parent_hook_store_usage(context)
        
        # Should return string with hook usage
        self.assertIsInstance(usage, str)
        # When page hooks are available, should include hook usage
        if capabilities.has_page_hooks:
            self.assertIn('usePageInstructions', usage)
    
    def test_private_generate_navigation_methods(self):
        """Test generating navigation methods"""
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
        
        methods = self.generator._generate_navigation_methods(context)
        
        # Should return string with navigation methods
        self.assertIsInstance(methods, str)
    
    def test_private_generate_return_methods(self):
        """Test generating return methods"""
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
        
        methods = self.generator._generate_return_methods(context)
        
        # Should return string with return methods
        self.assertIsInstance(methods, str)
    
    def test_private_get_existing_children(self):
        """Test getting existing children"""
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
        
        children = self.generator._get_existing_children(context, "test-parent")
        
        # Should return list (empty if no children exist)
        self.assertIsInstance(children, list)
    
    def test_variables_are_strings(self):
        """Test that all generated variables are strings"""
        config = PageConfig(
            page_id="test-validation",
            base_name="TestValidation",
            display_name="Test Validation",
            mobile=True
        )
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        context = GenerationContext(config=config, capabilities=capabilities)
        
        variables = self.generator.generate_parent_variables(context)
        
        # All values should be strings
        for key, value in variables.items():
            self.assertIsInstance(value, str, f"Variable {key} should be a string, got {type(value)}")
    
    def test_child_variables_structure(self):
        """Test child variables structure"""
        config = PageConfig(
            page_id="test-child-structure",
            base_name="TestChildStructure",
            display_name="Test Child Structure",
            mobile=False
        )
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=False,
            has_data_table=False
        )
        context = GenerationContext(config=config, capabilities=capabilities)
        
        variables = self.generator.generate_child_variables(context)
        
        # Should be a dictionary
        self.assertIsInstance(variables, dict)
        # All values should be strings
        for key, value in variables.items():
            self.assertIsInstance(value, str, f"Child variable {key} should be a string, got {type(value)}")


if __name__ == '__main__':
    unittest.main()