#!/usr/bin/env python3
"""
Test to verify that the capitalization bug fix works correctly.
"""

import sys
import tempfile
import shutil
import json
from pathlib import Path

# Add the shared modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from name_standardizer import NameStandardizer

# Add the modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))
from config import PageConfig
from config_integration import ConfigIntegration

def test_fix_works():
    """Test that the fix correctly reads from pages.config.json"""
    print("🔧 Testing that the fix works correctly...\n")
    
    # Create a temporary config file to simulate the real scenario
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_file = temp_path / "pages.config.json"
        
        # Create a config file with the real page data
        config_data = {
            "version": "1.0.0",
            "pages": {
                "chessboard": {
                    "id": "chessboard",
                    "name": "ChessBoard",  # Correct capitalization
                    "type": "child",
                    "parent_id": "gamehub"
                },
                "scoreboard": {
                    "id": "scoreboard", 
                    "name": "ScoreBoard",  # Correct capitalization
                    "type": "child",
                    "parent_id": "gamehub"
                }
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"📄 Created test config: {config_file}")
        
        # Test the config integration
        config_integration = ConfigIntegration(temp_path)
        
        # Test reading page info (this is what the fix uses)
        chessboard_info = config_integration.get_page_info("chessboard")
        scoreboard_info = config_integration.get_page_info("scoreboard")
        
        print(f"📝 Read chessboard info: {chessboard_info}")
        print(f"📝 Read scoreboard info: {scoreboard_info}")
        
        # Test creating PageConfig objects with the correct names
        if chessboard_info and scoreboard_info:
            chessboard_config = PageConfig(name=chessboard_info['name'], parent="gamehub")
            scoreboard_config = PageConfig(name=scoreboard_info['name'], parent="gamehub")
            
            print(f"\n🔍 Testing ChessBoard:")
            print(f"   Original name from config: '{chessboard_info['name']}'")
            print(f"   PageConfig base_name: '{chessboard_config.base_name}'") 
            chess_wrapper = f"{NameStandardizer.to_pascal_case(chessboard_config.base_name)}PageWrapper"
            print(f"   Generated wrapper name: '{chess_wrapper}'")
            
            print(f"\n🔍 Testing ScoreBoard:")
            print(f"   Original name from config: '{scoreboard_info['name']}'")
            print(f"   PageConfig base_name: '{scoreboard_config.base_name}'")
            score_wrapper = f"{NameStandardizer.to_pascal_case(scoreboard_config.base_name)}PageWrapper"
            print(f"   Generated wrapper name: '{score_wrapper}'")
            
            # Verify the fix produces correct names
            expected_chess = "ChessBoardPageWrapper"
            expected_score = "ScoreBoardPageWrapper"
            
            chess_correct = chess_wrapper == expected_chess
            score_correct = score_wrapper == expected_score
            
            print(f"\n✅ VERIFICATION:")
            print(f"   ChessBoard wrapper: {'✅' if chess_correct else '❌'} Expected: {expected_chess}, Got: {chess_wrapper}")
            print(f"   ScoreBoard wrapper: {'✅' if score_correct else '❌'} Expected: {expected_score}, Got: {score_wrapper}")
            
            return chess_correct and score_correct
        else:
            print(f"❌ Failed to read page info")
            return False

def test_integration():
    """Test the full integration with a real project setup."""
    print(f"\n🧪 Testing full integration...\n")
    
    # Test with the actual project path
    project_path = Path("/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/mini-test-app")
    
    if not (project_path / "pages.config.json").exists():
        print(f"❌ Project config not found: {project_path}")
        return False
        
    config_integration = ConfigIntegration(project_path)
    
    # Test reading the actual page info
    test_pages = ["chessboard", "scoreboard"]
    
    for page_id in test_pages:
        page_info = config_integration.get_page_info(page_id)
        if page_info:
            print(f"📝 {page_id}: {page_info['name']}")
            
            # Test what the fix would produce
            config = PageConfig(name=page_info['name'], parent=page_info['parent_id'])
            wrapper_name = f"{NameStandardizer.to_pascal_case(config.base_name)}PageWrapper"
            
            print(f"   Fix produces: {wrapper_name}")
        else:
            print(f"❌ Failed to read {page_id}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Testing the capitalization bug fix...\n")
    
    fix_works = test_fix_works()
    integration_works = test_integration()
    
    print(f"\n📊 RESULTS:")
    print(f"   Fix verification: {'✅ PASS' if fix_works else '❌ FAIL'}")
    print(f"   Integration test: {'✅ PASS' if integration_works else '❌ FAIL'}")
    
    if fix_works and integration_works:
        print(f"\n🎉 FIX VERIFIED - The bug should be resolved!")
        sys.exit(0)
    else:
        print(f"\n💥 FIX FAILED - Additional work needed!")
        sys.exit(1)