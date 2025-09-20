#!/usr/bin/env python3
"""
Test to simulate and reproduce the duplicate imports bug
by calling the template generation process multiple times.
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
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter


class TestDuplicateImportsSimulated(unittest.TestCase):
    """Test duplicate imports by simulating the real template generation process."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir) / "test-app"
        self.frontend_root.mkdir(exist_ok=True)
        
        # Create a pages config with parent and multiple children
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
        
        # Write the config
        with open(self.frontend_root / "pages.config.json", "w") as f:
            json.dump(self.pages_config, f, indent=2)
        
        self.capabilities = ProjectCapabilities()
        self.template_engine = TemplateEngine(current_dir / "templates")
        self.file_writer = FileWriter()
        
        # Create necessary directories
        actions_dir = self.frontend_root / "src" / "constants" / "actions"
        actions_dir.mkdir(parents=True, exist_ok=True)
    
    def test_template_regeneration_causes_duplicates(self):
        """Test that regenerating the page-actions template multiple times causes duplicates."""
        
        # Create context
        config = PageConfig(
            name="Analytics",
            parent="dashboard", 
            description="Analytics data"
        )
        
        context = GenerationContext(
            config=config,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Generate the page-actions.constants.ts template multiple times
        # This simulates what happens when multiple children are added
        
        template_path = "constants/page-actions.constants.ts.template"
        output_path = self.frontend_root / "src" / "constants" / "actions" / "page-actions.constants.ts"
        
        print("=== GENERATION 1 (Analytics child) ===")
        success1 = self.template_engine.generate_template(template_path, output_path, context)
        
        if output_path.exists():
            with open(output_path, "r") as f:
                content1 = f.read()
                print("Content after first generation:")
                print(content1[:1000] + "..." if len(content1) > 1000 else content1)
        
        # Simulate what happens when a second child is added - regenerate the template
        print("\n=== GENERATION 2 (Reports child) ===") 
        config2 = PageConfig(
            name="Reports",
            parent="dashboard",
            description="Report generation" 
        )
        
        context2 = GenerationContext(
            config=config2,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        success2 = self.template_engine.generate_template(template_path, output_path, context2)
        
        if output_path.exists():
            with open(output_path, "r") as f:
                content2 = f.read()
                print("Content after second generation:")
                print(content2[:1000] + "..." if len(content2) > 1000 else content2)
                
                # NOW CHECK FOR DUPLICATES
                import_lines = [line.strip() for line in content2.split('\n') 
                              if line.strip().startswith('import { pageActions as')]
                
                print(f"\nFound {len(import_lines)} import lines:")
                for i, line in enumerate(import_lines):
                    print(f"  {i+1}. {line}")
                
                # Check for duplicates
                seen_imports = set()
                duplicates = []
                for line in import_lines:
                    if line in seen_imports:
                        duplicates.append(line)
                    seen_imports.add(line)
                
                if duplicates:
                    print(f"\n❌ FOUND DUPLICATES: {duplicates}")
                    # This should demonstrate the bug
                    print("BUG CONFIRMED: Template regeneration creates duplicate imports!")
                else:
                    print("\n✅ No duplicate imports found")
                    print("Template regeneration works correctly")
    
    def test_variable_generator_multiple_calls(self):
        """Test calling the variable generator multiple times directly."""
        from modules.variable_generator import VariableGenerator
        
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
        
        generator = VariableGenerator()
        
        print("=== VARIABLE GENERATION CALL 1 ===")
        result1 = generator.generate_page_actions_registry_variables(context)
        print("Imports 1:", result1.get('DYNAMIC_PAGE_ACTION_IMPORTS', 'NOT FOUND'))
        
        print("\n=== VARIABLE GENERATION CALL 2 ===")
        result2 = generator.generate_page_actions_registry_variables(context)
        print("Imports 2:", result2.get('DYNAMIC_PAGE_ACTION_IMPORTS', 'NOT FOUND'))
        
        print("\n=== VARIABLE GENERATION CALL 3 ===") 
        result3 = generator.generate_page_actions_registry_variables(context)
        print("Imports 3:", result3.get('DYNAMIC_PAGE_ACTION_IMPORTS', 'NOT FOUND'))
        
        # Check if results are consistent across calls
        if result1 == result2 == result3:
            print("\n✅ Variable generator is consistent across multiple calls")
        else:
            print("\n❌ Variable generator produces different results on multiple calls")
            print(f"Call 1: {result1}")
            print(f"Call 2: {result2}")
            print(f"Call 3: {result3}")
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)