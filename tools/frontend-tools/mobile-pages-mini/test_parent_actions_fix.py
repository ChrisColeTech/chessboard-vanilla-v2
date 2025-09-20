#!/usr/bin/env python3
"""
Test for parent actions bug fix.

This test verifies that when using the one-shot command to create a parent with children,
the parent actions correctly include child navigation actions instead of placeholder text.

Bug: Parent actions were generated before children were registered in config,
so they contained placeholder text instead of actual child navigation.

Fix: Pre-register children in config before creating parent, so parent can find them.
"""

import tempfile
import shutil
import json
from pathlib import Path
import subprocess
import sys

def test_parent_actions_include_children():
    """Test that parent actions include child navigation after one-shot command."""
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        test_root = Path(temp_dir) / "test-app"
        
        # Copy base structure
        base_files = [
            "index.html", "vite.config.ts", "tsconfig.json", 
            "tsconfig.node.json", "package.json"
        ]
        
        # Create minimal test structure
        test_root.mkdir()
        for file in base_files:
            src_file = Path("../template-tests-v2/base-app") / file
            if src_file.exists():
                shutil.copy2(src_file, test_root / file)
        
        # Run one-shot command
        print("🧪 Testing one-shot command with Dashboard + children...")
        cmd = [
            sys.executable, "main.py", 
            "--frontend-root", str(test_root),
            "create", "Dashboard", 
            "--children", "Analytics", "Reports", "Overview"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode != 0:
            print(f"❌ Command failed: {result.stderr}")
            return False
        
        # Check that parent actions file exists and contains child navigation
        parent_actions_file = test_root / "src/constants/actions/pages/dashboard.ts"
        
        if not parent_actions_file.exists():
            print("❌ Parent actions file not created")
            return False
        
        # Read parent actions content
        content = parent_actions_file.read_text()
        
        # Check for bug symptoms (placeholder text)
        if "Child navigation actions will be added here when children are created" in content:
            print("❌ BUG: Parent actions still contain placeholder text")
            print("   This means children weren't found during parent generation")
            return False
        
        # Check for expected child navigation actions
        expected_actions = ["go-to-analytics", "go-to-reports", "go-to-overview"]
        missing_actions = []
        
        for action in expected_actions:
            if action not in content:
                missing_actions.append(action)
        
        if missing_actions:
            print(f"❌ BUG: Missing child navigation actions: {missing_actions}")
            print("   Parent actions should include all child navigation")
            return False
        
        # Check that Navigation icon is actually used (not just imported)
        if "icon: Navigation" not in content:
            print("❌ BUG: Navigation icon imported but not used")
            print("   This indicates child actions weren't generated")
            return False
        
        print("✅ SUCCESS: Parent actions correctly include child navigation")
        print(f"   Found all expected actions: {expected_actions}")
        return True

def test_config_registration_timing():
    """Test that children are registered in config before parent generation."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_root = Path(temp_dir) / "test-app"
        test_root.mkdir()
        
        # Copy minimal base files
        base_file = Path("../template-tests-v2/base-app/package.json")
        if base_file.exists():
            shutil.copy2(base_file, test_root / "package.json")
        
        # Run one-shot command
        print("🧪 Testing config registration timing...")
        cmd = [
            sys.executable, "main.py", 
            "--frontend-root", str(test_root),
            "create", "Settings", 
            "--children", "Profile", "Security"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode != 0:
            print(f"❌ Command failed: {result.stderr}")
            return False
        
        # Check that config file contains all pages
        config_file = test_root / "pages.config.json"
        
        if not config_file.exists():
            print("❌ Config file not created")
            return False
        
        config_data = json.loads(config_file.read_text())
        pages = config_data.get("pages", {})
        
        # Check all expected pages are in config
        expected_pages = ["settings", "profile", "security"]
        for page_id in expected_pages:
            if page_id not in pages:
                print(f"❌ BUG: Page '{page_id}' not found in config")
                return False
        
        # Check parent-child relationships
        if pages["profile"]["parent_id"] != "settings":
            print("❌ BUG: Profile not linked to Settings parent")
            return False
            
        if pages["security"]["parent_id"] != "settings":
            print("❌ BUG: Security not linked to Settings parent")
            return False
        
        print("✅ SUCCESS: All pages correctly registered in config")
        return True

if __name__ == "__main__":
    print("🧪 Running parent actions bug fix tests...\n")
    
    success = True
    
    # Test 1: Parent actions include children
    success &= test_parent_actions_include_children()
    print()
    
    # Test 2: Config registration timing
    success &= test_config_registration_timing()
    print()
    
    if success:
        print("🎉 All tests passed! Bug fix is working correctly.")
        sys.exit(0)
    else:
        print("💥 Some tests failed. Bug fix needs more work.")
        sys.exit(1)