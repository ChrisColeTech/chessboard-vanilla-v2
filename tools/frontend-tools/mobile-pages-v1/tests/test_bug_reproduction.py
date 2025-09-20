#!/usr/bin/env python3
"""
Test to reproduce and demonstrate the exact duplicate imports bug.

The bug occurs because two different systems write to the same file:
1. DependencyManager (template-based, replaces entire file)
2. ActionRegistryManager (line-based, appends to existing file)
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
import sys

# Add the current directory to the path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from modules.config import GenerationContext, PageConfig, ProjectCapabilities
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter
from modules.action_registry_manager import ActionRegistryManager
from modules.variable_generator import VariableGenerator


class TestBugReproduction(unittest.TestCase):
    """Reproduce the exact bug that causes duplicate imports."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir) / "test-app"
        self.frontend_root.mkdir(exist_ok=True)
        
        # Create initial config with parent and first child
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
                }
            },
            "metadata": {
                "total_pages": 2,
                "parent_pages": 1,
                "child_pages": 1
            }
        }
        
        # Write config
        with open(self.frontend_root / "pages.config.json", "w") as f:
            json.dump(self.pages_config, f, indent=2)
        
        self.capabilities = ProjectCapabilities()
        self.template_engine = TemplateEngine(current_dir / "templates")
        self.file_writer = FileWriter()
        
        # Create necessary directories
        actions_dir = self.frontend_root / "src" / "constants" / "actions"
        actions_dir.mkdir(parents=True, exist_ok=True)
        
        # Create page action files that would normally be created
        pages_dir = actions_dir / "pages"
        pages_dir.mkdir(exist_ok=True)
        
        # Create dummy page action files
        dashboard_actions = """export const pageActions = {
  actions: [
    { id: 'dashboard-action', label: 'Dashboard Action', icon: 'Navigation', variant: 'default' }
  ]
};"""
        analytics_actions = """export const pageActions = {
  actions: [
    { id: 'analytics-action', label: 'Analytics Action', icon: 'Navigation', variant: 'default' }
  ]
};"""
        
        (pages_dir / "dashboard.ts").write_text(dashboard_actions, encoding='utf-8')
        (pages_dir / "analytics.ts").write_text(analytics_actions, encoding='utf-8')
        
        # Create common actions file
        common_actions = """export const COMMON_ACTIONS = [
  { id: 'help', label: 'Help', icon: 'Help', variant: 'default' }
];

export function mergeWithCommonActions(pageActions: any[], siblingActions: string[]) {
  return [...pageActions, ...COMMON_ACTIONS];
}"""
        (actions_dir / "common-actions.constants.ts").write_text(common_actions, encoding='utf-8')
    
    def test_reproduce_duplicate_imports_bug(self):
        """Reproduce the exact sequence that causes duplicate imports."""
        
        print("\n" + "="*60)
        print("REPRODUCING DUPLICATE IMPORTS BUG")
        print("="*60)
        
        # STEP 1: DependencyManager generates initial file (template-based)
        print("\nSTEP 1: DependencyManager generates page-actions file")
        context = GenerationContext(
            config=PageConfig(name="Analytics", parent="dashboard", description="Analytics"),
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Simulate DependencyManager.regenerate_page_actions_registry
        generator = VariableGenerator()
        variables = generator.generate_page_actions_registry_variables(context)
        
        content = self.template_engine.render_template(
            'constants/page-actions.constants.ts.template',
            variables
        )
        
        registry_path = self.frontend_root / "src" / "constants" / "actions" / "page-actions.constants.ts"
        self.file_writer.write_file(
            registry_path,
            content,
            "DependencyManager",
            "test_bug_reproduction.py"
        )
        
        # Check content after DependencyManager
        with open(registry_path, "r") as f:
            content_after_dm1 = f.read()
            print("Content after DependencyManager (step 1):")
            print(content_after_dm1[:500] + "..." if len(content_after_dm1) > 500 else content_after_dm1)
        
        # STEP 2: ActionRegistryManager modifies the same file (line-based)
        print("\nSTEP 2: ActionRegistryManager adds to the same file")
        action_registry = ActionRegistryManager(self.frontend_root, self.file_writer)
        success = action_registry.register_child_actions("dashboard")
        
        # Check content after ActionRegistryManager  
        with open(registry_path, "r") as f:
            content_after_arm1 = f.read()
            print("Content after ActionRegistryManager (step 2):")
            print(content_after_arm1[:500] + "..." if len(content_after_arm1) > 500 else content_after_arm1)
        
        # STEP 3: Add second child to config
        print("\nSTEP 3: Adding second child to config")
        self.pages_config["pages"]["reports"] = {
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
        self.pages_config["metadata"]["total_pages"] = 3
        self.pages_config["metadata"]["child_pages"] = 2
        
        with open(self.frontend_root / "pages.config.json", "w") as f:
            json.dump(self.pages_config, f, indent=2)
        
        # Create reports action file
        reports_actions = """export const pageActions = {
  actions: [
    { id: 'reports-action', label: 'Reports Action', icon: 'Navigation', variant: 'default' }
  ]
};"""
        pages_dir = self.frontend_root / "src" / "constants" / "actions" / "pages"
        (pages_dir / "reports.ts").write_text(reports_actions, encoding='utf-8')
        
        # STEP 4: DependencyManager regenerates again (this can cause issues)
        print("\nSTEP 4: DependencyManager regenerates with new child")
        context2 = GenerationContext(
            config=PageConfig(name="Reports", parent="dashboard", description="Reports"),
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        variables2 = generator.generate_page_actions_registry_variables(context2)
        content2 = self.template_engine.render_template(
            'constants/page-actions.constants.ts.template',
            variables2
        )
        
        self.file_writer.write_file(
            registry_path,
            content2,
            "DependencyManager",
            "test_bug_reproduction.py"
        )
        
        # Check content after second DependencyManager call
        with open(registry_path, "r") as f:
            content_after_dm2 = f.read()
            print("Content after DependencyManager (step 4):")
            print(content_after_dm2[:500] + "..." if len(content_after_dm2) > 500 else content_after_dm2)
        
        # STEP 5: ActionRegistryManager processes again
        print("\nSTEP 5: ActionRegistryManager processes new children")
        success2 = action_registry.register_child_actions("dashboard")
        
        # Check final content - THIS IS WHERE DUPLICATES APPEAR
        with open(registry_path, "r") as f:
            final_content = f.read()
            print("FINAL CONTENT:")
            print(final_content)
        
        # CHECK FOR DUPLICATES
        print("\n" + "="*60)
        print("ANALYZING FOR DUPLICATES")
        print("="*60)
        
        import_lines = [line.strip() for line in final_content.split('\n') 
                       if line.strip().startswith('import { pageActions as')]
        
        print(f"Found {len(import_lines)} import lines:")
        for i, line in enumerate(import_lines):
            print(f"  {i+1}. {line}")
        
        # Check for duplicates (normalize quotes and semicolons to catch semantic duplicates)
        seen_imports = {}
        duplicates = []
        for line in import_lines:
            # Normalize the line by converting single quotes to double quotes and ensuring semicolon
            normalized_line = line.replace("'", '"')
            if not normalized_line.endswith(';'):
                normalized_line += ';'
            print(f"DEBUG: Processing '{line}' -> normalized: '{normalized_line}'")
            
            if normalized_line in seen_imports:
                duplicates.append(line)
                print(f"❌ DUPLICATE FOUND: {line} (semantically same as {seen_imports[normalized_line]})")
            else:
                seen_imports[normalized_line] = line
                print(f"  Adding to seen_imports: {normalized_line}")
        
        if duplicates:
            print(f"\n🐛 BUG REPRODUCED! Found {len(duplicates)} duplicate imports:")
            for dup in duplicates:
                print(f"  - {dup}")
            
            # This test is EXPECTED to fail - it demonstrates the bug
            self.fail(f"BUG CONFIRMED: Duplicate imports found: {duplicates}")
        else:
            print("\n✅ No duplicates found - bug may already be fixed")
    
    def tearDown(self):
        """Clean up test environment.""" 
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)