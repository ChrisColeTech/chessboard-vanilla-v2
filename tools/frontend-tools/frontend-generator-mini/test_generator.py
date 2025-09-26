#!/usr/bin/env python3
"""
Test the new services generator
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "generators"))
sys.path.append(str(Path(__file__).parent / "modules"))

from services.services_generator_new import ServicesGenerator

def test_services_generator():
    """Test the new services generator"""
    output_path = Path(__file__).parent / "test_output"
    output_path.mkdir(exist_ok=True)
    
    generator = ServicesGenerator(output_path)
    
    # Test with a simple endpoint config (like games from backend_config.json)
    endpoint_config = {
        'entity': 'Game',
        'methods': ['createGame', 'getGameById', 'listGames', 'updateGame', 'deleteGame']
    }
    
    try:
        generator.generate('games', endpoint_config, 'chess')
        print("✅ Service generation completed successfully!")
        
        # Check if file was created
        expected_file = output_path / "services" / "chess" / "gamesService.ts"
        if expected_file.exists():
            print(f"✅ Generated file: {expected_file}")
            with open(expected_file, 'r') as f:
                content = f.read()
                print("📄 Generated content preview:")
                print(content[:500] + "..." if len(content) > 500 else content)
        else:
            print(f"❌ Expected file not found: {expected_file}")
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_services_generator()