#!/usr/bin/env python3
"""
Integration test to reproduce the case sensitivity bug where APITester becomes ApiTester.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from main import MobilePagesMiniCLI

class TestCaseSensitivityBug:
    """Test case sensitivity issues in generated code."""
    
    def setup_method(self):
        """Set up test environment with temporary frontend directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create minimal frontend structure
        src_dir = self.frontend_root / "src"
        src_dir.mkdir(parents=True)
        
        # Create package.json with all required dependencies to bypass validation
        package_json = self.frontend_root / "package.json"
        package_json.write_text('''
{
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
}
        ''')
        
        # Create node_modules to satisfy dependency checks
        node_modules = self.frontend_root / "node_modules"
        node_modules.mkdir()
        
        self.cli = MobilePagesMiniCLI(str(self.frontend_root), force=True, log_mode="silent")
    
    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('modules.pre_generation_validator.PreGenerationValidator.validate_before_generation')
    def test_api_tester_case_sensitivity(self, mock_validate):
        """Test that APITester maintains correct case throughout generation."""
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
        self.cli.create_pages("Tools", ["APITester"])
        
        # Assert: Check generated parent page imports
        tools_page = self.frontend_root / "src/pages/tools/ToolsPage.tsx"
        assert tools_page.exists(), "ToolsPage.tsx should be generated"
        
        tools_content = tools_page.read_text()
        
        # Check import statement case
        expected_import = 'import { APITesterPageWrapper } from "../../components/tools/APITesterPageWrapper";'
        actual_imports = [line.strip() for line in tools_content.split('\n') if 'APITesterPageWrapper' in line and 'import' in line]
        
        print(f"Expected import: {expected_import}")
        print(f"Actual imports: {actual_imports}")
        
        assert any(expected_import in line for line in actual_imports), f"Expected {expected_import} in imports, got: {actual_imports}"
        
        # Check routing logic case
        expected_routing = "CurrentPageComponent = APITesterPageWrapper;"
        routing_lines = [line.strip() for line in tools_content.split('\n') if 'APITesterPageWrapper' in line and 'CurrentPageComponent' in line]
        
        print(f"Expected routing: {expected_routing}")
        print(f"Actual routing: {routing_lines}")
        
        assert any(expected_routing in line for line in routing_lines), f"Expected {expected_routing} in routing, got: {routing_lines}"
        
        # Assert: Check generated wrapper component export
        wrapper_file = self.frontend_root / "src/components/tools/APITesterPageWrapper.tsx"
        assert wrapper_file.exists(), "APITesterPageWrapper.tsx should be generated"
        
        wrapper_content = wrapper_file.read_text()
        expected_export = "export const APITesterPageWrapper: React.FC"
        
        assert expected_export in wrapper_content, f"Expected {expected_export} in wrapper export"
        
        # Assert: Check index.ts export
        index_file = self.frontend_root / "src/components/tools/index.ts"
        if index_file.exists():
            index_content = index_file.read_text()
            expected_index_export = "export * from './APITesterPageWrapper';"
            assert expected_index_export in index_content, f"Expected {expected_index_export} in index.ts"
    
    def test_mixed_case_children(self):
        """Test multiple children with different case patterns."""
        # Act: Create parent with mixed-case children
        children = ["APITester", "UserProfile", "DatabaseManager"]
        self.cli.create_pages("Admin", children)
        
        # Assert: Check all imports maintain correct case
        admin_page = self.frontend_root / "src/pages/admin/AdminPage.tsx"
        admin_content = admin_page.read_text()
        
        expected_imports = [
            "APITesterPageWrapper",
            "UserProfilePageWrapper", 
            "DatabaseManagerPageWrapper"
        ]
        
        for expected in expected_imports:
            import_lines = [line for line in admin_content.split('\n') if expected in line and 'import' in line]
            assert len(import_lines) > 0, f"Expected import for {expected} not found"
            
            # Verify exact case match
            import_line = import_lines[0]
            assert expected in import_line, f"Case mismatch in import: {import_line}"
    
    def test_acronym_preservation(self):
        """Test that acronyms like API, UI, HTTP are preserved in PascalCase."""
        acronym_names = ["APIClient", "UIRenderer", "HTTPService"]
        
        for name in acronym_names:
            # Act: Create individual pages
            self.cli.create_pages("Network", [name])
            
            # Assert: Check wrapper file exists with correct name
            wrapper_file = self.frontend_root / f"src/components/network/{name}PageWrapper.tsx"
            assert wrapper_file.exists(), f"{name}PageWrapper.tsx should exist"
            
            # Assert: Check export statement
            wrapper_content = wrapper_file.read_text()
            expected_export = f"export const {name}PageWrapper: React.FC"
            assert expected_export in wrapper_content, f"Export case mismatch for {name}"

if __name__ == "__main__":
    # Run the specific test that reproduces the bug
    test_instance = TestCaseSensitivityBug()
    test_instance.setup_method()
    
    try:
        print("=== Running Case Sensitivity Integration Test ===")
        
        # Mock the validation
        from unittest.mock import patch, MagicMock
        from modules.pre_generation_validator import ValidationResults
        
        mock_result = ValidationResults(
            dependencies=[],
            npm_packages_missing=[],
            templates_missing=[],
            chess_dependencies=[],
            critical_failures=[],
            warnings=[],
            can_proceed=True
        )
        
        with patch('modules.pre_generation_validator.PreGenerationValidator.validate_before_generation') as mock_validate:
            mock_validate.return_value = mock_result
            test_instance.test_api_tester_case_sensitivity()
            
        print("✅ Test passed - case sensitivity is working correctly")
    except AssertionError as e:
        print(f"❌ Test failed - Found case sensitivity bug: {e}")
        print("\n=== DEBUGGING GENERATED FILES ===")
        # Examine what was actually generated
        tools_page = test_instance.frontend_root / "src/pages/tools/ToolsPage.tsx"
        if tools_page.exists():
            content = tools_page.read_text()
            print("ToolsPage.tsx imports:")
            for line in content.split('\n'):
                if 'import' in line and ('APITester' in line or 'ApiTester' in line):
                    print(f"  {line.strip()}")
            print("ToolsPage.tsx routing:")
            for line in content.split('\n'):
                if 'CurrentPageComponent' in line and ('APITester' in line or 'ApiTester' in line):
                    print(f"  {line.strip()}")
        
        # Check wrapper files
        wrapper_files = list(test_instance.frontend_root.glob("src/components/tools/*APITester*"))
        wrapper_files.extend(list(test_instance.frontend_root.glob("src/components/tools/*ApiTester*")))
        print(f"Wrapper files found: {[f.name for f in wrapper_files]}")
        
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        test_instance.teardown_method()