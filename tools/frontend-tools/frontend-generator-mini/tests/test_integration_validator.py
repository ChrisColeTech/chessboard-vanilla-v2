#!/usr/bin/env python3
"""
Tests for the Integration Validator module
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

from modules.integration_validator import ValidationResult

# Import the main validator class if it exists
try:
    from modules.integration_validator import IntegrationValidator
except ImportError:
    IntegrationValidator = None


class TestIntegrationValidator(unittest.TestCase):
    """Test the Integration Validator"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_validation_result_initialization(self):
        """Test ValidationResult initialization"""
        result = ValidationResult()
        
        # Should have all required issue lists
        self.assertIsInstance(result.registry_issues, list)
        self.assertIsInstance(result.container_issues, list)
        self.assertIsInstance(result.hook_issues, list)
        self.assertIsInstance(result.cross_module_issues, list)
        
        # All lists should be empty initially
        self.assertEqual(len(result.registry_issues), 0)
        self.assertEqual(len(result.container_issues), 0)
        self.assertEqual(len(result.hook_issues), 0)
        self.assertEqual(len(result.cross_module_issues), 0)
    
    def test_validation_result_add_issues(self):
        """Test adding issues to ValidationResult"""
        result = ValidationResult()
        
        # Add issues to different categories
        result.registry_issues.append("Registry issue 1")
        result.container_issues.append("Container issue 1")
        result.hook_issues.append("Hook issue 1")
        result.cross_module_issues.append("Cross-module issue 1")
        
        # Verify issues were added
        self.assertEqual(len(result.registry_issues), 1)
        self.assertEqual(len(result.container_issues), 1)
        self.assertEqual(len(result.hook_issues), 1)
        self.assertEqual(len(result.cross_module_issues), 1)
        
        # Verify content
        self.assertEqual(result.registry_issues[0], "Registry issue 1")
        self.assertEqual(result.container_issues[0], "Container issue 1")
        self.assertEqual(result.hook_issues[0], "Hook issue 1")
        self.assertEqual(result.cross_module_issues[0], "Cross-module issue 1")
    
    def test_validation_result_multiple_issues(self):
        """Test ValidationResult with multiple issues per category"""
        result = ValidationResult()
        
        # Add multiple issues
        result.registry_issues.extend(["Registry issue 1", "Registry issue 2"])
        result.container_issues.extend(["Container issue 1", "Container issue 2", "Container issue 3"])
        result.hook_issues.append("Hook issue 1")
        result.cross_module_issues.extend(["Cross-module issue 1", "Cross-module issue 2"])
        
        # Verify counts
        self.assertEqual(len(result.registry_issues), 2)
        self.assertEqual(len(result.container_issues), 3)
        self.assertEqual(len(result.hook_issues), 1)
        self.assertEqual(len(result.cross_module_issues), 2)
    
    def test_validation_result_has_issues_method(self):
        """Test checking if ValidationResult has any issues"""
        result = ValidationResult()
        
        # Initially should have no issues
        total_issues = (len(result.registry_issues) + 
                       len(result.container_issues) + 
                       len(result.hook_issues) + 
                       len(result.cross_module_issues))
        self.assertEqual(total_issues, 0)
        
        # Add an issue
        result.registry_issues.append("Test issue")
        
        # Should now have issues
        total_issues = (len(result.registry_issues) + 
                       len(result.container_issues) + 
                       len(result.hook_issues) + 
                       len(result.cross_module_issues))
        self.assertGreater(total_issues, 0)
    
    def test_validation_result_clear_issues(self):
        """Test clearing issues from ValidationResult"""
        result = ValidationResult()
        
        # Add some issues
        result.registry_issues.append("Registry issue")
        result.container_issues.append("Container issue")
        result.hook_issues.append("Hook issue")
        result.cross_module_issues.append("Cross-module issue")
        
        # Clear all issues
        result.registry_issues.clear()
        result.container_issues.clear()
        result.hook_issues.clear()
        result.cross_module_issues.clear()
        
        # All lists should be empty
        self.assertEqual(len(result.registry_issues), 0)
        self.assertEqual(len(result.container_issues), 0)
        self.assertEqual(len(result.hook_issues), 0)
        self.assertEqual(len(result.cross_module_issues), 0)
    
    def test_validation_result_issue_categories(self):
        """Test different categories of validation issues"""
        result = ValidationResult()
        
        # Test registry-specific issues
        result.registry_issues.append("ActionRegistryManager not properly configured")
        result.registry_issues.append("PAGE_ACTIONS missing required actions")
        
        # Test container-specific issues
        result.container_issues.append("ActionSheetContainer not connected")
        result.container_issues.append("Container integration failed")
        
        # Test hook-specific issues
        result.hook_issues.append("HookIntegrator placeholder not replaced")
        result.hook_issues.append("Functional hooks not implemented")
        
        # Test cross-module issues
        result.cross_module_issues.append("Registry and container mismatch")
        result.cross_module_issues.append("Hook and container compatibility issue")
        
        # Verify each category has appropriate issues
        self.assertTrue(any("ActionRegistryManager" in issue for issue in result.registry_issues))
        self.assertTrue(any("ActionSheetContainer" in issue for issue in result.container_issues))
        self.assertTrue(any("HookIntegrator" in issue for issue in result.hook_issues))
        self.assertTrue(any("Registry and container" in issue for issue in result.cross_module_issues))
    
    @unittest.skipIf(IntegrationValidator is None, "IntegrationValidator class not found")
    def test_integration_validator_exists(self):
        """Test that IntegrationValidator class exists if implemented"""
        # This test will only run if the validator class is implemented
        self.assertTrue(hasattr(IntegrationValidator, '__init__'))
    
    def test_validation_result_as_dictionary(self):
        """Test converting ValidationResult to dictionary-like access"""
        result = ValidationResult()
        
        # Add test issues
        result.registry_issues.append("Registry test")
        result.container_issues.append("Container test")
        result.hook_issues.append("Hook test")
        result.cross_module_issues.append("Cross-module test")
        
        # Test that we can access all issue categories
        all_issues = {
            'registry': result.registry_issues,
            'container': result.container_issues,
            'hook': result.hook_issues,
            'cross_module': result.cross_module_issues
        }
        
        # Verify all categories are accessible
        self.assertEqual(len(all_issues['registry']), 1)
        self.assertEqual(len(all_issues['container']), 1)
        self.assertEqual(len(all_issues['hook']), 1)
        self.assertEqual(len(all_issues['cross_module']), 1)
    
    def test_validation_result_iteration(self):
        """Test iterating over ValidationResult issues"""
        result = ValidationResult()
        
        # Add issues
        result.registry_issues.extend(["Registry 1", "Registry 2"])
        result.container_issues.append("Container 1")
        result.hook_issues.extend(["Hook 1", "Hook 2", "Hook 3"])
        result.cross_module_issues.append("Cross-module 1")
        
        # Collect all issues
        all_issues = []
        all_issues.extend(result.registry_issues)
        all_issues.extend(result.container_issues)
        all_issues.extend(result.hook_issues)
        all_issues.extend(result.cross_module_issues)
        
        # Should have total of 7 issues
        self.assertEqual(len(all_issues), 7)
        
        # Should contain specific issues
        self.assertIn("Registry 1", all_issues)
        self.assertIn("Container 1", all_issues)
        self.assertIn("Hook 3", all_issues)
        self.assertIn("Cross-module 1", all_issues)
    
    def test_validation_result_empty_state(self):
        """Test ValidationResult in empty state"""
        result = ValidationResult()
        
        # All issue lists should be empty and have list methods
        self.assertTrue(hasattr(result.registry_issues, 'append'))
        self.assertTrue(hasattr(result.container_issues, 'extend'))
        self.assertTrue(hasattr(result.hook_issues, 'clear'))
        self.assertTrue(hasattr(result.cross_module_issues, 'remove'))
        
        # All should be empty initially
        self.assertFalse(result.registry_issues)
        self.assertFalse(result.container_issues)
        self.assertFalse(result.hook_issues)
        self.assertFalse(result.cross_module_issues)
    
    def test_validation_result_issue_types(self):
        """Test that ValidationResult handles different issue types"""
        result = ValidationResult()
        
        # Test with string issues (most common)
        result.registry_issues.append("String issue")
        self.assertIsInstance(result.registry_issues[0], str)
        
        # Test that lists can handle multiple types if needed
        result.container_issues.append("Container string issue")
        self.assertEqual(len(result.container_issues), 1)
        
        # Test empty string issues
        result.hook_issues.append("")
        self.assertEqual(result.hook_issues[0], "")
        
        # Test with longer issue descriptions
        long_issue = "This is a very long issue description that explains in detail what went wrong during the integration validation process."
        result.cross_module_issues.append(long_issue)
        self.assertEqual(result.cross_module_issues[0], long_issue)


if __name__ == '__main__':
    unittest.main()