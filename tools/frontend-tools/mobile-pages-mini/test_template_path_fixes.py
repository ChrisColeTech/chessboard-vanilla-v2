#!/usr/bin/env python3
"""
Test suite to verify template path fixes work correctly.
Tests the usePageData dependency manager fix and import path resolution.
"""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from modules.dependency_manager import DependencyManager
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter
from modules.config import GenerationContext, PageConfig


class TestTemplatePathFixes(unittest.TestCase):
    
    def setUp(self):
        self.templates_root = Path("templates")
        self.template_engine = TemplateEngine(self.templates_root)
        self.file_writer = Mock(spec=FileWriter)
        self.dependency_manager = DependencyManager(self.template_engine, self.file_writer)
    
    def test_use_page_data_template_exists(self):
        """Test that usePageData template exists in correct location."""
        template_path = self.templates_root / "dynamic/dependencies/use-page-data-hook.ts.template"
        self.assertTrue(template_path.exists(), 
                       f"usePageData template should exist at {template_path}")
    
    def test_use_page_data_template_uses_endpoint_parameter(self):
        """Test that usePageData template correctly uses endpoint parameter."""
        template_path = self.templates_root / "dynamic/dependencies/use-page-data-hook.ts.template"
        content = template_path.read_text(encoding='utf-8')
        
        self.assertIn("(endpoint: string)", content, 
                     "usePageData template should accept endpoint parameter")
        self.assertIn("generateMockData(endpoint)", content,
                     "usePageData template should use endpoint parameter")
    
    def test_dependency_manager_creates_generic_hook(self):
        """Test that dependency manager creates usePageData hook with correct template."""
        # Create mock context
        config = PageConfig(
            name="testpage",
            mobile=False
        )
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        # Mock the hook path to not exist so it tries to create it
        with patch('pathlib.Path.exists', return_value=False):
            with patch.object(self.template_engine, 'render_template') as mock_render:
                mock_render.return_value = "mock rendered content"
                
                # Call the method
                self.dependency_manager.ensure_use_page_data_hook(context)
                
                # Verify render_template was called with PARENT_ID
                mock_render.assert_called_once()
                call_args = mock_render.call_args
                
                # Check template name
                self.assertEqual(call_args[0][0], 'dependencies/use-page-data-hook.ts.template')
                
                # Check basic variables are present (no PARENT_ID needed)
                variables = call_args[0][1]
                self.assertIn('GENERATOR_NAME', variables)
                self.assertIn('SOURCE_FILE', variables)
    
    def test_parent_main_page_imports_match_generated_paths(self):
        """Test that parent-main-page imports match where files are generated."""
        template_path = self.templates_root / "dynamic/pages/parent-main-page.tsx.template"
        content = template_path.read_text(encoding='utf-8')
        
        # Check that imports match expected generated file locations
        self.assertIn('from "../../hooks/core/usePageData"', content,
                     "parent-main-page should import usePageData from correct path")
        self.assertIn('from "../../components/ui/DataTable"', content,
                     "parent-main-page should import DataTable from correct path")
    
    def test_data_table_template_exists(self):
        """Test that DataTable template exists in expected location."""
        template_path = self.templates_root / "static/components/ui/DataTable.tsx.template"
        self.assertTrue(template_path.exists(), 
                       f"DataTable template should exist at {template_path}")
    
    def test_dependency_manager_generates_to_correct_paths(self):
        """Test that dependency manager generates files to paths that match imports."""
        config = PageConfig(
            name="testpage",
            mobile=False
        )
        context = Mock(spec=GenerationContext)
        context.config = config
        context.frontend_root = Path("/mock/frontend")
        
        with patch('pathlib.Path.exists', return_value=False):
            with patch.object(self.template_engine, 'render_template', return_value="mock content"):
                with patch.object(self.file_writer, 'write_file') as mock_write:
                    # Call the method
                    self.dependency_manager.ensure_use_page_data_hook(context)
                    
                    # Verify file is written to correct path
                    mock_write.assert_called_once()
                    written_path = mock_write.call_args[0][0]
                    
                    expected_path = Path("/mock/frontend/src/hooks/core/usePageData.ts")
                    self.assertEqual(written_path, expected_path,
                                   f"usePageData should be written to {expected_path}")


class TestImportPathConsistency(unittest.TestCase):
    """Test that all template import paths are consistent with file generation."""
    
    def setUp(self):
        self.templates_root = Path("templates")
    
    def test_no_orphaned_imports_in_parent_main_page(self):
        """Test that parent-main-page doesn't import files that don't exist."""
        template_path = self.templates_root / "dynamic/pages/parent-main-page.tsx.template"
        
        if not template_path.exists():
            self.skipTest("parent-main-page template does not exist")
        
        content = template_path.read_text(encoding='utf-8')
        
        # Extract import statements
        import re
        import_pattern = r'import.*?from\s+[\'"]([^\'"]+)[\'"]'
        imports = re.findall(import_pattern, content)
        
        for import_path in imports:
            if import_path.startswith('./') or import_path.startswith('../'):
                # This is a relative import - we should be able to resolve it
                # For now, just verify the commonly problematic ones
                if 'usePageData' in import_path:
                    self.assertTrue(
                        import_path.endswith('hooks/core/usePageData') or 
                        import_path.endswith('hooks/core/usePageData.ts'),
                        f"usePageData import path should be correct: {import_path}"
                    )
                elif 'DataTable' in import_path:
                    self.assertTrue(
                        import_path.endswith('components/ui/DataTable') or
                        import_path.endswith('components/ui/DataTable.tsx'),
                        f"DataTable import path should be correct: {import_path}"
                    )


if __name__ == '__main__':
    print("🧪 Running Template Path Fixes Verification Tests...")
    unittest.main(verbosity=2)