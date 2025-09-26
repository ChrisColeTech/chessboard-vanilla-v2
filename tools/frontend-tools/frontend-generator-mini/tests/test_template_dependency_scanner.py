#!/usr/bin/env python3
"""
Tests for the Template Dependency Scanner module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.template_dependency_scanner import TemplateDependencyScanner, ScanResult


class TestTemplateDependencyScanner(unittest.TestCase):
    """Test the Template Dependency Scanner"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.static_dir = self.test_dir / "static"
        self.dynamic_dir = self.test_dir / "dynamic"
        
        # Create template directories
        self.static_dir.mkdir(parents=True)
        self.dynamic_dir.mkdir(parents=True)
        
        # Create some test templates
        self._create_test_templates()
        
        self.scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def _create_test_templates(self):
        """Create test template files"""
        # Static base template
        base_template = self.static_dir / "base.template"
        base_template.write_text("""
// Base template
import { Component } from './component';
import { Utils } from './utils';

// No dependencies
""")
        
        # Static component template
        component_template = self.static_dir / "component.template"
        component_template.write_text("""
// Component template
import { Utils } from './utils';

// Depends on utils
""")
        
        # Static utils template
        utils_template = self.static_dir / "utils.template"
        utils_template.write_text("""
// Utils template
// No dependencies
""")
        
        # Dynamic page template with dependencies
        page_dir = self.dynamic_dir / "pages"
        page_dir.mkdir(parents=True)
        page_template = page_dir / "main.template"
        page_template.write_text("""
// Page template
import { Component } from './component';
import { Layout } from '../layouts/main';

// Depends on component and layout
""")
        
        # Dynamic layout template
        layout_dir = self.dynamic_dir / "layouts"
        layout_dir.mkdir(parents=True)
        layout_template = layout_dir / "main.template"
        layout_template.write_text("""
// Layout template
import { Utils } from './utils';

// Depends on utils
""")
    
    def test_build_template_map(self):
        """Test building template map"""
        template_map = self.scanner._build_template_map()
        
        # Should contain static templates
        self.assertIn('base', template_map)
        self.assertIn('component', template_map)
        self.assertIn('utils', template_map)
        
        # Check relative paths
        self.assertEqual(template_map['base'], 'base')
        self.assertEqual(template_map['component'], 'component')
        self.assertEqual(template_map['utils'], 'utils')
    
    def test_scan_result_structure(self):
        """Test ScanResult dataclass structure"""
        result = ScanResult(
            required_templates={'template1', 'template2'},
            dependency_tree={'template1': {'template2'}},
            missing_templates={'missing1'}
        )
        
        self.assertIsInstance(result.required_templates, set)
        self.assertIsInstance(result.dependency_tree, dict)
        self.assertIsInstance(result.missing_templates, set)
        
        self.assertEqual(result.required_templates, {'template1', 'template2'})
        self.assertEqual(result.dependency_tree, {'template1': {'template2'}})
        self.assertEqual(result.missing_templates, {'missing1'})
    
    def test_scan_dependencies_basic(self):
        """Test basic dependency scanning"""
        # This is a basic test since the actual implementation may vary
        # We'll test what we can from the interface
        result = self.scanner.scan_dependencies("test_page")
        
        # Should return a ScanResult
        self.assertIsInstance(result, ScanResult)
        self.assertIsInstance(result.required_templates, set)
        self.assertIsInstance(result.dependency_tree, dict)
        self.assertIsInstance(result.missing_templates, set)
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
        
        # Should have template map
        self.assertIsInstance(scanner.template_map, dict)
        self.assertEqual(scanner.static_dir, self.static_dir)
        self.assertEqual(scanner.dynamic_dir, self.dynamic_dir)
    
    def test_template_map_with_subdirectories(self):
        """Test template map handles subdirectories correctly"""
        # Create nested template
        nested_dir = self.static_dir / "nested" / "deep"
        nested_dir.mkdir(parents=True)
        nested_template = nested_dir / "template.template"
        nested_template.write_text("// Nested template")
        
        # Rebuild scanner to pick up new template
        scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
        
        # Should include nested template in map
        self.assertIn('nested/deep/template', scanner.template_map)
    
    def test_empty_template_directories(self):
        """Test scanner with empty template directories"""
        empty_static = self.test_dir / "empty_static"
        empty_dynamic = self.test_dir / "empty_dynamic"
        empty_static.mkdir()
        empty_dynamic.mkdir()
        
        scanner = TemplateDependencyScanner(empty_static, empty_dynamic)
        
        # Should handle empty directories gracefully
        self.assertIsInstance(scanner.template_map, dict)
        self.assertEqual(len(scanner.template_map), 0)
    
    def test_nonexistent_template_directories(self):
        """Test scanner with nonexistent template directories"""
        nonexistent_static = self.test_dir / "nonexistent_static"
        nonexistent_dynamic = self.test_dir / "nonexistent_dynamic"
        
        scanner = TemplateDependencyScanner(nonexistent_static, nonexistent_dynamic)
        
        # Should handle nonexistent directories gracefully
        self.assertIsInstance(scanner.template_map, dict)
        self.assertEqual(len(scanner.template_map), 0)
    
    def test_template_file_extension_filtering(self):
        """Test that only .template files are included"""
        # Create non-template files
        self.static_dir.joinpath("readme.txt").write_text("Not a template")
        self.static_dir.joinpath("config.json").write_text("{}")
        self.static_dir.joinpath("script.js").write_text("// JavaScript")
        
        # Rebuild scanner
        scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
        
        # Should only include .template files
        for template_name in scanner.template_map.keys():
            self.assertNotIn("readme", template_name)
            self.assertNotIn("config", template_name)
            self.assertNotIn("script", template_name)
        
        # Should still include our original templates
        self.assertIn('base', scanner.template_map)
        self.assertIn('component', scanner.template_map)
        self.assertIn('utils', scanner.template_map)
    
    def test_dependency_scanning_interface(self):
        """Test dependency scanning method interface"""
        # Test that the method exists and has expected signature
        result = self.scanner.scan_dependencies("test")
        
        # Should return ScanResult with proper attributes
        self.assertTrue(hasattr(result, 'required_templates'))
        self.assertTrue(hasattr(result, 'dependency_tree'))
        self.assertTrue(hasattr(result, 'missing_templates'))
        
        # All attributes should be collections
        self.assertTrue(hasattr(result.required_templates, '__iter__'))
        self.assertTrue(hasattr(result.dependency_tree, '__iter__'))
        self.assertTrue(hasattr(result.missing_templates, '__iter__'))
    
    def test_scanner_attributes(self):
        """Test scanner has required attributes"""
        self.assertTrue(hasattr(self.scanner, 'static_dir'))
        self.assertTrue(hasattr(self.scanner, 'dynamic_dir'))
        self.assertTrue(hasattr(self.scanner, 'template_map'))
        
        # Attributes should have correct types
        self.assertIsInstance(self.scanner.static_dir, Path)
        self.assertIsInstance(self.scanner.dynamic_dir, Path)
        self.assertIsInstance(self.scanner.template_map, dict)


if __name__ == '__main__':
    unittest.main()