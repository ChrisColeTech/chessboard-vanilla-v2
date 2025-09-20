#!/usr/bin/env python3
"""
Comprehensive end-to-end test for mobile-pages-v2 generator
Tests the complete workflow: Settings parent with Profile + Preferences children
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

# Add the mobile-pages-v2 directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_complete_generation():
    """Test complete generation of Settings parent with Profile + Preferences children"""
    
    print("🧪 Starting comprehensive generation test...")
    
    # Define test directories
    test_output_dir = Path(__file__).parent / "test_output"
    generator_script = Path(__file__).parent.parent / "main.py"
    
    # Clean up previous test output
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)
    
    # Create test output directory structure
    test_output_dir.mkdir(parents=True)
    
    # Create minimal project structure
    (test_output_dir / "package.json").write_text('{"name": "test-app"}')
    (test_output_dir / "index.html").write_text('<div id="root"></div>')
    (test_output_dir / "vite.config.ts").write_text('export default {}')
    (test_output_dir / "tsconfig.json").write_text('{}')
    (test_output_dir / "tsconfig.node.json").write_text('{}')
    
    print(f"📁 Test output directory: {test_output_dir}")
    
    # Expected files that MUST be generated
    expected_files = [
        # Parent files
        "src/pages/settings/SettingsPage.tsx",
        "src/pages/settings/SettingsMainPage.tsx", 
        "src/hooks/settings/useSettingsActions.ts",
        "src/constants/actions/pages/settings.ts",
        "src/services/instructions/pages/settings.ts",
        
        # Child files - Profile
        "src/pages/settings/ProfilePage.tsx",
        "src/hooks/settings/useProfileActions.ts",
        "src/constants/actions/pages/profile.ts",
        "src/services/instructions/pages/profile.ts",
        "src/components/settings/ProfilePageWrapper.tsx",
        
        # Child files - Preferences
        "src/pages/settings/PreferencesPage.tsx", 
        "src/hooks/settings/usePreferencesActions.ts",  # This is the one that's missing!
        "src/constants/actions/pages/preferences.ts",
        "src/services/instructions/pages/preferences.ts",
        "src/components/settings/PreferencesPageWrapper.tsx",
        
        # Integration files
        "src/hooks/settings/index.ts",
        "pages.config.json",
        
        # Core files that should be updated
        "src/constants/actions/page-actions.constants.ts",
        "src/App.tsx",
    ]
    
    # Run the generator
    print("🚀 Running generator...")
    try:
        result = subprocess.run([
            sys.executable, str(generator_script), 
            "create", "Settings", 
            "--children", "Profile", "Preferences",
            "--mobile"
        ], 
        cwd=test_output_dir,
        capture_output=True, 
        text=True, 
        timeout=120
        )
        
        print(f"Generator exit code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Generator timed out!")
        return False
    except Exception as e:
        print(f"❌ Error running generator: {e}")
        return False
    
    # Verify all expected files were created
    print("\n📋 Checking expected files...")
    missing_files = []
    created_files = []
    
    for expected_file in expected_files:
        file_path = test_output_dir / expected_file
        if file_path.exists():
            created_files.append(expected_file)
            print(f"✅ {expected_file}")
        else:
            missing_files.append(expected_file)
            print(f"❌ MISSING: {expected_file}")
    
    # Check pages.config.json content
    print("\n📋 Checking pages.config.json...")
    config_file = test_output_dir / "pages.config.json"
    if config_file.exists():
        try:
            config_data = json.loads(config_file.read_text())
            print(f"Config data: {json.dumps(config_data, indent=2)}")
            
            # Verify expected structure
            if "pages" not in config_data:
                print("❌ Missing 'pages' key in config")
                missing_files.append("pages.config.json (invalid structure)")
            elif "settings" not in config_data["pages"]:
                print("❌ Missing 'settings' page in config")
                missing_files.append("pages.config.json (missing settings)")
            else:
                settings_config = config_data["pages"]["settings"]
                if "children" not in settings_config:
                    print("❌ Missing 'children' in settings config")
                else:
                    children = settings_config["children"]
                    if "profile" not in children:
                        print("❌ Missing 'profile' child")
                    if "preferences" not in children:
                        print("❌ Missing 'preferences' child")
                        
        except Exception as e:
            print(f"❌ Error reading config: {e}")
            missing_files.append("pages.config.json (invalid JSON)")
    
    # Check specific hook content
    print("\n📋 Checking hook file content...")
    for hook_name in ["useProfileActions", "usePreferencesActions", "useSettingsActions"]:
        hook_file = test_output_dir / f"src/hooks/settings/{hook_name}.ts"
        if hook_file.exists():
            content = hook_file.read_text()
            if "export function" not in content:
                print(f"❌ {hook_name}.ts missing export function")
                missing_files.append(f"{hook_name}.ts (invalid content)")
            else:
                print(f"✅ {hook_name}.ts has valid content")
        else:
            print(f"❌ {hook_name}.ts not found")
    
    # Check PAGE_ACTIONS integration
    print("\n📋 Checking PAGE_ACTIONS integration...")
    page_actions_file = test_output_dir / "src/constants/actions/page-actions.constants.ts"
    if page_actions_file.exists():
        content = page_actions_file.read_text()
        expected_integrations = [
            "import { pageActions as settingsActions }",
            "import { pageActions as profileActions }",
            "settings: settingsActions.actions",
            "profile: mergeWithCommonActions"
        ]
        
        for integration in expected_integrations:
            if integration in content:
                print(f"✅ Found: {integration}")
            else:
                print(f"❌ Missing integration: {integration}")
                missing_files.append(f"PAGE_ACTIONS integration: {integration}")
    
    # Check App.tsx integration
    print("\n📋 Checking App.tsx integration...")
    app_file = test_output_dir / "src/App.tsx"
    if app_file.exists():
        content = app_file.read_text()
        expected_app_integrations = [
            'import { SettingsPage }',
            '{selectedTab === "settings" && <SettingsPage />}'
        ]
        
        for integration in expected_app_integrations:
            if integration in content:
                print(f"✅ Found: {integration}")
            else:
                print(f"❌ Missing App integration: {integration}")
                missing_files.append(f"App.tsx integration: {integration}")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"✅ Created files: {len(created_files)}")
    print(f"❌ Missing files: {len(missing_files)}")
    
    if missing_files:
        print(f"\n🚨 MISSING FILES/INTEGRATIONS:")
        for missing in missing_files:
            print(f"   • {missing}")
        return False
    else:
        print(f"\n🎉 ALL TESTS PASSED!")
        return True

def test_hook_generation_specifically():
    """Focused test on hook generation"""
    print("\n🎯 Testing hook generation specifically...")
    
    test_output_dir = Path(__file__).parent / "test_output"
    
    # Check the hooks directory structure
    hooks_dir = test_output_dir / "src/hooks/settings"
    if not hooks_dir.exists():
        print(f"❌ Hooks directory doesn't exist: {hooks_dir}")
        return False
    
    # List all files in hooks directory
    print(f"📁 Files in {hooks_dir}:")
    for file in hooks_dir.glob("*.ts"):
        print(f"   • {file.name}")
        
    # Check each expected hook
    expected_hooks = ["useSettingsActions.ts", "useProfileActions.ts", "usePreferencesActions.ts"]
    for hook in expected_hooks:
        hook_path = hooks_dir / hook
        if hook_path.exists():
            print(f"✅ {hook} exists")
            # Check content
            content = hook_path.read_text()
            if "export function" in content:
                print(f"   ✅ Has export function")
            else:
                print(f"   ❌ Missing export function")
        else:
            print(f"❌ {hook} MISSING!")
            
    return True

if __name__ == "__main__":
    success = test_complete_generation()
    test_hook_generation_specifically()
    
    if not success:
        print("\n❌ Tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)