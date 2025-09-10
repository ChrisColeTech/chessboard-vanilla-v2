#!/usr/bin/env python3
"""
Hooks Generator Module
Handles generation of React hooks for all domains
"""

from typing import List
from base_generator import BaseFrontendGenerator

class HooksGenerator(BaseFrontendGenerator):
    """Generates React hooks for all domains"""
    
    def generate_domain_hooks(self, domain: str, endpoints: List[str]):
        """Generate individual React hook files for a domain using real backend endpoints"""
        src_path = self.get_src_path()
        hooks_path = src_path / "hooks" / domain
        
        # Get relevant endpoints for this domain
        domain_endpoints = []
        for endpoint_name in endpoints:
            if endpoint_name in self.backend_config['endpoints']:
                domain_endpoints.append(endpoint_name)
        
        if not domain_endpoints:
            return
            
        # Generate individual hook files for each main function
        generated_hooks = []
        
        # Create main domain hook file with real endpoints
        main_hook_name = f"use{self.capitalize_domain(domain)}"
        main_hook_content = self._generate_main_hook_content(domain, main_hook_name, domain_endpoints)
        
        main_hook_file = hooks_path / f"{main_hook_name}.ts"
        self.write_file(main_hook_file, main_hook_content)
        generated_hooks.append(main_hook_name)
        
        # Create query hooks file for GET operations
        query_hook_name = f"use{self.capitalize_domain(domain)}Queries"
        query_hook_content = self._generate_query_hook_content(domain, query_hook_name, domain_endpoints)
        
        query_hook_file = hooks_path / f"{query_hook_name}.ts"
        self.write_file(query_hook_file, query_hook_content)
        generated_hooks.append(query_hook_name)
        
        # Create mutations hook file for POST/PUT/DELETE operations
        mutations_hook_name = f"use{self.capitalize_domain(domain)}Mutations"
        mutations_hook_content = self._generate_mutations_hook_content(domain, mutations_hook_name, domain_endpoints)
        
        mutations_hook_file = hooks_path / f"{mutations_hook_name}.ts"
        self.write_file(mutations_hook_file, mutations_hook_content)
        generated_hooks.append(mutations_hook_name)
        
        # Generate index file that exports all hooks
        self._generate_hooks_index(hooks_path, domain, generated_hooks)
    
    def _generate_main_hook_content(self, domain: str, hook_name: str, domain_endpoints: List[str]) -> str:
        """Generate main domain hook content using real endpoints"""
        # Get all methods from the domain endpoints
        methods = []
        for endpoint_name in domain_endpoints:
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            for endpoint in endpoint_config.get('endpoints', []):
                method_name = endpoint['handler']
                methods.append(method_name)
        
        # Generate method calls for the client with simple, working signatures
        method_calls = []
        for method in methods[:3]:  # Limit to first 3 methods to keep it manageable
            method_calls.append(f"""
  const {method} = async (...args: any[]) => {{
    setLoading(true);
    setError(null);
    try {{
      // Call the client method with proper error handling
      const result = await (client.{method} as any)(...args);
      console.log('{method} result:', result);
      return result;
    }} catch (err: any) {{
      const errorMessage = err.message || '{method} failed';
      setError(errorMessage);
      console.error('{method} error:', err);
      throw err;
    }} finally {{
      setLoading(false);
    }}
  }};""")
        
        methods_export = ", ".join(methods[:3])
        
        return f"""import {{ useState }} from 'react';
import {{ {self.capitalize_domain(domain)}APIClient }} from '../../clients/{self.capitalize_domain(domain)}APIClient';

/**
 * {self.capitalize_domain(domain)} domain hook for {domain} operations
 * Uses real backend endpoints: {', '.join(domain_endpoints)}
 */
export const {hook_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new {self.capitalize_domain(domain)}APIClient();

  // Real API methods from backend config{''.join(method_calls)}
  
  return {{
    loading,
    error,
    clearError: () => setError(null),
    client,
    // Available methods
    {methods_export}
  }};
}};"""
    
    def _generate_query_hook_content(self, domain: str, hook_name: str, domain_endpoints: List[str]) -> str:
        """Generate query hooks content using real GET endpoints"""
        # Get GET methods from the domain endpoints
        get_methods = []
        for endpoint_name in domain_endpoints:
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            for endpoint in endpoint_config.get('endpoints', []):
                if endpoint['method'].upper() == 'GET':
                    get_methods.append(endpoint['handler'])
        
        # Pick the first GET method or fallback
        first_get_method = get_methods[0] if get_methods else "healthCheck"
        
        return f"""import {{ useState, useEffect }} from 'react';
import {{ {self.capitalize_domain(domain)}APIClient }} from '../../clients/{self.capitalize_domain(domain)}APIClient';

/**
 * Query hooks for {domain} GET operations
 * Available GET methods: {', '.join(get_methods) if get_methods else 'None'}
 */
export const {hook_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new {self.capitalize_domain(domain)}APIClient();

  // Real query operations using first available GET method
  const refetch = async (params?: any) => {{
    setLoading(true);
    setError(null);
    
    try {{
      console.log(`Fetching {domain} data using {first_get_method}`);
      // Call the GET method with type casting for flexibility
      const result = await (client.{first_get_method} as any)(params);
      setData(result);
      console.log('{domain} query result:', result);
    }} catch (err: any) {{
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
      console.error(`${hook_name} query error:`, err);
    }} finally {{
      setLoading(false);
    }}
  }};

  // Auto-fetch on mount
  useEffect(() => {{
    refetch();
  }}, []);
  
  return {{
    data,
    loading,
    error,
    refetch
  }};
}};"""
    
    def _generate_mutations_hook_content(self, domain: str, hook_name: str, domain_endpoints: List[str]) -> str:
        """Generate mutations hooks content using real POST/PUT/DELETE endpoints"""
        # Get mutation methods from the domain endpoints
        mutation_methods = []
        for endpoint_name in domain_endpoints:
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            for endpoint in endpoint_config.get('endpoints', []):
                if endpoint['method'].upper() in ['POST', 'PUT', 'DELETE']:
                    mutation_methods.append(endpoint['handler'])
        
        # Pick the first mutation method or fallback
        first_mutation_method = mutation_methods[0] if mutation_methods else None
        
        if not first_mutation_method:
            # No mutation methods available
            return f"""import {{ useState }} from 'react';

/**
 * Mutation hooks for {domain} POST/PUT/DELETE operations
 * No mutation methods available for this domain
 */
export const {hook_name} = () => {{
  const [loading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = async (_data: any) => {{
    setError('No mutation methods available for {domain} domain');
    return null;
  }};
  
  return {{
    loading,
    error,
    mutate
  }};
}};"""
        
        return f"""import {{ useState }} from 'react';
import {{ {self.capitalize_domain(domain)}APIClient }} from '../../clients/{self.capitalize_domain(domain)}APIClient';

/**
 * Mutation hooks for {domain} POST/PUT/DELETE operations
 * Available mutation methods: {', '.join(mutation_methods)}
 */
export const {hook_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new {self.capitalize_domain(domain)}APIClient();

  // Real mutation operations using first available mutation method
  const mutate = async (data: any, id?: string) => {{
    setLoading(true);
    setError(null);
    try {{
      console.log(`Mutating {domain} data using {first_mutation_method}:`, data);
      // Call mutation method with type casting for flexibility
      const result = await (client.{first_mutation_method} as any)(id || data, data);
      console.log('{domain} mutation result:', result);
      return result;
    }} catch (err: any) {{
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      console.error(`${hook_name} mutation error:`, err);
      throw err;
    }} finally {{
      setLoading(false);
    }}
  }};
  
  return {{
    loading,
    error,
    mutate
  }};
}};"""
    
    def _generate_hooks_index(self, hooks_path, domain: str, generated_hooks: List[str]):
        """Generate index file that exports all hooks for the domain"""
        index_content = f"""// {self.capitalize_domain(domain)} Domain Hooks
{chr(10).join([f'export {{ {hook} }} from \'./{hook}\';' for hook in generated_hooks])}
"""
        
        index_file = hooks_path / "index.ts"
        self.write_file(index_file, index_content)
    
    def generate_main_hooks_index(self):
        """Generate main hooks index file dynamically"""
        src_path = self.get_src_path()
        
        # Group endpoints by domain to get all domains
        from domain_mapping import DomainMapping
        domain_mapping_obj = DomainMapping()
        domains = domain_mapping_obj.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        # Generate exports for all domains
        exports = []
        for domain in domains.keys():
            exports.append(f"export * from './{domain}';")
        
        main_hooks_index = chr(10).join(exports) + chr(10)
        
        hooks_index_file = src_path / "hooks" / "index.ts"
        self.write_file(hooks_index_file, main_hooks_index)