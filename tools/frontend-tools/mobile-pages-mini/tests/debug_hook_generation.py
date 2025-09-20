#!/usr/bin/env python3
"""
Debug script to trace child hook generation issues
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

# Add the mobile-pages-v2 directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.hook_integrator import HookIntegrator

def debug_hook_generation():
    """Debug the hook generation process step by step"""
    
    print("🔍 Debugging hook generation...")
    
    # Set up test directory
    test_dir = Path(__file__).parent / "debug_output"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True)
    
    # Create pages.config.json manually
    config_data = {
        "version": "1.0.0",
        "generated_by": "mobile-pages-v2",
        "pages": {
            "settings": {
                "id": "settings", 
                "name": "Settings",
                "type": "parent",
                "parent_id": "",
                "created_at": "2025-01-01T00:00:00"
            },
            "profile": {
                "id": "profile",
                "name": "Profile", 
                "type": "child",
                "parent_id": "settings",
                "created_at": "2025-01-01T00:00:01"
            },
            "preferences": {
                "id": "preferences",
                "name": "Preferences",
                "type": "child", 
                "parent_id": "settings",
                "created_at": "2025-01-01T00:00:02"
            }
        },
        "metadata": {
            "total_pages": 3,
            "parent_pages": 1,
            "child_pages": 2
        }
    }
    
    config_file = test_dir / "pages.config.json"
    config_file.write_text(json.dumps(config_data, indent=2))
    
    print(f"📋 Created config at: {config_file}")
    print(f"Config content: {json.dumps(config_data, indent=2)}")
    
    # Create hook integrator
    integrator = HookIntegrator(test_dir)
    
    # Test child hook generation directly
    print(f"\n🧪 Testing child hook generation...")
    
    # Test Profile hook
    print(f"\n📝 Generating Profile hook...")
    result_profile = integrator.generate_child_action_hook("profile", "settings")
    print(f"Profile result: {result_profile}")
    
    # Test Preferences hook
    print(f"\n📝 Generating Preferences hook...")
    result_preferences = integrator.generate_child_action_hook("preferences", "settings")
    print(f"Preferences result: {result_preferences}")
    
    # Check what files were created
    print(f"\n📂 Checking created files...")
    hooks_dir = test_dir / "src/hooks/settings"
    if hooks_dir.exists():
        print(f"Hooks directory exists: {hooks_dir}")
        for file in hooks_dir.glob("*.ts"):
            print(f"  • {file.name} ({file.stat().st_size} bytes)")
    else:
        print(f"❌ Hooks directory doesn't exist: {hooks_dir}")
    
    # Test the integrator's internal methods
    print(f"\n🔍 Testing internal methods...")
    
    try:
        profile_info = integrator._get_page_info("profile")
        print(f"Profile info: {profile_info}")
    except Exception as e:
        print(f"❌ Error getting profile info: {e}")
    
    try:
        preferences_info = integrator._get_page_info("preferences")
        print(f"Preferences info: {preferences_info}")
    except Exception as e:
        print(f"❌ Error getting preferences info: {e}")
        
    try:
        profile_siblings = integrator._get_sibling_pages("profile", "settings")
        print(f"Profile siblings: {profile_siblings}")
    except Exception as e:
        print(f"❌ Error getting profile siblings: {e}")
        
    try:
        preferences_siblings = integrator._get_sibling_pages("preferences", "settings")
        print(f"Preferences siblings: {preferences_siblings}")
    except Exception as e:
        print(f"❌ Error getting preferences siblings: {e}")

if __name__ == "__main__":
    debug_hook_generation()