#!/usr/bin/env python3
"""
Final comprehensive test to verify the capitalization bug fix works end-to-end.
"""

import tempfile
import shutil
import subprocess
import sys
from pathlib import Path

def test_end_to_end_fix():
    """Test the entire workflow with the bug fix."""
    print("🚀 Testing end-to-end capitalization bug fix...\n")
    
    # Create a temporary project directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        print(f"📁 Created temporary project: {temp_path}")
        
        # Create a minimal project structure
        src_dir = temp_path / "src"
        src_dir.mkdir()
        
        # Create necessary directories
        (src_dir / "pages").mkdir()
        (src_dir / "components").mkdir()  
        (src_dir / "hooks").mkdir()
        (src_dir / "constants" / "actions" / "pages").mkdir(parents=True)
        (src_dir / "services" / "instructions" / "pages").mkdir(parents=True)
        (src_dir / "stores").mkdir()
        (src_dir / "types" / "core").mkdir(parents=True)
        
        # Create minimal required files to avoid dependency errors
        create_minimal_files(src_dir)
        
        # Test the generator with compound word names
        print(f"\n🧪 Testing generator with compound words...")
        
        try:
            # Create a parent
            result1 = subprocess.run([
                sys.executable, 
                str(Path(__file__).parent / "main.py"),
                "parent", 
                "GameHub",
                "--frontend-root", str(temp_path)
            ], capture_output=True, text=True, cwd=temp_path)
            
            print(f"📝 Parent creation result: {result1.returncode}")
            if result1.returncode != 0:
                print(f"❌ Parent creation failed: {result1.stderr}")
                return False
            
            # Create children with compound names
            compound_names = ["ChessBoard", "ScoreBoard"]
            
            for name in compound_names:
                result2 = subprocess.run([
                    sys.executable,
                    str(Path(__file__).parent / "main.py"), 
                    "child",
                    name,
                    "--parent", "GameHub",
                    "--frontend-root", str(temp_path)
                ], capture_output=True, text=True, cwd=temp_path)
                
                print(f"📝 Child '{name}' creation result: {result2.returncode}")
                if result2.returncode != 0:
                    print(f"❌ Child creation failed: {result2.stderr}")
                    return False
            
            # Check the generated parent page for consistent naming
            parent_file = temp_path / "src" / "pages" / "gamehub" / "GameHubPage.tsx"
            if parent_file.exists():
                with open(parent_file) as f:
                    content = f.read()
                
                print(f"\n🔍 Checking generated parent page...")
                
                # Check for imports
                imports = [line for line in content.split('\n') if 'import' in line and 'PageWrapper' in line]
                print(f"📝 Imports found:")
                for imp in imports:
                    print(f"   {imp.strip()}")
                
                # Check for routing logic
                routing = [line for line in content.split('\n') if 'CurrentPageComponent' in line and '=' in line]
                print(f"📝 Routing logic found:")
                for route in routing:
                    print(f"   {route.strip()}")
                
                # Verify naming consistency
                has_chess_import = any('ChessBoardPageWrapper' in line for line in imports)
                has_score_import = any('ScoreBoardPageWrapper' in line for line in imports)
                has_chess_routing = any('ChessBoardPageWrapper' in line for line in routing)  
                has_score_routing = any('ScoreBoardPageWrapper' in line for line in routing)
                
                print(f"\n✅ CONSISTENCY CHECK:")
                print(f"   ChessBoard import: {'✅' if has_chess_import else '❌'}")
                print(f"   ChessBoard routing: {'✅' if has_chess_routing else '❌'}")
                print(f"   ScoreBoard import: {'✅' if has_score_import else '❌'}")
                print(f"   ScoreBoard routing: {'✅' if has_score_routing else '❌'}")
                
                # Check for the specific bug (incorrect casing)
                has_wrong_chess = any('ChessboardPageWrapper' in line for line in routing)  # lowercase 'b'
                has_wrong_score = any('ScoreboardPageWrapper' in line for line in routing)  # lowercase 'b'
                
                if has_wrong_chess or has_wrong_score:
                    print(f"💥 BUG STILL EXISTS!")
                    print(f"   Found incorrect casing: chess={has_wrong_chess}, score={has_wrong_score}")
                    return False
                
                all_correct = has_chess_import and has_score_import and has_chess_routing and has_score_routing
                return all_correct
            
            else:
                print(f"❌ Parent page file not found: {parent_file}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            return False

def create_minimal_files(src_dir: Path):
    """Create minimal required files to avoid dependency errors."""
    
    # Create minimal store
    (src_dir / "stores" / "appStore.ts").write_text("""
export const useAppStore = (selector: any) => ({
  currentChildPage: null,
  setCurrentChildPage: () => {},
});
""")
    
    # Create minimal hooks  
    (src_dir / "hooks" / "core").mkdir(parents=True, exist_ok=True)
    (src_dir / "hooks" / "core" / "usePageInstructions.ts").write_text("export const usePageInstructions = () => {};")
    (src_dir / "hooks" / "core" / "usePageActions.ts").write_text("export const usePageActions = () => {};")
    
    # Create minimal action sheet
    (src_dir / "components" / "action-sheet").mkdir(parents=True, exist_ok=True)
    (src_dir / "components" / "action-sheet" / "ActionSheetContainer.tsx").write_text("""
export const ActionSheetContainer = () => null;
""")
    
    # Create minimal types
    (src_dir / "types" / "core" / "action-sheet.types.ts").write_text("""
export interface ActionSheetAction {
  id: string;
  label: string;
  icon: any;
  variant: string;
}
""")

if __name__ == "__main__":
    print("🧪 Running final end-to-end verification...\n")
    
    success = test_end_to_end_fix()
    
    print(f"\n📊 FINAL RESULT:")
    if success:
        print(f"🎉 SUCCESS - Capitalization bug has been fixed!")
        print(f"   ✅ Imports use correct casing")
        print(f"   ✅ Routing logic uses correct casing")
        print(f"   ✅ No TypeScript casing conflicts")
        sys.exit(0)
    else:
        print(f"💥 FAILURE - Bug still exists or other issues found")
        sys.exit(1)