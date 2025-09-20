#!/usr/bin/env python3
"""
Test suite for the Variable Generator module.
"""

import unittest
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.variable_generator import VariableGenerator
from modules.config import PageConfig, ProjectCapabilities, GenerationContext, WrapperType


class TestVariableGenerator(unittest.TestCase):
    """Test cases for VariableGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = VariableGenerator()
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_generate_parent_variables(self):
        """Test parent variable generation."""
        config = PageConfig(name="SettingsPage", parent=None, mobile=False)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.temp_dir / "templates"
        )
        
        variables = self.generator.generate_parent_variables(context)
        
        # Check required parent variables
        self.assertEqual(variables['PAGE_NAME'], 'SettingsPage')
        self.assertEqual(variables['BASE_NAME'], 'Settings')
        self.assertEqual(variables['PARENT_ID'], 'settings')
        self.assertIn('GENERATOR_NAME', variables)
        self.assertIn('TIMESTAMP', variables)
    
    def test_generate_child_variables(self):
        """Test child variable generation."""
        config = PageConfig(name="UserProfile", parent="Settings", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=False,
            has_data_table=True
        )
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.temp_dir / "templates"
        )
        
        variables = self.generator.generate_child_variables(context)
        
        # Check required child variables
        self.assertEqual(variables['CHILD_NAME'], 'UserProfile')
        self.assertEqual(variables['PARENT_NAME'], 'Settings')
        self.assertEqual(variables['PARENT_ID'], 'settings')
        self.assertEqual(variables['CHILD_ID'], 'userprofile')
        self.assertEqual(variables['HAS_MOBILE'], 'true')
    
    def test_generate_wrapper_variables(self):
        """Test wrapper variable generation."""
        config = PageConfig(name="UserProfile", parent="Settings", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.temp_dir / "templates"
        )
        
        wrapper_type = WrapperType.FULL_HOOKS
        variables = self.generator.generate_wrapper_variables(context, wrapper_type)
        
        # Check wrapper-specific variables
        self.assertEqual(variables['WRAPPER_TYPE'], wrapper_type)
        self.assertEqual(variables['HAS_PAGE_HOOKS'], 'true')
        self.assertEqual(variables['HAS_MOBILE_HOOK'], 'true')
    
    def test_variable_name_normalization(self):
        """Test that variable names are properly normalized."""
        config = PageConfig(name="Complex-Page_Name", parent="Parent-With_Special", mobile=False)
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.temp_dir / "templates"
        )
        
        variables = self.generator.generate_parent_variables(context)
        
        # Check normalization
        self.assertEqual(variables['PARENT_ID'], 'parent-with_special')
        self.assertIn('PAGE_NAME', variables)
    
    def test_boolean_string_conversion(self):
        """Test that booleans are converted to lowercase strings for templates."""
        config = PageConfig(name="TestPage", mobile=True)
        capabilities = ProjectCapabilities(
            has_page_hooks=False,
            has_mobile_hook=True,
            has_data_table=False
        )
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.temp_dir / "templates"
        )
        
        variables = self.generator.generate_parent_variables(context)
        
        # Check boolean conversions
        self.assertEqual(variables['HAS_PAGE_HOOKS'], 'false')
        self.assertEqual(variables['HAS_MOBILE_HOOK'], 'true')
        self.assertEqual(variables['HAS_DATA_TABLE'], 'false')


if __name__ == '__main__':
    unittest.main()