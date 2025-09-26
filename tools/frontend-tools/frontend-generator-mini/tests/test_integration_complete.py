#!/usr/bin/env python3
"""
Integration test for complete frontend generation workflow
Tests the full CLI and FrontendGenerator orchestration
"""

import sys
import json
import tempfile
import subprocess
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent / "shared"))
sys.path.append(str(Path(__file__).parent.parent / "generators"))
sys.path.append(str(Path(__file__).parent.parent / "core"))

from core.frontend_generator import FrontendGenerator




def test_complete_frontend_generation():
    """Test complete frontend generation from config to files"""
    print("🧪 Testing complete frontend generation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Use existing real config files
        backend_config_path = Path("/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json")
        
        # Create output directory
        output_dir = temp_path / "frontend_output"
        output_dir.mkdir()
        
        try:
            # Initialize and run generator with real config
            generator = FrontendGenerator(output_dir, backend_config_path, verbose=True)
            generator.generate()
            
            # Verify generated structure
            assert output_dir.exists(), "Output directory should exist"
            
            # Check for generated directories
            expected_dirs = ['types', 'services', 'hooks', 'pages']
            for dir_name in expected_dirs:
                dir_path = output_dir / dir_name
                assert dir_path.exists(), f"{dir_name} directory should exist"
                print(f"✅ {dir_name}/ directory created")
            
            # Check for domain-specific files (using real domain structure)
            gameplay_types_dir = output_dir / "types" / "gameplay"
            puzzles_types_dir = output_dir / "types" / "puzzles"
            
            if gameplay_types_dir.exists():
                print("✅ Gameplay types directory created")
                
            if puzzles_types_dir.exists():
                print("✅ Puzzles types directory created")
            
            # Check for specific generated files from real config
            games_types = output_dir / "types" / "gameplay" / "games.ts"
            puzzles_types = output_dir / "types" / "puzzles" / "puzzles.ts"
            
            if games_types.exists():
                print("✅ Games types generated")
                
                # Verify content
                content = games_types.read_text()
                assert "Game" in content, "Game interface should be in types"
                
            if puzzles_types.exists():
                print("✅ Puzzles types generated")
            
            # Check for services
            gameplay_services_dir = output_dir / "services" / "gameplay"
            if gameplay_services_dir.exists() and (gameplay_services_dir / "gamesService.ts").exists():
                print("✅ Games services generated")
                
                service_content = (gameplay_services_dir / "gamesService.ts").read_text()
                assert "GameService" in service_content, "Service class should exist"
            
            # Check for hooks
            gameplay_hooks_dir = output_dir / "hooks" / "gameplay" 
            if gameplay_hooks_dir.exists() and (gameplay_hooks_dir / "useGames.ts").exists():
                print("✅ Games hooks generated")
                
                hook_content = (gameplay_hooks_dir / "useGames.ts").read_text()
                assert "useGames" in hook_content, "Hook function should exist"
            
            # Check for pages
            gameplay_pages_dir = output_dir / "pages" / "gameplay"
            if gameplay_pages_dir.exists():
                print("✅ Gameplay pages directory created")
            
            print("🎉 Complete frontend generation test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_cli_integration():
    """Test the CLI interface"""
    print("🧪 Testing CLI integration...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Use existing real config
        config_path = Path("/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json")
        output_path = temp_path / "output"
        
        try:
            # Test CLI
            main_script = Path(__file__).parent.parent / "main.py"
            cmd = [
                sys.executable, str(main_script),
                "--config", str(config_path),
                "--output", str(output_path),
                "--verbose"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ CLI execution successful")
                print(f"Output: {result.stdout}")
                
                # Verify output directory was created
                if output_path.exists():
                    print("✅ Output directory created by CLI")
                    return True
                else:
                    print("❌ Output directory not created")
                    return False
            else:
                print(f"❌ CLI failed with return code {result.returncode}")
                print(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ CLI test timed out")
            return False
        except Exception as e:
            print(f"❌ CLI test failed: {e}")
            return False


if __name__ == "__main__":
    print("🚀 Running Complete Integration Tests")
    print("="*50)
    
    success1 = test_complete_frontend_generation()
    print()
    success2 = test_cli_integration()
    
    print("\n" + "="*50)
    if success1 and success2:
        print("🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print("❌ Some integration tests failed!")
        sys.exit(1)