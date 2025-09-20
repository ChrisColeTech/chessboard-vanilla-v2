"""
Tests for ContainerIntegrator - Integration with ActionSheetContainer system.

This test suite verifies the ContainerIntegrator functionality including:
- Parent page container integration
- Child page container integration  
- Mobile variant container integration
- Action handling imports and setup
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

from container_integrator import ContainerIntegrator, integrate_parent_container, integrate_child_containers
from file_writer import FileWriter


class TestContainerIntegrator(unittest.TestCase):
    """Test ContainerIntegrator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create directory structure
        self.src_dir = self.frontend_root / "src"
        self.pages_dir = self.src_dir / "pages"
        self.components_dir = self.src_dir / "components"
        self.shared_dir = self.components_dir / "shared"
        self.testsection_dir = self.pages_dir / "testsection"
        
        self.src_dir.mkdir(parents=True)
        self.pages_dir.mkdir(parents=True)
        self.components_dir.mkdir(parents=True)
        self.shared_dir.mkdir(parents=True)
        self.testsection_dir.mkdir(parents=True)
        
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
        
        # Create mock component files
        self.create_mock_components()
        
        # Mock file writer
        self.mock_file_writer = Mock(spec=FileWriter)
        
        # Create integrator instance
        self.integrator = ContainerIntegrator(self.frontend_root, self.mock_file_writer)
    
    def create_mock_components(self):
        """Create mock component files for testing."""
        
        # ActionSheetContainer
        container_content = '''import React from 'react';

export function ActionSheetContainer() {
  return <div className="action-sheet-container">Actions</div>;
}
'''
        container_path = self.shared_dir / "ActionSheetContainer.tsx"
        container_path.write_text(container_content, encoding='utf-8')
        
        # Parent page (without action handling)
        parent_content = '''import React from 'react';

function TestsectionPage() {
  return (
    <div className="testsection-page">
      <h1>Testsection</h1>
    </div>
  );
}

export default TestsectionPage;
'''
        parent_path = self.testsection_dir / "TestsectionPage.tsx"
        parent_path.write_text(parent_content, encoding='utf-8')
        
        # Child page (without action handling)
        child_content = '''import React from 'react';

function Analytics() {
  return (
    <div className="analytics-page">
      <h1>Analytics</h1>
    </div>
  );
}

export default Analytics;
'''
        child_path = self.testsection_dir / "Analytics.tsx"
        child_path.write_text(child_content, encoding='utf-8')
        
        # Mobile child page
        mobile_child_content = '''import React from 'react';

function MobileAnalytics() {
  return (
    <div className="mobile-analytics-page">
      <h1>Mobile Analytics</h1>
    </div>
  );
}

export default MobileAnalytics;
'''
        mobile_child_path = self.testsection_dir / "MobileAnalytics.tsx"
        mobile_child_path.write_text(mobile_child_content, encoding='utf-8')
        
        # Dashboard child (without mobile variant)
        dashboard_content = '''import React from 'react';

function Dashboard() {
  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
    </div>
  );
}

export default Dashboard;
'''
        dashboard_path = self.testsection_dir / "Dashboard.tsx"
        dashboard_path.write_text(dashboard_content, encoding='utf-8')
    
    def test_integrate_parent_page_success(self):
        """Test successful parent page container integration."""
        result = self.integrator.integrate_parent_page("testsection")
        
        self.assertTrue(result)
        
        # Check that parent page was updated
        parent_path = self.integrator._get_parent_page_path("testsection")
        parent_content = parent_path.read_text(encoding='utf-8')
        
        # Should contain action handling imports
        self.assertIn("usePageActions", parent_content)
        self.assertIn("ActionSheetContainer", parent_content)
        
        # Should contain hook usage
        self.assertIn('usePageActions("testsection")', parent_content)
        
        # Should contain ActionSheetContainer in JSX
        self.assertIn('<ActionSheetContainer', parent_content)
    
    def test_integrate_parent_page_invalid_parent(self):
        """Test parent integration with invalid parent ID."""
        result = self.integrator.integrate_parent_page("nonexistent")
        
        self.assertFalse(result)
    
    def test_integrate_parent_page_missing_container(self):
        """Test parent integration when ActionSheetContainer is missing."""
        # Remove ActionSheetContainer
        self.integrator.action_sheet_container_path.unlink()
        
        result = self.integrator.integrate_parent_page("testsection")
        
        self.assertFalse(result)
    
    def test_integrate_child_pages_success(self):
        """Test successful child pages container integration."""
        result = self.integrator.integrate_child_pages("testsection")
        
        self.assertTrue(result)
        
        # Check that both child pages were updated
        analytics_path = self.integrator._get_child_page_path("analytics", "testsection")
        analytics_content = analytics_path.read_text(encoding='utf-8')
        
        # Should contain action handling
        self.assertIn("usePageActions", analytics_content)
        self.assertIn('usePageActions("analytics")', analytics_content)
        
        # Check dashboard page
        dashboard_path = self.integrator._get_child_page_path("dashboard", "testsection")
        dashboard_content = dashboard_path.read_text(encoding='utf-8')
        
        self.assertIn("usePageActions", dashboard_content)
        self.assertIn('usePageActions("dashboard")', dashboard_content)
        
        # Check mobile variant for analytics
        mobile_path = self.integrator._get_mobile_child_page_path("analytics", "testsection")
        mobile_content = mobile_path.read_text(encoding='utf-8')
        
        self.assertIn("usePageActions", mobile_content)
        self.assertIn('usePageActions("analytics")', mobile_content)
    
    def test_integrate_child_pages_no_children(self):
        """Test child integration with parent that has no children."""
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
        
        result = self.integrator.integrate_child_pages("lonely_parent")
        
        # Should succeed but not process any children
        self.assertTrue(result)
    
    def test_validate_container_integration_parent_valid(self):
        """Test validation for properly integrated parent page."""
        # First integrate the parent
        self.integrator.integrate_parent_page("testsection")
        
        issues = self.integrator.validate_container_integration("testsection")
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_container_integration_parent_invalid(self):
        """Test validation for parent page without integration."""
        issues = self.integrator.validate_container_integration("testsection")
        
        # Should find missing action handling
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("usePageActions" in issue for issue in issues))
        self.assertTrue(any("ActionSheetContainer" in issue for issue in issues))
    
    def test_validate_container_integration_child_valid(self):
        """Test validation for properly integrated child page."""
        # First integrate the child
        self.integrator.integrate_child_pages("testsection")
        
        issues = self.integrator.validate_container_integration("analytics")
        
        self.assertEqual(len(issues), 0)
    
    def test_validate_container_integration_child_invalid(self):
        """Test validation for child page without integration."""
        issues = self.integrator.validate_container_integration("analytics")
        
        # Should find missing action handling
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("usePageActions" in issue for issue in issues))
    
    def test_validate_container_integration_nonexistent_page(self):
        """Test validation for nonexistent page."""
        issues = self.integrator.validate_container_integration("nonexistent")
        
        self.assertGreater(len(issues), 0)
        self.assertIn("not found in config", issues[0])
    
    def test_get_children_for_parent(self):
        """Test retrieving children for a parent from config."""
        children = self.integrator._get_children_for_parent("testsection")
        
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
        children = self.integrator._get_children_for_parent("nonexistent")
        
        self.assertEqual(len(children), 0)
    
    def test_page_path_methods(self):
        """Test page path generation methods."""
        # Test parent path
        parent_path = self.integrator._get_parent_page_path("testsection")
        expected_parent = self.frontend_root / "src/pages/testsection/TestsectionPage.tsx"
        self.assertEqual(parent_path, expected_parent)
        
        # Test child path
        child_path = self.integrator._get_child_page_path("analytics", "testsection")
        expected_child = self.frontend_root / "src/pages/testsection/Analytics.tsx"
        self.assertEqual(child_path, expected_child)
        
        # Test mobile child path
        mobile_path = self.integrator._get_mobile_child_page_path("analytics", "testsection")
        expected_mobile = self.frontend_root / "src/pages/testsection/MobileAnalytics.tsx"
        self.assertEqual(mobile_path, expected_mobile)
    
    def test_has_import_detection(self):
        """Test import detection functionality."""
        content = "import { usePageActions } from './hooks/usePageActions';"
        
        self.assertTrue(self.integrator._has_import(content, "usePageActions"))
        self.assertFalse(self.integrator._has_import(content, "useOtherHook"))
    
    def test_add_import_functionality(self):
        """Test import addition functionality."""
        content = '''import React from 'react';
import { useState } from 'react';

function Component() {
  return <div>Test</div>;
}'''
        
        new_import = 'import { usePageActions } from "../../hooks/core/usePageActions";'
        result = self.integrator._add_import(content, new_import)
        
        # Should add import after existing imports
        lines = result.split('\n')
        import_lines = [line for line in lines if line.startswith('import')]
        
        self.assertEqual(len(import_lines), 3)  # Original 2 + 1 new
        self.assertIn('usePageActions', result)
    
    def test_add_import_to_empty_file(self):
        """Test adding import to file without existing imports."""
        content = '''function Component() {
  return <div>Test</div>;
}'''
        
        new_import = 'import { usePageActions } from "../../hooks/core/usePageActions";'
        result = self.integrator._add_import(content, new_import)
        
        # Should add import at the top
        self.assertTrue(result.startswith(new_import))
    
    def test_add_hook_usage_functionality(self):
        """Test hook usage addition functionality."""
        content = '''function TestComponent() {
  const [state, setState] = useState(false);
  
  return <div>Test</div>;
}'''
        
        hook_usage = '  usePageActions("test");'
        result = self.integrator._add_hook_usage(content, hook_usage)
        
        # Should add hook usage inside function
        self.assertIn('usePageActions("test");', result)
        
        # Should be after function opening brace
        lines = result.split('\n')
        function_line_idx = next(i for i, line in enumerate(lines) if 'function TestComponent' in line)
        hook_line_idx = next(i for i, line in enumerate(lines) if 'usePageActions' in line)
        
        self.assertLess(function_line_idx, hook_line_idx)
    
    def test_add_hook_usage_arrow_function(self):
        """Test hook usage addition with arrow function."""
        content = '''const TestComponent = () => {
  const [state, setState] = useState(false);
  
  return <div>Test</div>;
};'''
        
        hook_usage = '  usePageActions("test");'
        result = self.integrator._add_hook_usage(content, hook_usage)
        
        # Should add hook usage inside arrow function
        self.assertIn('usePageActions("test");', result)
    
    def test_add_action_sheet_container_to_jsx(self):
        """Test adding ActionSheetContainer to JSX."""
        content = '''function TestComponent() {
  return (
    <div className="test">
      <h1>Test</h1>
    </div>
  );
}'''
        
        result = self.integrator._add_action_sheet_container_to_jsx(content)
        
        # Should add ActionSheetContainer
        self.assertIn('<ActionSheetContainer />', result)
        
        # Should be before closing div
        self.assertIn('ActionSheetContainer', result)
    
    def test_convenience_functions(self):
        """Test convenience functions for direct usage."""
        # Test parent integration convenience function
        result = integrate_parent_container(self.frontend_root, "testsection")
        self.assertTrue(result)
        
        # Test child integration convenience function
        result = integrate_child_containers(self.frontend_root, "testsection")
        self.assertTrue(result)
    
    def test_integration_with_existing_action_handling(self):
        """Test integration when pages already have action handling."""
        # Modify parent to already have action handling
        parent_path = self.integrator._get_parent_page_path("testsection")
        existing_content = '''import React from 'react';
import { usePageActions } from "../../hooks/core/usePageActions";
import { ActionSheetContainer } from "../../components/shared/ActionSheetContainer";

function TestsectionPage() {
  usePageActions("testsection");
  
  return (
    <div className="testsection-page">
      <h1>Testsection</h1>
      <ActionSheetContainer />
    </div>
  );
}

export default TestsectionPage;
'''
        parent_path.write_text(existing_content, encoding='utf-8')
        
        # Should still succeed without duplicating
        result = self.integrator.integrate_parent_page("testsection")
        self.assertTrue(result)
        
        # Content should not have duplicated imports/hooks
        final_content = parent_path.read_text(encoding='utf-8')
        
        # Check that there's only one function call (not counting import)
        lines = final_content.split('\n')
        hook_call_lines = [line for line in lines if 'usePageActions("testsection")' in line and not line.strip().startswith('import')]
        self.assertEqual(len(hook_call_lines), 1)  # Only one function call
        
        # Check that there's only one import statement
        import_lines = [line for line in lines if 'import { usePageActions }' in line]
        self.assertEqual(len(import_lines), 1)  # Only one import
    
    @patch('sys.path')
    def test_config_integration_error_handling(self, mock_sys_path):
        """Test error handling when config integration fails."""
        # Mock config integration failure
        with patch.object(self.integrator.config_integration, 'load_config', side_effect=Exception("Config error")):
            result = self.integrator._get_page_info("testsection")
            self.assertIsNone(result)
            
            children = self.integrator._get_children_for_parent("testsection")
            self.assertEqual(len(children), 0)
    
    def test_missing_page_files_error_handling(self):
        """Test error handling when page files don't exist."""
        # Remove parent page file
        parent_path = self.integrator._get_parent_page_path("testsection")
        parent_path.unlink()
        
        result = self.integrator.integrate_parent_page("testsection")
        self.assertFalse(result)
        
        # Remove child page file
        child_path = self.integrator._get_child_page_path("analytics", "testsection")
        child_path.unlink()
        
        result = self.integrator.integrate_child_pages("testsection")
        self.assertFalse(result)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestContainerIntegratorIntegration(unittest.TestCase):
    """Integration tests for ContainerIntegrator with realistic scenarios."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.frontend_root = Path(self.temp_dir)
        
        # Create realistic directory structure
        self.src_dir = self.frontend_root / "src"
        self.pages_dir = self.src_dir / "pages"
        self.components_dir = self.src_dir / "components"
        self.shared_dir = self.components_dir / "shared"
        self.settings_dir = self.pages_dir / "settings"
        
        self.src_dir.mkdir(parents=True)
        self.pages_dir.mkdir(parents=True)
        self.components_dir.mkdir(parents=True)
        self.shared_dir.mkdir(parents=True)
        self.settings_dir.mkdir(parents=True)
        
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
                }
            }
        }
        
        config_path = self.frontend_root / "pages.config.json"
        config_path.write_text(json.dumps(self.config_data, indent=2), encoding='utf-8')
        
        # Create realistic component files
        self.create_realistic_components()
        
        self.integrator = ContainerIntegrator(self.frontend_root)
    
    def create_realistic_components(self):
        """Create realistic component files for integration testing."""
        
        # ActionSheetContainer with realistic implementation
        container_content = '''import React from 'react';
import { useActionSheet } from '../../hooks/useActionSheet';

export function ActionSheetContainer() {
  const { isVisible, currentAction, executeAction } = useActionSheet();
  
  if (!isVisible || !currentAction) {
    return null;
  }
  
  return (
    <div className="action-sheet-overlay">
      <div className="action-sheet">
        <button onClick={() => executeAction(currentAction)}>
          {currentAction.label}
        </button>
      </div>
    </div>
  );
}
'''
        container_path = self.shared_dir / "ActionSheetContainer.tsx"
        container_path.write_text(container_content, encoding='utf-8')
        
        # Realistic parent page
        parent_content = '''import React, { useState } from 'react';

function SettingsPage() {
  const [currentChildPage, setCurrentChildPage] = useState<string>('profile');
  
  return (
    <div className="settings-page">
      <header className="settings-header">
        <h1>Settings</h1>
      </header>
      <nav className="settings-nav">
        <button onClick={() => setCurrentChildPage('profile')}>Profile</button>
        <button onClick={() => setCurrentChildPage('preferences')}>Preferences</button>
      </nav>
      <main className="settings-content">
        {/* Child page content will be rendered here */}
      </main>
    </div>
  );
}

export default SettingsPage;
'''
        parent_path = self.settings_dir / "SettingsPage.tsx"
        parent_path.write_text(parent_content, encoding='utf-8')
        
        # Realistic child pages
        profile_content = '''import React, { useState } from 'react';

function Profile() {
  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
    avatar: ''
  });
  
  return (
    <div className="profile-page">
      <h2>Profile Settings</h2>
      <form className="profile-form">
        <input 
          type="text" 
          placeholder="Name" 
          value={profileData.name}
          onChange={(e) => setProfileData(prev => ({ ...prev, name: e.target.value }))}
        />
        <input 
          type="email" 
          placeholder="Email" 
          value={profileData.email}
          onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
        />
      </form>
    </div>
  );
}

export default Profile;
'''
        profile_path = self.settings_dir / "Profile.tsx"
        profile_path.write_text(profile_content, encoding='utf-8')
        
        # Mobile variant
        mobile_profile_content = '''import React, { useState } from 'react';

function MobileProfile() {
  const [profileData, setProfileData] = useState({
    name: '',
    email: ''
  });
  
  return (
    <div className="mobile-profile-page">
      <div className="mobile-header">
        <h2>Profile</h2>
      </div>
      <div className="mobile-form">
        <input type="text" placeholder="Name" value={profileData.name} />
        <input type="email" placeholder="Email" value={profileData.email} />
      </div>
    </div>
  );
}

export default MobileProfile;
'''
        mobile_profile_path = self.settings_dir / "MobileProfile.tsx"
        mobile_profile_path.write_text(mobile_profile_content, encoding='utf-8')
        
        # Preferences page (no mobile)
        preferences_content = '''import React, { useState } from 'react';

function Preferences() {
  const [preferences, setPreferences] = useState({
    theme: 'light',
    notifications: true,
    language: 'en'
  });
  
  return (
    <div className="preferences-page">
      <h2>Preferences</h2>
      <div className="preferences-form">
        <label>
          Theme:
          <select 
            value={preferences.theme}
            onChange={(e) => setPreferences(prev => ({ ...prev, theme: e.target.value }))}
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label>
          <input 
            type="checkbox"
            checked={preferences.notifications}
            onChange={(e) => setPreferences(prev => ({ ...prev, notifications: e.target.checked }))}
          />
          Enable Notifications
        </label>
      </div>
    </div>
  );
}

export default Preferences;
'''
        preferences_path = self.settings_dir / "Preferences.tsx"
        preferences_path.write_text(preferences_content, encoding='utf-8')
    
    def test_full_integration_workflow(self):
        """Test the complete container integration workflow."""
        # Step 1: Integrate parent
        result = self.integrator.integrate_parent_page("settings")
        self.assertTrue(result)
        
        # Verify parent was properly integrated
        parent_path = self.integrator._get_parent_page_path("settings")
        parent_content = parent_path.read_text(encoding='utf-8')
        
        self.assertIn("usePageActions", parent_content)
        self.assertIn("ActionSheetContainer", parent_content)
        self.assertIn('usePageActions("settings")', parent_content)
        self.assertIn('<ActionSheetContainer', parent_content)
        
        # Step 2: Integrate children
        result = self.integrator.integrate_child_pages("settings")
        self.assertTrue(result)
        
        # Verify profile was integrated
        profile_path = self.integrator._get_child_page_path("profile", "settings")
        profile_content = profile_path.read_text(encoding='utf-8')
        
        self.assertIn("usePageActions", profile_content)
        self.assertIn('usePageActions("profile")', profile_content)
        
        # Verify mobile profile was integrated
        mobile_profile_path = self.integrator._get_mobile_child_page_path("profile", "settings")
        mobile_profile_content = mobile_profile_path.read_text(encoding='utf-8')
        
        self.assertIn("usePageActions", mobile_profile_content)
        self.assertIn('usePageActions("profile")', mobile_profile_content)
        
        # Verify preferences was integrated (no mobile variant)
        preferences_path = self.integrator._get_child_page_path("preferences", "settings")
        preferences_content = preferences_path.read_text(encoding='utf-8')
        
        self.assertIn("usePageActions", preferences_content)
        self.assertIn('usePageActions("preferences")', preferences_content)
        
        # Step 3: Validate all integrations
        parent_issues = self.integrator.validate_container_integration("settings")
        self.assertEqual(len(parent_issues), 0)
        
        profile_issues = self.integrator.validate_container_integration("profile")
        self.assertEqual(len(profile_issues), 0)
        
        preferences_issues = self.integrator.validate_container_integration("preferences")
        self.assertEqual(len(preferences_issues), 0)
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    # Run all tests
    unittest.main()