#!/usr/bin/env python3
"""
Frontend Generator Mini - Unified CLI
Generates complete frontend applications from backend config
"""

import argparse
import sys
import json
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))
sys.path.append(str(Path(__file__).parent / "shared"))
sys.path.append(str(Path(__file__).parent / "generators"))

from core.frontend_generator import FrontendGenerator


def main():
    parser = argparse.ArgumentParser(description='Frontend Generator Mini - Unified Generation Tool')
    parser.add_argument('--output', type=str, required=True, help='Output directory for generated files')
    parser.add_argument('--config', type=str, required=True, help='Backend config JSON file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        config_path = Path(args.config)
        output_path = Path(args.output)
        
        if not config_path.exists():
            print(f"❌ Config file not found: {config_path}")
            sys.exit(1)
        
        print(f"🚀 Frontend Generator Mini")
        print(f"📖 Config: {config_path}")
        print(f"📁 Output: {output_path}")
        
        if args.verbose:
            print("🔍 Verbose mode enabled")
        
        # Initialize generator
        generator = FrontendGenerator(output_path, config_path, verbose=args.verbose)
        
        # Generate all components
        generator.generate()
        
        print("✅ Generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()