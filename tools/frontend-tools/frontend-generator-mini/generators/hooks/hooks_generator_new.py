"""
Hooks Generator - Refactored to use template engine and name standardizer
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent.parent / "modules"))
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from template_engine import TemplateEngine
from name_standardizer import NameStandardizer
from generators.base_generator import BaseGenerator


class HooksGenerator(BaseGenerator):
    """Generates React hooks using template engine"""
    
    def __init__(self, output_path: Path):
        super().__init__(output_path)
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.template_engine = TemplateEngine(self.template_dir)
    
    def generate(self, endpoint_name: str, endpoint_config: dict, domain: str = 'other'):
        """Generate React hooks from backend config using templates"""
        print(f"🪝 Generating hooks: {endpoint_name} (domain: {domain})")
        
        # Check for named template first
        named_template = self.template_dir / "named" / "hooks" / f"{endpoint_name}.ts.template"
        if named_template.exists():
            print(f"📝 Using named template: {endpoint_name}.ts.template")
            self._generate_from_named_template(endpoint_name, endpoint_config, domain, named_template)
            return
        
        # Skip dynamic generation for endpoints with special routing (e.g., auth)
        if endpoint_config.get('special_routing', False):
            print(f"⏭️  Skipping dynamic hook generation for {endpoint_name} (special routing)")
            return
        
        # Generate from template using template engine
        entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
        methods = endpoint_config.get('methods', [])
        
        # Generate hook components
        imports_list = self._determine_imports(methods)
        state_str = self._generate_state_string(entity_name)
        error_handler = self._generate_error_handler()
        methods_str = self._generate_methods_string(methods, entity_name, endpoint_name)
        use_effect = self._generate_use_effect(methods, entity_name)
        return_items_str = self._generate_return_items(methods, entity_name)
        
        # Prepare template variables
        template_vars = {
            'entity_name': entity_name,
            'entity_name_lower': entity_name.lower(),
            'endpoint_name': endpoint_name,
            'camel_endpoint': NameStandardizer.to_camel_case(endpoint_name),
            'camel_entity_name': NameStandardizer.to_camel_case(entity_name),
            'domain': domain,
            'imports_str': ', '.join(imports_list),
            'state_str': state_str,
            'error_handler': error_handler,
            'hook_methods_str': methods_str,
            'hook_return_methods': return_items_str,
            'use_effect': use_effect
        }
        
        # Load and render template
        hook_content = self.template_engine.render_template(
            'api/hook.ts.template',
            template_vars,
            is_static=False
        )
        
        # Write hook file organized by domain
        output_dir = self.output_path / "hooks" / domain
        hook_name = f"use{entity_name}"
        output_file = output_dir / f"{hook_name}.ts"
        
        self.write_file(output_file, hook_content)
    
    def _determine_imports(self, methods: List[str]) -> List[str]:
        """Determine which React hooks to import based on methods"""
        imports = ['useState', 'useCallback']
        
        # Add useEffect if we have list methods that should auto-load
        if any(method.startswith('list') or method.startswith('get') and not method.endswith('ById') for method in methods):
            imports.append('useEffect')
        
        return imports
    
    def _generate_state_string(self, entity_name: str) -> str:
        """Generate state declarations"""
        entity_name_lower = entity_name.lower()
        return f"""  const [{entity_name_lower}s, set{entity_name}s] = useState<{entity_name}[]>([]);
  const [{entity_name_lower}, set{entity_name}] = useState<{entity_name} | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);"""
    
    def _generate_error_handler(self) -> str:
        """Generate error handler function"""
        return """  const handleError = useCallback((err: any) => {
    const errorMessage = err?.message || 'An unexpected error occurred';
    setError(errorMessage);
    setLoading(false);
    console.error('API Error:', err);
  }, []);"""
    
    def _generate_methods_string(self, methods: List[str], entity_name: str, endpoint_name: str) -> str:
        """Generate method implementations"""
        method_implementations = []
        for method in methods:
            method_impl = self._generate_method_function(method, entity_name, endpoint_name)
            if method_impl:
                method_implementations.append(method_impl)
        
        return "\n\n".join(method_implementations)
    
    def _generate_method_function(self, method: str, entity_name: str, endpoint_name: str) -> str:
        """Generate individual method function"""
        camel_endpoint = NameStandardizer.to_camel_case(endpoint_name)
        entity_name_lower = entity_name.lower()
        
        # Authentication methods (special handling)
        if method == 'login':
            return f"""  const login = useCallback(async (credentials: any) => {{
    try {{
      setLoading(true);
      setError(null);
      const response = await {camel_endpoint}Service.login(credentials);
      setLoading(false);
      return response;
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method == 'register':
            return f"""  const register = useCallback(async (userData: any) => {{
    try {{
      setLoading(true);
      setError(null);
      const response = await {camel_endpoint}Service.register(userData);
      setLoading(false);
      return response;
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method == 'getCurrentUser':
            return f"""  const getCurrentUser = useCallback(async () => {{
    try {{
      setLoading(true);
      setError(null);
      const user = await {camel_endpoint}Service.getCurrentUser();
      set{entity_name}(user);
      setLoading(false);
      return user;
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method == 'logout':
            return f"""  const logout = useCallback(async () => {{
    try {{
      setLoading(true);
      setError(null);
      await {camel_endpoint}Service.logout();
      set{entity_name}(null);
      setLoading(false);
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        # CRUD methods
        elif method.startswith('get') and method.endswith('ById'):
            return f"""  const {method} = useCallback(async (id: string) => {{
    try {{
      setLoading(true);
      setError(null);
      const {entity_name_lower} = await {camel_endpoint}Service.{method}(id);
      set{entity_name}({entity_name_lower});
      setLoading(false);
      return {entity_name_lower};
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method.startswith('list') or (method.startswith('get') and not method.endswith('ById')):
            return f"""  const {method} = useCallback(async () => {{
    try {{
      setLoading(true);
      setError(null);
      const {entity_name_lower}s = await {camel_endpoint}Service.{method}();
      set{entity_name}s({entity_name_lower}s);
      setLoading(false);
      return {entity_name_lower}s;
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method.startswith('create'):
            return f"""  const {method} = useCallback(async (data: any) => {{
    try {{
      setLoading(true);
      setError(null);
      const new{entity_name} = await {camel_endpoint}Service.{method}(data);
      
      // Update local state
      set{entity_name}s(prev => [...prev, new{entity_name}]);
      setLoading(false);
      return new{entity_name};
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method.startswith('update'):
            return f"""  const {method} = useCallback(async (id: string, data: any) => {{
    try {{
      setLoading(true);
      setError(null);
      const updated{entity_name} = await {camel_endpoint}Service.{method}(id, data);
      
      // Update local state
      set{entity_name}s(prev => prev.map(item => 
        item.id === id ? updated{entity_name} : item
      ));
      set{entity_name}(updated{entity_name});
      setLoading(false);
      return updated{entity_name};
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        elif method.startswith('delete'):
            return f"""  const {method} = useCallback(async (id: string) => {{
    try {{
      setLoading(true);
      setError(null);
      await {camel_endpoint}Service.{method}(id);
      
      // Update local state
      set{entity_name}s(prev => prev.filter(item => item.id !== id));
      if ({entity_name_lower}?.id === id) {{
        set{entity_name}(null);
      }}
      setLoading(false);
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
        
        else:
            # Generic method
            return f"""  const {method} = useCallback(async (...args: any[]) => {{
    try {{
      setLoading(true);
      setError(null);
      const result = await {camel_endpoint}Service.{method}(...args);
      setLoading(false);
      return result;
    }} catch (err) {{
      handleError(err);
      throw err;
    }}
  }}, [handleError]);"""
    
    def _generate_use_effect(self, methods: List[str], entity_name: str) -> str:
        """Generate useEffect for auto-loading data"""
        list_methods = [m for m in methods if m.startswith('list') or (m.startswith('get') and not m.endswith('ById'))]
        
        if not list_methods:
            return ""
        
        # Use the first list method for auto-loading
        method = list_methods[0]
        return f"""
  
  useEffect(() => {{
    {method}();
  }}, []);"""
    
    def _generate_return_items(self, methods: List[str], entity_name: str) -> str:
        """Generate return object items"""
        entity_name_lower = entity_name.lower()
        items = [
            f"{entity_name_lower}s",
            f"{entity_name_lower}",
            "loading",
            "error"
        ]
        
        # Add all methods
        items.extend(methods)
        
        return ",\n    ".join(items)
    
    def _generate_fallback(self, endpoint_name: str, endpoint_config: dict, domain: str):
        """Fallback to original hardcoded generation"""
        print(f"🔄 Using fallback generation for {endpoint_name}")
        # Could implement fallback logic here if needed
        pass
    
    def _generate_from_named_template(self, endpoint_name: str, endpoint_config: dict, domain: str, template_path: Path):
        """Generate hook from a named template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Write to the domain-specific hooks directory
            output_dir = self.output_path / "hooks" / domain
            entity_name = endpoint_config.get('entity', endpoint_name.capitalize())
            hook_name = f"use{entity_name}"
            output_file = output_dir / f"{hook_name}.ts"
            
            self.write_file(output_file, template_content)
            
        except Exception as e:
            print(f"❌ Error generating from named template: {e}")