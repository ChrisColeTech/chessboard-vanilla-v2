#!/usr/bin/env python3
"""
Tests for the Template File Referencer module
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from modules.template_file_referencer import TemplateFileReferencer


class TestTemplateFileReferencer(unittest.TestCase):
    """Test the Template File Referencer"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.templates_dir = self.test_dir / "templates"
        self.templates_dir.mkdir(parents=True)
        
        # Create test template files
        self._create_test_templates()
        
        self.referencer = TemplateFileReferencer(self.templates_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def _create_test_templates(self):
        """Create test template files"""
        # Template with relative imports
        main_template = self.templates_dir / "main.template"
        main_template.write_text("""
import React from 'react';
import { Component } from './component';
import { Utils } from '../utils/helper';
import { Layout } from './layout/main';
// Some template content
""")
        
        # Template with no imports
        simple_template = self.templates_dir / "simple.template"
        simple_template.write_text("""
// Simple template with no imports
const SimpleComponent = () => {
    return <div>Simple</div>;
};
""")
        
        # Template with mixed imports
        mixed_template = self.templates_dir / "mixed.template"
        mixed_template.write_text("""
import React from 'react';
import { ExternalLib } from 'external-library';
import { LocalComponent } from './local';
import { NestedComponent } from '../nested/component';
""")
        
        # Create nested directory structure
        nested_dir = self.templates_dir / "nested"
        nested_dir.mkdir()
        nested_template = nested_dir / "component.template"
        nested_template.write_text("""
import { Utils } from '../utils';
// Nested component
""")
        
        # Create utils directory
        utils_dir = self.templates_dir / "utils"
        utils_dir.mkdir()
        utils_template = utils_dir / "helper.template"
        utils_template.write_text("""
// Utility functions
export const helper = () => {};
""")
    
    def test_scan_all_templates(self):
        """Test scanning all available templates"""
        templates = self.referencer._scan_all_templates()
        
        # Should find all template files
        self.assertIsInstance(templates, set)
        self.assertIn("main.template", templates)
        self.assertIn("simple.template", templates)
        self.assertIn("mixed.template", templates)
        self.assertIn("nested/component.template", templates)
        self.assertIn("utils/helper.template", templates)
    
    def test_get_imports_from_template_with_imports(self):
        """Test getting imports from template with relative imports"""
        imports = self.referencer.get_imports_from_template("main.template")
        
        # Should extract relative imports only
        self.assertIsInstance(imports, list)
        self.assertIn("./component", imports)
        self.assertIn("../utils/helper", imports)
        self.assertIn("./layout/main", imports)
        
        # Should not include absolute imports
        self.assertNotIn("react", imports)
    
    def test_get_imports_from_template_no_imports(self):
        """Test getting imports from template with no imports"""
        imports = self.referencer.get_imports_from_template("simple.template")
        
        # Should return empty list
        self.assertIsInstance(imports, list)
        self.assertEqual(len(imports), 0)
    
    def test_get_imports_from_template_mixed_imports(self):
        """Test getting imports from template with mixed imports"""
        imports = self.referencer.get_imports_from_template("mixed.template")
        
        # Should extract only relative imports
        self.assertIsInstance(imports, list)
        self.assertIn("./local", imports)
        self.assertIn("../nested/component", imports)
        
        # Should not include external library imports
        self.assertNotIn("react", imports)
        self.assertNotIn("external-library", imports)
    
    def test_get_imports_from_nonexistent_template(self):
        """Test getting imports from nonexistent template"""
        imports = self.referencer.get_imports_from_template("nonexistent.template")
        
        # Should return empty list
        self.assertIsInstance(imports, list)
        self.assertEqual(len(imports), 0)
    
    def test_find_referenced_templates(self):
        """Test finding referenced templates"""
        references = self.referencer.find_referenced_templates("main.template")
        
        # Should return list of referenced templates
        self.assertIsInstance(references, list)
    
    def test_referencer_initialization(self):
        """Test referencer initialization"""
        referencer = TemplateFileReferencer(self.templates_dir)
        
        # Should have templates directory and available templates
        self.assertEqual(referencer.templates_dir, self.templates_dir)
        self.assertIsInstance(referencer.available_templates, set)
        self.assertGreater(len(referencer.available_templates), 0)
    
    def test_referencer_with_empty_directory(self):
        """Test referencer with empty templates directory"""
        empty_dir = self.test_dir / "empty"
        empty_dir.mkdir()
        
        referencer = TemplateFileReferencer(empty_dir)
        
        # Should handle empty directory gracefully
        self.assertIsInstance(referencer.available_templates, set)
        self.assertEqual(len(referencer.available_templates), 0)
    
    def test_referencer_with_nonexistent_directory(self):
        """Test referencer with nonexistent directory"""
        nonexistent_dir = self.test_dir / "nonexistent"
        
        referencer = TemplateFileReferencer(nonexistent_dir)
        
        # Should handle nonexistent directory gracefully
        self.assertIsInstance(referencer.available_templates, set)
        self.assertEqual(len(referencer.available_templates), 0)
    
    def test_import_pattern_matching(self):
        """Test import pattern matching with various formats"""
        # Create template with different import formats
        test_template = self.templates_dir / "test_imports.template"
        test_template.write_text("""
import { Component } from './component';
import Utils from '../utils';
import * as Helpers from './helpers';
import type { Types } from '../types';
const dynamicImport = import('./dynamic');
""")
        
        imports = self.referencer.get_imports_from_template("test_imports.template")
        
        # Should match various import formats
        self.assertIn("./component", imports)
        self.assertIn("../utils", imports)
        self.assertIn("./helpers", imports)
        self.assertIn("../types", imports)
        # Dynamic imports should not be matched by the current pattern
    
    def test_template_file_filtering(self):
        """Test that only .template files are scanned"""
        # Create non-template files
        self.templates_dir.joinpath("readme.txt").write_text("Not a template")
        self.templates_dir.joinpath("config.json").write_text("{}")
        self.templates_dir.joinpath("script.js").write_text("// JavaScript")
        
        # Re-scan templates
        templates = self.referencer._scan_all_templates()
        
        # Should only include .template files
        template_files = [t for t in templates if t.endswith('.template')]
        non_template_files = [t for t in templates if not t.endswith('.template')]
        
        self.assertEqual(len(templates), len(template_files))
        self.assertEqual(len(non_template_files), 0)
    
    def test_relative_import_detection(self):
        """Test detection of relative vs absolute imports"""
        # Create template with various import types
        import_test_template = self.templates_dir / "import_test.template"
        import_test_template.write_text("""
import React from 'react';
import { Component } from '@/components/Component';
import { LocalComponent } from './local';
import { ParentComponent } from '../parent';
import { PackageComponent } from 'some-package';
""")
        
        imports = self.referencer.get_imports_from_template("import_test.template")
        
        # Should only include relative imports (starting with ./ or ../)
        relative_imports = [imp for imp in imports if imp.startswith('./') or imp.startswith('../')]
        absolute_imports = [imp for imp in imports if not (imp.startswith('./') or imp.startswith('../'))]
        
        self.assertEqual(len(imports), len(relative_imports))
        self.assertEqual(len(absolute_imports), 0)
        
        # Check specific relative imports
        self.assertIn("./local", imports)
        self.assertIn("../parent", imports)


if __name__ == '__main__':
    unittest.main()