#!/usr/bin/env python3
"""
Main backend generation script
Reads configuration and generates all required backend files
"""

import json
import argparse
from pathlib import Path
from backend_generator import BackendGenerator

def load_config(config_path: str = "backend_config.json") -> dict:
    """Load generation configuration from JSON file"""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        return json.load(f)

def generate_all_endpoints(config: dict, generator: BackendGenerator):
    """Generate all endpoints from configuration"""
    endpoints = config.get('endpoints', {})
    
    print(f"🚀 Generating {len(endpoints)} backend endpoints...")
    
    for endpoint_name, endpoint_config in endpoints.items():
        print(f"\n📦 Processing {endpoint_name}...")
        try:
            generator.generate_endpoint(endpoint_config)
            print(f"✅ {endpoint_name} generated successfully")
        except Exception as e:
            print(f"❌ Error generating {endpoint_name}: {e}")
            continue
    
    print(f"\n🎉 Backend generation complete!")

def generate_single_endpoint(endpoint_name: str, config: dict, generator: BackendGenerator):
    """Generate a single endpoint"""
    endpoints = config.get('endpoints', {})
    
    if endpoint_name not in endpoints:
        print(f"❌ Endpoint '{endpoint_name}' not found in configuration")
        available = ', '.join(endpoints.keys())
        print(f"Available endpoints: {available}")
        return
    
    print(f"🚀 Generating {endpoint_name} endpoint...")
    
    try:
        generator.generate_endpoint(endpoints[endpoint_name])
        print(f"✅ {endpoint_name} generated successfully")
    except Exception as e:
        print(f"❌ Error generating {endpoint_name}: {e}")

def list_available_endpoints(config: dict):
    """List all available endpoints in configuration"""
    endpoints = config.get('endpoints', {})
    
    print("📋 Available endpoints:")
    for name, config in endpoints.items():
        entity = config.get('entity', 'Unknown')
        methods = len(config.get('endpoints', []))
        print(f"  - {name}: {entity} ({methods} methods)")

def main():
    parser = argparse.ArgumentParser(description='Generate backend endpoints from configuration')
    parser.add_argument('--config', '-c', default='backend_config.json', 
                        help='Configuration file path')
    parser.add_argument('--endpoint', '-e', 
                        help='Generate specific endpoint only')
    parser.add_argument('--list', '-l', action='store_true',
                        help='List available endpoints')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Generate all endpoints')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        generator = BackendGenerator()
        
        if args.list:
            list_available_endpoints(config)
            return
        
        if args.endpoint:
            generate_single_endpoint(args.endpoint, config, generator)
        elif args.all:
            generate_all_endpoints(config, generator)
        else:
            # Interactive mode
            print("🤖 Backend Generator Interactive Mode")
            list_available_endpoints(config)
            print("\nOptions:")
            print("  - Type endpoint name to generate single endpoint")
            print("  - Type 'all' to generate all endpoints")
            print("  - Type 'quit' to exit")
            
            while True:
                choice = input("\n> ").strip().lower()
                
                if choice == 'quit':
                    break
                elif choice == 'all':
                    generate_all_endpoints(config, generator)
                    break
                elif choice in config.get('endpoints', {}):
                    generate_single_endpoint(choice, config, generator)
                else:
                    print(f"❌ Unknown option: {choice}")
                    
    except FileNotFoundError as e:
        print(f"❌ {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()