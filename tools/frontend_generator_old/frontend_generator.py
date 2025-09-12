#!/usr/bin/env python3
"""
Frontend Pattern Generator
Generates TypeScript frontend files (types, API services, hooks, components) based on backend API contract
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class FrontendGenerator:
    def __init__(self, frontend_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2"):
        self.frontend_path = Path(frontend_path)
        self.backend_config = {}
        self.templates = {}
        
    def load_backend_config(self, config_path: str = "backend_config.json"):
        """Load backend configuration to understand API contract"""
        with open(config_path, 'r') as f:
            self.backend_config = json.load(f)
        print(f"📖 Loaded backend config with {len(self.backend_config['endpoints'])} endpoints")
    
    def analyze_backend_models(self):
        """Analyze backend models to extract TypeScript types"""
        backend_models_path = Path("../backend/src/models")
        model_files = list(backend_models_path.glob("*.ts"))
        
        print(f"🔍 Found {len(model_files)} backend model files")
        
        types_content = []
        for model_file in model_files:
            content = model_file.read_text()
            # Extract interface definitions
            types_content.append(f"// Generated from {model_file.name}")
            types_content.append(content)
            types_content.append("")
        
        return "\n".join(types_content)
    
    def generate_api_response_type(self):
        """Generate standard API response wrapper type"""
        return '''// Standard API response wrapper
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Pagination wrapper
export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Auth token type
export interface AuthToken {
  token: string;
  expiresAt: string;
}
'''
    
    def generate_types_file(self):
        """Generate comprehensive TypeScript types file"""
        print("📝 Generating TypeScript types...")
        
        # Create src directory structure
        src_path = self.frontend_path / "src"
        types_path = src_path / "types"
        types_path.mkdir(parents=True, exist_ok=True)
        
        # Generate types from backend models
        backend_types = self.analyze_backend_models()
        api_types = self.generate_api_response_type()
        
        # Additional frontend-specific types
        frontend_types = '''
// Frontend-specific types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface UseQueryResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseMutationResult<T, V = any> {
  mutate: (variables: V) => Promise<T>;
  loading: boolean;
  error: string | null;
}

// Puzzle query parameters
export interface PuzzleQueryParams {
  minRating?: number;
  maxRating?: number;
  themes?: string[];
  limit?: number;
  offset?: number;
}

// Search parameters
export interface SearchParams {
  q?: string;
  limit?: number;
  offset?: number;
}
'''
        
        # Combine all types
        content = f"""// Auto-generated TypeScript types
// Generated from backend API contract

{api_types}

{backend_types}

{frontend_types}
"""
        
        # Write types file
        types_file = types_path / "index.ts"
        types_file.write_text(content)
        
        print(f"✅ Generated {types_file}")
    
    def generate_api_client_service(self, endpoint_name: str, endpoint_config: Dict[str, Any]):
        """Generate API client service for a specific endpoint"""
        entity = endpoint_config['entity']
        endpoints = endpoint_config.get('endpoints', [])
        
        # Determine base URL path
        if endpoint_name == 'auth':
            base_path = '/auth'
        elif endpoint_name == 'users':
            base_path = '/api/users'
        else:
            base_path = f'/api/{endpoint_config.get("entities", endpoint_name)}'
        
        # Generate service class
        service_methods = []
        
        for endpoint in endpoints:
            method = endpoint['method'].lower()
            path = endpoint['path']
            handler = endpoint['handler']
            auth_required = endpoint.get('auth_required', True)
            
            # Generate method based on handler name and HTTP method
            service_method = self._generate_service_method(
                method, path, handler, entity, auth_required, base_path
            )
            service_methods.append(service_method)
        
        # Generate service class template
        service_class = f"""import {{ ApiResponse, {entity}Response, Create{entity}Request, Update{entity}Request, PuzzleQueryParams, SearchParams }} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001';

class {entity}ApiService {{
  private baseUrl = API_BASE_URL + '{base_path}';
  
  private async request<T>(
    endpoint: string,
    options: RequestInit = {{}}
  ): Promise<ApiResponse<T>> {{
    const url = endpoint.startsWith('http') ? endpoint : `${{this.baseUrl}}${{endpoint}}`;
    
    const defaultHeaders: HeadersInit = {{
      'Content-Type': 'application/json',
    }};
    
    // Add auth header if token exists
    const token = localStorage.getItem('auth_token');
    if (token) {{
      defaultHeaders.Authorization = `Bearer ${{token}}`;
    }}
    
    const config: RequestInit = {{
      ...options,
      headers: {{
        ...defaultHeaders,
        ...options.headers,
      }},
    }};
    
    try {{
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {{
        throw new Error(data.error || `HTTP error! status: ${{response.status}}`);
      }}
      
      return data;
    }} catch (error) {{
      console.error(`API request failed:`, error);
      throw error;
    }}
  }}

{chr(10).join(service_methods)}
}}

export const {entity.lower()}ApiService = new {entity}ApiService();
export default {entity.lower()}ApiService;
"""
        
        return service_class
    
    def _generate_service_method(self, method: str, path: str, handler: str, entity: str, auth_required: bool, base_path: str) -> str:
        """Generate individual service method"""
        
        # Clean up handler name for method name
        method_name = handler
        if method_name.startswith('get'):
            method_name = method_name[3:]  # Remove 'get' prefix
        elif method_name.startswith('create'):
            method_name = method_name[6:]  # Remove 'create' prefix
        elif method_name.startswith('update'):
            method_name = method_name[6:]  # Remove 'update' prefix
        elif method_name.startswith('delete'):
            method_name = method_name[6:]  # Remove 'delete' prefix
        
        method_name = method_name[0].lower() + method_name[1:] if method_name else handler
        
        # Generate method based on HTTP method and path pattern
        if method == 'get' and '/:id' in path:
            return f"""  async {method_name}(id: string): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>(`/${{id}}`);
  }}"""
        
        elif method == 'get' and path == '/':
            return f"""  async {method_name}(params?: PuzzleQueryParams): Promise<ApiResponse<{entity}Response[]>> {{
    const queryString = params ? '?' + new URLSearchParams(params as any).toString() : '';
    return this.request<{entity}Response[]>(`/${{queryString}}`);
  }}"""
        
        elif method == 'get' and '/random' in path:
            return f"""  async {method_name}(params?: PuzzleQueryParams): Promise<ApiResponse<{entity}Response>> {{
    const queryString = params ? '?' + new URLSearchParams(params as any).toString() : '';
    return this.request<{entity}Response>(`/random${{queryString}}`);
  }}"""
        
        elif method == 'get' and '/themes' in path:
            return f"""  async {method_name}(): Promise<ApiResponse<string[]>> {{
    return this.request<string[]>('/themes');
  }}"""
        
        elif method == 'get' and '/stats' in path:
            return f"""  async {method_name}(): Promise<ApiResponse<any>> {{
    return this.request<any>('/stats');
  }}"""
        
        elif method == 'get' and '/search' in path:
            return f"""  async {method_name}(params: SearchParams): Promise<ApiResponse<{entity}Response[]>> {{
    const queryString = '?' + new URLSearchParams(params as any).toString();
    return this.request<{entity}Response[]>(`/search${{queryString}}`);
  }}"""
        
        elif method == 'post' and '/:id/' in path:
            return f"""  async {method_name}(id: string, data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`/${{id}}{path.replace('/:id', '')}`, {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'post' and path == '/':
            return f"""  async {method_name}(data: Create{entity}Request): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>('/', {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'post':
            return f"""  async {method_name}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>('{path}', {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'put' and '/:id' in path:
            return f"""  async {method_name}(id: string, data: Update{entity}Request): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>(`/${{id}}`, {{
      method: 'PUT',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'put':
            return f"""  async {method_name}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>('{path}', {{
      method: 'PUT',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'delete':
            return f"""  async {method_name}(id: string): Promise<ApiResponse<void>> {{
    return this.request<void>(`/${{id}}`, {{
      method: 'DELETE',
    }});
  }}"""
        
        else:
            # Default method
            return f"""  async {method_name}(...args: any[]): Promise<ApiResponse<any>> {{
    // TODO: Implement {handler}
    throw new Error('{handler} not implemented');
  }}"""
    
    def generate_react_hook(self, endpoint_name: str, endpoint_config: Dict[str, Any]):
        """Generate React hooks for API service"""
        entity = endpoint_config['entity']
        endpoints = endpoint_config.get('endpoints', [])
        
        # Generate hook for each endpoint
        hook_methods = []
        
        # Generate useQuery-style hooks for GET endpoints
        get_hooks = []
        mutation_hooks = []
        
        for endpoint in endpoints:
            method = endpoint['method'].lower()
            handler = endpoint['handler']
            
            if method == 'get':
                get_hooks.append(self._generate_query_hook(handler, entity, endpoint))
            else:
                mutation_hooks.append(self._generate_mutation_hook(handler, entity, endpoint))
        
        # Generate main hook file
        hook_content = f"""import {{ useState, useEffect, useCallback }} from 'react';
import {{ UseQueryResult, UseMutationResult }} from '../types';
import {entity.lower()}ApiService from '../services/{entity}ApiService';

// Query hooks for GET requests
{chr(10).join(get_hooks)}

// Mutation hooks for POST/PUT/DELETE requests  
{chr(10).join(mutation_hooks)}

// Main hook that combines all operations
export const use{entity} = () => {{
  return {{
    // Add hook methods here
    service: {entity.lower()}ApiService,
  }};
}};

export default use{entity};
"""
        
        return hook_content
    
    def _generate_query_hook(self, handler: str, entity: str, endpoint: Dict) -> str:
        """Generate useQuery-style hook for GET requests"""
        hook_name = f"use{handler.capitalize()}"
        
        return f"""export const {hook_name} = (params?: any): UseQueryResult<any> => {{
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const fetchData = useCallback(async () => {{
    setLoading(true);
    setError(null);
    
    try {{
      const response = await {entity.lower()}ApiService.{handler}(params);
      setData(response.data);
    }} catch (err: any) {{
      setError(err.message || 'An error occurred');
    }} finally {{
      setLoading(false);
    }}
  }}, [params]);
  
  useEffect(() => {{
    fetchData();
  }}, [fetchData]);
  
  return {{
    data,
    loading,
    error,
    refetch: fetchData,
  }};
}};"""
    
    def _generate_mutation_hook(self, handler: str, entity: str, endpoint: Dict) -> str:
        """Generate useMutation-style hook for POST/PUT/DELETE requests"""
        hook_name = f"use{handler.capitalize()}"
        
        return f"""export const {hook_name} = (): UseMutationResult<any> => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const mutate = useCallback(async (variables: any) => {{
    setLoading(true);
    setError(null);
    
    try {{
      const response = await {entity.lower()}ApiService.{handler}(variables);
      return response.data;
    }} catch (err: any) {{
      setError(err.message || 'An error occurred');
      throw err;
    }} finally {{
      setLoading(false);
    }}
  }}, []);
  
  return {{
    mutate,
    loading,
    error,
  }};
}};"""
    
    def generate_placeholder_component(self, endpoint_name: str, endpoint_config: Dict[str, Any]):
        """Generate placeholder React component for testing"""
        entity = endpoint_config['entity']
        
        component_content = f"""import React from 'react';
import use{entity} from '../hooks/use{entity}';

interface {entity}ComponentProps {{
  // Add props as needed
}}

const {entity}Component: React.FC<{entity}ComponentProps> = () => {{
  const {{ service }} = use{entity}();
  
  return (
    <div className="{entity.lower()}-component">
      <h2>{entity} Component</h2>
      <p>This is a placeholder component for {entity} operations.</p>
      
      <div>
        <button onClick={{() => console.log('TODO: Implement {entity} operations')}}>
          Test {entity} Service
        </button>
      </div>
    </div>
  );
}};

export default {entity}Component;
"""
        
        return component_content
    
    def generate_all_frontend_files(self):
        """Generate all frontend files for all endpoints"""
        print("🚀 Frontend Generator Starting...")
        
        # Load backend configuration
        self.load_backend_config()
        
        # Generate types
        self.generate_types_file()
        
        # Create directory structure
        src_path = self.frontend_path / "src"
        services_path = src_path / "services"
        hooks_path = src_path / "hooks"
        components_path = src_path / "components"
        
        services_path.mkdir(parents=True, exist_ok=True)
        hooks_path.mkdir(parents=True, exist_ok=True)
        components_path.mkdir(parents=True, exist_ok=True)
        
        # Generate files for each endpoint
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            entity = endpoint_config['entity']
            
            print(f"🔧 Generating {entity} frontend files...")
            
            # Generate API service
            service_content = self.generate_api_client_service(endpoint_name, endpoint_config)
            service_file = services_path / f"{entity}ApiService.ts"
            service_file.write_text(service_content)
            print(f"📝 Generated {service_file}")
            
            # Generate React hooks
            hook_content = self.generate_react_hook(endpoint_name, endpoint_config)
            hook_file = hooks_path / f"use{entity}.ts"
            hook_file.write_text(hook_content)
            print(f"📝 Generated {hook_file}")
            
            # Generate placeholder component
            component_content = self.generate_placeholder_component(endpoint_name, endpoint_config)
            component_file = components_path / f"{entity}Component.tsx"
            component_file.write_text(component_content)
            print(f"📝 Generated {component_file}")
        
        # Generate index files for easier imports
        self._generate_index_files()
        
        print("✅ Frontend generation complete!")
    
    def _generate_index_files(self):
        """Generate index files for easier imports"""
        src_path = self.frontend_path / "src"
        
        # Services index
        services_path = src_path / "services"
        services_index = []
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            entity = endpoint_config['entity']
            services_index.append(f"export {{ default as {entity.lower()}ApiService }} from './{entity}ApiService';")
        
        services_index_file = services_path / "index.ts"
        services_index_file.write_text("\n".join(services_index))
        
        # Hooks index
        hooks_path = src_path / "hooks"
        hooks_index = []
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            entity = endpoint_config['entity']
            hooks_index.append(f"export {{ default as use{entity} }} from './use{entity}';")
        
        hooks_index_file = hooks_path / "index.ts"
        hooks_index_file.write_text("\n".join(hooks_index))
        
        # Components index
        components_path = src_path / "components"
        components_index = []
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            entity = endpoint_config['entity']
            components_index.append(f"export {{ default as {entity}Component }} from './{entity}Component';")
        
        components_index_file = components_path / "index.ts"
        components_index_file.write_text("\n".join(components_index))
        
        print("📝 Generated index files for easier imports")

def main():
    """Main function to run the generator"""
    generator = FrontendGenerator()
    generator.generate_all_frontend_files()

if __name__ == "__main__":
    main()