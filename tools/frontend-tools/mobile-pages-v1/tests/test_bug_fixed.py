#!/usr/bin/env python3
"""
Test to verify that the duplicate imports bug has been fixed.

This test should pass after the ActionRegistryManager fix.
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


class TestBugFixed(unittest.TestCase):
    """Test that the duplicate imports bug has been fixed."""
    
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
        reports_actions = """export const pageActions = {
  actions: [
    { id: 'reports-action', label: 'Reports Action', icon: 'Navigation', variant: 'default' }
  ]
};"""
        
        (pages_dir / "dashboard.ts").write_text(dashboard_actions, encoding='utf-8')
        (pages_dir / "analytics.ts").write_text(analytics_actions, encoding='utf-8')
        (pages_dir / "reports.ts").write_text(reports_actions, encoding='utf-8')
        
        # Create common actions file
        common_actions = """export const COMMON_ACTIONS = [
  { id: 'help', label: 'Help', icon: 'Help', variant: 'default' }
];

export function mergeWithCommonActions(pageActions: any[], siblingActions: string[]) {
  return [...pageActions, ...COMMON_ACTIONS];
}"""
        (actions_dir / "common-actions.constants.ts").write_text(common_actions, encoding='utf-8')
    
    def test_fixed_no_duplicate_imports(self):
        """Test that the same sequence no longer produces duplicate imports."""
        
        print("\n" + "="*60)
        print("TESTING FIX: No Duplicate Imports")
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
            "test_bug_fixed.py"
        )
        
        # STEP 2: ActionRegistryManager attempts to modify the same file
        print("\nSTEP 2: ActionRegistryManager processes (should detect existing imports)")
        action_registry = ActionRegistryManager(self.frontend_root, self.file_writer)
        success = action_registry.register_child_actions("dashboard")
        
        # Check final content
        with open(registry_path, "r") as f:
            final_content = f.read()
            print("FINAL CONTENT:")
            print(final_content[:1000] + "..." if len(final_content) > 1000 else final_content)
        
        # CHECK FOR DUPLICATES
        print("\n" + "="*60)
        print("ANALYZING FOR DUPLICATES")
        print("="*60)
        
        import_lines = [line.strip() for line in final_content.split('\n') 
                       if line.strip().startswith('import { pageActions as')]
        
        print(f"Found {len(import_lines)} import lines:")
        for i, line in enumerate(import_lines):
            print(f"  {i+1}. {line}")
        
        # Check for semantic duplicates (normalize quotes and semicolons)
        seen_imports = {}
        duplicates = []
        for line in import_lines:
            # Normalize the line by converting single quotes to double quotes and ensuring semicolon
            normalized_line = line.replace("'", '"')
            if not normalized_line.endswith(';'):
                normalized_line += ';'
            
            if normalized_line in seen_imports:
                duplicates.append(line)
                print(f"❌ DUPLICATE FOUND: {line} (same as {seen_imports[normalized_line]})")
            else:
                seen_imports[normalized_line] = line
        
        if duplicates:
            print(f"\n❌ FIX FAILED! Still found {len(duplicates)} duplicate imports:")
            for dup in duplicates:
                print(f"  - {dup}")
            self.fail(f"Fix failed: duplicate imports still found: {duplicates}")
        else:
            print("\n✅ FIX SUCCESSFUL! No duplicate imports found")
        
        # Also verify we have the expected imports
        expected_pages = ['dashboard', 'analytics', 'reports']
        for page in expected_pages:
            found = any(f"from \"./pages/{page}\"" in line or f"from './pages/{page}'" in line 
                       for line in import_lines)
            self.assertTrue(found, f"Missing import for page: {page}")
        
        print(f"✅ All expected imports found: {expected_pages}")
    
    def test_import_detection_with_different_quotes(self):
        """Test that _has_import method correctly detects imports with different quote styles."""
        action_registry = ActionRegistryManager(self.frontend_root, self.file_writer)
        
        # Test content with double quotes
        content_double = """import { pageActions as analyticsActions } from "./pages/analytics";"""
        
        # Test content with single quotes  
        content_single = """import { pageActions as analyticsActions } from './pages/analytics';"""
        
        # Should detect import regardless of quote style used in check
        self.assertTrue(action_registry._has_import(content_double, "from \"./pages/analytics\""))
        self.assertTrue(action_registry._has_import(content_double, "from './pages/analytics'"))
        self.assertTrue(action_registry._has_import(content_single, "from \"./pages/analytics\""))
        self.assertTrue(action_registry._has_import(content_single, "from './pages/analytics'"))
        
        # Should not detect non-existent imports
        self.assertFalse(action_registry._has_import(content_double, "from \"./pages/nonexistent\""))
        
        print("✅ Import detection with different quotes works correctly")
    
    def tearDown(self):
        """Clean up test environment.""" 
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)