#!/usr/bin/env python3
"""
Test to examine the actual naming issues in our real generated project.
"""

import sys
import json
from pathlib import Path

def test_real_project_naming():
    """Test the actual naming in our generated project."""
    print("🧪 Testing real project naming issues...\n")
    
    # Path to our test project
    project_root = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/mini-test-app")
    
    # Read the pages config
    config_file = project_root / "pages.config.json"
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return False
    
    with open(config_file) as f:
        config_data = json.load(f)
    
    print("📋 Pages in config:")
    for page_id, page_info in config_data["pages"].items():
        if page_info["type"] == "child":
            print(f"  {page_id}: {page_info['name']} (parent: {page_info['parent_id']})")
    
    # Check gamehub children specifically
    gamehub_children = [
        ("chessboard", "ChessBoard"),
        ("scoreboard", "ScoreBoard")
    ]
    
    print("\n🔍 Checking GameHub children...")
    
    components_dir = project_root / "src" / "components" / "gamehub"
    parent_page_file = project_root / "src" / "pages" / "gamehub" / "GameHubPage.tsx"
    
    for child_id, expected_name in gamehub_children:
        print(f"\n📝 Checking {child_id} ({expected_name}):")
        
        # Check what files exist
        expected_wrapper_file = components_dir / f"{expected_name}PageWrapper.tsx"
        print(f"   Expected wrapper file: {expected_wrapper_file}")
        print(f"   File exists: {expected_wrapper_file.exists()}")
        
        if expected_wrapper_file.exists():
            print(f"   ✅ Wrapper file found with expected name")
        else:
            # List all files in the directory
            if components_dir.exists():
                print(f"   📁 Files in {components_dir}:")
                for file in components_dir.iterdir():
                    if file.is_file():
                        print(f"      {file.name}")
        
        # Check what's in the parent page imports
        if parent_page_file.exists():
            with open(parent_page_file) as f:
                parent_content = f.read()
            
            # Look for imports of this child
            import_lines = [line.strip() for line in parent_content.split('\n') if 'import' in line and expected_name in line]
            print(f"   Import lines containing '{expected_name}':")
            for line in import_lines:
                print(f"      {line}")
            
            # Look for component usage
            usage_lines = [line.strip() for line in parent_content.split('\n') if f'{expected_name}PageWrapper' in line and 'import' not in line]
            print(f"   Usage lines:")
            for line in usage_lines:
                print(f"      {line}")
    
    return True

def check_typescript_compilation():
    """Check what the TypeScript compiler is complaining about."""
    print("\n🔍 Checking TypeScript compilation issues...")
    
    project_root = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/mini-test-app")
    
    # Check the index.ts file in components/gamehub
    index_file = project_root / "src" / "components" / "gamehub" / "index.ts"
    
    if index_file.exists():
        print(f"📄 Contents of {index_file}:")
        with open(index_file) as f:
            content = f.read()
        print(content)
    else:
        print(f"❌ Index file not found: {index_file}")
    
    # Check actual parent page imports
    parent_file = project_root / "src" / "pages" / "gamehub" / "GameHubPage.tsx"
    if parent_file.exists():
        print(f"\n📄 Import section of {parent_file}:")
        with open(parent_file) as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines[:30], 1):  # First 30 lines
            if 'import' in line:
                print(f"  {i:2d}: {line.rstrip()}")
    
    return True

if __name__ == "__main__":
    print("🚀 Running real project naming analysis...\n")
    
    test_real_project_naming()
    check_typescript_compilation()