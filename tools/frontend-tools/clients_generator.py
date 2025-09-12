#!/usr/bin/env python3
"""
Clients Generator Module
Handles generation of API clients for all domains
"""

from typing import List, Dict, Any
from base_generator import BaseFrontendGenerator
from domain_mapping import DomainMapping

class ClientsGenerator(BaseFrontendGenerator):
    """Generates API clients for all domains"""
    
    def __init__(self, frontend_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2"):
        super().__init__(frontend_path)
        self.domain_mapping_obj = DomainMapping()
    
    def generate_domain_clients(self):
        """Generate domain-specific API clients following architecture guide"""
        src_path = self.get_src_path()
        clients_path = src_path / "clients"
        
        # Group endpoints by domain
        domains = self.domain_mapping_obj.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        # Generate base HTTP client first
        self._generate_base_client(clients_path)
        
        # Generate domain-specific clients
        for domain, endpoints in domains.items():
            self._generate_domain_client(domain, endpoints)
        
        # Generate main client index that exports all domain clients
        self._generate_client_index(clients_path)
    
    def _generate_base_client(self, clients_path):
        """Generate base HTTP client"""
        base_client_content = """import type { ApiResponse } from '../types/common';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001';

export class BaseAPIClient {
  protected async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    
    const defaultHeaders: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    // Add auth header if token exists
    const token = localStorage.getItem('auth_token');
    if (token) {
      defaultHeaders.Authorization = `Bearer ${token}`;
    }
    
    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };
    
    try {
      const response = await fetch(url, config);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }
      
      return data;
    } catch (error) {
      console.error(`API request failed:`, error);
      throw error;
    }
  }
}

export default BaseAPIClient;
"""
        
        base_client_file = clients_path / "BaseAPIClient.ts"
        self.write_file(base_client_file, base_client_content)
    
    def _generate_domain_client(self, domain: str, endpoints: List[str]):
        """Generate a domain-specific API client"""
        src_path = self.get_src_path()
        clients_path = src_path / "clients"
        
        # Get relevant endpoints for this domain
        domain_methods = []
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = self.get_entity_name(endpoint_name)
            api_endpoints = endpoint_config.get('endpoints', [])
            
            # Determine base path
            base_path = self.get_api_base_path(endpoint_name, endpoint_config)
            
            if entity:
                for api_endpoint in api_endpoints:
                    method = api_endpoint['method'].lower()
                    path = api_endpoint['path']
                    handler = api_endpoint['handler']
                    
                    client_method = self._generate_client_method(
                        method, path, handler, entity, base_path
                    )
                    domain_methods.append(client_method)
        
        if not domain_methods:
            return
            
        # Generate domain-specific import statement - only import what we actually use
        type_imports = []  # We'll build this based on actual usage
        
        client_content = f"""import type {{ ApiResponse }} from '../types/common';
import {{ BaseAPIClient }} from './BaseAPIClient';

/**
 * {self.capitalize_domain(domain)} Domain API Client
 * Handles all {domain}-related API operations
 */
export class {self.capitalize_domain(domain)}APIClient extends BaseAPIClient {{
{chr(10).join(domain_methods)}
}}

export default {self.capitalize_domain(domain)}APIClient;
"""
        
        # Write domain client file
        client_file = clients_path / f"{self.capitalize_domain(domain)}APIClient.ts"
        self.write_file(client_file, client_content)
    
    def _generate_client_method(self, method: str, path: str, handler: str, entity: str, base_path: str) -> str:
        """Generate individual client method using generic types"""
        
        if method == 'get' and '/:id' in path:
            return f"""  async {handler}(id: string): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}/${{id}}`);
  }}"""
        
        elif method == 'get' and path == '/':
            return f"""  async {handler}(params?: any): Promise<ApiResponse<any[]>> {{
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`{base_path}${{queryString}}`);
  }}"""
        
        elif method == 'get':
            clean_path = path.replace('/:id', '')
            return f"""  async {handler}(params?: any): Promise<ApiResponse<any>> {{
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`{base_path}{clean_path}${{queryString}}`);
  }}"""
        
        elif method == 'post' and '/:id/' in path:
            clean_path = path.replace('/:id', '')
            return f"""  async {handler}(id: string, data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}/${{id}}{clean_path}`, {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'post':
            return f"""  async {handler}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}{path}`, {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'put':
            if '/:id' in path:
                return f"""  async {handler}(id: string, data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}/${{id}}`, {{
      method: 'PUT',
      body: JSON.stringify(data),
    }});
  }}"""
            else:
                return f"""  async {handler}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}{path}`, {{
      method: 'PUT',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'delete':
            return f"""  async {handler}(id: string): Promise<ApiResponse<void>> {{
    return this.request<void>(`{base_path}/${{id}}`, {{
      method: 'DELETE',
    }});
  }}"""
        
        else:
            return f"""  async {handler}(...args: any[]): Promise<ApiResponse<any>> {{
    throw new Error('{handler} not implemented');
  }}"""
    
    def _generate_client_index(self, clients_path):
        """Generate main client index that exports all domain clients dynamically"""
        # Group endpoints by domain to get all domains
        domains = self.domain_mapping_obj.group_endpoints_by_domain(self.backend_config['endpoints'])
        
        # Generate exports for all domain clients
        exports = ["export { BaseAPIClient } from './BaseAPIClient';"]
        imports = []
        client_properties = []
        
        for domain in domains.keys():
            client_class_name = f"{self.capitalize_domain(domain)}APIClient"
            exports.append(f"export {{ {client_class_name} }} from './{client_class_name}';")
            imports.append(f"import {{ {client_class_name} }} from './{client_class_name}';")
            client_properties.append(f"  public readonly {self.camel_case_domain(domain)} = new {client_class_name}();")
        
        client_index_content = f"""// Domain-specific API clients
{chr(10).join(exports)}

// Unified client for convenience (optional)
{chr(10).join(imports)}

export class APIClient {{
{chr(10).join(client_properties)}
}}

// Singleton instance for convenience
export const apiClient = new APIClient();
export default apiClient;
"""
        
        client_index_file = clients_path / "index.ts"
        self.write_file(client_index_file, client_index_content)