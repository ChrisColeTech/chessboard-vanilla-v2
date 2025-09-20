"""
Unit tests for TemplateFileReferencer
"""

import unittest
import tempfile
import shutil
from pathlib import Path

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.template_file_referencer import TemplateFileReferencer


class TestTemplateFileReferencer(unittest.TestCase):
    
    def setUp(self):
        """Set up test template files."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.templates_dir = self.test_dir / "templates"
        self.templates_dir.mkdir()
        
        # Create test templates
        self._create_test_templates()
        
        self.referencer = TemplateFileReferencer(self.templates_dir)
    
    def tearDown(self):
        """Clean up test files."""
        shutil.rmtree(self.test_dir)
    
    def _create_test_templates(self):
        """Create test template files."""
        
        # App.tsx.template with imports
        app_template = self.templates_dir / "App.tsx.template"
        app_template.write_text('''
import { AppLayout } from "./components/layout";
import { useGlobalUIAudio } from "./hooks/audio/useGlobalUIAudio";
import { DragProvider } from "./providers/DragProvider";
import { store } from "./stores/appStore";
        ''')
        
        # AppLayout.tsx.template with imports
        layout_dir = self.templates_dir / "components" / "layout"
        layout_dir.mkdir(parents=True)
        
        (layout_dir / "AppLayout.tsx.template").write_text('''
import { Header } from "./Header";
import { SettingsPanel } from "../core/SettingsPanel";
import { useSettings } from "../../stores/appStore";
        ''')
        
        (layout_dir / "Header.tsx.template").write_text('''
import React from 'react';
        ''')
        
        # Core components
        core_dir = self.templates_dir / "components" / "core"
        core_dir.mkdir(parents=True)
        
        (core_dir / "SettingsPanel.tsx.template").write_text('''
import { useSettings } from "../../stores/appStore";
        ''')
        
        # Hooks
        hooks_dir = self.templates_dir / "hooks" / "audio"
        hooks_dir.mkdir(parents=True)
        
        (hooks_dir / "useGlobalUIAudio.ts.template").write_text('''
import { audioService } from "../../services/audioService";
        ''')
        
        # Providers
        providers_dir = self.templates_dir / "providers"
        providers_dir.mkdir()
        
        (providers_dir / "DragProvider.tsx.template").write_text('''
import React from 'react';
        ''')
        
        # Stores
        stores_dir = self.templates_dir / "stores"
        stores_dir.mkdir()
        
        (stores_dir / "appStore.ts.template").write_text('''
import { create } from 'zustand';
        ''')
    
    def test_scan_all_templates(self):
        """Test scanning all available templates."""
        templates = self.referencer.available_templates
        
        expected_templates = {
            'App.tsx.template',
            'components/layout/AppLayout.tsx.template',
            'components/layout/Header.tsx.template',
            'components/core/SettingsPanel.tsx.template',
            'hooks/audio/useGlobalUIAudio.ts.template',
            'providers/DragProvider.tsx.template',
            'stores/appStore.ts.template'
        }
        
        self.assertEqual(templates, expected_templates)
    
    def test_get_imports_from_template(self):
        """Test extracting imports from template."""
        imports = self.referencer.get_imports_from_template("App.tsx.template")
        
        expected_imports = [
            "./components/layout",
            "./hooks/audio/useGlobalUIAudio", 
            "./providers/DragProvider",
            "./stores/appStore"
        ]
        
        self.assertEqual(sorted(imports), sorted(expected_imports))
    
    def test_get_imports_missing_template(self):
        """Test getting imports from non-existent template."""
        imports = self.referencer.get_imports_from_template("missing.template")
        self.assertEqual(imports, [])
    
    def test_find_template_matches_exact(self):
        """Test finding exact template matches."""
        matches = self.referencer._find_template_matches("./stores/appStore")
        self.assertEqual(matches, ["stores/appStore.ts.template"])
    
    def test_find_template_matches_directory(self):
        """Test finding directory template matches."""
        matches = self.referencer._find_template_matches("./components/layout")
        
        expected = [
            "components/layout/AppLayout.tsx.template",
            "components/layout/Header.tsx.template"
        ]
        
        self.assertEqual(sorted(matches), sorted(expected))
    
    def test_find_template_matches_none(self):
        """Test finding no matches for non-existent import."""
        matches = self.referencer._find_template_matches("./missing/component")
        self.assertEqual(matches, [])
    
    def test_find_referenced_templates(self):
        """Test finding all referenced templates."""
        refs = self.referencer.find_referenced_templates("App.tsx.template")
        
        expected = [
            "components/layout/AppLayout.tsx.template",
            "components/layout/Header.tsx.template",
            "hooks/audio/useGlobalUIAudio.ts.template",
            "providers/DragProvider.tsx.template",
            "stores/appStore.ts.template"
        ]
        
        self.assertEqual(sorted(refs), sorted(expected))
    
    def test_get_all_dependencies_recursive(self):
        """Test getting all dependencies recursively."""
        deps = self.referencer.get_all_dependencies(["App.tsx.template"])
        
        expected = {
            "App.tsx.template",
            "components/layout/AppLayout.tsx.template",
            "components/layout/Header.tsx.template", 
            "components/core/SettingsPanel.tsx.template",
            "hooks/audio/useGlobalUIAudio.ts.template",
            "providers/DragProvider.tsx.template",
            "stores/appStore.ts.template"
        }
        
        self.assertEqual(deps, expected)
    
    def test_get_all_dependencies_multiple_start(self):
        """Test getting dependencies from multiple starting templates."""
        deps = self.referencer.get_all_dependencies([
            "App.tsx.template",
            "components/core/SettingsPanel.tsx.template"
        ])
        
        # Should include all deps from both templates
        self.assertIn("App.tsx.template", deps)
        self.assertIn("components/core/SettingsPanel.tsx.template", deps)
        self.assertIn("stores/appStore.ts.template", deps)  # Referenced by both
    
    def test_circular_dependencies(self):
        """Test handling circular dependencies."""
        # Create circular dependency
        circular_a = self.templates_dir / "circularA.tsx.template"
        circular_b = self.templates_dir / "circularB.tsx.template"
        
        circular_a.write_text('import { B } from "./circularB";')
        circular_b.write_text('import { A } from "./circularA";')
        
        # Recreate referencer to pick up new templates
        referencer = TemplateFileReferencer(self.templates_dir)
        
        # Should not infinite loop
        deps = referencer.get_all_dependencies(["circularA.tsx.template"])
        
        expected = {
            "circularA.tsx.template",
            "circularB.tsx.template"
        }
        
        self.assertTrue(expected.issubset(deps))


if __name__ == '__main__':
    unittest.main()