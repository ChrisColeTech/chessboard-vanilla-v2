"""
Services Generator - Refactored to use template engine
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


class ServicesGenerator(BaseGenerator):
    """Generates service classes using template engine"""
    
    def __init__(self, output_path: Path):
        super().__init__(output_path)
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.template_engine = TemplateEngine(self.template_dir)
    
    def generate(self, endpoint_name: str, endpoint_config: dict, domain: str = 'other'):
        """Generate a service class from backend config using templates"""
        print(f"🔧 Generating service: {endpoint_name} (domain: {domain})")
        
        # Check for named template first (allow for special routing entities)
        named_template = self.template_dir / "named" / "services" / f"{endpoint_name}.ts.template"
        if named_template.exists():
            print(f"📝 Using named template: {endpoint_name}.ts.template")
            self._generate_from_named_template(endpoint_name, endpoint_config, domain, named_template)
            return
        
        # Skip dynamic generation for endpoints with special routing (e.g., auth)
        if endpoint_config.get('special_routing', False):
            print(f"⏭️  Skipping dynamic service generation for {endpoint_name} (special routing)")
            return
        
        # Generate from template using template engine
        entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
        methods = endpoint_config.get('methods', [])
        
        # Generate methods string
        methods_str = self._generate_methods_string(methods, entity_name, endpoint_name)
        
        # Prepare template variables
        template_vars = {
            'entity_name': entity_name,
            'endpoint_name': endpoint_name,
            'domain': domain,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'camel_entity_name': NameStandardizer.to_camel_case(entity_name),
            'methods_str': methods_str
        }
        
        # Load and render template
        service_content = self.template_engine.render_template(
            'api/service.ts.template',
            template_vars,
            is_static=False
        )
        
        # Write service file organized by domain
        output_dir = self.output_path / "services" / domain
        camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
        output_file = output_dir / f"{camel_endpoint}Service.ts"
        
        self.write_file(output_file, service_content)
    
    def _generate_methods_string(self, methods: list, entity_name: str, endpoint_name: str) -> str:
        """Generate methods based on config"""
        method_implementations = []
        for method in methods:
            method_impl = self._generate_method_implementation(method, entity_name, endpoint_name)
            if method_impl:
                method_implementations.append(method_impl)
        
        return "\n\n".join(method_implementations)
    
    def _generate_method_implementation(self, method: str, entity_name: str, endpoint_name: str) -> str:
        """Generate individual method implementation"""
        camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
        
        # Get methods
        if method.startswith('get') and method.endswith('ById'):
            return f"""  async {method}(id: string): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/${{id}}`, {{
      method: 'GET',
      headers: this.getHeaders()
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method.startswith('list') or method.startswith('get') and not method.endswith('ById'):
            return f"""  async {method}(): Promise<{entity_name}[]> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}`, {{
      method: 'GET',
      headers: this.getHeaders()
    }});
    return this.handleResponse<{entity_name}[]>(response);
  }}"""
        
        elif method.startswith('create'):
            return f"""  async {method}(data: Partial<{entity_name}>): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method.startswith('update'):
            return f"""  async {method}(id: string, data: Partial<{entity_name}>): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/${{id}}`, {{
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method.startswith('delete'):
            return f"""  async {method}(id: string): Promise<void> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/${{id}}`, {{
      method: 'DELETE',
      headers: this.getHeaders()
    }});
    await this.handleResponse<void>(response);
  }}"""
        
        else:
            # Generic method
            return f"""  async {method}(...args: any[]): Promise<{entity_name}> {{
    // TODO: Implement {method} method
    throw new Error('Method {method} not implemented');
  }}"""
    
    def _generate_fallback(self, endpoint_name: str, endpoint_config: dict, domain: str):
        """Fallback to original hardcoded generation"""
        print(f"🔄 Using fallback generation for {endpoint_name}")
        # Import and use original generator logic
        # For now, just placeholder
        pass
    
    def _generate_from_named_template(self, endpoint_name: str, endpoint_config: dict, domain: str, template_path: Path):
        """Generate service from a named template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Write to the domain-specific services directory
            output_dir = self.output_path / "services" / domain
            camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
            output_file = output_dir / f"{camel_endpoint}Service.ts"
            
            self.write_file(output_file, template_content)
            
        except Exception as e:
            print(f"❌ Error generating from named template: {e}")