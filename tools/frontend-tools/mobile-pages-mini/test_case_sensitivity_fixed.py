#!/usr/bin/env python3
"""
Test to confirm that the case sensitivity bug has been fixed.
This test verifies that APITester, UIRenderer, and other mixed-case names work correctly.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
from unittest.mock import patch

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from main import MobilePagesMiniCLI

class TestCaseSensitivityFixed:
    """Test that case sensitivity issues have been resolved."""
    
    def setup_method(self):
        """Set up test environment with temporary frontend directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create minimal frontend structure
        src_dir = self.frontend_root / "src"
        src_dir.mkdir(parents=True)
        
        # Create package.json with all required dependencies to bypass validation
        package_json = self.frontend_root / "package.json"
        package_json.write_text('''{
  "name": "test-app",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "tailwind-merge": "^1.0.0",
    "clsx": "^1.0.0",
    "@headlessui/react": "^1.0.0",
    "zod": "^3.0.0",
    "zustand": "^4.0.0",
    "lucide-react": "^0.200.0",
    "@react-spring/web": "^9.0.0",
    "howler": "^2.0.0",
    "@radix-ui/react-label": "^2.0.0",
    "react-icons": "^4.0.0",
    "react-hook-form": "^7.0.0",
    "class-variance-authority": "^0.6.0",
    "@hookform/resolvers": "^3.0.0",
    "@radix-ui/react-slot": "^1.0.0"
  }
}''')
        
        # Create node_modules to satisfy dependency checks
        node_modules = self.frontend_root / "node_modules"
        node_modules.mkdir()
        
        self.cli = MobilePagesMiniCLI(str(self.frontend_root), force=True, log_mode="silent")
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('modules.pre_generation_validator.PreGenerationValidator.validate_before_generation')
    def test_acronym_case_preserved(self, mock_validate):
        """Test that acronym-heavy names like APITester maintain correct case."""
        # Mock validation to always pass
        from modules.pre_generation_validator import ValidationResults
        mock_validate.return_value = ValidationResults(
            dependencies=[],
            npm_packages_missing=[],
            templates_missing=[],
            chess_dependencies=[],
            critical_failures=[],
            warnings=[],
            can_proceed=True
        )
        
        # Act: Create parent with APITester child
        self.cli.create_pages("Development", ["APITester"])
        
        # Assert: Check generated parent page imports maintain case
        dev_page = self.frontend_root / "src/pages/development/DevelopmentPage.tsx"
        assert dev_page.exists(), "DevelopmentPage.tsx should be generated"
        
        dev_content = dev_page.read_text()
        
        # Check for correct import (should be APITesterPageWrapper, not ApiTesterPageWrapper)
        expected_import = 'import { APITesterPageWrapper } from "../../components/development/APITesterPageWrapper";'
        assert expected_import in dev_content, f"Expected correct case import: {expected_import}"
        
        # Check routing logic maintains case
        expected_routing = "CurrentPageComponent = APITesterPageWrapper;"
        assert expected_routing in dev_content, f"Expected correct case routing: {expected_routing}"
        
        # Assert: Check generated wrapper component exists with correct name
        wrapper_file = self.frontend_root / "src/components/development/APITesterPageWrapper.tsx"
        assert wrapper_file.exists(), "APITesterPageWrapper.tsx should be generated"
        
        wrapper_content = wrapper_file.read_text()
        expected_export = "export const APITesterPageWrapper: React.FC"
        assert expected_export in wrapper_content, f"Expected correct case export: {expected_export}"
    
    @patch('modules.pre_generation_validator.PreGenerationValidator.validate_before_generation')
    def test_multiple_acronym_cases(self, mock_validate):
        """Test multiple children with different acronym patterns."""
        # Mock validation
        from modules.pre_generation_validator import ValidationResults
        mock_validate.return_value = ValidationResults(
            dependencies=[], npm_packages_missing=[], templates_missing=[],
            chess_dependencies=[], critical_failures=[], warnings=[], can_proceed=True
        )
        
        # Act: Create parent with multiple acronym-heavy children
        children = ["APIClient", "UIRenderer", "HTTPService", "XMLParser"]
        self.cli.create_pages("Services", children)
        
        # Assert: Check all imports maintain correct case
        services_page = self.frontend_root / "src/pages/services/ServicesPage.tsx"
        services_content = services_page.read_text()
        
        expected_cases = {
            "APIClient": "APIClientPageWrapper",
            "UIRenderer": "UIRendererPageWrapper", 
            "HTTPService": "HTTPServicePageWrapper",
            "XMLParser": "XMLParserPageWrapper"
        }
        
        for original_name, expected_wrapper in expected_cases.items():
            # Check import statement
            expected_import = f'import {{ {expected_wrapper} }} from "../../components/services/{expected_wrapper}";'
            assert expected_import in services_content, f"Missing correct import for {original_name}: {expected_import}"
            
            # Check routing logic
            expected_routing = f"CurrentPageComponent = {expected_wrapper};"
            assert expected_routing in services_content, f"Missing correct routing for {original_name}: {expected_routing}"
            
            # Check wrapper file exists
            wrapper_file = self.frontend_root / f"src/components/services/{expected_wrapper}.tsx"
            assert wrapper_file.exists(), f"Wrapper file should exist: {expected_wrapper}.tsx"
    
    @patch('modules.pre_generation_validator.PreGenerationValidator.validate_before_generation')
    def test_mixed_case_patterns(self, mock_validate):
        """Test edge cases with mixed casing patterns."""
        # Mock validation
        from modules.pre_generation_validator import ValidationResults
        mock_validate.return_value = ValidationResults(
            dependencies=[], npm_packages_missing=[], templates_missing=[],
            chess_dependencies=[], critical_failures=[], warnings=[], can_proceed=True
        )
        
        # Act: Create with various casing patterns
        children = ["JSONValidator", "PDFGenerator", "URLRouter"]
        self.cli.create_pages("Utils", children)
        
        # Assert: All maintain proper case
        utils_page = self.frontend_root / "src/pages/utils/UtilsPage.tsx"
        utils_content = utils_page.read_text()
        
        # These should NOT be converted to JsonValidator, PdfGenerator, UrlRouter
        expected_correct_cases = [
            "JSONValidatorPageWrapper",
            "PDFGeneratorPageWrapper", 
            "URLRouterPageWrapper"
        ]
        
        for expected_name in expected_correct_cases:
            assert expected_name in utils_content, f"Expected {expected_name} to be preserved in utils page"

if __name__ == "__main__":
    # Run focused test
    test_instance = TestCaseSensitivityFixed()
    test_instance.setup_method()
    
    try:
        print("=== Testing Case Sensitivity Fix ===" )
        
        # Mock validation
        from unittest.mock import patch
        from modules.pre_generation_validator import ValidationResults
        
        mock_result = ValidationResults(
            dependencies=[], npm_packages_missing=[], templates_missing=[],
            chess_dependencies=[], critical_failures=[], warnings=[], can_proceed=True
        )
        
        with patch('modules.pre_generation_validator.PreGenerationValidator.validate_before_generation') as mock_validate:
            mock_validate.return_value = mock_result
            
            print("🧪 Testing APITester case preservation...")
            test_instance.test_acronym_case_preserved()
            print("✅ APITester case preserved correctly")
            
            print("🧪 Testing multiple acronym cases...")
            test_instance.test_multiple_acronym_cases()
            print("✅ Multiple acronym cases preserved correctly")
            
            print("🧪 Testing mixed case patterns...")
            test_instance.test_mixed_case_patterns()
            print("✅ Mixed case patterns preserved correctly")
            
        print("\n🎉 All case sensitivity tests PASSED - fix confirmed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        test_instance.teardown_method()