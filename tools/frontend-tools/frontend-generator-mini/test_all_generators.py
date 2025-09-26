#!/usr/bin/env python3
"""
Test all refactored generators with name standardizer
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "generators"))
sys.path.append(str(Path(__file__).parent / "modules"))
sys.path.append(str(Path(__file__).parent / "shared"))

from generators.services.services_generator_new import ServicesGenerator
from generators.types.types_generator_new import TypesGenerator
from generators.hooks.hooks_generator_new import HooksGenerator
from generators.pages.pages_generator_new import PagesGenerator
from generators.components.components_generator_new import ComponentsGenerator


def test_all_generators():
    """Test all generators with a chess backend entity"""
    output_path = Path(tempfile.mkdtemp())
    print(f"🗂️  Testing in: {output_path}")
    
    try:
        # Initialize all generators
        services_gen = ServicesGenerator(output_path)
        types_gen = TypesGenerator(output_path)
        hooks_gen = HooksGenerator(output_path)
        pages_gen = PagesGenerator(output_path)
        components_gen = ComponentsGenerator(output_path)
        
        # Test with a realistic chess backend entity
        endpoint_config = {
            'entity': 'Game',
            'properties': {
                'id': 'string',
                'user_id': 'string', 
                'ai_level': 'number',
                'user_color': 'string',
                'current_fen': 'string',
                'pgn': 'string',
                'status': 'string',
                'result': 'string',
                'time_control': 'string',
                'started_at': 'datetime',
                'completed_at': 'datetime',
                'created_at': 'datetime',
                'updated_at': 'datetime'
            },
            'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
        }
        
        domain = 'chess'
        endpoint_name = 'games'
        
        print("\\n🧪 Testing all generators...")
        
        # Test Services Generator
        print("\\n1️⃣  Testing Services Generator...")
        services_gen.generate(endpoint_name, endpoint_config, domain)
        services_file = output_path / "services" / domain / "gamesService.ts"
        assert services_file.exists(), f"Services file not created: {services_file}"
        print("✅ Services generator working")
        
        # Test Types Generator  
        print("\\n2️⃣  Testing Types Generator...")
        types_gen.generate(endpoint_name, endpoint_config, domain)
        types_file = output_path / "types" / domain / "games.ts"
        assert types_file.exists(), f"Types file not created: {types_file}"
        print("✅ Types generator working")
        
        # Test Hooks Generator
        print("\\n3️⃣  Testing Hooks Generator...")
        hooks_gen.generate(endpoint_name, endpoint_config, domain)
        hooks_file = output_path / "hooks" / domain / "useGame.ts"
        assert hooks_file.exists(), f"Hooks file not created: {hooks_file}"
        print("✅ Hooks generator working")
        
        # Test Pages Generator
        print("\\n4️⃣  Testing Pages Generator...")
        pages_gen.generate(endpoint_name, endpoint_config, domain)
        pages_file = output_path / "pages" / domain / "GamePage.tsx"
        assert pages_file.exists(), f"Pages file not created: {pages_file}"
        print("✅ Pages generator working")
        
        # Test Components Generator
        print("\\n5️⃣  Testing Components Generator...")
        components_gen.generate(endpoint_name, endpoint_config, domain)
        components_file = output_path / "components" / domain / "GameList.tsx"
        assert components_file.exists(), f"Components file not created: {components_file}"
        print("✅ Components generator working")
        
        # Verify name standardization consistency
        print("\\n🔍 Verifying name standardization...")
        _verify_name_consistency(output_path, domain)
        
        # Show generated file structure
        print("\\n📁 Generated file structure:")
        _show_generated_structure(output_path)
        
        # Show sample generated content
        print("\\n📄 Sample generated content:")
        _show_sample_content(output_path, domain)
        
        print("\\n🎉 All generators working perfectly with name standardizer!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        if output_path.exists():
            shutil.rmtree(output_path)


def _verify_name_consistency(output_path: Path, domain: str):
    """Verify that all generators use consistent naming"""
    
    # Check service file uses camelCase for service name
    services_file = output_path / "services" / domain / "gamesService.ts"
    with open(services_file, 'r') as f:
        services_content = f.read()
        assert "gamesService" in services_content, "Service should use camelCase naming"
        assert "export const gamesService" in services_content, "Export should use camelCase"
    
    # Check types file uses PascalCase for interfaces
    types_file = output_path / "types" / domain / "games.ts"
    with open(types_file, 'r') as f:
        types_content = f.read()
        assert "export interface Game" in types_content, "Interface should use PascalCase"
        assert "export interface GameCreate" in types_content, "Related interfaces should use PascalCase"
    
    # Check hooks file uses camelCase for hook name
    hooks_file = output_path / "hooks" / domain / "useGame.ts"
    with open(hooks_file, 'r') as f:
        hooks_content = f.read()
        assert "export const useGame" in hooks_content, "Hook should use camelCase with 'use' prefix"
    
    print("✅ Name standardization verified across all generators")


def _show_generated_structure(output_path: Path):
    """Show the generated file structure"""
    for root, dirs, files in output_path.walk():
        level = len(root.parts) - len(output_path.parts)
        indent = "  " * level
        print(f"{indent}{root.name}/")
        subindent = "  " * (level + 1)
        for file in files:
            print(f"{subindent}{file}")


def _show_sample_content(output_path: Path, domain: str):
    """Show sample content from generated files"""
    
    # Show service content
    services_file = output_path / "services" / domain / "gamesService.ts"
    print(f"\\n📋 {services_file.name}:")
    with open(services_file, 'r') as f:
        lines = f.readlines()[:15]  # First 15 lines
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line.rstrip()}")
        print("   ... (truncated)")
    
    # Show types content
    types_file = output_path / "types" / domain / "games.ts"
    print(f"\\n📋 {types_file.name}:")
    with open(types_file, 'r') as f:
        lines = f.readlines()[:10]  # First 10 lines
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line.rstrip()}")
        print("   ... (truncated)")


if __name__ == '__main__':
    test_all_generators()