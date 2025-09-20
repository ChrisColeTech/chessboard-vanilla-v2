"""
Tests for ActionRegistryManager - Integration of generated actions with registry system.

This test suite verifies the ActionRegistryManager functionality including:
- PAGE_ACTIONS registry integration
- COMMON_ACTIONS sibling navigation
- COMMON_ACTION_GROUPS creation
- pages.config.json source of truth validation
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys
# Add modules path for imports
sys.path.append(str(Path(__file__).parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from action_registry_manager import ActionRegistryManager, register_parent_page_actions, register_child_page_actions
from file_writer import FileWriter


class TestActionRegistryManager(unittest.TestCase):
    """Test ActionRegistryManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create directory structure
        self.src_dir = self.frontend_root / "src"
        self.actions_dir = self.src_dir / "constants" / "actions"
        self.pages_actions_dir = self.actions_dir / "pages"
        
        self.src_dir.mkdir(parents=True)
        self.actions_dir.mkdir(parents=True) 
        self.pages_actions_dir.mkdir(parents=True)
        
        # Create pages.config.json
        self.config_data = {
            "version": "1.0.0",
            "generated_by": "mobile-pages-v2",
            "last_updated": "2025-09-16T08:16:14.098238",
            "pages": {
                "testsection": {
                    "id": "testsection",
                    "name": "Testsection", 
                    "type": "parent",
                    "parent_id": "",
                    "icon": "Navigation",
                    "description": "",
                    "route": "/testsection",
                    "component_name": "TestsectionPage",
                    "has_mobile": False,
                    "created_at": "2025-09-16T08:16:14.098211"
                },
                "analytics": {
                    "id": "analytics",
                    "name": "Analytics",
                    "type": "child",
                    "parent_id": "testsection",
                    "icon": "Navigation", 
                    "description": "",
                    "route": "/analytics",
                    "component_name": "AnalyticsPage",
                    "has_mobile": True,
                    "created_at": "2025-09-16T08:15:13.252651"
                },
                "dashboard": {
                    "id": "dashboard",
                    "name": "Dashboard",
                    "type": "child", 
                    "parent_id": "testsection",
                    "icon": "Navigation",
                    "description": "",
                    "route": "/dashboard",
                    "component_name": "DashboardPage",
                    "has_mobile": True,
                    "created_at": "2025-09-16T08:15:23.286873"
                }
            },
            "metadata": {
                "total_pages": 3,
                "parent_pages": 1,
                "child_pages": 2
            }
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        # Create mock action files
        self.create_mock_action_files()
        
        # Mock file writer
        self.mock_file_writer = Mock(spec=FileWriter)
        
        # Create manager instance
        self.manager = ActionRegistryManager(self.frontend_root, self.mock_file_writer)
    
    def create_mock_action_files(self):
        """Create mock action constant files for testing."""
        
        # PAGE_ACTIONS file
        page_actions_content = '''import { mergeWithCommonActions } from './common-actions.constants';

export const PAGE_ACTIONS = {
  // Entries will be added here
};
'''
        page_actions_path = self.actions_dir / "page-actions.constants.ts"
        page_actions_path.write_text(page_actions_content, encoding='utf-8')
        
        # COMMON_ACTIONS file
        common_actions_content = '''import { Navigation } from 'lucide-react';

export const COMMON_ACTIONS = {
  // Actions will be added here
};

export const COMMON_ACTION_GROUPS = {
  // Groups will be added here
};
'''
        common_actions_path = self.actions_dir / "common-actions.constants.ts"
        common_actions_path.write_text(common_actions_content, encoding='utf-8')
    
    def test_register_parent_actions_success(self):
        """Test successful parent action registration."""
        result = self.manager.register_parent_actions("testsection")
        
        self.assertTrue(result)
        
        # Check that page actions file was updated
        page_actions_content = self.manager.page_actions_path.read_text(encoding='utf-8')
        
        # Should contain import
        self.assertIn("from './pages/testsection'", page_actions_content)
        self.assertIn("testsectionActions", page_actions_content)
        
        # Should contain registry entry
        self.assertIn("testsection: testsectionActions.actions", page_actions_content)
    
    def test_register_parent_actions_invalid_parent(self):
        """Test parent action registration with invalid parent ID."""
        result = self.manager.register_parent_actions("nonexistent")
        
        self.assertFalse(result)
    
    def test_register_child_actions_success(self):
        """Test successful child action registration."""
        result = self.manager.register_child_actions("testsection")
        
        self.assertTrue(result)
        
        # Check that page actions file was updated
        page_actions_content = self.manager.page_actions_path.read_text(encoding='utf-8')
        
        # Should contain imports for both children
        self.assertIn("from './pages/analytics'", page_actions_content)
        self.assertIn("from './pages/dashboard'", page_actions_content)
        
        # Should contain registry entries with mergeWithCommonActions
        self.assertIn("analytics: mergeWithCommonActions", page_actions_content)
        self.assertIn("dashboard: mergeWithCommonActions", page_actions_content)
        
        # Should include sibling navigation
        self.assertIn("'go-to-dashboard'", page_actions_content)  # analytics siblings
        self.assertIn("'go-to-analytics'", page_actions_content)  # dashboard siblings
    
    def test_register_child_actions_no_children(self):
        """Test child action registration with parent that has no children."""
        # Create a parent with no children
        self.config_data["pages"]["lonely_parent"] = {
            "id": "lonely_parent",
            "name": "Lonely Parent",
            "type": "parent",
            "parent_id": "",
            "created_at": "2025-09-16T08:16:14.098211"
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        result = self.manager.register_child_actions("lonely_parent")
        
        # Should succeed but not add any entries
        self.assertTrue(result)
    
    def test_add_sibling_navigation_success(self):
        """Test successful sibling navigation addition."""
        result = self.manager.add_sibling_navigation("testsection")
        
        self.assertTrue(result)
        
        # Check that common actions file was updated
        common_actions_content = self.manager.common_actions_path.read_text(encoding='utf-8')
        
        # Should contain navigation actions for both children
        self.assertIn('"go-to-analytics"', common_actions_content)
        self.assertIn('"go-to-dashboard"', common_actions_content)
        self.assertIn("→ Analytics", common_actions_content)
        self.assertIn("→ Dashboard", common_actions_content)
        
        # Should contain sibling group
        self.assertIn("testsectionSiblings:", common_actions_content)
        self.assertIn("'go-to-analytics', 'go-to-dashboard'", common_actions_content)
    
    def test_add_sibling_navigation_single_child(self):
        """Test sibling navigation with only one child (no siblings)."""
        # Remove one child to test single child scenario
        del self.config_data["pages"]["dashboard"]
        self.config_data["metadata"]["child_pages"] = 1
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        result = self.manager.add_sibling_navigation("testsection")
        
        self.assertTrue(result)
        
        # Check that common actions file was updated
        common_actions_content = self.manager.common_actions_path.read_text(encoding='utf-8')
        
        # Should contain navigation action for single child
        self.assertIn('"go-to-analytics"', common_actions_content)
        
        # Should NOT contain sibling group (only one child)
        self.assertNotIn("testsectionSiblings:", common_actions_content)
    
    def test_validate_registry_integration_success(self):
        """Test registry integration validation for properly integrated page."""
        # First register the page
        self.manager.register_parent_actions("testsection")
        
        issues = self.manager.validate_registry_integration("testsection")
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_registry_integration_missing_import(self):
        """Test registry integration validation with missing import."""
        issues = self.manager.validate_registry_integration("testsection")
        
        # Should find missing import and registry entry
        self.assertEqual(len(issues), 2)
        self.assertIn("Missing import for testsection", issues)
        self.assertIn("Missing registry entry for testsection", issues)
    
    def test_get_children_for_parent(self):
        """Test retrieving children for a parent from config."""
        children = self.manager._get_children_for_parent("testsection")
        
        self.assertEqual(len(children), 2)
        
        # Check children are sorted by creation date
        child_ids = [child['id'] for child in children]
        self.assertIn("analytics", child_ids)
        self.assertIn("dashboard", child_ids)
        
        # Verify analytics comes first (earlier created_at)
        self.assertEqual(children[0]['id'], "analytics")
        self.assertEqual(children[1]['id'], "dashboard")
    
    def test_get_children_for_parent_no_children(self):
        """Test retrieving children for parent with no children."""
        children = self.manager._get_children_for_parent("nonexistent")
        
        self.assertEqual(len(children), 0)
    
    def test_has_import_detection(self):
        """Test import detection functionality."""
        content = "import { something } from './pages/testsection';"
        
        self.assertTrue(self.manager._has_import(content, "from './pages/testsection'"))
        self.assertFalse(self.manager._has_import(content, "from './pages/other'"))
    
    def test_add_import_functionality(self):
        """Test import addition functionality."""
        content = '''import { mergeWithCommonActions } from './common-actions.constants';

export const PAGE_ACTIONS = {
  // Entries here
};'''
        
        new_import = "import { pageActions as testsectionActions } from './pages/testsection'"
        result = self.manager._add_import(content, new_import)
        
        # Should add import before mergeWithCommonActions import
        lines = result.split('\n')
        import_line_idx = next(i for i, line in enumerate(lines) if 'testsectionActions' in line)
        merge_line_idx = next(i for i, line in enumerate(lines) if 'mergeWithCommonActions' in line)
        
        self.assertLess(import_line_idx, merge_line_idx)
    
    def test_add_registry_entry_functionality(self):
        """Test registry entry addition functionality."""
        content = '''export const PAGE_ACTIONS = {
  existing: existingActions.actions,
}'''
        
        registry_entry = "  testsection: testsectionActions.actions,"
        result = self.manager._add_registry_entry(content, registry_entry)
        
        # Should add entry before closing brace
        self.assertIn("testsection: testsectionActions.actions", result)
        self.assertIn("existing: existingActions.actions", result)
    
    def test_add_common_action_functionality(self):
        """Test common action addition functionality."""
        content = '''export const COMMON_ACTIONS = {
  existing: { id: 'existing' },
};'''
        
        action_definition = '''  "go-to-analytics": {
    id: "go-to-analytics",
    label: "→ Analytics",
    icon: Navigation,
    variant: "secondary",
  },'''
        
        result = self.manager._add_common_action(content, action_definition)
        
        # Should add action before closing
        self.assertIn('"go-to-analytics"', result)
        self.assertIn("→ Analytics", result)
        self.assertIn("existing:", result)
    
    def test_add_action_group_functionality(self):
        """Test action group addition functionality."""
        content = '''export const COMMON_ACTION_GROUPS = {
  existing: ['action1', 'action2'],
}'''
        
        group_definition = '''testsectionSiblings: [
    'go-to-analytics', 'go-to-dashboard'
  ],'''
        
        result = self.manager._add_action_group(content, group_definition)
        
        # Should add group before closing
        self.assertIn("testsectionSiblings:", result)
        self.assertIn("go-to-analytics", result)
        self.assertIn("existing:", result)
    
    def test_convenience_functions(self):
        """Test convenience functions for direct usage."""
        # Test parent registration convenience function
        result = register_parent_page_actions(self.frontend_root, "testsection")
        self.assertTrue(result)
        
        # Test child registration convenience function
        result = register_child_page_actions(self.frontend_root, "testsection")
        self.assertTrue(result)
    
    @patch('sys.path')
    def test_config_integration_error_handling(self, mock_sys_path):
        """Test error handling when config integration fails."""
        # Mock config integration failure
        with patch.object(self.manager.config_integration, 'load_config', side_effect=Exception("Config error")):
            result = self.manager._get_page_info("testsection")
            self.assertIsNone(result)
            
            children = self.manager._get_children_for_parent("testsection")
            self.assertEqual(len(children), 0)
    
    def test_file_not_found_error_handling(self):
        """Test error handling when action files don't exist."""
        # Remove the page actions file
        self.manager.page_actions_path.unlink()
        
        result = self.manager.register_parent_actions("testsection")
        self.assertFalse(result)
        
        result = self.manager.register_child_actions("testsection")
        self.assertFalse(result)
    
    def test_missing_common_actions_file(self):
        """Test error handling when common actions file doesn't exist."""
        # Remove the common actions file
        self.manager.common_actions_path.unlink()
        
        result = self.manager.add_sibling_navigation("testsection")
        self.assertFalse(result)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestActionRegistryManagerIntegration(unittest.TestCase):
    """Integration tests for ActionRegistryManager with real file operations."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create realistic directory structure
        self.src_dir = self.frontend_root / "src"
        self.actions_dir = self.src_dir / "constants" / "actions"
        self.pages_actions_dir = self.actions_dir / "pages"
        
        self.src_dir.mkdir(parents=True)
        self.actions_dir.mkdir(parents=True)
        self.pages_actions_dir.mkdir(parents=True)
        
        # Create realistic config
        self.config_data = {
            "pages": {
                "settings": {
                    "id": "settings",
                    "name": "Settings",
                    "type": "parent",
                    "parent_id": "",
                    "created_at": "2025-09-16T08:16:14.098211"
                },
                "profile": {
                    "id": "profile",
                    "name": "Profile",
                    "type": "child",
                    "parent_id": "settings",
                    "created_at": "2025-09-16T08:15:13.252651"
                },
                "preferences": {
                    "id": "preferences", 
                    "name": "Preferences",
                    "type": "child",
                    "parent_id": "settings",
                    "created_at": "2025-09-16T08:15:23.286873"
                }
            }
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        # Create realistic action files
        self.create_realistic_action_files()
        
        self.manager = ActionRegistryManager(self.frontend_root)
    
    def create_realistic_action_files(self):
        """Create realistic action files for integration testing."""
        
        # Realistic PAGE_ACTIONS file
        page_actions_content = '''import { mergeWithCommonActions } from './common-actions.constants';
import { pageActions as homeActions } from './pages/home';

export const PAGE_ACTIONS = {
  home: homeActions.actions,
} as const;

export type PageActionIds = keyof typeof PAGE_ACTIONS;
'''
        page_actions_path = self.actions_dir / "page-actions.constants.ts"
        page_actions_path.write_text(page_actions_content, encoding='utf-8')
        
        # Realistic COMMON_ACTIONS file
        common_actions_content = '''import { Navigation, Settings, User } from 'lucide-react';

export const COMMON_ACTIONS = {
  "go-to-home": {
    id: "go-to-home",
    label: "→ Home", 
    icon: Navigation,
    variant: "secondary",
  },
} as const;

export const COMMON_ACTION_GROUPS = {
  mainNavigation: [
    'go-to-home'
  ],
} as const;

export function mergeWithCommonActions(pageActions: any[], siblingActions: string[]) {
  const sibling = siblingActions.map(actionId => COMMON_ACTIONS[actionId as keyof typeof COMMON_ACTIONS]);
  return [...pageActions, ...sibling];
}
'''
        common_actions_path = self.actions_dir / "common-actions.constants.ts"
        common_actions_path.write_text(common_actions_content, encoding='utf-8')
    
    def test_full_integration_workflow(self):
        """Test the complete workflow from parent to children registration."""
        # Step 1: Register parent
        result = self.manager.register_parent_actions("settings")
        self.assertTrue(result)
        
        # Verify parent was added to PAGE_ACTIONS
        page_actions_content = self.manager.page_actions_path.read_text(encoding='utf-8')
        self.assertIn("settingsActions", page_actions_content)
        self.assertIn("settings: settingsActions.actions", page_actions_content)
        
        # Step 2: Register children
        result = self.manager.register_child_actions("settings")
        self.assertTrue(result)
        
        # Verify children were added to PAGE_ACTIONS
        page_actions_content = self.manager.page_actions_path.read_text(encoding='utf-8')
        self.assertIn("profileActions", page_actions_content)
        self.assertIn("preferencesActions", page_actions_content)
        self.assertIn("profile: mergeWithCommonActions", page_actions_content)
        self.assertIn("preferences: mergeWithCommonActions", page_actions_content)
        
        # Step 3: Add sibling navigation
        result = self.manager.add_sibling_navigation("settings")
        self.assertTrue(result)
        
        # Verify sibling navigation was added to COMMON_ACTIONS
        common_actions_content = self.manager.common_actions_path.read_text(encoding='utf-8')
        self.assertIn('"go-to-profile"', common_actions_content)
        self.assertIn('"go-to-preferences"', common_actions_content)
        self.assertIn("settingsSiblings:", common_actions_content)
        
        # Step 4: Validate integration
        issues = self.manager.validate_registry_integration("settings")
        self.assertEqual(len(issues), 0)
        
        issues = self.manager.validate_registry_integration("profile")
        self.assertEqual(len(issues), 0)
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    # Run all tests
    unittest.main()