#!/usr/bin/env python3
"""
Test Multiple Children Generation

This test reproduces the issue where adding multiple children to the same parent
causes duplicate imports and malformed common actions.
"""

import unittest
import tempfile
import json
import os
import sys
from pathlib import Path

# Add the current directory to the path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from modules.config import GenerationContext, PageConfig, ProjectCapabilities
from modules.variable_generator import VariableGenerator


class TestMultipleChildrenGeneration(unittest.TestCase):
    """Test that multiple children generation works correctly without duplicates."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = os.path.join(self.temp_dir, "test-app")
        os.makedirs(self.frontend_root, exist_ok=True)
        
        # Create pages.config.json with a parent and multiple children
        self.pages_config = {
            "version": "1.0.0",
            "generated_by": "mobile-pages-v2",
            "last_updated": "2025-09-16T15:30:00.000000",
            "pages": {
                "dashboard": {
                    "id": "dashboard",
                    "name": "Dashboard",
                    "type": "parent",
                    "parent_id": "",
                    "icon": "Navigation",
                    "description": "Main dashboard",
                    "route": "/dashboard",
                    "component_name": "DashboardPage",
                    "has_mobile": False,
                    "created_at": "2025-09-16T15:25:00.000000"
                },
                "analytics": {
                    "id": "analytics",
                    "name": "Analytics",
                    "type": "child",
                    "parent_id": "dashboard",
                    "icon": "Navigation",
                    "description": "Analytics data",
                    "route": "/analytics",
                    "component_name": "AnalyticsPage",
                    "has_mobile": False,
                    "created_at": "2025-09-16T15:26:00.000000"
                },
                "reports": {
                    "id": "reports", 
                    "name": "Reports",
                    "type": "child",
                    "parent_id": "dashboard",
                    "icon": "Navigation",
                    "description": "Report generation",
                    "route": "/reports",
                    "component_name": "ReportsPage",
                    "has_mobile": False,
                    "created_at": "2025-09-16T15:27:00.000000"
                }
            },
            "metadata": {
                "total_pages": 3,
                "parent_pages": 1,
                "child_pages": 2
            }
        }
        
        # Write the config to file
        with open(os.path.join(self.frontend_root, "pages.config.json"), "w") as f:
            json.dump(self.pages_config, f, indent=2)
        
        self.capabilities = ProjectCapabilities()
        self.generator = VariableGenerator()
    
    def test_page_actions_registry_no_duplicates(self):
        """Test that page actions registry doesn't generate duplicate imports."""
        # Create context
        config = PageConfig(
            name="Dashboard",
            parent="",
            description="Main dashboard"
        )
        
        context = GenerationContext(
            config=config,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Generate page actions registry variables
        result = self.generator.generate_page_actions_registry_variables(context)
        
        # Check that we have the expected keys
        self.assertIn('DYNAMIC_PAGE_ACTION_IMPORTS', result)
        self.assertIn('DYNAMIC_PAGE_ACTION_ENTRIES', result)
        
        imports = result['DYNAMIC_PAGE_ACTION_IMPORTS']
        entries = result['DYNAMIC_PAGE_ACTION_ENTRIES']
        
        print(f"\n=== IMPORTS ===")
        print(imports)
        print(f"\n=== ENTRIES ===") 
        print(entries)
        
        # Check for duplicate imports
        import_lines = [line.strip() for line in imports.split('\n') if line.strip()]
        unique_imports = set(import_lines)
        
        self.assertEqual(len(import_lines), len(unique_imports), 
                        f"Found duplicate imports! Duplicates: {[line for line in import_lines if import_lines.count(line) > 1]}")
        
        # Verify specific imports are present
        expected_imports = [
            'import { pageActions as dashboardActions } from "./pages/dashboard";',
            'import { pageActions as analyticsActions } from "./pages/analytics";',
            'import { pageActions as reportsActions } from "./pages/reports";'
        ]
        
        for expected in expected_imports:
            self.assertIn(expected, imports, f"Missing expected import: {expected}")
        
        # Verify registry entries
        self.assertIn('dashboard:', entries)
        self.assertIn('analytics:', entries)
        self.assertIn('reports:', entries)
        
        # Check sibling navigation is correct
        self.assertIn("'go-to-reports'", entries)  # analytics should have go-to-reports
        self.assertIn("'go-to-analytics'", entries)  # reports should have go-to-analytics
    
    def test_multiple_calls_consistency(self):
        """Test that calling the generator multiple times produces consistent results."""
        config = PageConfig(
            name="Dashboard",
            parent="",
            description="Main dashboard"
        )
        
        context = GenerationContext(
            config=config,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Call the generator multiple times (simulating what happens during child creation)
        result1 = self.generator.generate_page_actions_registry_variables(context)
        result2 = self.generator.generate_page_actions_registry_variables(context)
        result3 = self.generator.generate_page_actions_registry_variables(context)
        
        # Results should be identical
        self.assertEqual(result1['DYNAMIC_PAGE_ACTION_IMPORTS'], 
                        result2['DYNAMIC_PAGE_ACTION_IMPORTS'],
                        "Multiple calls should produce identical imports")
        
        self.assertEqual(result1['DYNAMIC_PAGE_ACTION_ENTRIES'],
                        result2['DYNAMIC_PAGE_ACTION_ENTRIES'], 
                        "Multiple calls should produce identical entries")
        
        self.assertEqual(result2['DYNAMIC_PAGE_ACTION_IMPORTS'],
                        result3['DYNAMIC_PAGE_ACTION_IMPORTS'],
                        "Third call should match previous calls")
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)