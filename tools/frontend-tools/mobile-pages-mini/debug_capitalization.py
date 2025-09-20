#!/usr/bin/env python3
"""
Debug script to trace exactly where the capitalization issue is happening.
"""

import sys
import json
from pathlib import Path

# Add the shared modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from name_standardizer import NameStandardizer

# Add the modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))
from config import PageConfig

def debug_capitalization():
    """Debug the exact capitalization flow."""
    print("🔍 Debugging capitalization flow...\n")
    
    # Load the actual page config from our project
    project_root = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/mini-test-app")
    config_file = project_root / "pages.config.json"
    
    with open(config_file) as f:
        config_data = json.load(f)
    
    # Focus on the problematic children
    problem_pages = ["chessboard", "scoreboard"]
    
    for page_id in problem_pages:
        page_info = config_data["pages"][page_id]
        print(f"📝 Debugging {page_id}:")
        print(f"   Config name: '{page_info['name']}'")
        
        # Create PageConfig object as the generator would
        page_config = PageConfig(name=page_info['name'], parent=page_info['parent_id'])
        
        print(f"   PageConfig.base_name: '{page_config.base_name}'")
        print(f"   PageConfig.page_name: '{page_config.page_name}'")
        print(f"   PageConfig.page_id: '{page_config.page_id}'")
        
        # Test name standardizer directly
        print(f"   NameStandardizer.to_pascal_case('{page_info['name']}'): '{NameStandardizer.to_pascal_case(page_info['name'])}'")
        print(f"   NameStandardizer.to_pascal_case('{page_config.base_name}'): '{NameStandardizer.to_pascal_case(page_config.base_name)}'")
        
        # Test what the variable generator would produce
        wrapper_name = f"{NameStandardizer.to_pascal_case(page_config.base_name)}PageWrapper"
        import_path = f"{NameStandardizer.to_pascal_case(page_config.base_name)}PageWrapper"
        
        print(f"   Generated wrapper_name: '{wrapper_name}'")
        print(f"   Generated import_path: '{import_path}'")
        
        # Test splitting the original name
        words = NameStandardizer._split_to_words(page_info['name'])
        print(f"   Split words from '{page_info['name']}': {words}")
        
        print()

def test_name_standardizer_directly():
    """Test the name standardizer directly with our problem cases."""
    print("🧪 Testing NameStandardizer directly...\n")
    
    test_cases = [
        "ChessBoard",
        "chessboard", 
        "chess_board",
        "chess-board",
        "ScoreBoard",
        "scoreboard"
    ]
    
    for test_case in test_cases:
        words = NameStandardizer._split_to_words(test_case)
        pascal = NameStandardizer.to_pascal_case(test_case)
        print(f"'{test_case}' -> words: {words} -> pascal: '{pascal}'")

if __name__ == "__main__":
    debug_capitalization()
    test_name_standardizer_directly()