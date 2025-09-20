#!/usr/bin/env python3
"""
Test suite for the Routing Updater module.
"""

import unittest
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.routing_updater import ParentRoutingUpdater, RoutingUpdateError
from modules.template_engine import TemplateEngine
from modules.file_writer import FileWriter
from modules.variable_generator import VariableGenerator
from modules.config import PageConfig, ProjectCapabilities, GenerationContext


class TestParentRoutingUpdater(unittest.TestCase):
    """Test cases for ParentRoutingUpdater."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.templates_dir = self.temp_dir / "templates"
        
        # Create template structure
        self.templates_dir.mkdir(parents=True)
        (self.templates_dir / "routing").mkdir()
        
        # Create routing templates
        self._create_routing_templates()
        
        # Initialize components
        self.template_engine = TemplateEngine(self.templates_dir)
        self.file_writer = FileWriter()
        self.variable_generator = VariableGenerator()
        
        self.updater = ParentRoutingUpdater(
            self.template_engine,
            self.file_writer,
            self.variable_generator
        )
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def _create_routing_templates(self):
        """Create routing template files for testing."""
        # Import template
        import_template = self.templates_dir / "routing" / "child-import.template"
        import_template.write_text("import {{CHILD_NAME}}Wrapper from '@/components/{{PARENT_ID}}/{{CHILD_NAME}}Wrapper';")
        
        # Route config template
        route_template = self.templates_dir / "routing" / "child-route-config.template"
        route_template.write_text("    { path: '{{CHILD_ID}}', label: '{{CHILD_NAME}}' }")
        
        # Switch case template
        switch_template = self.templates_dir / "routing" / "child-switch-case.template"
        switch_template.write_text("case '{{CHILD_ID}}':\n        return <{{CHILD_NAME}}Wrapper />;")
    
    def _create_mock_parent_file(self, parent_name: str) -> Path:
        """Create a mock parent page file with routing markers."""
        pages_dir = self.temp_dir / "src" / "pages" / parent_name.lower()
        pages_dir.mkdir(parents=True)
        
        parent_file = pages_dir / f"{parent_name.capitalize()}Page.tsx"
        parent_file.write_text(f"""
import React from 'react';
import {{ useState }} from 'react';
// Child page imports

const routes = [
    {{ path: 'main', label: 'Main' }}
    // Child page routes
];

const {parent_name.capitalize()}Page = () => {{
    const [currentRoute, setCurrentRoute] = useState('main');
    
    const renderContent = () => {{
        switch (currentRoute) {{
            case 'main':
                return <{parent_name.capitalize()}MainPage />;
            // Child page components
            default:
                return <div>Not Found</div>;
        }}
    }};
    
    return <div>{{renderContent()}}</div>;
}};

export default {parent_name.capitalize()}Page;
""".strip())
        
        return parent_file
    
    def test_update_parent_routing(self):
        """Test updating parent routing with new child."""
        # Create mock parent file
        parent_file = self._create_mock_parent_file("Settings")
        
        config = PageConfig(name="UserProfile", parent="Settings", mobile=True)
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        # Update routing
        self.updater.update_parent_routing(context, "UserProfile")
        
        # Check that file was updated
        updated_content = parent_file.read_text()
        self.assertIn('UserProfileWrapper', updated_content)
        self.assertIn("path: 'userprofile'", updated_content)
        self.assertIn("case 'userprofile'", updated_content)
    
    def test_validate_routing_injection(self):
        """Test validation of routing injection."""
        # Create mock parent file and update it
        parent_file = self._create_mock_parent_file("Settings")
        
        config = PageConfig(name="TestChild", parent="Settings")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        # Update routing first
        self.updater.update_parent_routing(context, "TestChild")
        
        # Then validate
        validation = self.updater.validate_routing_injection(context, "TestChild")
        
        self.assertTrue(validation.get('parent_file_exists', False))
        self.assertTrue(validation.get('has_import', False))
        self.assertTrue(validation.get('has_route_config', False))
        self.assertTrue(validation.get('has_switch_case', False))
    
    def test_get_child_routes_in_parent(self):
        """Test getting existing child routes from parent."""
        # Create parent with existing routes
        pages_dir = self.temp_dir / "src" / "pages" / "settings"
        pages_dir.mkdir(parents=True)
        
        parent_file = pages_dir / "SettingsPage.tsx"
        parent_file.write_text("""
const SettingsPage = () => {
    const renderContent = () => {
        switch (currentRoute) {
            case 'main':
                return <SettingsMainPage />;
            case 'profile':
                return <ProfileWrapper />;
            case 'preferences':
                return <PreferencesWrapper />;
            default:
                return <div>Not Found</div>;
        }
    };
};
""".strip())
        
        config = PageConfig(name="dummy")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        routes = self.updater.get_child_routes_in_parent(context, "settings")
        
        # Should find profile and preferences, but not main
        self.assertIn('profile', routes)
        self.assertIn('preferences', routes)
        self.assertNotIn('main', routes)
    
    def test_remove_child_routing(self):
        """Test removing child routing from parent."""
        # Create parent with child route
        parent_file = self._create_mock_parent_file("Settings")
        
        config = PageConfig(name="OldChild", parent="Settings")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        # First add the route
        self.updater.update_parent_routing(context, "OldChild")
        
        # Verify it was added
        content = parent_file.read_text()
        self.assertIn('OldChild', content)
        
        # Then remove it
        self.updater.remove_child_routing(context, "OldChild")
        
        # Verify it was removed
        updated_content = parent_file.read_text()
        self.assertNotIn('OldChild', updated_content)
    
    def test_sync_routing_with_filesystem(self):
        """Test syncing routing with actual filesystem."""
        # Create parent directory with child files
        parent_dir = self.temp_dir / "src" / "pages" / "settings"
        parent_dir.mkdir(parents=True)
        
        # Create main parent files
        (parent_dir / "SettingsPage.tsx").write_text("// Main parent")
        (parent_dir / "SettingsMainPage.tsx").write_text("// Main page")
        
        # Create child files
        (parent_dir / "UserProfile.tsx").write_text("// Child page")
        (parent_dir / "Preferences.tsx").write_text("// Child page")
        (parent_dir / "MobilePreferences.tsx").write_text("// Mobile variant")
        
        # Create parent with only one route
        parent_file = parent_dir / "SettingsPage.tsx"
        parent_file.write_text("""
switch (currentRoute) {
    case 'main':
        return <SettingsMainPage />;
    case 'userprofile':
        return <UserProfileWrapper />;
    default:
        return <div>Not Found</div>;
}
""".strip())
        
        config = PageConfig(name="dummy")
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        sync_result = self.updater.sync_routing_with_filesystem(context, "settings")
        
        # Should find discrepancies
        self.assertFalse(sync_result['in_sync'])
        self.assertIn('preferences', sync_result['missing_in_routing'])
        self.assertIn('userprofile', sync_result['routing_children'])
        self.assertIn('userprofile', sync_result['filesystem_children'])
        self.assertIn('preferences', sync_result['filesystem_children'])
    
    def test_routing_update_error_no_parent(self):
        """Test error handling when no parent is specified."""
        config = PageConfig(name="TestChild", parent=None)  # No parent
        capabilities = ProjectCapabilities()
        
        context = GenerationContext(
            config=config,
            capabilities=capabilities,
            frontend_root=self.temp_dir,
            templates_dir=self.templates_dir
        )
        
        with self.assertRaises(RoutingUpdateError):
            self.updater.update_parent_routing(context, "TestChild")


if __name__ == '__main__':
    unittest.main()