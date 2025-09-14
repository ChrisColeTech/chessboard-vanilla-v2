#!/usr/bin/env python3
"""
Frontend Generator V2 - CLI
Generates frontend components from backend config
"""

import argparse
import sys
import json
from pathlib import Path
from core.frontend_generator import FrontendGenerator

def main():
    parser = argparse.ArgumentParser(description='Frontend Generator V2')
    parser.add_argument('--output', type=str, default='../../../frontend-v2/src', help='Output directory')
    parser.add_argument('--config', type=str, default='../backend-tools/backend-generator-v2/migrated_config.json', help='Backend config file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        config_path = Path(args.config)
        output_path = Path(args.output)
        
        print(f"🚀 Frontend Generator V2")
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