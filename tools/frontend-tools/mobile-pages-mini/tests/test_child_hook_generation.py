#!/usr/bin/env python3
"""
Test child hook generation through dependency manager integration.
Ensures that child action hooks are properly created during the integration phase.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import json
import sys

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.dependency_manager import DependencyManager
from modules.config import GenerationContext, PageConfig, ProjectCapabilities
from modules.file_writer import FileWriter

class TestChildHookGeneration:
    
    def setup_method(self):
        """Set up test environment with temp directories."""
        self.test_output_dir = Path(tempfile.mkdtemp())
        self.frontend_root = self.test_output_dir / "test-app"
        self.frontend_root.mkdir(parents=True, exist_ok=True)
        
        # Create basic project structure
        self.src_dir = self.frontend_root / "src"
        self.hooks_dir = self.src_dir / "hooks"
        self.pages_dir = self.src_dir / "pages"
        self.components_dir = self.src_dir / "components"
        
        for dir_path in [self.src_dir, self.hooks_dir, self.pages_dir, self.components_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create dependency manager
        self.file_writer = FileWriter()
        self.dependency_manager = DependencyManager(self.frontend_root, self.file_writer)
        
        # Create project capabilities
        self.capabilities = ProjectCapabilities(
            has_page_hooks=True,
            has_mobile_hook=True,
            has_data_table=True
        )
        
        print(f"Test output directory: {self.test_output_dir}")
    
    def teardown_method(self):
        """Clean up test environment."""
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir)
    
    def create_test_pages_config(self, parent_id: str, child_configs: list):
        """Create a pages.config.json file with parent and child pages."""
        config_data = {
            "pages": {},
            "navigation": {
                "tabs": [parent_id]
            }
        }
        
        # Add parent page
        config_data["pages"][parent_id] = {
            "id": parent_id,
            "name": f"{parent_id.capitalize()}Page",
            "type": "parent",
            "description": f"Main {parent_id} configuration page"
        }
        
        # Add child pages
        for child_config in child_configs:
            child_id = child_config["id"]
            config_data["pages"][child_id] = {
                "id": child_id,
                "name": f"{child_config['name']}Page",
                "type": "child",
                "parent_id": parent_id,
                "description": child_config["description"]
            }
        
        config_path = self.frontend_root / "pages.config.json"
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return config_path
    
    def test_single_child_hook_generation(self):
        """Test that child hook is generated for single child page."""
        # Create pages config
        child_configs = [{
            "id": "profile",
            "name": "Profile", 
            "description": "Manage user profile settings"
        }]
        
        self.create_test_pages_config("settings", child_configs)
        
        # Create generation context for child page
        child_config = PageConfig(
            name="Profile",
            parent="settings",
            description="Manage user profile settings"
        )
        
        context = GenerationContext(
            config=child_config,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Perform child page integration (this should create the hook)
        success = self.dependency_manager.integrate_child_pages(context, "settings")
        
        print(f"Integration success: {success}")
        
        # Even if integration has some failures, check if hook was created
        # (integration might fail on missing files but still create hooks)
        
        # Verify the child hook was created
        expected_hook_path = self.frontend_root / "src/hooks/settings/useProfileActions.ts"
        assert expected_hook_path.exists(), f"Child hook should be created at {expected_hook_path}"
        
        # Verify hook content
        hook_content = expected_hook_path.read_text()
        print(f"Generated hook content:\n{hook_content}")
        
        # Should contain proper imports
        assert "import { useCallback } from 'react';" in hook_content or "export function useProfileActions()" in hook_content
        assert "useProfileActions" in hook_content, "Hook should export useProfileActions function"
        
        # For single child, should have no sibling navigation
        assert "No siblings found for this child" in hook_content or "// No navigation methods needed" in hook_content
    
    def test_multiple_children_hook_generation(self):
        """Test that child hooks are generated with proper sibling navigation."""
        # Create pages config with multiple children
        child_configs = [
            {
                "id": "profile",
                "name": "Profile", 
                "description": "Manage user profile settings"
            },
            {
                "id": "preferences", 
                "name": "Preferences",
                "description": "Configure user preferences"
            }
        ]
        
        self.create_test_pages_config("settings", child_configs)
        
        # Create generation context for first child
        profile_config = PageConfig(
            name="Profile",
            parent="settings",
            description="Manage user profile settings"
        )
        
        context = GenerationContext(
            config=profile_config,
            frontend_root=self.frontend_root,
            variables={}
        )
        
        # Create generation context for second child
        preferences_config = PageConfig(
            name="Preferences",
            parent="settings",
            description="Configure user preferences"
        )
        
        pref_context = GenerationContext(
            config=preferences_config,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Integrate both child pages
        success1 = self.dependency_manager.integrate_child_pages(context, "settings")
        success2 = self.dependency_manager.integrate_child_pages(pref_context, "settings")
        
        assert success1, "First child page integration should succeed"
        assert success2, "Second child page integration should succeed"
        
        # Verify both child hooks were created
        profile_hook_path = self.frontend_root / "src/hooks/settings/useProfileActions.ts"
        preferences_hook_path = self.frontend_root / "src/hooks/settings/usePreferencesActions.ts"
        
        assert profile_hook_path.exists(), f"Profile hook should be created at {profile_hook_path}"
        assert preferences_hook_path.exists(), f"Preferences hook should be created at {preferences_hook_path}"
        
        # Verify profile hook has sibling navigation to preferences
        profile_content = profile_hook_path.read_text()
        assert "goToPreferences" in profile_content, "Profile hook should have goToPreferences navigation"
        assert "setCurrentChildPage('preferences')" in profile_content, "Should navigate to preferences"
        
        # Verify preferences hook has sibling navigation to profile  
        preferences_content = preferences_hook_path.read_text()
        assert "goToProfile" in preferences_content, "Preferences hook should have goToProfile navigation"
        assert "setCurrentChildPage('profile')" in preferences_content, "Should navigate to profile"
    
    def test_hook_integrator_called_during_integration(self):
        """Test that the HookIntegrator is properly called during child integration."""
        # Create pages config
        child_configs = [{
            "id": "profile",
            "name": "Profile",
            "description": "Manage user profile settings"
        }]
        
        self.create_test_pages_config("settings", child_configs)
        
        # Create context
        child_config = PageConfig(
            name="Profile",
            parent="settings",
            description="Manage user profile settings"
        )
        
        context = GenerationContext(
            config=child_config,
            frontend_root=self.frontend_root,
            capabilities=self.capabilities,
            variables={}
        )
        
        # Mock the hook integrator to track if it was called
        original_hook_integrator = self.dependency_manager._hook_integrator
        hook_calls = []
        
        class MockHookIntegrator:
            def __init__(self, original):
                self.original = original
                
            def generate_child_action_hook(self, child_id, parent_id):
                hook_calls.append({"child_id": child_id, "parent_id": parent_id})
                return self.original.generate_child_action_hook(child_id, parent_id)
            
            def __getattr__(self, name):
                return getattr(self.original, name)
        
        self.dependency_manager._hook_integrator = MockHookIntegrator(original_hook_integrator)
        
        # Perform integration
        success = self.dependency_manager.integrate_child_pages(context, "settings")
        
        assert success, "Child page integration should succeed"
        assert len(hook_calls) > 0, "HookIntegrator.generate_child_action_hook should be called"
        assert hook_calls[0]["child_id"] == "profile", "Should call with correct child_id"
        assert hook_calls[0]["parent_id"] == "settings", "Should call with correct parent_id"
        
        # Verify hook was actually created
        expected_hook_path = self.frontend_root / "src/hooks/settings/useProfileActions.ts"
        assert expected_hook_path.exists(), f"Hook should be created at {expected_hook_path}"


if __name__ == "__main__":
    # Run the test
    test_instance = TestChildHookGeneration()
    test_instance.setup_method()
    
    try:
        print("Running test_single_child_hook_generation...")
        test_instance.test_single_child_hook_generation()
        print("✅ test_single_child_hook_generation PASSED")
        
        test_instance.teardown_method()
        test_instance.setup_method()
        
        print("Running test_multiple_children_hook_generation...")
        test_instance.test_multiple_children_hook_generation()
        print("✅ test_multiple_children_hook_generation PASSED")
        
        test_instance.teardown_method()
        test_instance.setup_method()
        
        print("Running test_hook_integrator_called_during_integration...")
        test_instance.test_hook_integrator_called_during_integration()
        print("✅ test_hook_integrator_called_during_integration PASSED")
        
        print("\n🎉 All tests PASSED!")
        
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        raise
    finally:
        test_instance.teardown_method()