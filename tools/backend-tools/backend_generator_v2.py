#!/usr/bin/env python3
"""
Backend Generator v2 - Enhanced Orchestrator
Builds on the existing modular architecture with improved features and better UX
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

# Import existing modular components
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pattern_analyzer import PatternAnalyzer
from template_generator import TemplateGenerator
from service_generator import ServiceGenerator
from infrastructure_generator import InfrastructureGenerator
from config import DEFAULT_BACKEND_PATH, GeneratorConfig


@dataclass
class GenerationOptions:
    """Enhanced options for code generation"""
    dry_run: bool = False
    verbose: bool = False
    validate_config: bool = True
    backup_existing: bool = False
    force_overwrite: bool = False
    output_format: str = "typescript"  # typescript, javascript
    include_tests: bool = False
    include_docs: bool = False


class BackendGeneratorV2:
    """Enhanced backend generator v2 - orchestrates existing modules with better features"""
    
    def __init__(self, backend_path: str = None):
        self.backend_path = Path(backend_path or DEFAULT_BACKEND_PATH)
        
        # Use existing modular components
        self.pattern_analyzer = PatternAnalyzer(backend_path)
        self.template_generator = TemplateGenerator(backend_path)
        self.service_generator = ServiceGenerator(backend_path)
        self.infrastructure_generator = InfrastructureGenerator(backend_path)
        
        # Setup enhanced logging
        self.logger = logging.getLogger("backend_generator_v2")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def generate_endpoint(self, config: Dict[str, Any], options: Optional[GenerationOptions] = None) -> bool:
        """Generate endpoint with enhanced options and validation"""
        if options is None:
            options = GenerationOptions()
        
        try:
            entity = config['entity']
            entities = config.get('entities', f"{entity.lower()}s")
            
            self.logger.info(f"🚀 Starting v2 generation for {entity} endpoint")
            
            # Enhanced validation
            if options.validate_config:
                validation_errors = self._validate_config(config)
                if validation_errors:
                    for error in validation_errors:
                        self.logger.error(f"❌ Validation error: {error}")
                    return False
            
            # Backup disabled by default
            # if options.backup_existing:
            #     self._backup_existing_files(entity, entities)
            
            # Dry run check
            if options.dry_run:
                self.logger.info("🔍 DRY RUN MODE - No files will be created")
                self._preview_generation(config)
                return True
            
            # Generate with existing modules
            success = True
            
            # Generate model
            self.logger.info(f"📝 Generating {entity} model...")
            try:
                self.template_generator.generate_model(
                    entity, 
                    config.get('properties', {}), 
                    config
                )
            except Exception as e:
                self.logger.error(f"❌ Model generation failed: {e}")
                success = False
            
            # Generate service
            self.logger.info(f"🔧 Generating {entity} service...")
            try:
                self.service_generator.generate_service(
                    entity,
                    entities,
                    config.get('table_name', entities.lower()),
                    config.get('methods', ['getAll', 'getById', 'create', 'update', 'delete']),
                    config
                )
            except Exception as e:
                self.logger.error(f"❌ Service generation failed: {e}")
                success = False
            
            # Generate routes
            self.logger.info(f"🛣️ Generating {entity} routes...")
            try:
                self.template_generator.generate_route(
                    entity,
                    entities,
                    config.get('endpoints', []),
                    config
                )
            except Exception as e:
                self.logger.error(f"❌ Route generation failed: {e}")
                success = False
            
            # Generate tests if requested
            if options.include_tests:
                self.logger.info(f"🧪 Generating {entity} tests...")
                self._generate_tests(config)
            
            # Generate documentation if requested
            if options.include_docs:
                self.logger.info(f"📚 Generating {entity} documentation...")
                self._generate_docs(config)
            
            if success:
                self.logger.info(f"✅ Successfully generated {entity} endpoint!")
                self._print_generation_summary(config)
            else:
                self.logger.error(f"❌ Generation failed for {entity} endpoint")
            
            return success
            
        except Exception as e:
            self.logger.error(f"💥 Unexpected error during generation: {e}")
            return False
    
    def generate_multiple_endpoints(self, config_file: Union[str, Path], options: Optional[GenerationOptions] = None) -> Dict[str, bool]:
        """Generate multiple endpoints from a configuration file"""
        config_path = Path(config_file)
        
        if not config_path.exists():
            self.logger.error(f"❌ Config file not found: {config_path}")
            return {}
        
        with open(config_path, 'r') as f:
            full_config = json.load(f)
        
        results = {}
        endpoints = full_config.get('endpoints', {})
        
        self.logger.info(f"🚀 Generating {len(endpoints)} endpoints from {config_path}")
        
        # Generate infrastructure files once at the beginning
        self.infrastructure_generator.generate_infrastructure()
        
        for endpoint_name, endpoint_config in endpoints.items():
            self.logger.info(f"\n📦 Processing {endpoint_name}...")
            results[endpoint_name] = self.generate_endpoint(endpoint_config, options)
        
        # Print final summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        self.logger.info(f"\n📊 Generation Summary:")
        self.logger.info(f"   ✅ Successful: {successful}/{total}")
        self.logger.info(f"   ❌ Failed: {total - successful}/{total}")
        
        return results
    
    def _validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Enhanced configuration validation"""
        errors = []
        
        # Required fields
        if not config.get('entity'):
            errors.append("Entity name is required")
        
        # Entity name validation
        entity = config.get('entity', '')
        if entity and not entity.replace('_', '').isalnum():
            errors.append(f"Entity name '{entity}' contains invalid characters")
        
        # Properties validation
        properties = config.get('properties', {})
        if not properties:
            errors.append("At least one property is required")
        
        for prop_name, prop_type in properties.items():
            if not prop_name.replace('_', '').isalnum():
                errors.append(f"Property name '{prop_name}' contains invalid characters")
        
        # Methods validation
        methods = config.get('methods', [])
        valid_methods = ['getAll', 'getById', 'create', 'update', 'delete']
        for method in methods:
            if not method.startswith(tuple(['get', 'create', 'update', 'delete'])):
                # Allow custom methods but warn
                self.logger.warning(f"⚠️ Custom method '{method}' may not be supported")
        
        return errors
    
    def _backup_existing_files(self, entity: str, entities: str):
        """Backup existing files before overwriting"""
        entity_upper = entity.capitalize()
        entity_lower = entity.lower()
        entities_lower = entities.lower()
        
        backup_dir = self.backend_path / "backup" / "generated"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        files_to_backup = [
            self.backend_path / "src/models" / f"{entity_upper}.ts",
            self.backend_path / "src/services" / f"{entity_lower}Service.ts",
            self.backend_path / "src/routes" / f"{entities_lower}.ts"
        ]
        
        for file_path in files_to_backup:
            if file_path.exists():
                backup_path = backup_dir / file_path.name
                backup_path.write_text(file_path.read_text())
                self.logger.info(f"📋 Backed up {file_path.name}")
    
    def _preview_generation(self, config: Dict[str, Any]):
        """Preview what would be generated (dry run)"""
        entity = config['entity']
        entities = config.get('entities', f"{entity.lower()}s")
        
        self.logger.info(f"📋 Generation Preview for {entity}:")
        self.logger.info(f"   📝 Model: src/models/{entity.capitalize()}.ts")
        self.logger.info(f"   🔧 Service: src/services/{entity.lower()}Service.ts")
        self.logger.info(f"   🛣️ Routes: src/routes/{entities.lower()}.ts")
        self.logger.info(f"   📊 Properties: {list(config.get('properties', {}).keys())}")
        self.logger.info(f"   ⚙️ Methods: {config.get('methods', [])}")
    
    def _generate_tests(self, config: Dict[str, Any]):
        """Generate test files (placeholder for future implementation)"""
        self.logger.info("🧪 Test generation not yet implemented")
    
    def _generate_docs(self, config: Dict[str, Any]):
        """Generate documentation (placeholder for future implementation)"""
        self.logger.info("📚 Documentation generation not yet implemented")
    
    def _print_generation_summary(self, config: Dict[str, Any]):
        """Print a summary of what was generated"""
        entity = config['entity']
        
        self.logger.info(f"\n📊 Generation Summary for {entity}:")
        self.logger.info(f"   📁 Files created: 3 (model, service, routes)")
        self.logger.info(f"   📊 Properties: {len(config.get('properties', {}))}")
        self.logger.info(f"   ⚙️ Methods: {len(config.get('methods', []))}")
        self.logger.info(f"   🛣️ Endpoints: {len(config.get('endpoints', []))}")


def main():
    """Enhanced CLI for v2 generator"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Backend Generator v2 - Enhanced code generation')
    parser.add_argument('endpoint', nargs='?', help='Endpoint name to generate')
    parser.add_argument('--config', '-c', default='backend_config.json', help='Configuration file')
    parser.add_argument('--dry-run', action='store_true', help='Preview generation without creating files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--no-backup', action='store_true', help='Skip backing up existing files')
    parser.add_argument('--force', action='store_true', help='Force overwrite existing files')
    parser.add_argument('--all', action='store_true', help='Generate all endpoints from config')
    parser.add_argument('--backend-path', default=DEFAULT_BACKEND_PATH, help='Backend directory path')
    
    args = parser.parse_args()
    
    # Create generator with enhanced options
    options = GenerationOptions(
        dry_run=args.dry_run,
        verbose=args.verbose,
        backup_existing=not args.no_backup,
        force_overwrite=args.force
    )
    
    generator = BackendGeneratorV2(args.backend_path)
    
    print("🚀 Backend Generator v2 Starting...")
    
    if args.all:
        # Generate all endpoints
        results = generator.generate_multiple_endpoints(args.config, options)
        success_count = sum(1 for success in results.values() if success)
        print(f"✅ Generated {success_count}/{len(results)} endpoints successfully")
    else:
        if not args.endpoint:
            print("❌ Endpoint name required (or use --all)")
            sys.exit(1)
        
        # Load config and generate single endpoint
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            
            if args.endpoint not in config.get('endpoints', {}):
                print(f"❌ Endpoint '{args.endpoint}' not found in config")
                sys.exit(1)
            
            endpoint_config = config['endpoints'][args.endpoint]
            success = generator.generate_endpoint(endpoint_config, options)
            
            if success:
                print(f"✅ Successfully generated {args.endpoint} endpoint!")
            else:
                print(f"❌ Failed to generate {args.endpoint} endpoint")
                sys.exit(1)
                
        except FileNotFoundError:
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
        except Exception as e:
            print(f"💥 Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()