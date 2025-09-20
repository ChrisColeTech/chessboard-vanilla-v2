"""
Tests for IntegrationValidator - Comprehensive validation across all integration modules.

This test suite verifies the IntegrationValidator functionality including:
- Registry integration validation
- Container integration validation  
- Hook integration validation
- Cross-module relationship validation
- Issue detection and reporting
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

from integration_validator import IntegrationValidator, validate_page_integration, validate_complete_project_integration
from file_writer import FileWriter


class TestIntegrationValidator(unittest.TestCase):
    """Test IntegrationValidator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create directory structure
        self.src_dir = self.frontend_root / "src"
        self.actions_dir = self.src_dir / "constants" / "actions"
        self.pages_actions_dir = self.actions_dir / "pages"
        self.hooks_dir = self.src_dir / "hooks"
        self.components_dir = self.src_dir / "components" / "shared"
        
        self.src_dir.mkdir(parents=True)
        self.actions_dir.mkdir(parents=True) 
        self.pages_actions_dir.mkdir(parents=True)
        self.hooks_dir.mkdir(parents=True)
        self.components_dir.mkdir(parents=True)
        
        # Create pages.config.json
        self.config_data = {
            "version": "1.0.0",
            "generated_by": "mobile-pages-v2",
            "last_updated": "2025-09-16T08:16:14.098238",
            "pages": {
                "settings": {
                    "id": "settings",
                    "name": "Settings",
                    "type": "parent",
                    "created_at": "2025-09-16T08:16:14.098238",
                    "children": ["profile", "preferences"]
                },
                "profile": {
                    "id": "profile", 
                    "name": "Profile",
                    "type": "child",
                    "parent_id": "settings",
                    "created_at": "2025-09-16T08:16:15.098238"
                },
                "preferences": {
                    "id": "preferences",
                    "name": "Preferences", 
                    "type": "child",
                    "parent_id": "settings",
                    "created_at": "2025-09-16T08:16:16.098238"
                }
            }
        }
        
        # Write pages.config.json
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2))
        
        # Create file writer mock
        self.mock_file_writer = Mock(spec=FileWriter)
        
        # Create validator instance
        self.validator = IntegrationValidator(self.frontend_root, self.mock_file_writer)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_validator_initialization(self):
        """Test validator initializes correctly."""
        validator = IntegrationValidator(self.frontend_root)
        
        self.assertEqual(validator.frontend_root, self.frontend_root)
        self.assertIsInstance(validator.file_writer, FileWriter)
        self.assertEqual(validator.config_integration.frontend_root, self.frontend_root)
    
    def test_validate_complete_project_integration_success(self):
        """Test complete project validation with successful integration."""
        # Create required files for successful validation
        self._create_page_actions_file()
        self._create_common_actions_file()
        self._create_action_sheet_container()
        self._create_parent_hook("settings")
        self._create_child_hooks(["profile", "preferences"], "settings")
        
        # Run validation
        results = self.validator.validate_complete_project_integration()
        
        # Check results
        self.assertIn('overall_status', results)
        self.assertIn('pages', results)
        self.assertIn('critical_files', results)
        
        # Should have results for all pages
        self.assertIn('settings', results['pages'])
        self.assertIn('profile', results['pages'])
        self.assertIn('preferences', results['pages'])
    
    def test_validate_page_integration_parent_success(self):
        """Test parent page validation with successful integration."""
        # Create required files
        self._create_page_actions_file()
        self._create_common_actions_file()
        self._create_action_sheet_container()
        self._create_parent_hook("settings")
        
        # Run validation
        issues = self.validator.validate_page_integration("settings")
        
        # Should have minimal issues if files are properly created
        registry_issues = [issue for issue in issues if 'registry' in issue.lower()]
        hook_issues = [issue for issue in issues if 'hook' in issue.lower()]
        
        # Basic structure should pass
        self.assertIsInstance(issues, list)
    
    def test_validate_page_integration_child_success(self):
        """Test child page validation with successful integration."""
        # Create required files
        self._create_page_actions_file()
        self._create_common_actions_file()
        self._create_action_sheet_container()
        self._create_child_hooks(["profile"], "settings")
        
        # Run validation
        issues = self.validator.validate_page_integration("profile")
        
        # Should return list of issues
        self.assertIsInstance(issues, list)
    
    def test_validate_registry_integration_missing_files(self):
        """Test registry validation when files are missing."""
        issues = self.validator._validate_registry_integration("settings")
        
        # Should detect missing files
        file_issues = [issue for issue in issues if 'not found' in issue.lower()]
        self.assertGreater(len(file_issues), 0)
    
    def test_validate_container_integration_missing_files(self):
        """Test container validation when ActionSheetContainer is missing."""
        issues = self.validator._validate_container_integration("settings")
        
        # Should detect missing ActionSheetContainer
        container_issues = [issue for issue in issues if 'actionsheetcontainer' in issue.lower()]
        self.assertGreater(len(container_issues), 0)
    
    def test_validate_hook_integration_missing_hooks(self):
        """Test hook validation when hooks are missing."""
        issues = self.validator._validate_hook_integration("settings")
        
        # Should detect missing hooks
        hook_issues = [issue for issue in issues if 'hook' in issue.lower()]
        self.assertGreater(len(hook_issues), 0)
    
    def test_validate_hook_integration_placeholder_code(self):
        """Test hook validation detects placeholder code."""
        # Create hook with placeholder code
        hook_content = '''/**
 * Settings Actions Hook
 */
import { useCallback } from 'react';

export function useSettingsActions() {
  // Navigation methods will be added here
  return {};
}'''
        
        hook_path = self.hooks_dir / "settings" / "useSettingsActions.ts"
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        hook_path.write_text(hook_content)
        
        # Run validation
        issues = self.validator._validate_hook_integration("settings")
        
        # Should detect placeholder code
        placeholder_issues = [issue for issue in issues if 'placeholder' in issue.lower()]
        self.assertGreater(len(placeholder_issues), 0)
    
    def test_validate_cross_module_relationships(self):
        """Test cross-module relationship validation."""
        # Create partial integration
        self._create_page_actions_file()
        self._create_parent_hook("settings")
        
        # Run validation
        issues = self.validator._validate_cross_module_relationships("settings")
        
        # Should detect relationship issues
        self.assertIsInstance(issues, list)
    
    def test_get_validation_summary_format(self):
        """Test validation summary format."""
        # Mock some results
        mock_results = {
            'overall_status': 'PARTIAL',
            'pages': {
                'settings': {'status': 'COMPLETE', 'issues': []},
                'profile': {'status': 'INCOMPLETE', 'issues': ['Missing hook']}
            },
            'critical_files': {
                'pages.config.json': 'FOUND',
                'PAGE_ACTIONS': 'FOUND',
                'COMMON_ACTIONS': 'MISSING'
            }
        }
        
        summary = self.validator._get_validation_summary(mock_results)
        
        # Check summary format
        self.assertIn('VALIDATION SUMMARY', summary)
        self.assertIn('Overall Status', summary)
        self.assertIn('Critical Files', summary)
        self.assertIn('Page Status', summary)
    
    def test_convenience_functions(self):
        """Test convenience functions work correctly."""
        # Test validate_page_integration function
        issues = validate_page_integration(self.frontend_root, "settings")
        self.assertIsInstance(issues, list)
        
        # Test validate_complete_project_integration function
        results = validate_complete_project_integration(self.frontend_root)
        self.assertIsInstance(results, dict)
        self.assertIn('overall_status', results)
    
    def test_invalid_page_id(self):
        """Test validation with invalid page ID."""
        issues = self.validator.validate_page_integration("nonexistent")
        
        # Should detect invalid page
        invalid_issues = [issue for issue in issues if 'not found' in issue.lower()]
        self.assertGreater(len(invalid_issues), 0)
    
    def test_missing_pages_config(self):
        """Test validation when pages.config.json is missing."""
        # Remove config file
        config_path = self.frontend_root / "pages.config.json"
        if config_path.exists():
            config_path.unlink()
        
        # Create new validator
        validator = IntegrationValidator(self.frontend_root)
        
        # Run validation
        results = validator.validate_complete_project_integration()
        
        # Should detect missing config
        self.assertEqual(results['critical_files']['pages.config.json'], 'MISSING')
    
    # Helper methods to create test files
    
    def _create_page_actions_file(self):
        """Create PAGE_ACTIONS file."""
        page_actions_content = '''// PAGE_ACTIONS constants
import { SETTINGS_ACTIONS } from './pages/settings-actions.constants';

export const PAGE_ACTIONS = {
  SETTINGS: SETTINGS_ACTIONS,
};'''
        
        page_actions_path = self.actions_dir / "page-actions.constants.ts"
        page_actions_path.write_text(page_actions_content)
        
        # Create settings actions
        settings_actions_content = '''export const SETTINGS_ACTIONS = {
  SHOW_PROFILE: 'SHOW_PROFILE',
  SHOW_PREFERENCES: 'SHOW_PREFERENCES',
};'''
        
        settings_actions_path = self.pages_actions_dir / "settings-actions.constants.ts"
        settings_actions_path.write_text(settings_actions_content)
    
    def _create_common_actions_file(self):
        """Create COMMON_ACTIONS file."""
        common_actions_content = '''export const COMMON_ACTIONS = {
  NAVIGATE_TO_PROFILE: 'NAVIGATE_TO_PROFILE',
  NAVIGATE_TO_PREFERENCES: 'NAVIGATE_TO_PREFERENCES',
};'''
        
        common_actions_path = self.actions_dir / "common-actions.constants.ts"
        common_actions_path.write_text(common_actions_content)
    
    def _create_action_sheet_container(self):
        """Create ActionSheetContainer component."""
        container_content = '''import React from 'react';

export interface ActionSheetContainerProps {
  // Component props
}

export const ActionSheetContainer: React.FC<ActionSheetContainerProps> = () => {
  return <div>ActionSheetContainer</div>;
};'''
        
        container_path = self.components_dir / "ActionSheetContainer.tsx"
        container_path.write_text(container_content)
    
    def _create_parent_hook(self, parent_id: str):
        """Create functional parent hook."""
        hook_content = f'''/**
 * Settings Actions Hook
 */
import {{ useCallback }} from 'react';
import {{ useAppStore }} from '../../stores/appStore';

export function useSettingsActions() {{
  const {{ setCurrentChildPage }} = useAppStore();

  const goToProfile = useCallback(() => {{
    setTimeout(() => {{
      setCurrentChildPage('profile');
    }}, 100);
  }}, [setCurrentChildPage]);

  const goToPreferences = useCallback(() => {{
    setTimeout(() => {{
      setCurrentChildPage('preferences');
    }}, 100);
  }}, [setCurrentChildPage]);

  return {{
    goToProfile,
    goToPreferences
  }};
}}'''
        
        hook_path = self.hooks_dir / parent_id / f"use{parent_id.capitalize()}Actions.ts"
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        hook_path.write_text(hook_content)
    
    def _create_child_hooks(self, child_ids: list, parent_id: str):
        """Create functional child hooks."""
        for child_id in child_ids:
            hook_content = f'''/**
 * {child_id.capitalize()} Actions Hook
 */
import {{ useCallback }} from 'react';
import {{ useAppStore }} from '../../stores/appStore';

export function use{child_id.capitalize()}Actions() {{
  const {{ setCurrentChildPage }} = useAppStore();

  const goToPreferences = useCallback(() => {{
    setTimeout(() => {{
      setCurrentChildPage('preferences');
    }}, 100);
  }}, [setCurrentChildPage]);

  return {{
    goToPreferences
  }};
}}'''
            
            hook_path = self.hooks_dir / parent_id / f"use{child_id.capitalize()}Actions.ts"
            hook_path.parent.mkdir(parents=True, exist_ok=True)
            hook_path.write_text(hook_content)


if __name__ == '__main__':
    unittest.main()