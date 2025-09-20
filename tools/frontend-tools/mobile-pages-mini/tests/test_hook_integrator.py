"""
Tests for HookIntegrator - Functional hook generation and integration.

This test suite verifies the HookIntegrator functionality including:
- Parent action hook generation with real navigation methods
- Child action hook generation with sibling navigation
- Hook updating for new children
- Placeholder code removal and functional implementation
- pages.config.json source of truth validation
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

import sys
# Add modules path for imports
sys.path.append(str(Path(__file__).parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from hook_integrator import HookIntegrator, generate_parent_hook, generate_child_hook
from file_writer import FileWriter


class TestHookIntegrator(unittest.TestCase):
    """Test HookIntegrator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create directory structure
        self.src_dir = self.frontend_root / "src"
        self.hooks_dir = self.src_dir / "hooks"
        self.testsection_hooks_dir = self.hooks_dir / "testsection"
        
        self.src_dir.mkdir(parents=True)
        self.hooks_dir.mkdir(parents=True)
        self.testsection_hooks_dir.mkdir(parents=True)
        
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
                    "has_mobile": False,
                    "created_at": "2025-09-16T08:15:23.286873"
                },
                "reports": {
                    "id": "reports",
                    "name": "Reports",
                    "type": "child", 
                    "parent_id": "testsection",
                    "icon": "Navigation",
                    "description": "",
                    "route": "/reports",
                    "component_name": "ReportsPage",
                    "has_mobile": False,
                    "created_at": "2025-09-16T08:16:23.286873"
                }
            },
            "metadata": {
                "total_pages": 4,
                "parent_pages": 1,
                "child_pages": 3
            }
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        # Mock file writer
        self.mock_file_writer = Mock(spec=FileWriter)
        
        # Create integrator instance
        self.integrator = HookIntegrator(self.frontend_root, self.mock_file_writer)
    
    def test_generate_parent_action_hook_success(self):
        """Test successful parent action hook generation."""
        result = self.integrator.generate_parent_action_hook("testsection")
        
        self.assertTrue(result)
        
        # Check that hook file was created
        hook_path = self.integrator._get_parent_hook_path("testsection")
        self.assertTrue(hook_path.exists())
        
        hook_content = hook_path.read_text(encoding='utf-8')
        
        # Should contain functional implementation
        self.assertIn("import { useCallback } from 'react';", hook_content)
        self.assertIn("import { useAppStore } from '../../stores/appStore';", hook_content)
        self.assertIn("export function useTestsectionActions()", hook_content)
        
        # Should contain navigation methods for all children
        self.assertIn("goToAnalytics", hook_content)
        self.assertIn("goToDashboard", hook_content)
        self.assertIn("goToReports", hook_content)
        
        # Should have proper navigation logic
        self.assertIn("setCurrentChildPage('analytics')", hook_content)
        self.assertIn("setCurrentChildPage('dashboard')", hook_content)
        self.assertIn("setCurrentChildPage('reports')", hook_content)
        
        # Should NOT contain placeholder code
        self.assertNotIn("// Navigation methods will be added here", hook_content)
        self.assertNotIn("// Action methods will be returned here", hook_content)
    
    def test_generate_parent_action_hook_no_children(self):
        """Test parent hook generation with no children."""
        # Create parent with no children
        self.config_data["pages"]["lonely_parent"] = {
            "id": "lonely_parent",
            "name": "Lonely Parent",
            "type": "parent",
            "parent_id": "",
            "created_at": "2025-09-16T08:16:14.098211"
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        result = self.integrator.generate_parent_action_hook("lonely_parent")
        
        self.assertTrue(result)
        
        # Check hook content for no-children case
        hook_path = self.integrator._get_parent_hook_path("lonely_parent")
        hook_content = hook_path.read_text(encoding='utf-8')
        
        # Should have minimal imports (no useAppStore needed)
        self.assertIn("import { useCallback } from 'react';", hook_content)
        self.assertNotIn("import { useAppStore }", hook_content)
        
        # Should have appropriate messaging
        self.assertIn("No children found", hook_content)
        self.assertIn("return {};", hook_content)
    
    def test_generate_parent_action_hook_invalid_parent(self):
        """Test parent hook generation with invalid parent ID."""
        result = self.integrator.generate_parent_action_hook("nonexistent")
        
        self.assertFalse(result)
    
    def test_generate_child_action_hook_success(self):
        """Test successful child action hook generation."""
        result = self.integrator.generate_child_action_hook("analytics", "testsection")
        
        self.assertTrue(result)
        
        # Check that hook file was created
        hook_path = self.integrator._get_child_hook_path("analytics", "testsection")
        self.assertTrue(hook_path.exists())
        
        hook_content = hook_path.read_text(encoding='utf-8')
        
        # Should contain functional implementation
        self.assertIn("import { useCallback } from 'react';", hook_content)
        self.assertIn("import { useAppStore } from '../../stores/appStore';", hook_content)
        self.assertIn("export function useAnalyticsActions()", hook_content)
        
        # Should contain sibling navigation methods (dashboard and reports)
        self.assertIn("goToDashboard", hook_content)
        self.assertIn("goToReports", hook_content)
        # Should NOT contain self-navigation
        self.assertNotIn("goToAnalytics", hook_content)
        
        # Should have proper sibling navigation logic
        self.assertIn("setCurrentChildPage('dashboard')", hook_content)
        self.assertIn("setCurrentChildPage('reports')", hook_content)
        
        # Should NOT contain placeholder code
        self.assertNotIn("// Action methods will be returned here", hook_content)
    
    def test_generate_child_action_hook_no_siblings(self):
        """Test child hook generation with no siblings."""
        # Remove other children to test single child scenario
        del self.config_data["pages"]["dashboard"]
        del self.config_data["pages"]["reports"]
        self.config_data["metadata"]["child_pages"] = 1
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        result = self.integrator.generate_child_action_hook("analytics", "testsection")
        
        self.assertTrue(result)
        
        # Check hook content for no-siblings case
        hook_path = self.integrator._get_child_hook_path("analytics", "testsection")
        hook_content = hook_path.read_text(encoding='utf-8')
        
        # Should have minimal imports (no useAppStore needed)
        self.assertIn("import { useCallback } from 'react';", hook_content)
        self.assertNotIn("import { useAppStore }", hook_content)
        
        # Should have appropriate messaging
        self.assertIn("No siblings found", hook_content)
        self.assertIn("return {};", hook_content)
    
    def test_generate_child_action_hook_invalid_child(self):
        """Test child hook generation with invalid child ID."""
        result = self.integrator.generate_child_action_hook("nonexistent", "testsection")
        
        self.assertFalse(result)
    
    def test_update_parent_hook_for_new_child(self):
        """Test updating parent hook when new child is added."""
        # First generate initial parent hook
        self.integrator.generate_parent_action_hook("testsection")
        
        # Add new child to config
        self.config_data["pages"]["settings"] = {
            "id": "settings",
            "name": "Settings",
            "type": "child",
            "parent_id": "testsection",
            "created_at": "2025-09-16T08:17:00.000000"
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        # Update parent hook for new child
        result = self.integrator.update_parent_hook_for_new_child("testsection", "settings")
        
        self.assertTrue(result)
        
        # Check that hook was updated
        hook_path = self.integrator._get_parent_hook_path("testsection")
        hook_content = hook_path.read_text(encoding='utf-8')
        
        # Should now contain method for new child
        self.assertIn("goToSettings", hook_content)
        self.assertIn("setCurrentChildPage('settings')", hook_content)
        
        # Should still contain existing children
        self.assertIn("goToAnalytics", hook_content)
        self.assertIn("goToDashboard", hook_content)
        self.assertIn("goToReports", hook_content)
    
    def test_update_parent_hook_nonexistent_hook(self):
        """Test updating parent hook when hook doesn't exist."""
        # Should generate new hook
        result = self.integrator.update_parent_hook_for_new_child("testsection", "analytics")
        
        self.assertTrue(result)
        
        # Should create new hook file
        hook_path = self.integrator._get_parent_hook_path("testsection")
        self.assertTrue(hook_path.exists())
    
    def test_validate_hook_integration_parent_valid(self):
        """Test validation for properly integrated parent hook."""
        # Generate functional hook
        self.integrator.generate_parent_action_hook("testsection")
        
        issues = self.integrator.validate_hook_integration("testsection")
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_hook_integration_parent_placeholder(self):
        """Test validation for parent hook with placeholder code."""
        # Create hook with placeholder code
        hook_path = self.integrator._get_parent_hook_path("testsection")
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        placeholder_content = '''export function useTestsectionActions() {
  // Navigation methods will be added here when children are created
  return {
    // Action methods will be returned here when children are created
  }
}'''
        
        hook_path.write_text(placeholder_content, encoding='utf-8')
        
        issues = self.integrator.validate_hook_integration("testsection")
        
        # Should find placeholder issues
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("placeholder code" in issue for issue in issues))
    
    def test_validate_hook_integration_parent_missing_store(self):
        """Test validation for parent hook missing Zustand store integration."""
        # Create hook without store integration
        hook_path = self.integrator._get_parent_hook_path("testsection")
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        no_store_content = '''export function useTestsectionActions() {
  return {};
}'''
        
        hook_path.write_text(no_store_content, encoding='utf-8')
        
        issues = self.integrator.validate_hook_integration("testsection")
        
        # Should find store integration issues
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("Zustand store" in issue for issue in issues))
    
    def test_validate_hook_integration_child_valid(self):
        """Test validation for properly integrated child hook."""
        # Generate functional child hook
        self.integrator.generate_child_action_hook("analytics", "testsection")
        
        issues = self.integrator.validate_hook_integration("analytics")
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_hook_integration_child_placeholder(self):
        """Test validation for child hook with placeholder code."""
        # Create hook with placeholder code
        hook_path = self.integrator._get_child_hook_path("analytics", "testsection")
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        placeholder_content = '''export function useAnalyticsActions() {
  return {
    // Action methods will be returned here when children are created
  }
}'''
        
        hook_path.write_text(placeholder_content, encoding='utf-8')
        
        issues = self.integrator.validate_hook_integration("analytics")
        
        # Should find placeholder issues
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("placeholder code" in issue for issue in issues))
    
    def test_validate_hook_integration_nonexistent_page(self):
        """Test validation for nonexistent page."""
        issues = self.integrator.validate_hook_integration("nonexistent")
        
        self.assertGreater(len(issues), 0)
        self.assertIn("not found in config", issues[0])
    
    def test_validate_hook_integration_missing_hook_file(self):
        """Test validation when hook file doesn't exist."""
        issues = self.integrator.validate_hook_integration("testsection")
        
        # Should find missing hook file
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("hook file not found" in issue.lower() for issue in issues))
    
    def test_get_children_for_parent(self):
        """Test retrieving children for a parent from config."""
        children = self.integrator._get_children_for_parent("testsection")
        
        self.assertEqual(len(children), 3)
        
        # Check children are sorted by creation date
        child_ids = [child['id'] for child in children]
        self.assertEqual(child_ids, ["analytics", "dashboard", "reports"])  # Sorted by created_at
    
    def test_get_children_for_parent_no_children(self):
        """Test retrieving children for parent with no children."""
        children = self.integrator._get_children_for_parent("nonexistent")
        
        self.assertEqual(len(children), 0)
    
    def test_get_sibling_pages(self):
        """Test retrieving sibling pages for a child."""
        siblings = self.integrator._get_sibling_pages("analytics", "testsection")
        
        self.assertEqual(len(siblings), 2)  # dashboard and reports
        
        sibling_ids = [sibling['id'] for sibling in siblings]
        self.assertIn("dashboard", sibling_ids)
        self.assertIn("reports", sibling_ids)
        self.assertNotIn("analytics", sibling_ids)  # Should not include self
    
    def test_hook_path_methods(self):
        """Test hook path generation methods."""
        # Test parent hook path
        parent_path = self.integrator._get_parent_hook_path("testsection")
        expected_parent = self.hooks_dir / "testsection/useTestsectionActions.ts"
        self.assertEqual(parent_path, expected_parent)
        
        # Test child hook path
        child_path = self.integrator._get_child_hook_path("analytics", "testsection")
        expected_child = self.hooks_dir / "testsection/useAnalyticsActions.ts"
        self.assertEqual(child_path, expected_child)
    
    def test_remove_hook_placeholders(self):
        """Test removing placeholder code from existing hooks."""
        # Create hook with placeholders
        hook_path = self.integrator._get_parent_hook_path("testsection")
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        placeholder_content = '''import { useCallback } from 'react';
// import { useAppStore } from '../../stores/appStore';

export function useTestsectionActions() {
  // const { setSelectedTab, setCurrentChildPage } = useAppStore();
  
  // Navigation methods will be added here when children are created
  
  return {
    // Action methods will be returned here when children are created
  };
}'''
        
        hook_path.write_text(placeholder_content, encoding='utf-8')
        
        # Remove placeholders
        result = self.integrator.remove_hook_placeholders(hook_path)
        
        self.assertTrue(result)
        
        # Check that placeholders were removed
        final_content = hook_path.read_text(encoding='utf-8')
        self.assertNotIn("// Navigation methods will be added here", final_content)
        self.assertNotIn("// Action methods will be returned here", final_content)
        self.assertNotIn("// import { useAppStore }", final_content)
        self.assertNotIn("// const { setSelectedTab", final_content)
    
    def test_remove_hook_placeholders_no_placeholders(self):
        """Test removing placeholders from hook without any."""
        # Create hook without placeholders
        hook_path = self.integrator._get_parent_hook_path("testsection")
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        clean_content = '''export function useTestsectionActions() {
  return {};
}'''
        
        hook_path.write_text(clean_content, encoding='utf-8')
        
        # Should return False (no modifications made)
        result = self.integrator.remove_hook_placeholders(hook_path)
        
        self.assertFalse(result)
    
    def test_remove_hook_placeholders_nonexistent_file(self):
        """Test removing placeholders from nonexistent file."""
        nonexistent_path = self.hooks_dir / "nonexistent/hook.ts"
        
        result = self.integrator.remove_hook_placeholders(nonexistent_path)
        
        self.assertFalse(result)
    
    def test_generate_hook_index_file(self):
        """Test generating index file for hook directory."""
        result = self.integrator.generate_hook_index_file("testsection")
        
        self.assertTrue(result)
        
        # Check that index file was created
        index_path = self.hooks_dir / "testsection/index.ts"
        self.assertTrue(index_path.exists())
        
        index_content = index_path.read_text(encoding='utf-8')
        
        # Should export parent hook
        self.assertIn("export { useTestsectionActions }", index_content)
        
        # Should export all child hooks
        self.assertIn("export { useAnalyticsActions }", index_content)
        self.assertIn("export { useDashboardActions }", index_content)
        self.assertIn("export { useReportsActions }", index_content)
        
        # Should have proper imports
        self.assertIn("from './useTestsectionActions'", index_content)
        self.assertIn("from './useAnalyticsActions'", index_content)
    
    def test_generate_hook_index_file_invalid_parent(self):
        """Test generating index file for invalid parent."""
        result = self.integrator.generate_hook_index_file("nonexistent")
        
        self.assertFalse(result)
    
    def test_convenience_functions(self):
        """Test convenience functions for direct usage."""
        # Test parent hook generation convenience function
        result = generate_parent_hook(self.frontend_root, "testsection")
        self.assertTrue(result)
        
        # Test child hook generation convenience function  
        result = generate_child_hook(self.frontend_root, "analytics", "testsection")
        self.assertTrue(result)
    
    def test_generate_parent_hook_content_functionality(self):
        """Test the content generation for parent hooks."""
        parent_info = self.config_data["pages"]["testsection"]
        children = self.integrator._get_children_for_parent("testsection")
        
        content = self.integrator._generate_parent_hook_content("testsection", parent_info, children)
        
        # Should contain proper imports
        self.assertIn("import { useCallback } from 'react';", content)
        self.assertIn("import { useAppStore } from '../../stores/appStore';", content)
        
        # Should contain hook function
        self.assertIn("export function useTestsectionActions()", content)
        
        # Should contain navigation methods for each child
        for child in children:
            method_name = f"goTo{child['name']}"
            self.assertIn(method_name, content)
            self.assertIn(f"setCurrentChildPage('{child['id']}')", content)
        
        # Should have timeout wrapper for navigation
        self.assertIn("setTimeout(() => {", content)
        self.assertIn("}, 100);", content)
    
    def test_generate_child_hook_content_functionality(self):
        """Test the content generation for child hooks."""
        child_info = self.config_data["pages"]["analytics"]
        siblings = self.integrator._get_sibling_pages("analytics", "testsection")
        
        content = self.integrator._generate_child_hook_content("analytics", child_info, siblings)
        
        # Should contain proper imports
        self.assertIn("import { useCallback } from 'react';", content)
        self.assertIn("import { useAppStore } from '../../stores/appStore';", content)
        
        # Should contain hook function
        self.assertIn("export function useAnalyticsActions()", content)
        
        # Should contain sibling navigation methods
        for sibling in siblings:
            method_name = f"goTo{sibling['name']}"
            self.assertIn(method_name, content)
            self.assertIn(f"setCurrentChildPage('{sibling['id']}')", content)
    
    @patch('sys.path')
    def test_config_integration_error_handling(self, mock_sys_path):
        """Test error handling when config integration fails."""
        # Mock config integration failure
        with patch.object(self.integrator.config_integration, 'load_config', side_effect=Exception("Config error")):
            result = self.integrator._get_page_info("testsection")
            self.assertIsNone(result)
            
            children = self.integrator._get_children_for_parent("testsection")
            self.assertEqual(len(children), 0)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestHookIntegratorIntegration(unittest.TestCase):
    """Integration tests for HookIntegrator with realistic scenarios."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create realistic directory structure
        self.src_dir = self.frontend_root / "src"
        self.hooks_dir = self.src_dir / "hooks"
        self.settings_hooks_dir = self.hooks_dir / "settings"
        
        self.src_dir.mkdir(parents=True)
        self.hooks_dir.mkdir(parents=True)
        self.settings_hooks_dir.mkdir(parents=True)
        
        # Create realistic config with complex relationships
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
                    "has_mobile": True,
                    "created_at": "2025-09-16T08:15:13.252651"
                },
                "preferences": {
                    "id": "preferences", 
                    "name": "Preferences",
                    "type": "child",
                    "parent_id": "settings",
                    "has_mobile": False,
                    "created_at": "2025-09-16T08:15:23.286873"
                },
                "security": {
                    "id": "security",
                    "name": "Security", 
                    "type": "child",
                    "parent_id": "settings",
                    "has_mobile": True,
                    "created_at": "2025-09-16T08:16:23.286873"
                }
            }
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        self.integrator = HookIntegrator(self.frontend_root)
    
    def test_full_hook_integration_workflow(self):
        """Test the complete hook integration workflow."""
        # Step 1: Generate parent hook
        result = self.integrator.generate_parent_action_hook("settings")
        self.assertTrue(result)
        
        # Verify parent hook was properly generated
        parent_hook_path = self.integrator._get_parent_hook_path("settings")
        self.assertTrue(parent_hook_path.exists())
        
        parent_content = parent_hook_path.read_text(encoding='utf-8')
        
        # Should have all navigation methods
        self.assertIn("goToProfile", parent_content)
        self.assertIn("goToPreferences", parent_content)
        self.assertIn("goToSecurity", parent_content)
        
        # Should have proper navigation logic
        self.assertIn("setCurrentChildPage('profile')", parent_content)
        self.assertIn("setCurrentChildPage('preferences')", parent_content)
        self.assertIn("setCurrentChildPage('security')", parent_content)
        
        # Step 2: Generate child hooks
        result = self.integrator.generate_child_action_hook("profile", "settings")
        self.assertTrue(result)
        
        result = self.integrator.generate_child_action_hook("preferences", "settings")
        self.assertTrue(result)
        
        result = self.integrator.generate_child_action_hook("security", "settings")
        self.assertTrue(result)
        
        # Verify child hooks have proper sibling navigation
        profile_hook_path = self.integrator._get_child_hook_path("profile", "settings")
        profile_content = profile_hook_path.read_text(encoding='utf-8')
        
        # Profile should have navigation to preferences and security, but not itself
        self.assertIn("goToPreferences", profile_content)
        self.assertIn("goToSecurity", profile_content)
        self.assertNotIn("goToProfile", profile_content)
        
        # Step 3: Generate hook index
        result = self.integrator.generate_hook_index_file("settings")
        self.assertTrue(result)
        
        # Verify index exports all hooks
        index_path = self.hooks_dir / "settings/index.ts"
        index_content = index_path.read_text(encoding='utf-8')
        
        self.assertIn("export { useSettingsActions }", index_content)
        self.assertIn("export { useProfileActions }", index_content)
        self.assertIn("export { usePreferencesActions }", index_content)
        self.assertIn("export { useSecurityActions }", index_content)
        
        # Step 4: Add new child and update parent hook
        self.config_data["pages"]["notifications"] = {
            "id": "notifications",
            "name": "Notifications",
            "type": "child",
            "parent_id": "settings",
            "created_at": "2025-09-16T08:17:00.000000"
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        result = self.integrator.update_parent_hook_for_new_child("settings", "notifications")
        self.assertTrue(result)
        
        # Verify parent hook was updated
        updated_parent_content = parent_hook_path.read_text(encoding='utf-8')
        self.assertIn("goToNotifications", updated_parent_content)
        self.assertIn("setCurrentChildPage('notifications')", updated_parent_content)
        
        # Step 5: Validate all integrations
        parent_issues = self.integrator.validate_hook_integration("settings")
        self.assertEqual(len(parent_issues), 0)
        
        for child_id in ["profile", "preferences", "security"]:
            child_issues = self.integrator.validate_hook_integration(child_id)
            self.assertEqual(len(child_issues), 0)
    
    def test_hook_generation_with_realistic_names(self):
        """Test hook generation with realistic component names."""
        # Generate hooks
        self.integrator.generate_parent_action_hook("settings")
        self.integrator.generate_child_action_hook("profile", "settings")
        
        # Check that generated methods use proper naming
        parent_hook_path = self.integrator._get_parent_hook_path("settings")
        parent_content = parent_hook_path.read_text(encoding='utf-8')
        
        # Should use actual page names from config
        self.assertIn("goToProfile", parent_content)  # Uses "Profile" from config name
        self.assertIn("goToPreferences", parent_content)  # Uses "Preferences" from config name
        self.assertIn("goToSecurity", parent_content)  # Uses "Security" from config name
        
        # Child hook should use proper naming for siblings
        child_hook_path = self.integrator._get_child_hook_path("profile", "settings")
        child_content = child_hook_path.read_text(encoding='utf-8')
        
        self.assertIn("goToPreferences", child_content)
        self.assertIn("goToSecurity", child_content)
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    # Run all tests
    unittest.main()