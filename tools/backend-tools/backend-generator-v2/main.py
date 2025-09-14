#!/usr/bin/env python3
"""
Configuration-Driven Backend Generator v2
Main orchestrator that coordinates all modules following SRP
"""

import json
import logging
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

# Import core modules
from core.config_loader import ConfigLoader
from core.template_engine import TemplateEngine
from core.file_writer import FileWriter, FilePathHelper

# Import generator modules
from generators.model_generator import ModelGenerator
from generators.service_generator import ServiceGenerator
from generators.route_generator import RouteGenerator
from generators.infrastructure_generator import InfrastructureGenerator


@dataclass
class GenerationOptions:
    """Options for code generation"""
    dry_run: bool = False
    verbose: bool = False
    validate_config: bool = True
    output_path: str = "../../backend-v2"
    force_overwrite: bool = False


class BackendGeneratorOrchestrator:
    """Main orchestrator that coordinates all generator modules"""
    
    def __init__(self, backend_path: str = None, config_dir: str = None):
        self.backend_path = backend_path or "../../backend-v2"
        
        # Setup logging
        self.logger = logging.getLogger("backend_generator_orchestrator")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Initialize core modules
        self.config_loader = ConfigLoader(config_dir)
        self.template_engine = TemplateEngine()
        self.file_writer = None  # Will be initialized with options
        
        # Generator modules (will be initialized when file_writer is ready)
        self.model_generator = None
        self.service_generator = None
        self.route_generator = None
        self.infrastructure_generator = None
    
    def _initialize_generators(self, options: GenerationOptions):
        """Initialize generator modules with file writer"""
        self.file_writer = FileWriter(options.output_path, options.dry_run)
        
        # Initialize all generator modules
        self.model_generator = ModelGenerator(self.file_writer, self.template_engine)
        self.service_generator = ServiceGenerator(self.file_writer, self.template_engine)
        self.route_generator = RouteGenerator(self.file_writer, self.template_engine, self.config_loader)
        self.infrastructure_generator = InfrastructureGenerator(self.file_writer, self.template_engine)
    
    def generate_backend(self, entities_config: Dict[str, Any], options: GenerationOptions) -> bool:
        """Generate complete backend from entities configuration"""
        try:
            self.logger.info("🚀 Starting configuration-driven backend generation")
            
            # Initialize generators with options
            self._initialize_generators(options)
            
            # Load all configurations
            configs = self.config_loader.load_all_configs()
            
            if options.validate_config:
                self._validate_all_configs(configs)
            
            if options.dry_run:
                self.logger.info("🔍 DRY RUN MODE - No files will be created")
                return self._preview_generation(entities_config)
            
            # Generate infrastructure files first
            infra_success = self.infrastructure_generator.generate_infrastructure(configs)
            if not infra_success:
                self.logger.error("❌ Infrastructure generation failed")
                return False
            
            # Generate each entity
            success_count = 0
            total_count = len(entities_config.get('endpoints', {}))
            
            for entity_name, entity_config in entities_config.get('endpoints', {}).items():
                self.logger.info(f"📦 Generating {entity_name}...")
                if self._generate_entity(entity_name, entity_config, configs):
                    success_count += 1
                else:
                    self.logger.error(f"❌ Failed to generate {entity_name}")
            
            # Generate app.ts with dynamic route registration
            app_success = self.infrastructure_generator.generate_app_file(entities_config, configs)
            if not app_success:
                self.logger.error("❌ App.ts generation failed")
                return False
            
            # Report results
            self._report_generation_results(success_count, total_count)
            return success_count == total_count
            
        except Exception as e:
            self.logger.error(f"💥 Generation failed: {e}")
            return False
    
    def _generate_entity(self, entity_name: str, entity_config: Dict[str, Any], configs: Dict[str, Any]) -> bool:
        """Generate model, service, and routes for a single entity"""
        try:
            entity = entity_config.get('entity', entity_name.capitalize())
            entities = entity_config.get('entities', f"{entity_name}s")
            table_name = entity_config.get('table_name', entities.lower())
            properties = entity_config.get('properties', {})
            methods = entity_config.get('methods', [])
            endpoints = entity_config.get('endpoints', [])
            
            # Apply entity overrides
            entity_info = self.template_engine.apply_entity_overrides(entity_name, entity, entities, configs)
            
            # Generate files using specialized generators
            model_success = self.model_generator.generate_model(entity_info, properties, configs)
            service_success = self.service_generator.generate_service(entity_info, table_name, methods, properties, configs)
            route_success = self.route_generator.generate_routes(entity_info, endpoints, configs)
            
            return model_success and service_success and route_success
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate {entity_name}: {e}")
            return False
    
    def _validate_all_configs(self, configs: Dict[str, Any]):
        """Validate all configuration files"""
        self.logger.info("🔍 Validating configurations...")
        
        for config_name, config_data in configs.items():
            if config_data:  # Only validate non-empty configs
                is_valid = self.config_loader.validate_config(config_data, config_name)
                if not is_valid:
                    self.logger.warning(f"⚠️ Configuration validation failed: {config_name}")
    
    def _preview_generation(self, entities_config: Dict[str, Any]) -> bool:
        """Preview what would be generated (dry run)"""
        self.logger.info("📋 Generation Preview:")
        
        # Infrastructure files
        self.logger.info("  🏗️ Infrastructure:")
        infra_paths = FilePathHelper.get_infrastructure_paths()
        for name, path in infra_paths.items():
            self.logger.info(f"    📝 {name}: {path}")
        
        # Entity files
        for entity_name, entity_config in entities_config.get('endpoints', {}).items():
            entity = entity_config.get('entity', entity_name.capitalize())
            entities = entity_config.get('entities', f"{entity_name}s")
            
            self.logger.info(f"  📦 {entity_name}:")
            self.logger.info(f"    📝 Model: {FilePathHelper.get_model_path(entity)}")
            self.logger.info(f"    🔧 Service: {FilePathHelper.get_service_path(entity_name)}")
            self.logger.info(f"    🛣️  Routes: {FilePathHelper.get_routes_path(entities)}")
        
        return True
    
    def _report_generation_results(self, success_count: int, total_count: int):
        """Report generation results"""
        self.logger.info(f"📊 Generation Summary: {success_count}/{total_count} entities successful")
        
        if self.file_writer:
            stats = self.file_writer.get_stats()
            self.logger.info(f"📁 Total files written: {stats['total_files']}")
            self.logger.info(f"📂 Output path: {stats['output_path']}")


def main():
    """CLI for the configuration-driven generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Configuration-Driven Backend Generator v2')
    parser.add_argument('config', help='Path to entities configuration file')
    parser.add_argument('--backend-path', default='../../backend-v2', help='Backend output path')
    parser.add_argument('--config-dir', help='Configuration directory path')
    parser.add_argument('--dry-run', action='store_true', help='Preview generation without creating files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--force', action='store_true', help='Force overwrite existing files')
    parser.add_argument('--no-validate', action='store_true', help='Skip configuration validation')
    
    args = parser.parse_args()
    
    # Setup verbose logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load entities configuration
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return 1
    
    try:
        with open(config_path, 'r') as f:
            entities_config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config file: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error reading config file: {e}")
        return 1
    
    # Create generator options
    options = GenerationOptions(
        dry_run=args.dry_run,
        verbose=args.verbose,
        validate_config=not args.no_validate,
        output_path=args.backend_path,
        force_overwrite=args.force
    )
    
    # Create orchestrator
    orchestrator = BackendGeneratorOrchestrator(args.backend_path, args.config_dir)
    
    print("🚀 Configuration-Driven Backend Generator v2 Starting...")
    
    success = orchestrator.generate_backend(entities_config, options)
    
    if success:
        print("✅ Backend generation completed successfully!")
        return 0
    else:
        print("❌ Backend generation failed")
        return 1


if __name__ == "__main__":
    exit(main())