"""
Unit tests for TemplateDependencyScanner
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.template_dependency_scanner import TemplateDependencyScanner, ScanResult


class TestTemplateDependencyScanner(unittest.TestCase):
    
    def setUp(self):
        """Set up test directories and files."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.static_dir = self.test_dir / "static" 
        self.dynamic_dir = self.test_dir / "dynamic"
        
        self.static_dir.mkdir()
        self.dynamic_dir.mkdir()
        
        # Create mock template files
        self._create_test_templates()
        
        self.scanner = TemplateDependencyScanner(self.static_dir, self.dynamic_dir)
    
    def tearDown(self):
        """Clean up test directories."""
        shutil.rmtree(self.test_dir)
    
    def _create_test_templates(self):
        """Create test template files with various import patterns."""
        
        # Core template with imports
        app_content = '''
import { useEffect } from "react";
import { AppLayout } from "./components/layout";
import { useGlobalUIAudio } from "./hooks/audio/useGlobalUIAudio";
import { DragProvider } from "./providers/DragProvider";
import { useAppStore } from "./stores/appStore";
        '''
        (self.static_dir / "App.tsx.template").write_text(app_content)
        
        # Main template with imports
        main_content = '''
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import withSplashScreen from './components/splash/withSplashScreen'
        '''
        (self.static_dir / "main.tsx.template").write_text(main_content)
        
        # Component with dependency
        layout_dir = self.static_dir / "components" / "layout"
        layout_dir.mkdir(parents=True)
        layout_content = '''
import { TabBar } from "./TabBar";
import { Header } from "./Header";
        '''
        (layout_dir / "index.ts.template").write_text(layout_content)
        
        # Hook template
        hook_dir = self.static_dir / "hooks" / "audio"  
        hook_dir.mkdir(parents=True)
        hook_content = '''
import { useCallback } from 'react';
import { audioContext } from '../audio/context';
        '''
        (hook_dir / "useGlobalUIAudio.ts.template").write_text(hook_content)
        
        # Provider template
        provider_dir = self.static_dir / "providers"
        provider_dir.mkdir(parents=True)
        provider_content = '''
import React from 'react';
import { createContext } from 'react';
        '''
        (provider_dir / "DragProvider.tsx.template").write_text(provider_content)
        
        # Store template  
        store_dir = self.static_dir / "stores"
        store_dir.mkdir(parents=True)
        store_content = '''
import { create } from 'zustand';
import { TabId } from '../components/layout/types';
        '''
        (store_dir / "appStore.ts.template").write_text(store_content)
        
        # Dynamic parent template
        (self.dynamic_dir / "parent-page.tsx.template").write_text('''
import { usePageActions } from '../hooks/core/usePageActions';
import { usePageInstructions } from '../hooks/core/usePageInstructions';
        ''')
    
    def test_get_core_templates(self):
        """Test finding core template files."""
        core_templates = self.scanner._get_core_templates()
        
        expected = {"App.tsx.template", "main.tsx.template"}
        self.assertEqual(core_templates, expected)
    
    def test_get_dynamic_templates_parent(self):
        """Test finding dynamic templates for parent page type."""
        dynamic_templates = self.scanner._get_dynamic_templates("parent")
        
        expected = {"parent-page.tsx.template"}
        self.assertEqual(dynamic_templates, expected)
    
    def test_get_dynamic_templates_child(self):
        """Test finding dynamic templates for child page type.""" 
        # Create a child template
        (self.dynamic_dir / "child-page.tsx.template").write_text("// child template")
        
        dynamic_templates = self.scanner._get_dynamic_templates("child")
        
        expected = {"child-page.tsx.template"}
        self.assertEqual(dynamic_templates, expected)
    
    def test_extract_imports(self):
        """Test extracting import statements from template content."""
        content = '''
        import { useEffect } from "react";
        import { AppLayout } from "./components/layout";
        import "./styles.css";
        import { utils } from "../utils/helper";
        import { external } from "external-lib";
        '''
        
        imports = self.scanner._extract_imports(content)
        
        expected = {
            "./components/layout",
            "./styles.css", 
            "../utils/helper"
        }
        self.assertEqual(imports, expected)
    
    def test_convert_import_to_template_path(self):
        """Test converting import paths to template file paths."""
        # Test direct file match
        result = self.scanner._convert_import_to_template_path("./components/layout")
        self.assertEqual(result, "components/layout/index.ts.template")
        
        # Test file with extension match
        result = self.scanner._convert_import_to_template_path("./stores/appStore")
        self.assertEqual(result, "stores/appStore.ts.template")
        
        # Test missing file
        result = self.scanner._convert_import_to_template_path("./missing/file")
        self.assertIsNone(result)
        
        # Test dynamic dependency (should be skipped)
        result = self.scanner._convert_import_to_template_path("./hooks/core/usePageData")
        self.assertIsNone(result)
    
    def test_template_exists(self):
        """Test checking if template files exist."""
        # Existing static template
        self.assertTrue(self.scanner._template_exists("App.tsx.template"))
        
        # Existing dynamic template  
        self.assertTrue(self.scanner._template_exists("parent-page.tsx.template"))
        
        # Non-existing template
        self.assertFalse(self.scanner._template_exists("missing.template"))
    
    def test_read_template_content(self):
        """Test reading template file content."""
        # Read static template
        content = self.scanner._read_template_content("App.tsx.template")
        self.assertIsNotNone(content)
        self.assertIn("AppLayout", content)
        
        # Read dynamic template
        content = self.scanner._read_template_content("parent-page.tsx.template")
        self.assertIsNotNone(content)
        self.assertIn("usePageActions", content)
        
        # Read non-existing template
        content = self.scanner._read_template_content("missing.template")
        self.assertIsNone(content)
    
    def test_scan_dependencies_parent(self):
        """Test full dependency scan for parent page type."""
        result = self.scanner.scan_dependencies("parent")
        
        # Should find core templates and their dependencies
        self.assertIsInstance(result, ScanResult)
        self.assertGreater(len(result.required_templates), 0)
        
        # Should include core dependencies
        self.assertIn("components/layout/index.ts.template", result.required_templates)
        self.assertIn("hooks/audio/useGlobalUIAudio.ts.template", result.required_templates)
        self.assertIn("providers/DragProvider.tsx.template", result.required_templates)
        
        # Should have dependency tree
        self.assertIn("App.tsx.template", result.dependency_tree)
        app_deps = result.dependency_tree["App.tsx.template"]
        self.assertIn("components/layout/index.ts.template", app_deps)
    
    def test_find_missing_templates(self):
        """Test finding missing template files."""
        # Create a set with some existing and some missing templates
        required = {
            "App.tsx.template",  # exists
            "missing.template",   # doesn't exist
            "stores/appStore.ts.template"  # exists
        }
        
        missing = self.scanner._find_missing_templates(required)
        
        expected = {"missing.template"}
        self.assertEqual(missing, expected)
    
    def test_scan_template_recursive(self):
        """Test recursive template scanning."""
        required_templates = set()
        dependency_tree = {}
        processed = set()
        
        self.scanner._scan_template_recursive(
            "App.tsx.template",
            required_templates,
            dependency_tree, 
            processed
        )
        
        # Should have found dependencies
        self.assertGreater(len(required_templates), 0)
        self.assertIn("components/layout/index.ts.template", required_templates)
        
        # Should have dependency tree entry
        self.assertIn("App.tsx.template", dependency_tree)
        
        # Should mark as processed
        self.assertIn("App.tsx.template", processed)
    
    def test_circular_dependencies(self):
        """Test handling of circular dependencies."""
        # Create circular dependency
        circular_a = self.static_dir / "circular_a.ts.template"
        circular_b = self.static_dir / "circular_b.ts.template"
        
        circular_a.write_text('import { B } from "./circular_b";')
        circular_b.write_text('import { A } from "./circular_a";')
        
        required_templates = set()
        dependency_tree = {}
        processed = set()
        
        # Should not infinite loop
        self.scanner._scan_template_recursive(
            "circular_a.ts.template",
            required_templates,
            dependency_tree,
            processed
        )
        
        # Should process both files
        self.assertIn("circular_a.ts.template", processed)
        self.assertIn("circular_b.ts.template", processed)


if __name__ == '__main__':
    unittest.main()