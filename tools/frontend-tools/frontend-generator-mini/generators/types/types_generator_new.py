"""
Types Generator - Refactored to use template engine and name standardizer
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from template_engine import TemplateEngine
from name_standardizer import NameStandardizer
from generators.base_generator import BaseGenerator


class TypesGenerator(BaseGenerator):
    """Generates TypeScript type definitions using template engine"""
    
    def __init__(self, output_path: Path):
        super().__init__(output_path)
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.template_engine = TemplateEngine(self.template_dir)
    
    def generate(self, endpoint_name: str, endpoint_config: dict, domain: str = 'other'):
        """Generate TypeScript types from backend config using templates"""
        print(f"📋 Generating types: {endpoint_name} (domain: {domain})")
        
        # Check for named template first
        named_template = self.template_dir / "named" / "types" / f"{endpoint_name}.ts.template"
        if named_template.exists():
            print(f"📝 Using named template: {endpoint_name}.ts.template")
            self._generate_from_named_template(endpoint_name, endpoint_config, domain, named_template)
            return
        
        # Skip dynamic generation for endpoints with special routing (e.g., auth)
        if endpoint_config.get('special_routing', False):
            print(f"⏭️  Skipping dynamic type generation for {endpoint_name} (special routing)")
            return
        
        # Generate from template using template engine
        entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
        properties = endpoint_config.get('properties', {})
        
        # Generate properties string
        properties_str = self._generate_properties_string(properties)
        
        # Prepare template variables
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'ENTITY_NAME_UPPER': entity_name.upper(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'properties_str': properties_str
        }
        
        # Load and render template
        try:
            type_content = self.template_engine.render_template(
                'api/types.ts.template',
                template_vars,
                is_static=False
            )
            
            # Write types file organized by domain
            output_dir = self.output_path / "types" / domain
            camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
            output_file = output_dir / f"{camel_endpoint}.ts"
            
            self.write_file(output_file, type_content)
            
        except Exception as e:
            print(f"❌ Error generating types {endpoint_name}: {e}")
            # Fallback to original hardcoded method
            self._generate_fallback(endpoint_name, endpoint_config, domain)
    
    def _generate_properties_string(self, properties: dict) -> str:
        """Generate TypeScript properties from backend properties"""
        if not properties:
            return "  // No properties defined"
        
        ts_properties = []
        for prop_name, prop_type in properties.items():
            ts_type = self._map_type(prop_type)
            # Use name standardizer for property names if needed
            formatted_prop_name = NameStandardizer.to_camel_case(prop_name)
            ts_properties.append(f"  {formatted_prop_name}: {ts_type};")
        
        return "\n".join(ts_properties)
    
    def _map_type(self, backend_type: str) -> str:
        """Map backend type to TypeScript type"""
        type_mapping = {
            'string': 'string',
            'number': 'number', 
            'boolean': 'boolean',
            'object': 'object',
            'array': 'any[]',
            'integer': 'number',
            'float': 'number',
            'datetime': 'string',  # ISO date string
            'date': 'string',
            'time': 'string',
            'uuid': 'string',
            'text': 'string',
            'json': 'object',
            'jsonb': 'object'
        }
        
        return type_mapping.get(backend_type.lower(), 'any')
    
    def _generate_fallback(self, endpoint_name: str, endpoint_config: dict, domain: str):
        """Fallback to original hardcoded generation"""
        print(f"🔄 Using fallback generation for {endpoint_name}")
        entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
        properties = endpoint_config.get('properties', {})
        
        # Generate using original logic but with name standardizer
        properties_str = self._generate_properties_string(properties)
        
        content = f"""// Generated types for {entity_name}

export interface {entity_name} {{
{properties_str}
}}

export interface {entity_name}Create {{
  // Properties needed for creating new {entity_name}
{properties_str}
}}

export interface {entity_name}Update {{
  // Properties that can be updated
{properties_str}
}}

export interface {entity_name}Filter {{
  // Properties for filtering/searching
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}}

export default {entity_name};"""
        
        # Write file
        output_dir = self.output_path / "types" / domain
        camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
        output_file = output_dir / f"{camel_endpoint}.ts"
        self.write_file(output_file, content)
    
    def _generate_from_named_template(self, endpoint_name: str, endpoint_config: dict, domain: str, template_path: Path):
        """Generate types from a named template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Write to the domain-specific types directory
            output_dir = self.output_path / "types" / domain
            camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
            output_file = output_dir / f"{camel_endpoint}.ts"
            
            self.write_file(output_file, template_content)
            
        except Exception as e:
            print(f"❌ Error generating from named template: {e}")
    
    def generate_barrel_exports(self):
        """Generate barrel export files for types"""
        print("📦 Generating types barrel exports...")
        
        types_dir = self.output_path / "types"
        if not types_dir.exists():
            return
            
        # Generate main types index
        self._generate_main_types_barrel()
        
        # Generate domain-specific barrel exports
        for domain_dir in types_dir.iterdir():
            if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                self._generate_domain_barrel(domain_dir)
    
    def _generate_main_types_barrel(self):
        """Generate main types/index.ts barrel export"""
        types_dir = self.output_path / "types"
        exports = ["// Barrel exports for types", ""]
        
        # Export from domain directories
        for domain_dir in sorted(types_dir.iterdir()):
            if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                domain = domain_dir.name
                exports.append(f"// {domain.title()} types")
                exports.append(f"export * from './{domain}';")
                exports.append("")
        
        # Export common/shared types that might be in root
        for type_file in types_dir.glob("*.ts"):
            if type_file.name != "index.ts":
                type_name = type_file.stem
                exports.append(f"export * from './{type_name}';")
        
        content = "\n".join(exports)
        index_file = types_dir / "index.ts"
        self.write_file(index_file, content)
    
    def _generate_domain_barrel(self, domain_dir: Path):
        """Generate barrel export for a domain directory"""
        domain = domain_dir.name
        exports = [f"// {domain.title()} types barrel exports", ""]
        
        # Export all TypeScript files in the domain
        for type_file in sorted(domain_dir.glob("*.ts")):
            if type_file.name != "index.ts":
                type_name = type_file.stem
                exports.append(f"export * from './{type_name}';")
        
        if len(exports) > 2:  # Only create if there are actual exports
            content = "\n".join(exports)
            index_file = domain_dir / "index.ts"
            self.write_file(index_file, content)