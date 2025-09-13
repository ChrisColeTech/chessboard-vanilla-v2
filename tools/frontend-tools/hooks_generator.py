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
    
    def generate_core_hooks(self):
        """Generate core hooks like usePageData"""
        src_path = self.get_src_path()
        core_hooks_path = src_path / "hooks" / "core"
        core_hooks_path.mkdir(parents=True, exist_ok=True)
        
        # Generate usePageData hook
        use_page_data_content = '''import { useState, useEffect } from "react";

export interface UsePageDataResult {
  data: any[];
  loading: boolean;
  error: string | null;
}

export const usePageData = (endpoint: string): UsePageDataResult => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // For testing, generate mock data based on endpoint name
        const mockData = generateMockData(endpoint);
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        setData(mockData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch data");
        setData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, loading, error };
};

// Helper function to generate mock data for testing
function generateMockData(endpoint: string): any[] {
  const baseData = {
    id: Math.floor(Math.random() * 1000),
    name: `${endpoint} Item`,
    status: Math.random() > 0.5 ? "active" : "inactive",
    createdAt: new Date().toISOString(),
    endpoint: endpoint,
  };

  // Generate 5-15 mock items
  const count = Math.floor(Math.random() * 10) + 5;
  return Array.from({ length: count }, (_, index) => ({
    ...baseData,
    id: baseData.id + index,
    name: `${endpoint} Item ${index + 1}`,
    sortOrder: index,
  }));
}'''
        
        use_page_data_file = core_hooks_path / "usePageData.ts"
        self.write_file(use_page_data_file, use_page_data_content)
        
        # Generate comprehensive useAuth hook that matches production
        use_auth_content = '''// React hooks for authentication functionality
import { useCallback, useEffect } from 'react';
import { useShallow } from 'zustand/react/shallow';
import type {
  UseAuthReturn,
  UseLoginReturn,
  LoginRequest
} from '../../types/auth';

import { useAuthStore } from '../../stores/authStore';

/**
 * Main authentication hook
 * Provides access to auth state and all auth actions
 */
export const useAuth = (): UseAuthReturn => {
  const store = useAuthStore(
    useShallow((state) => ({
      // State
      user: state.user,
      token: state.token,
      isLoading: state.isLoading,
      isAuthenticated: state.isAuthenticated,
      error: state.error,
      progress: state.progress,
      
      // Actions
      login: state.login,
      register: state.register,
      logout: state.logout,
      forgotPassword: state.forgotPassword,
      resetPassword: state.resetPassword,
      changePassword: state.changePassword,
      updateProfile: state.updateProfile,
      verifyToken: state.verifyToken,
      refreshUser: state.refreshUser,
      clearError: state.clearError,
      initialize: state.initialize
    }))
  );

  // Initialize auth state on mount
  useEffect(() => {
    store.initialize();
  }, []);

  return store;
};

/**
 * Authentication status hook
 * Provides only authentication status without actions
 */
export const useAuthStatus = () => {
  return useAuthStore(
    useShallow((state) => ({
      isAuthenticated: state.isAuthenticated,
      user: state.user,
      isLoading: state.isLoading
    }))
  );
};

// Export all other hooks from production useAuth.ts
export const useLogin = (): UseLoginReturn => {
  const { login, isLoading, error, clearError } = useAuthStore(
    useShallow((state) => ({
      login: state.login,
      isLoading: state.isLoading,
      error: state.error,
      clearError: state.clearError
    }))
  );

  const handleLogin = useCallback(async (credentials: LoginRequest) => {
    await login(credentials);
  }, [login]);

  return {
    login: handleLogin,
    isLoading,
    error,
    clearError
  };
};
'''
        
        # Generate useAuth.ts directly in hooks/ directory, not in hooks/core/
        hooks_path = src_path / "hooks"
        use_auth_file = hooks_path / "useAuth.ts"
        self.write_file(use_auth_file, use_auth_content)

        # Generate core hooks index (useAuth is now standalone, not in core)
        core_index_content = '''export { usePageData, type UsePageDataResult } from "./usePageData";
'''
        core_index_file = core_hooks_path / "index.ts"
        self.write_file(core_index_file, core_index_content)
        
        print("  📝 Generated core hooks (usePageData) and standalone useAuth")

    def generate_standalone_hooks(self):
        """Generate standalone utility hooks"""
        src_path = self.get_src_path()
        hooks_path = src_path / "hooks"
        
        # Generate useActionSheet hook
        use_action_sheet_content = '''import { useState } from "react";

export const useActionSheet = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSheet = () => setIsOpen(!isOpen);
  const closeSheet = () => setIsOpen(false);
  const openSheet = () => setIsOpen(true);

  return {
    isOpen,
    toggleSheet,
    closeSheet,
    openSheet,
  };
};'''
        
        use_action_sheet_file = hooks_path / "useActionSheet.ts"
        self.write_file(use_action_sheet_file, use_action_sheet_content)
        
        # Generate useInstructions hook
        use_instructions_content = '''import { useState } from "react";

export const useInstructions = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [instructions, setInstructions] = useState<string[]>([]);

  const showInstructions = (instructionTitle: string, instructionList: string[]) => {
    setTitle(instructionTitle);
    setInstructions(instructionList);
    setIsOpen(true);
  };

  const openInstructions = () => setIsOpen(true);
  const closeInstructions = () => setIsOpen(false);

  return {
    isOpen,
    title,
    instructions,
    showInstructions,
    openInstructions,
    closeInstructions,
    setInstructions: (instructionTitle: string, instructionList: string[]) => {
      setTitle(instructionTitle);
      setInstructions(instructionList);
    },
    clearInstructions: () => {
      setTitle("");
      setInstructions([]);
    },
  };
};'''
        
        use_instructions_file = hooks_path / "useInstructions.ts"
        self.write_file(use_instructions_file, use_instructions_content)

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
        
        # Add core hooks export
        exports.append("export * from './core';")
        
        # Add standalone hooks exports
        exports.append("export { useActionSheet } from './useActionSheet';")
        exports.append("export { useInstructions } from './useInstructions';")
        
        main_hooks_index = chr(10).join(exports) + chr(10)
        
        hooks_index_file = src_path / "hooks" / "index.ts"
        self.write_file(hooks_index_file, main_hooks_index)