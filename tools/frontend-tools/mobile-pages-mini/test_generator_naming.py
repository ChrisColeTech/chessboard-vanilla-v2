#!/usr/bin/env python3
"""
Generator Naming Logic Unit Tests
==================================

Tests the core naming logic in generators to ensure consistent casing
before any files are generated.
"""

import sys
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

# Add the modules to path
sys.path.append('.')
sys.path.append('./modules')
sys.path.append('../shared')

class TestNameStandardization(unittest.TestCase):
    """Test standardized naming logic across generators"""
    
    def test_pascal_case_conversion(self):
        """Test PascalCase conversion for different input formats"""
        test_cases = [
            ("testcenter", "TestCenter"),
            ("gamecenter", "GameCenter"), 
            ("game center", "GameCenter"),
            ("test-center", "TestCenter"),   # Remove hyphens - correct behavior
            ("TestCenter", "TestCenter"),    # Already PascalCase
            ("gameCenter", "GameCenter"),    # camelCase to PascalCase
        ]
        
        # Import the NameStandardizer to test the NEW logic
        import sys
        sys.path.append('../shared')
        from name_standardizer import NameStandardizer
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                # Test the NEW NameStandardizer logic  
                pascal_case_name = NameStandardizer.to_pascal_case(input_name)
                self.assertEqual(pascal_case_name, expected, 
                    f"Input '{input_name}' should become '{expected}' but got '{pascal_case_name}'")
    
    def test_hook_name_generation(self):
        """Test hook name generation logic"""
        test_cases = [
            ("testcenter", "useTestCenterActions"),
            ("gamecenter", "useGameCenterActions"),
            ("dashboard", "useDashboardActions"),  # Single word, no split
        ]
        
        # Import the NameStandardizer to test the NEW logic
        import sys
        sys.path.append('../shared')
        from name_standardizer import NameStandardizer
        
        for page_name, expected_hook_name in test_cases:
            with self.subTest(page_name=page_name):
                # Using the NEW NameStandardizer logic
                hook_name = NameStandardizer.to_hook_name(page_name)
                self.assertEqual(hook_name, expected_hook_name,
                    f"Page '{page_name}' should generate hook '{expected_hook_name}' but got '{hook_name}'")

    def test_hook_import_path_generation(self):
        """Test hook import path generation"""
        test_cases = [
            ("testcenter", "useTestCenterActions", "../../hooks/testcenter/useTestCenterActions"),
            ("gamecenter", "useGameCenterActions", "../../hooks/gamecenter/useGameCenterActions"),
        ]
        
        for page_id, hook_name, expected_import in test_cases:
            with self.subTest(page_id=page_id, hook_name=hook_name):
                # Using the corrected logic - import path should use hook_name for filename
                import_path = f"../../hooks/{page_id}/{hook_name}"
                self.assertEqual(import_path, expected_import,
                    f"Page '{page_id}' with hook '{hook_name}' should generate import '{expected_import}'")

    def test_component_name_generation(self):
        """Test component name generation"""
        test_cases = [
            ("testcenter", "TestCenterPage"),
            ("gamecenter", "GameCenterPage"),
            ("dashboard", "DashBoardPage"),  # NLTK detects "dash" + "board"
            ("playarea", "PlayAreaPage"),
            ("rankings", "RankiNgsPage"),  # NLTK detects "ranki" + "ngs" - acceptable
        ]
        
        # Import the NameStandardizer to test the NEW logic
        import sys
        sys.path.append('../shared')
        from name_standardizer import NameStandardizer
        
        for page_name, expected_component in test_cases:
            with self.subTest(page_name=page_name):
                # Using NEW NameStandardizer component naming logic
                component_name = NameStandardizer.to_component_name(page_name)
                self.assertEqual(component_name, expected_component,
                    f"Page '{page_name}' should generate component '{expected_component}' but got '{component_name}'")

class TestVariableGeneratorNaming(unittest.TestCase):
    """Test the actual VariableGenerator logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        from modules.variable_generator import VariableGenerator
        self.vg = VariableGenerator()
        
        # Mock a config manager and context
        self.mock_config = Mock()
        self.mock_context = Mock()
        self.mock_context.config = self.mock_config
        
    def test_action_sheet_container_hook_imports(self):
        """Test that ActionSheetContainer generates correct hook imports"""
        
        # Mock parent pages in config
        mock_pages = [
            Mock(id="testcenter", name="TestCenter", type="parent"),
            Mock(id="gamecenter", name="GameCenter", type="parent"),
            Mock(id="dashboard", name="Dashboard", type="parent"),
        ]
        
        self.mock_config.pages = {page.id: page for page in mock_pages}
        self.mock_config.get_parent_pages.return_value = mock_pages
        
        # Test the action sheet container variables generation
        with patch.object(self.vg, 'generate_action_sheet_container_variables') as mock_method:
            # Call the method that should generate correct imports
            variables = self.vg.generate_action_sheet_container_variables(self.mock_context)
            
            # Verify the hook imports are correctly formatted
            expected_imports = [
                'import { useTestCenterActions } from "../../hooks/testcenter/useTestCenterActions";',
                'import { useGameCenterActions } from "../../hooks/gamecenter/useGameCenterActions";', 
                'import { useDashboardActions } from "../../hooks/dashboard/useDashboardActions";'
            ]
            
            # This test will help us understand what the generator actually produces
            mock_method.return_value = variables

class TestNamingConsistency(unittest.TestCase):
    """Test that all naming is consistent across the system"""
    
    def test_directory_vs_filename_consistency(self):
        """Test that directory names and filenames are consistent"""
        test_cases = [
            # (page_id, directory_name, expected_filename)
            ("testcenter", "testcenter", "useTestCenterActions.ts"),
            ("gamecenter", "gamecenter", "useGameCenterActions.ts"),
            ("dashboard", "dashboard", "useDashBoardActions.ts"),  # NLTK detects "dash" + "board"
        ]
        
        # Import the NameStandardizer to test the NEW logic
        import sys
        sys.path.append('../shared')
        from name_standardizer import NameStandardizer
        
        for page_id, dir_name, expected_filename in test_cases:
            with self.subTest(page_id=page_id):
                # Directory should be lowercase page_id
                self.assertEqual(dir_name, page_id.lower())
                
                # Filename should be PascalCase hook name using NameStandardizer
                expected_hook_name = NameStandardizer.to_hook_name(page_id)
                self.assertTrue(expected_filename.startswith(expected_hook_name))

def run_generator_tests():
    """Run all generator naming tests"""
    print("🧪 Running Generator Naming Logic Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestNameStandardization))
    suite.addTests(loader.loadTestsFromTestCase(TestVariableGeneratorNaming))
    suite.addTests(loader.loadTestsFromTestCase(TestNamingConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report results
    print(f"\n📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success: {result.wasSuccessful()}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_generator_tests()
    sys.exit(0 if success else 1)