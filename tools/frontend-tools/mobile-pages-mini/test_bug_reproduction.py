#!/usr/bin/env python3
"""
Test to reproduce and confirm the exact capitalization bug.
"""

import sys
from pathlib import Path

# Add the shared modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from name_standardizer import NameStandardizer

# Add the modules to path  
sys.path.insert(0, str(Path(__file__).parent / "modules"))
from config import PageConfig

def test_bug_reproduction():
    """Reproduce the exact bug in parent routing update."""
    print("🐛 Reproducing the exact capitalization bug...\n")
    
    # Simulate what happens in the original page creation
    print("📝 ORIGINAL PAGE CREATION:")
    original_config = PageConfig(name="ChessBoard", parent="gamehub")
    print(f"   Input: PageConfig(name='ChessBoard')")
    print(f"   base_name: '{original_config.base_name}'")
    print(f"   page_id: '{original_config.page_id}'")
    
    # What the wrapper name would be
    original_wrapper = f"{NameStandardizer.to_pascal_case(original_config.base_name)}PageWrapper"
    print(f"   Wrapper name: '{original_wrapper}'")
    
    print("\n" + "="*60)
    
    # Simulate what happens in the parent routing update (THE BUG)
    print("\n📝 PARENT ROUTING UPDATE (BUGGY):")
    child_id = original_config.page_id  # "chessboard"
    print(f"   Child ID from existing children: '{child_id}'")
    
    # This is the buggy line from main.py:272
    child_name_proper = NameStandardizer.to_pascal_case(child_id)
    print(f"   NameStandardizer.to_pascal_case('{child_id}'): '{child_name_proper}'")
    
    # Create the config as main.py does
    recreated_config = PageConfig(name=child_name_proper, parent="gamehub")
    print(f"   Recreated PageConfig base_name: '{recreated_config.base_name}'")
    
    # What the wrapper name would be
    recreated_wrapper = f"{NameStandardizer.to_pascal_case(recreated_config.base_name)}PageWrapper"
    print(f"   Recreated wrapper name: '{recreated_wrapper}'")
    
    print(f"\n🔍 COMPARISON:")
    print(f"   Original wrapper:  '{original_wrapper}'")
    print(f"   Recreated wrapper: '{recreated_wrapper}'")
    print(f"   Match: {original_wrapper == recreated_wrapper}")
    
    if original_wrapper != recreated_wrapper:
        print(f"\n💥 BUG CONFIRMED!")
        print(f"   This causes TypeScript error: 'File name differs only in casing'")
        print(f"   Import: {original_wrapper}")
        print(f"   Usage:  {recreated_wrapper}")
        return False
    else:
        print(f"\n✅ No bug detected")
        return True

def test_correct_approach():
    """Test what the correct approach should be."""
    print(f"\n🔧 CORRECT APPROACH:")
    print(f"   Instead of recreating PageConfig from child_id,")
    print(f"   should read the actual page info from pages.config.json")
    
    # Simulate reading from config (what it should be)
    original_page_info = {
        "id": "chessboard",
        "name": "ChessBoard",  # This is the correct name from JSON
        "parent_id": "gamehub"
    }
    
    print(f"   Page info from JSON: {original_page_info}")
    correct_config = PageConfig(name=original_page_info["name"], parent=original_page_info["parent_id"])
    print(f"   Correct base_name: '{correct_config.base_name}'")
    
    correct_wrapper = f"{NameStandardizer.to_pascal_case(correct_config.base_name)}PageWrapper"
    print(f"   Correct wrapper name: '{correct_wrapper}'")
    
    return correct_wrapper

if __name__ == "__main__":
    print("🚀 Testing capitalization bug reproduction...\n")
    
    bug_exists = not test_bug_reproduction()
    correct_wrapper = test_correct_approach()
    
    print(f"\n📊 RESULTS:")
    print(f"   Bug exists: {'✅ YES' if bug_exists else '❌ NO'}")
    print(f"   Fix needed: {'✅ YES' if bug_exists else '❌ NO'}")
    
    if bug_exists:
        print(f"\n🎯 THE FIX:")
        print(f"   In main.py:_update_parent_for_new_child()")
        print(f"   Line 272-273 should read from pages.config.json instead of")
        print(f"   recreating PageConfig from child_id")