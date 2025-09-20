#!/usr/bin/env python3
"""
Database Configuration Tool

Unified CLI for database schema introspection and configuration management.
Provides commands to generate, validate, and update API configurations.
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'payload-generator', 'seeders'))

from database_manager import DatabaseManager
from schema_introspector import SchemaIntrospector, ConfigGenerator
from config_validator import ConfigValidator, load_config


class DatabaseConfigTool:
    """Main tool class for database configuration management"""
    
    def __init__(self):
        self.db_manager = None
        self.introspector = None
        
    def initialize_database(self):
        """Initialize database connection"""
        print("📡 Connecting to database...")
        self.db_manager = DatabaseManager()
        self.introspector = SchemaIntrospector(self.db_manager)
        
    def command_generate(self, args) -> int:
        """Generate new configuration from database schema"""
        print("🔧 Generating configuration from database schema...")
        
        try:
            self.initialize_database()
            
            # Introspect schema
            tables = self.introspector.introspect_database()
            
            # Generate configuration
            config_generator = ConfigGenerator(self.introspector)
            config = config_generator.generate_config(tables)
            
            # Determine output path - default to /config/backend_config.json
            if args.output:
                output_path = Path(args.output)
            else:
                # Default to /config/backend_config.json relative to project root
                project_root = Path(__file__).parent.parent.parent.parent
                config_dir = project_root / "config" 
                config_dir.mkdir(exist_ok=True)  # Create config directory if it doesn't exist
                output_path = "/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json"
            
            # Save configuration
            print(f"💾 Saving configuration to: {output_path}")
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            print(f"✅ Configuration generated successfully!")
            print(f"📊 Generated config for {len(config['endpoints'])} tables")
            
            # Show summary
            if args.verbose:
                print("\n📋 Generated Endpoints:")
                for table_name, table_config in config['endpoints'].items():
                    entity = table_config['entity']
                    prop_count = len(table_config['properties'])
                    print(f"   • {table_name} -> {entity} ({prop_count} properties)")
                    
            return 0
            
        except Exception as error:
            print(f"❌ Generation failed: {error}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
            
    def command_validate(self, args) -> int:
        """Validate existing configuration against database schema"""
        print("🔍 Validating configuration against database schema...")
        
        try:
            # Load configuration
            config_path = "/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json"
            print(f"📄 Loading config from: {config_path}")
            config = load_config(config_path)
            
            # Get database schema
            self.initialize_database()
            tables = self.introspector.introspect_database()
            
            # Validate
            validator = ConfigValidator()
            result = validator.validate_config(config, tables)
            
            # Print results
            if args.verbose or not result.is_valid:
                validator.print_detailed_report(result)
            else:
                print(result.summary)
                
            return 0 if result.is_valid else 1
            
        except Exception as error:
            print(f"❌ Validation failed: {error}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
            
    def command_compare(self, args) -> int:
        """Compare two configurations to show differences"""
        print("🔀 Comparing configurations...")
        
        try:
            # Load configurations
            config1_path = Path(args.config1)
            config2_path = Path(args.config2)
            
            print(f"📄 Loading config 1 from: {config1_path}")
            config1 = load_config(config1_path)
            
            print(f"📄 Loading config 2 from: {config2_path}")
            config2 = load_config(config2_path)
            
            # Compare
            self._compare_configs(config1, config2, args.verbose)
            
            return 0
            
        except Exception as error:
            print(f"❌ Comparison failed: {error}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
            
    def command_update(self, args) -> int:
        """Update existing configuration with new schema"""
        print("🔄 Updating configuration with current database schema...")
        
        try:
            # Load existing config
            config_path = "/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json"
            print(f"📄 Loading existing config from: {config_path}")
            existing_config = load_config(config_path)
            
            # Generate new config
            self.initialize_database()
            tables = self.introspector.introspect_database()
            config_generator = ConfigGenerator(self.introspector)
            new_config = config_generator.generate_config(tables)
            
            # Merge configurations (preserve custom settings)
            merged_config = self._merge_configurations(existing_config, new_config)
            
            # Save updated configuration
            output_path = Path(args.output) if args.output else config_path.with_name(f"updated_{config_path.name}")
            
            print(f"💾 Saving updated configuration to: {output_path}")
            with open(output_path, 'w') as f:
                json.dump(merged_config, f, indent=2)
                
            print(f"✅ Configuration updated successfully!")
            return 0
            
        except Exception as error:
            print(f"❌ Update failed: {error}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
            
    def _compare_configs(self, config1: Dict[str, Any], config2: Dict[str, Any], verbose: bool = False):
        """Compare two configurations and show differences"""
        endpoints1 = config1.get('endpoints', {})
        endpoints2 = config2.get('endpoints', {})
        
        tables1 = set(endpoints1.keys())
        tables2 = set(endpoints2.keys())
        
        # Show table differences
        only_in_1 = tables1 - tables2
        only_in_2 = tables2 - tables1
        common = tables1 & tables2
        
        print(f"\n📊 Comparison Results:")
        print(f"   Config 1 tables: {len(tables1)}")
        print(f"   Config 2 tables: {len(tables2)}")
        print(f"   Common tables: {len(common)}")
        
        if only_in_1:
            print(f"\n📋 Only in Config 1: {', '.join(only_in_1)}")
        if only_in_2:
            print(f"\n📋 Only in Config 2: {', '.join(only_in_2)}")
            
        # Compare common tables
        if verbose and common:
            print(f"\n🔍 Detailed comparison of common tables:")
            for table in sorted(common):
                props1 = set(endpoints1[table].get('properties', {}).keys())
                props2 = set(endpoints2[table].get('properties', {}).keys())
                
                if props1 != props2:
                    print(f"   • {table}:")
                    only_1 = props1 - props2
                    only_2 = props2 - props1
                    if only_1:
                        print(f"     - Only in Config 1: {', '.join(only_1)}")
                    if only_2:
                        print(f"     - Only in Config 2: {', '.join(only_2)}")
                        
    def _merge_configurations(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new configuration with existing, preserving custom settings"""
        merged = new.copy()
        merged['description'] = f"Updated configuration (merged from existing)"
        
        # Preserve any custom endpoint configurations
        existing_endpoints = existing.get('endpoints', {})
        new_endpoints = new.get('endpoints', {})
        
        for table_name, table_config in new_endpoints.items():
            if table_name in existing_endpoints:
                existing_table = existing_endpoints[table_name]
                
                # Preserve custom methods and endpoints if they exist
                if 'custom_methods' in existing_table:
                    table_config['custom_methods'] = existing_table['custom_methods']
                if 'custom_endpoints' in existing_table:
                    table_config['custom_endpoints'] = existing_table['custom_endpoints']
                    
        return merged


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Database Configuration Tool - Manage API configurations from database schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate new configuration from database (exports to /config/backend_config.json)
  python db_config_tool.py generate

  # Validate existing configuration
  python db_config_tool.py validate --config /mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json

  # Compare two configurations
  python db_config_tool.py compare old_config.json new_config.json

  # Update configuration with current schema
  python db_config_tool.py update --config old_config.json --output updated_config.json
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate configuration from database schema')
    generate_parser.add_argument('-o', '--output', help='Output file path (default: /config/backend_config.json)')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate configuration against database')
    validate_parser.add_argument('-c', '--config', help='Configuration file to validate')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two configurations')
    compare_parser.add_argument('config1', help='First configuration file')
    compare_parser.add_argument('config2', help='Second configuration file')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update configuration with current schema')
    update_parser.add_argument('-c', '--config', help='Existing configuration file')
    update_parser.add_argument('-o', '--output', help='Output file path')
    
    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
        
    print("🛠️  Database Configuration Tool")
    print("=" * 50)
    
    tool = DatabaseConfigTool()
    
    try:
        if args.command == 'generate':
            return tool.command_generate(args)
        elif args.command == 'validate':
            return tool.command_validate(args)
        elif args.command == 'compare':
            return tool.command_compare(args)
        elif args.command == 'update':
            return tool.command_update(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        return 1
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())