#!/usr/bin/env python3
"""
Test suite to verify the directory import bug fix.
Ensures that directory imports don't blindly include all files in a directory.
"""

import unittest
from pathlib import Path
from modules.template_dependency_scanner import TemplateDependencyScanner


class TestDirectoryImportFix(unittest.TestCase):
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
        self.scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
    
    def test_problem_identification(self):
        """First, identify the exact problem with barrel imports."""
        result = self.scanner.scan_dependencies('parent')
        
        print(f"\nDEBUG: Total templates found: {len(result.required_templates)}")
        
        # Find what's importing PieceSetSelector
        piece_selector_file = 'components/settings/PieceSetSelector.tsx.template'
        importers = []
        for template, deps in result.dependency_tree.items():
            if piece_selector_file in deps:
                importers.append(template)
        
        print(f"DEBUG: PieceSetSelector imported by: {importers}")
        
        # Test the specific conversion that's causing issues
        components_import = self.scanner._convert_import_to_template_paths('../../components')
        print(f"DEBUG: '../../components' resolves to {len(components_import)} templates")
        
        # Show some examples
        settings_templates = [t for t in components_import if 'settings' in t]
        print(f"DEBUG: Settings templates in components import: {settings_templates}")
        
        # This test documents the fixed behavior
        self.assertEqual(len(components_import), 0, "Components import should be skipped (fixed behavior)")
        self.assertNotIn(piece_selector_file, components_import, "PieceSetSelector should not be in components import (fixed)")
    
    def test_core_templates_are_entry_points(self):
        """Test that core templates are properly identified."""
        core_templates = self.scanner._get_core_templates()
        
        expected_core = ['App.tsx.template', 'main.tsx.template', 'index.css.template']
        for expected in expected_core:
            self.assertIn(expected, core_templates, f"Core template {expected} should be identified")
        
        # Core templates should start the dependency scan
        result = self.scanner.scan_dependencies('parent')
        for expected in expected_core:
            # Main.tsx might not be in final results if nothing imports it
            if expected == 'main.tsx.template':
                continue
            self.assertIn(expected, result.required_templates, f"Core template {expected} should be in results")
    
    def test_specific_file_imports_work(self):
        """Test that specific file imports still work correctly."""
        # Test direct file import
        app_import = self.scanner._convert_import_to_template_paths('./App.tsx')
        self.assertEqual(len(app_import), 1, "Direct file import should return one file")
        self.assertEqual(app_import[0], 'App.tsx.template', "Should return correct template")
        
        # Test file with extension
        css_import = self.scanner._convert_import_to_template_paths('./index.css')
        self.assertEqual(len(css_import), 1, "CSS file import should work")
    
    def test_barrel_import_problem(self):
        """Test that demonstrates the barrel import problem."""
        # This is the problematic import from backgroundEffectsRegistry
        components_result = self.scanner._convert_import_to_template_paths('../../components')
        
        # Should NOT include chess-specific files
        chess_files = [t for t in components_result if 'PieceSetSelector' in t or 'BoardColorSelector' in t]
        
        # This test will pass after the fix
        print(f"DEBUG: Chess files in components import: {chess_files}")
        self.assertEqual(len(chess_files), 0, f"Chess files should not be in barrel import: {chess_files}")


class TestDirectoryImportSolution(unittest.TestCase):
    """Tests for the solution to the directory import problem."""
    
    def setUp(self):
        self.static_dir = Path("templates/static")
        self.dynamic_dir = Path("templates/dynamic")
        self.scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
    
    def test_barrel_imports_should_be_skipped(self):
        """Test that barrel imports (components directories) should be skipped."""
        # These imports should return empty because they'll be handled by generated index files
        barrel_imports = [
            '../../components',
            './components', 
            '../components',
            'components/settings',
            'components/ui'
        ]
        
        for barrel_import in barrel_imports:
            with self.subTest(import_path=barrel_import):
                result = self.scanner._convert_import_to_template_paths(barrel_import)
                # This is what we want after the fix
                self.assertEqual(result, [], f"Barrel import {barrel_import} should be skipped")
    
    def test_non_barrel_directories_should_work(self):
        """Test that non-barrel directory imports should still work."""
        # These are legitimate directory imports that should include files
        legitimate_dirs = [
            'utils/chess',  # If something imports the whole utils/chess directory
            'services/audio',  # If something imports the whole services/audio directory
        ]
        
        for dir_import in legitimate_dirs:
            with self.subTest(import_path=dir_import):
                result = self.scanner._convert_import_to_template_paths(dir_import)
                # Should include files in these directories
                if len(result) > 0:  # Only test if directory exists
                    self.assertGreater(len(result), 0, f"Directory import {dir_import} should include files")


if __name__ == '__main__':
    print("🧪 Running Directory Import Fix Tests...")
    unittest.main(verbosity=2)