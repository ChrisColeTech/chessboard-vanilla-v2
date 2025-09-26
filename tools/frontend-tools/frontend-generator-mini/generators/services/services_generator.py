"""
Services Generator
"""

from pathlib import Path
from generators.base_generator import BaseGenerator

class ServicesGenerator(BaseGenerator):
    """Generates service classes"""
    
    def __init__(self, output_path: Path):
        super().__init__(output_path)
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.config_dir = Path(__file__).parent.parent.parent / "config" / "services"
    
    def generate(self, endpoint_name: str, endpoint_config: dict, domain: str = 'other'):
        """Generate a service class from backend config"""
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
        
        # Generate from config using configuration-driven approach
            entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
            methods = endpoint_config.get('methods', [])
            
            # Generate service class
            service_content = self._generate_service(entity_name, endpoint_name, methods, domain)
            
            # Write service file organized by domain
            output_dir = self.output_path / "services" / domain
            camel_endpoint = self._snake_to_camel(endpoint_name)
            output_file = output_dir / f"{camel_endpoint}Service.ts"
            
            self.write_file(output_file, service_content)
    
    def _generate_service(self, entity_name: str, endpoint_name: str, methods: list, domain: str = 'other') -> str:
        """Generate service class content from template"""
        # Try to read from template file
        template_path = self.template_dir / "entityService.ts.template"
        
        if template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                # Apply template substitutions
                content = template_content
                content = content.replace('{entity_name}', entity_name)
                content = content.replace('{entity_name_lower}', entity_name.lower())
                content = content.replace('{endpoint_name}', endpoint_name)
                content = content.replace('{domain}', domain)
                
                return content
            except Exception as e:
                print(f"⚠️ Error reading service template: {e}, falling back to hardcoded")
        
        # Generate methods based on config
        method_implementations = []
        for method in methods:
            method_impl = self._generate_method_implementation(method, entity_name, endpoint_name)
            if method_impl:
                method_implementations.append(method_impl)
        
        methods_str = "\n\n".join(method_implementations)
        
        # Fallback to configuration-driven template
        camel_endpoint = self._snake_to_camel(endpoint_name)
        return f"""// Generated service for {entity_name}
import type {{ {entity_name} }} from '../../types/{domain}/{camel_endpoint}';

export interface ApiResponse<T> {{
  data: T;
  message?: string;
  success: boolean;
}}

class {entity_name}Service {{
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {{
    this.baseUrl = baseUrl;
  }}

  private async handleResponse<T>(response: Response): Promise<T> {{
    if (!response.ok) {{
      const error = await response.text();
      throw new Error(`HTTP ${{response.status}}: ${{error}}`);
    }}
    return response.json();
  }}

  private getHeaders(): Record<string, string> {{
    const token = localStorage.getItem('authToken');
    return {{
      'Content-Type': 'application/json',
      ...(token && {{ Authorization: `Bearer ${{token}}` }})
    }};
  }}

{methods_str}
}}

export const {endpoint_name}Service = new {entity_name}Service();
export default {endpoint_name}Service;"""
    
    def _generate_from_named_template(self, endpoint_name: str, endpoint_config: dict, domain: str, template_path: Path):
        """Generate service from a named template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Write to the domain-specific services directory
            output_dir = self.output_path / "services" / domain
            camel_endpoint = self._snake_to_camel(endpoint_name)
            output_file = output_dir / f"{camel_endpoint}Service.ts"
            
            self.write_file(output_file, template_content)
            
        except Exception as e:
            print(f"❌ Error generating from named template {template_path}: {e}")

    def _generate_method_implementation(self, method: str, entity_name: str, endpoint_name: str) -> str:
        """Generate individual method implementation based on method name"""
        
        # Standard CRUD operations
        if method == f'get{entity_name}ById':
            return f"""  async {method}(id: string): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/${{id}}`, {{
      method: 'GET',
      headers: this.getHeaders(),
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method == f'list{entity_name}s':
            return f"""  async {method}(): Promise<{entity_name}[]> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}`, {{
      method: 'GET',
      headers: this.getHeaders(),
    }});
    return this.handleResponse<{entity_name}[]>(response);
  }}"""
        
        elif method == f'create{entity_name}':
            return f"""  async {method}(data: Partial<{entity_name}>): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method == f'update{entity_name}':
            return f"""  async {method}(id: string, data: Partial<{entity_name}>): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/${{id}}`, {{
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method == f'delete{entity_name}':
            return f"""  async {method}(id: string): Promise<void> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/${{id}}`, {{
      method: 'DELETE',
      headers: this.getHeaders(),
    }});
    await this.handleResponse<void>(response);
  }}"""
        
        # Authentication methods
        elif method == 'login':
            return f"""  async {method}(credentials: any): Promise<any> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/login`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(credentials),
    }});
    return this.handleResponse<any>(response);
  }}"""
        
        elif method == 'register':
            return f"""  async {method}(userData: any): Promise<any> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/register`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(userData),
    }});
    return this.handleResponse<any>(response);
  }}"""
        
        elif method == 'getCurrentUser':
            return f"""  async {method}(): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/current`, {{
      method: 'GET',
      headers: this.getHeaders(),
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        elif method == 'logout':
            return f"""  async {method}(): Promise<void> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/logout`, {{
      method: 'POST',
      headers: this.getHeaders(),
    }});
    await this.handleResponse<void>(response);
  }}"""
        
        # Generic methods - create intelligent defaults based on method name patterns
        else:
            return self._generate_generic_method(method, entity_name, endpoint_name)

    def _generate_generic_method(self, method: str, entity_name: str, endpoint_name: str) -> str:
        """Generate generic method implementation based on naming patterns"""
        entity_lower = entity_name.lower()
        
        # Methods that return arrays
        if (method.startswith('get') and 'By' in method) or method.startswith('list') or method.startswith('search'):
            if method.endswith('s') or 'list' in method.lower() or 'search' in method.lower():
                # Returns array
                return f"""  async {method}(...args: any[]): Promise<{entity_name}[]> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/{method.lower()}`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(args),
    }});
    return this.handleResponse<{entity_name}[]>(response);
  }}"""
            else:
                # Returns single item
                return f"""  async {method}(...args: any[]): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/{method.lower()}`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(args),
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""
        
        # Action methods that don't return data
        elif any(action in method.lower() for action in ['complete', 'activate', 'cleanup', 'expire', 'cancel']):
            return f"""  async {method}(...args: any[]): Promise<void> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/{method.lower()}`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(args),
    }});
    await this.handleResponse<void>(response);
  }}"""
        
        # Default: return single entity
        else:
            return f"""  async {method}(...args: any[]): Promise<{entity_name}> {{
    const response = await fetch(`${{this.baseUrl}}/{endpoint_name}/{method.lower()}`, {{
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(args),
    }});
    return this.handleResponse<{entity_name}>(response);
  }}"""

    def generate_template_services(self):
        """Services generator should not handle static templates - this is handled by the main generator"""
        # Static template processing is handled by FrontendGenerator._generate_static_files()
        # Services generator only handles named templates + dynamic generation
        pass
    
    def _snake_to_camel(self, snake_str: str) -> str:
        """Convert snake_case to camelCase"""
        components = snake_str.split('_')
        return components[0] + ''.join(word.capitalize() for word in components[1:])