#!/usr/bin/env python3
"""
Test Integration Duplicate Imports Issue

This test reproduces the actual bug where child page creation leads to
duplicate imports in the generated files.
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
from modules.dependency_manager import DependencyManager
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter


class TestIntegrationDuplicateImports(unittest.TestCase):
    """Test the actual integration process that causes duplicate imports."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = os.path.join(self.temp_dir, "test-app")
        os.makedirs(self.frontend_root, exist_ok=True)
        
        # Create a basic pages.config.json with just a parent
        self.initial_config = {
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
                }
            },
            "metadata": {
                "total_pages": 1,
                "parent_pages": 1,
                "child_pages": 0
            }
        }
        
        # Write the initial config
        with open(os.path.join(self.frontend_root, "pages.config.json"), "w") as f:
            json.dump(self.initial_config, f, indent=2)
        
        self.capabilities = ProjectCapabilities()
        
        # Initialize template engine and file writer
        self.template_engine = TemplateEngine(current_dir / "templates")
        self.file_writer = FileWriter()
        self.dependency_manager = DependencyManager(self.template_engine, self.file_writer)
        
        # Create necessary directories 
        os.makedirs(os.path.join(self.frontend_root, "src", "constants", "actions"), exist_ok=True)
    
    def test_sequential_child_creation_creates_duplicates(self):
        """Test that creating children sequentially leads to duplicate imports."""
        
        # Step 1: Create the first child (analytics)
        analytics_config = PageConfig(
            name="Analytics",
            parent="dashboard", 
            description="Analytics data"
        )
        
        analytics_context = GenerationContext(
            config=analytics_config,
            frontend_root=Path(self.frontend_root),
            capabilities=self.capabilities,
            variables={}
        )
        
        # Simulate what happens during child creation - integration is called
        print("\n=== STEP 1: Creating Analytics child ===")
        success1 = self.dependency_manager.integrate_child_pages(analytics_context, "dashboard")
        
        # Check what was generated after first child
        page_actions_file = os.path.join(self.frontend_root, "src", "constants", "actions", "page-actions.constants.ts")
        if os.path.exists(page_actions_file):
            with open(page_actions_file, "r") as f:
                content_after_first = f.read()
                print("Content after first child:")
                print(content_after_first)
        else:
            content_after_first = "FILE NOT FOUND"
        
        # Step 2: Update the config to include the analytics child
        self.initial_config["pages"]["analytics"] = {
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
        }
        self.initial_config["metadata"]["total_pages"] = 2
        self.initial_config["metadata"]["child_pages"] = 1
        
        with open(os.path.join(self.frontend_root, "pages.config.json"), "w") as f:
            json.dump(self.initial_config, f, indent=2)
        
        # Step 3: Create the second child (reports)
        reports_config = PageConfig(
            name="Reports",
            parent="dashboard",
            description="Report generation"
        )
        
        reports_context = GenerationContext(
            config=reports_config,
            frontend_root=Path(self.frontend_root),
            capabilities=self.capabilities,
            variables={}
        )
        
        print("\n=== STEP 2: Creating Reports child ===")
        success2 = self.dependency_manager.integrate_child_pages(reports_context, "dashboard")
        
        # Check what was generated after second child
        if os.path.exists(page_actions_file):
            with open(page_actions_file, "r") as f:
                content_after_second = f.read()
                print("Content after second child:")
                print(content_after_second)
                
                # THIS IS WHERE WE EXPECT TO FIND THE BUG
                # Count import statements
                import_lines = [line.strip() for line in content_after_second.split('\n') 
                              if line.strip().startswith('import { pageActions as')]
                
                print(f"\nFound {len(import_lines)} import lines:")
                for i, line in enumerate(import_lines):
                    print(f"  {i+1}. {line}")
                
                # Check for duplicates
                unique_imports = set(import_lines)
                duplicates = [line for line in import_lines if import_lines.count(line) > 1]
                
                if duplicates:
                    print(f"\n❌ FOUND DUPLICATES: {duplicates}")
                    self.fail(f"Duplicate imports found: {duplicates}")
                else:
                    print("\n✅ No duplicate imports found")
                
                # Also check for proper deduplication
                expected_imports = {
                    'import { pageActions as dashboardActions } from "./pages/dashboard";',
                    'import { pageActions as analyticsActions } from "./pages/analytics";', 
                    'import { pageActions as reportsActions } from "./pages/reports";'
                }
                
                actual_imports = set(import_lines)
                
                print(f"\nExpected imports: {expected_imports}")
                print(f"Actual imports: {actual_imports}")
                
                if expected_imports != actual_imports:
                    missing = expected_imports - actual_imports
                    extra = actual_imports - expected_imports
                    if missing:
                        print(f"Missing imports: {missing}")
                    if extra:
                        print(f"Extra imports: {extra}")
                    self.fail("Import statements don't match expected set")
        
        else:
            self.fail("page-actions.constants.ts file was not generated")
    
    def test_common_actions_malformation(self):
        """Test that common actions don't get malformed during multiple child creation."""
        
        # Similar setup but focus on common-actions.constants.ts
        analytics_config = PageConfig(
            name="Analytics", 
            parent="dashboard",
            description="Analytics data"
        )
        
        context = GenerationContext(
            config=analytics_config,
            frontend_root=Path(self.frontend_root),
            capabilities=self.capabilities,
            variables={}
        )
        
        # Call integration
        success = self.dependency_manager.integrate_child_pages(context, "dashboard")
        
        # Check common actions file
        common_actions_file = os.path.join(self.frontend_root, "src", "constants", "actions", "common-actions.constants.ts")
        
        if os.path.exists(common_actions_file):
            with open(common_actions_file, "r") as f:
                content = f.read()
                print("\nCommon actions content:")
                print(content)
                
                # Check for syntax errors like missing commas
                if "dashboardSiblings: [" in content:
                    # Find the object structure around this
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "dashboardSiblings:" in line:
                            # Check previous line ends with comma
                            if i > 0:
                                prev_line = lines[i-1].strip()
                                if prev_line and not prev_line.endswith(',') and not prev_line.endswith('{'):
                                    print(f"❌ SYNTAX ERROR: Line {i} missing comma: '{prev_line}'")
                                    self.fail(f"Syntax error in common actions: missing comma before line {i+1}")
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)