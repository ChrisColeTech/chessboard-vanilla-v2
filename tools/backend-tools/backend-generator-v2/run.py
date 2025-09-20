#!/usr/bin/env python3
"""
Quick runner for the new modular configuration-driven backend generator
"""

import sys
from pathlib import Path
from main import BackendGeneratorOrchestrator, GenerationOptions

def run_with_existing_config():
    """Run the generator with the existing backend config from the v1 generator"""
    
    # Path to the existing backend config
    old_config_path = Path("/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json")
    
    if not old_config_path.exists():
        print(f"❌ Backend config not found at: {old_config_path}")
        print("   Make sure you're running from the backend-generator-v2 directory")
        return 1
    
    print("🔧 Using existing backend config from v1 generator")
    print(f"📄 Config: {old_config_path}")
    
    # Create generator with default settings
    options = GenerationOptions(
        dry_run=False,
        verbose=True,
        output_path="../../../backend-v2",
        force_overwrite=True
    )
    
    orchestrator = BackendGeneratorOrchestrator("../../../backend-v2")
    
    print("🚀 Configuration-Driven Backend Generator v2 Starting...")
    
    # Load the existing config
    import json
    with open(old_config_path, 'r') as f:
        entities_config = json.load(f)
    
    success = orchestrator.generate_backend(entities_config, options)
    
    if success:
        print("✅ Backend generation completed successfully!")
        print("📁 Generated files in: ../../../backend-v2/src/")
        return 0
    else:
        print("❌ Backend generation failed")
        return 1

def run_with_test_config():
    """Run the generator with the test config"""
    
    test_config_path = Path("test_config.json")
    
    print("🧪 Using test configuration")
    print(f"📄 Config: {test_config_path}")
    
    # Create generator with test settings
    options = GenerationOptions(
        dry_run=False,
        verbose=True,
        output_path="./test_output",
        force_overwrite=True
    )
    
    orchestrator = BackendGeneratorOrchestrator("./test_output")
    
    print("🚀 Configuration-Driven Backend Generator v2 Starting...")
    
    # Load the test config
    import json
    with open(test_config_path, 'r') as f:
        entities_config = json.load(f)
    
    success = orchestrator.generate_backend(entities_config, options)
    
    if success:
        print("✅ Backend generation completed successfully!")
        print("📁 Generated files in: ./test_output/src/")
        return 0
    else:
        print("❌ Backend generation failed")
        return 1

def run_dry_run():
    """Run a dry run with existing config"""
    
    old_config_path = Path("/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json")
    
    if not old_config_path.exists():
        print(f"❌ Backend config not found at: {old_config_path}")
        return 1
    
    print("🔍 DRY RUN - Previewing generation with existing config")
    
    options = GenerationOptions(
        dry_run=True,
        verbose=True,
        output_path="../../../backend-v2",
        force_overwrite=False
    )
    
    orchestrator = BackendGeneratorOrchestrator("../../../backend-v2")
    
    # Load the existing config
    import json
    with open(old_config_path, 'r') as f:
        entities_config = json.load(f)
    
    success = orchestrator.generate_backend(entities_config, options)
    return 0 if success else 1

def main():
    """Main CLI"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            return run_with_test_config()
        elif command == "existing":
            return run_with_existing_config()
        elif command == "dry-run" or command == "preview":
            return run_dry_run()
        elif command == "help":
            print("🛠️  Configuration-Driven Backend Generator v2 (Modular)")
            print("")
            print("Usage:")
            print("  python run.py existing   # Use existing v1 backend config")
            print("  python run.py test       # Use test config")
            print("  python run.py dry-run    # Preview with existing config")  
            print("  python run.py help       # Show this help")
            print("")
            print("Or use the main generator directly:")
            print("  python main.py <config.json> [options]")
            print("")
            print("Features:")
            print("  ✅ Modular architecture following SRP")
            print("  ✅ Configuration-driven with zero hardcoding")
            print("  ✅ Clean separation of concerns")
            print("  ✅ Extensible and maintainable")
            return 0
        else:
            print(f"❌ Unknown command: {command}")
            print("   Use 'help' to see available commands")
            return 1
    else:
        # Default: use existing config
        return run_with_existing_config()

if __name__ == "__main__":
    exit(main())