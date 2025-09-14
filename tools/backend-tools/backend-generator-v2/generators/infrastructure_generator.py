#!/usr/bin/env python3
"""
Infrastructure Generator
Responsible for generating infrastructure files (database, middleware, app.ts)
"""

import logging
from typing import Dict, Any
from core.file_writer import FileWriter, FilePathHelper
from core.template_engine import TemplateEngine


class InfrastructureGenerator:
    """Generates infrastructure files"""
    
    def __init__(self, file_writer: FileWriter, template_engine: TemplateEngine):
        self.file_writer = file_writer
        self.template_engine = template_engine
        self.logger = logging.getLogger("infrastructure_generator")
    
    def generate_infrastructure(self, configs: Dict[str, Any]) -> bool:
        """Generate all infrastructure files"""
        try:
            self.logger.info("🏗️ Generating infrastructure files...")
            
            infrastructure_templates = configs.get('infrastructure_templates', {})
            templates = infrastructure_templates.get('templates', {})
            
            success_count = 0
            total_count = 0
            
            # Generate core infrastructure files
            infrastructure_files = ['database', 'auth_middleware', 'validation_middleware']
            
            for template_name in infrastructure_files:
                if template_name in templates:
                    success = self._generate_infrastructure_file(template_name, templates[template_name])
                    if success:
                        success_count += 1
                    total_count += 1
            
            self.logger.info(f"📊 Infrastructure generation: {success_count}/{total_count} successful")
            return success_count == total_count
            
        except Exception as e:
            self.logger.error(f"❌ Infrastructure generation failed: {e}")
            return False
    
    def generate_app_file(self, entities_config: Dict[str, Any], configs: Dict[str, Any]) -> bool:
        """Generate app.ts with dynamic route registration"""
        try:
            route_imports = []
            route_registrations = []
            
            for entity_name, entity_config in entities_config.get('endpoints', {}).items():
                entities = entity_config.get('entities', f"{entity_name}s")
                entity = entity_config.get('entity', entity_name.capitalize())
                
                # Generate import and registration
                router_name = f"{entity}Router"
                filename = FilePathHelper.to_camel_case(entities)
                
                # Use kebab-case for API routes (best practice)
                kebab_route = FilePathHelper.to_kebab_case(entity_name)
                
                route_imports.append(f"import {router_name} from './routes/{filename}';")
                route_registrations.append(f"app.use('/api/{kebab_route}', {router_name});")
            
            # Get app template
            infrastructure_templates = configs.get('infrastructure_templates', {})
            app_template = infrastructure_templates.get('templates', {}).get('app_template', {}).get('template', '')
            
            if not app_template:
                self.logger.error("❌ No app template found in configuration")
                return False
            
            # Build app.ts content
            content = self.template_engine.process_template(app_template, {
                'ROUTE_IMPORTS': '\n'.join(route_imports),
                'ROUTE_REGISTRATIONS': '\n'.join(route_registrations)
            })
            
            # Write app.ts
            success = self.file_writer.write_file("src/app.ts", content)
            
            if success:
                self.logger.info(f"📝 Generated app.ts with {len(route_imports)} routes")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate app.ts: {e}")
            return False
    
    def _generate_infrastructure_file(self, template_name: str, template_config: Dict[str, Any]) -> bool:
        """Generate a single infrastructure file"""
        try:
            file_path = template_config.get('path', '')
            template = template_config.get('template', '')
            
            if not file_path or not template:
                self.logger.error(f"❌ Invalid template config for {template_name}")
                return False
            
            success = self.file_writer.write_file(file_path, template)
            
            if success:
                self.logger.info(f"📝 Generated: {file_path}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate {template_name}: {e}")
            return False