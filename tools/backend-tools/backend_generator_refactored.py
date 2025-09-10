#!/usr/bin/env python3
"""
Refactored Backend Pattern Generator
Orchestrates modular components to generate TypeScript backend files
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

from .pattern_analyzer import PatternAnalyzer
from .template_generator import TemplateGenerator
from .service_generator import ServiceGenerator


class BackendGeneratorRefactored:
    """Refactored backend generator using modular components"""
    
    def __init__(self, backend_path: str = "../backend"):
        self.backend_path = Path(backend_path)
        self.pattern_analyzer = PatternAnalyzer(backend_path)
        self.template_generator = TemplateGenerator(backend_path)
        self.service_generator = ServiceGenerator(backend_path)
        
    def analyze_existing_pattern(self, reference_service: str = "puzzles") -> Dict:
        """Analyze existing files to extract patterns"""
        return self.pattern_analyzer.analyze_existing_pattern(reference_service)
    
    def generate_endpoint(self, config: Dict[str, Any]) -> bool:
        """Generate a complete endpoint (route + service + model)"""
        try:
            entity = config['entity']
            entities = config.get('entities', f"{entity.lower()}s")
            table_name = config.get('table_name', entities)
            
            print(f"🔧 Generating {entity} endpoint...")
            
            # Generate model
            self.template_generator.generate_model(
                entity, 
                config.get('properties', {}), 
                config
            )
            
            # Generate service  
            self.service_generator.generate_service(
                entity, 
                entities, 
                table_name, 
                config.get('methods', ['getAll', 'getById', 'create', 'update', 'delete']),
                config
            )
            
            # Generate route
            self.template_generator.generate_route(
                entity, 
                entities, 
                config.get('endpoints', []),
                config
            )
            
            print(f"✅ Generated {entity} endpoint files")
            return True
            
        except Exception as e:
            print(f"❌ Error generating {entity} endpoint: {str(e)}")
            return False


def main():
    """Main function to run the refactored generator"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python backend_generator_refactored.py <endpoint_name>")
        print("Available endpoints: users, puzzles, games, stats, learning, tutorials")
        return
    
    endpoint_name = sys.argv[1].lower()
    
    # Load config
    config_path = Path(__file__).parent.parent / 'backend_config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    if endpoint_name not in config['endpoints']:
        print(f"Error: {endpoint_name} not found in config")
        print(f"Available endpoints: {', '.join(config['endpoints'].keys())}")
        return
    
    target_dir = config.get('target_directory', '../backend')
    generator = BackendGeneratorRefactored(target_dir)
    endpoint_config = config['endpoints'][endpoint_name]
    
    print("🚀 Refactored Backend Generator Starting...")
    print(f"🔧 Generating {endpoint_config['entity']} endpoint...")
    success = generator.generate_endpoint(endpoint_config)
    
    if success:
        print(f"✅ Generated {endpoint_config['entity']} endpoint files")
        print("✅ Backend generation complete!")
    else:
        print("❌ Failed to generate endpoint files")


if __name__ == "__main__":
    main()