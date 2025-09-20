#!/usr/bin/env python3
"""
Domain-Driven Frontend Generator
Generates TypeScript frontend files following the project's domain-driven design architecture
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class DomainDrivenFrontendGenerator:
    def __init__(self, frontend_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2"):
        self.frontend_path = Path(frontend_path)
        self.backend_config = {}
        
        # Domain mapping based on backend endpoints
        self.domain_mapping = {
            'auth': 'auth',
            'users': 'auth',  # User management is part of auth domain
            'puzzles': 'chess',
            'games': 'chess',
            'stats': 'performance',
            'learning': 'learning',
            'tutorials': 'learning'
        }
        
    def load_backend_config(self, config_path: str = "/mnt/c/Projects/chessboard-vanilla-v2/config/backend_config.json"):
        """Load backend configuration to understand API contract"""
        with open(config_path, 'r') as f:
            self.backend_config = json.load(f)
        print(f"📖 Loaded backend config with {len(self.backend_config['endpoints'])} endpoints")
    
    def create_directory_structure(self):
        """Create domain-driven directory structure"""
        src_path = self.frontend_path / "src"
        
        # Create base directories following architecture guide
        directories = [
            # Priority 1: Foundation Layer
            "types/auth",
            "types/chess", 
            "types/performance",
            "types/learning",
            "types/api",
            "types/ui",
            
            "utils/auth",
            "utils/chess",
            "utils/performance", 
            "utils/learning",
            "utils/api",
            "utils/common",
            "utils/ui",
            
            "constants/auth",
            "constants/chess",
            "constants/performance",
            "constants/learning",
            "constants/api",
            "constants/ui",
            
            # Priority 2: Infrastructure Layer
            "services/auth",
            "services/chess",
            "services/performance",
            "services/learning",
            
            "clients/auth",
            "clients/chess", 
            "clients/performance",
            "clients/learning",
            
            # Priority 3: Data Layer
            "hooks/auth",
            "hooks/chess",
            "hooks/performance",
            "hooks/learning",
            "hooks/queries",
            "hooks/mutations",
            
            "stores",
            "providers",
            
            # Priority 4: Presentation Layer
            "components/auth",
            "components/chess",
            "components/performance",
            "components/learning",
            "components/ui",
        ]
        
        for directory in directories:
            (src_path / directory).mkdir(parents=True, exist_ok=True)
        
        print("📁 Created domain-driven directory structure")
    
    def generate_domain_types(self, domain: str, endpoints: List[str]):
        """Generate TypeScript types for a specific domain"""
        src_path = self.frontend_path / "src"
        types_path = src_path / "types" / domain
        
        # Collect all types for this domain
        domain_types = []
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = endpoint_config['entity']
            
            # Read the backend model file
            backend_model_path = Path(f"../backend/src/models/{entity}.ts")
            if backend_model_path.exists():
                content = backend_model_path.read_text()
                domain_types.append(f"// {entity} types from backend")
                domain_types.append(content)
                domain_types.append("")
        
        # Add domain-specific frontend types
        if domain == 'auth':
            domain_types.extend([
                "// Frontend-specific auth types",
                "export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated' | 'error';",
                "",
                "export interface AuthState {",
                "  status: AuthStatus;",
                "  user: UserInfo | null;",
                "  token: string | null;",
                "  error: string | null;",
                "}",
                "",
                "export interface LoginCredentials {",
                "  email: string;",
                "  password: string;",
                "}",
                "",
                "export interface RegisterData {",
                "  username: string;",
                "  email: string;",
                "  password: string;",
                "  confirmPassword: string;",
                "}",
                ""
            ])
        
        elif domain == 'chess':
            domain_types.extend([
                "// Frontend-specific chess types",
                "export type GameStatus = 'idle' | 'active' | 'paused' | 'completed' | 'abandoned';",
                "",
                "export interface ChessPosition {",
                "  rank: number;",
                "  file: string;",
                "}",
                "",
                "export interface ChessMove {",
                "  from: ChessPosition;",
                "  to: ChessPosition;",
                "  piece?: string;",
                "  promotion?: string;",
                "}",
                "",
                "export interface PuzzleFilters {",
                "  minRating?: number;",
                "  maxRating?: number;",
                "  themes?: string[];",
                "  limit?: number;",
                "  offset?: number;",
                "}",
                ""
            ])
        
        elif domain == 'performance':
            domain_types.extend([
                "// Frontend-specific performance types",
                "export interface PerformanceMetrics {",
                "  totalPuzzles: number;",
                "  correctPuzzles: number;",
                "  accuracy: number;",
                "  averageTime: number;",
                "  currentRating: number;",
                "}",
                "",
                "export interface StatsPeriod {",
                "  period: 'day' | 'week' | 'month' | 'year' | 'all';",
                "  startDate?: string;",
                "  endDate?: string;",
                "}",
                ""
            ])
        
        elif domain == 'learning':
            domain_types.extend([
                "// Frontend-specific learning types",
                "export interface LearningProgress {",
                "  completedModules: number;",
                "  totalModules: number;",
                "  currentLevel: string;",
                "  skillPoints: number;",
                "}",
                "",
                "export interface CourseEnrollment {",
                "  courseId: string;",
                "  enrolledAt: string;",
                "  progress: number;",
                "  status: 'active' | 'completed' | 'paused';",
                "}",
                ""
            ])
        
        # Add common API types
        domain_types.extend([
            "// Common API response types",
            "export interface ApiResponse<T = any> {",
            "  success: boolean;",
            "  data?: T;",
            "  error?: string;",
            "  message?: string;",
            "}",
            "",
            "export interface PaginatedResponse<T> {",
            "  data: T[];",
            "  pagination: {",
            "    page: number;",
            "    limit: number;",
            "    total: number;",
            "    totalPages: number;",
            "  };",
            "}",
            "",
            "// React hook types",
            "export type LoadingState = 'idle' | 'loading' | 'success' | 'error';",
            "",
            "export interface UseQueryResult<T> {",
            "  data: T | null;",
            "  loading: boolean;",
            "  error: string | null;",
            "  refetch: () => Promise<void>;",
            "}",
            "",
            "export interface UseMutationResult<T, V = any> {",
            "  mutate: (variables: V) => Promise<T>;",
            "  loading: boolean;",
            "  error: string | null;",
            "}",
            ""
        ])
        
        # Write domain types file
        content = "\n".join(domain_types)
        types_file = types_path / "index.ts"
        types_file.write_text(content)
        
        print(f"📝 Generated {types_file}")
    
    def generate_domain_client(self, domain: str, endpoints: List[str]):
        """Generate API client for a specific domain"""
        src_path = self.frontend_path / "src"
        clients_path = src_path / "clients" / domain
        
        # Determine base API path for domain
        if domain == 'auth':
            base_path = '/auth'
        else:
            base_path = f'/api/{domain}'
        
        client_methods = []
        imports = set()
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = endpoint_config['entity']
            api_endpoints = endpoint_config.get('endpoints', [])
            
            imports.add(f"{entity}Response")
            imports.add(f"Create{entity}Request")
            imports.add(f"Update{entity}Request")
            
            for api_endpoint in api_endpoints:
                method = api_endpoint['method'].lower()
                path = api_endpoint['path'] 
                handler = api_endpoint['handler']
                
                client_method = self._generate_client_method(
                    method, path, handler, entity, base_path
                )
                client_methods.append(client_method)
        
        # Generate client class
        imports_str = ", ".join(sorted(imports))
        
        client_content = f"""import {{ ApiResponse, {imports_str} }} from '../types/{domain}';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001';

export class {domain.capitalize()}APIClient {{
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

{chr(10).join(client_methods)}
}}

// Singleton instance
export const {domain}APIClient = new {domain.capitalize()}APIClient();
"""
        
        # Write client file
        client_file = clients_path / "index.ts"
        client_file.write_text(client_content)
        
        print(f"📝 Generated {client_file}")
    
    def _generate_client_method(self, method: str, path: str, handler: str, entity: str, base_path: str) -> str:
        """Generate individual client method"""
        
        if method == 'get' and '/:id' in path:
            return f"""  async {handler}(id: string): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>(`/${{id}}`);
  }}"""
        
        elif method == 'get' and path == '/':
            return f"""  async {handler}(params?: any): Promise<ApiResponse<{entity}Response[]>> {{
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<{entity}Response[]>(`/${{queryString}}`);
  }}"""
        
        elif method == 'get':
            clean_path = path.replace('/:id', '')
            return f"""  async {handler}(params?: any): Promise<ApiResponse<any>> {{
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`{clean_path}${{queryString}}`);
  }}"""
        
        elif method == 'post' and '/:id/' in path:
            clean_path = path.replace('/:id', '')
            return f"""  async {handler}(id: string, data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`/${{id}}{clean_path}`, {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'post':
            return f"""  async {handler}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>('{path}', {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'put':
            if '/:id' in path:
                return f"""  async {handler}(id: string, data: Update{entity}Request): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>(`/${{id}}`, {{
      method: 'PUT',
      body: JSON.stringify(data),
    }});
  }}"""
            else:
                return f"""  async {handler}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>('{path}', {{
      method: 'PUT',
      body: JSON.stringify(data),
    }});
  }}"""
        
        elif method == 'delete':
            return f"""  async {handler}(id: string): Promise<ApiResponse<void>> {{
    return this.request<void>(`/${{id}}`, {{
      method: 'DELETE',
    }});
  }}"""
        
        else:
            return f"""  async {handler}(...args: any[]): Promise<ApiResponse<any>> {{
    throw new Error('{handler} not implemented');
  }}"""
    
    def generate_domain_hooks(self, domain: str, endpoints: List[str]):
        """Generate React Query hooks for a domain"""
        src_path = self.frontend_path / "src"
        hooks_path = src_path / "hooks" / domain
        
        # Generate query hooks (GET requests)
        query_hooks = []
        mutation_hooks = []
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            api_endpoints = endpoint_config.get('endpoints', [])
            
            for api_endpoint in api_endpoints:
                method = api_endpoint['method'].lower()
                handler = api_endpoint['handler']
                
                if method == 'get':
                    query_hook = self._generate_query_hook(handler, domain)
                    query_hooks.append(query_hook)
                else:
                    mutation_hook = self._generate_mutation_hook(handler, domain)
                    mutation_hooks.append(mutation_hook)
        
        # Generate hooks file
        hooks_content = f"""import {{ useState, useCallback }} from 'react';
import {{ UseQueryResult, UseMutationResult }} from '../types/{domain}';
import {{ {domain}APIClient }} from '../clients/{domain}';

// Query hooks for GET requests
{chr(10).join(query_hooks)}

// Mutation hooks for POST/PUT/DELETE requests
{chr(10).join(mutation_hooks)}

// Main domain hook that combines operations
export const use{domain.capitalize()} = () => {{
  return {{
    client: {domain}APIClient,
    // Add combined operations here
  }};
}};
"""
        
        # Write hooks file
        hooks_file = hooks_path / "index.ts"
        hooks_file.write_text(hooks_content)
        
        print(f"📝 Generated {hooks_file}")
    
    def _generate_query_hook(self, handler: str, domain: str) -> str:
        """Generate useQuery-style hook"""
        hook_name = f"use{handler.capitalize()}"
        
        return f"""export const {hook_name} = (params?: any): UseQueryResult<any> => {{
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const fetchData = useCallback(async () => {{
    setLoading(true);
    setError(null);
    
    try {{
      const response = await {domain}APIClient.{handler}(params);
      setData(response.data);
    }} catch (err: any) {{
      setError(err.message || 'An error occurred');
    }} finally {{
      setLoading(false);
    }}
  }}, [params]);
  
  return {{
    data,
    loading,
    error,
    refetch: fetchData,
  }};
}};"""
    
    def _generate_mutation_hook(self, handler: str, domain: str) -> str:
        """Generate useMutation-style hook"""
        hook_name = f"use{handler.capitalize()}"
        
        return f"""export const {hook_name} = (): UseMutationResult<any> => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const mutate = useCallback(async (variables: any) => {{
    setLoading(true);
    setError(null);
    
    try {{
      const response = await {domain}APIClient.{handler}(variables);
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
    
    def generate_domain_stores(self):
        """Generate Zustand stores for each domain"""
        src_path = self.frontend_path / "src"
        stores_path = src_path / "stores"
        
        # Generate auth store
        auth_store = """import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthState, LoginCredentials, UserInfo } from '../types/auth';
import { authAPIClient } from '../clients/auth';

interface AuthStore extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  updateUser: (user: Partial<UserInfo>) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      status: 'idle',
      user: null,
      token: null,
      error: null,
      
      login: async (credentials) => {
        set({ status: 'loading', error: null });
        
        try {
          const response = await authAPIClient.login(credentials);
          const { user, token } = response.data;
          
          localStorage.setItem('auth_token', token);
          set({ 
            status: 'authenticated', 
            user, 
            token, 
            error: null 
          });
        } catch (error: any) {
          set({ 
            status: 'error', 
            error: error.message 
          });
          throw error;
        }
      },
      
      logout: () => {
        localStorage.removeItem('auth_token');
        set({ 
          status: 'unauthenticated', 
          user: null, 
          token: null, 
          error: null 
        });
      },
      
      refreshToken: async () => {
        try {
          const token = get().token;
          if (!token) return false;
          
          const response = await authAPIClient.verifyToken({ token });
          const { user } = response.data;
          
          set({ user });
          return true;
        } catch {
          get().logout();
          return false;
        }
      },
      
      updateUser: (userData) => {
        const currentUser = get().user;
        if (currentUser) {
          set({ user: { ...currentUser, ...userData } });
        }
      },
      
      clearError: () => {
        set({ error: null });
      }
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        status: state.status 
      }),
    }
  )
);
"""
        
        auth_store_file = stores_path / "authStore.ts"
        auth_store_file.write_text(auth_store)
        
        # Generate chess store  
        chess_store = """import { create } from 'zustand';
import { GameStatus, PuzzleFilters } from '../types/chess';

interface ChessStore {
  currentGameId: string | null;
  gameStatus: GameStatus;
  puzzleFilters: PuzzleFilters;
  selectedPuzzleId: string | null;
  
  setCurrentGame: (gameId: string | null) => void;
  setGameStatus: (status: GameStatus) => void;
  updatePuzzleFilters: (filters: Partial<PuzzleFilters>) => void;
  selectPuzzle: (puzzleId: string | null) => void;
}

export const useChessStore = create<ChessStore>((set) => ({
  currentGameId: null,
  gameStatus: 'idle',
  puzzleFilters: {
    minRating: 800,
    maxRating: 2000,
    limit: 10,
    offset: 0
  },
  selectedPuzzleId: null,
  
  setCurrentGame: (gameId) => set({ currentGameId: gameId }),
  
  setGameStatus: (status) => set({ gameStatus: status }),
  
  updatePuzzleFilters: (filters) => 
    set((state) => ({ 
      puzzleFilters: { ...state.puzzleFilters, ...filters } 
    })),
    
  selectPuzzle: (puzzleId) => set({ selectedPuzzleId: puzzleId }),
}));
"""
        
        chess_store_file = stores_path / "chessStore.ts"
        chess_store_file.write_text(chess_store)
        
        # Generate main stores index
        stores_index = """export { useAuthStore } from './authStore';
export { useChessStore } from './chessStore';
"""
        
        stores_index_file = stores_path / "index.ts"
        stores_index_file.write_text(stores_index)
        
        print(f"📝 Generated stores in {stores_path}")
    
    def generate_domain_components(self, domain: str, endpoints: List[str]):
        """Generate placeholder components for a domain"""
        src_path = self.frontend_path / "src"
        components_path = src_path / "components" / domain
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = endpoint_config['entity']
            
            component_content = f"""import React from 'react';
import {{ use{domain.capitalize()} }} from '../../hooks/{domain}';

interface {entity}ComponentProps {{
  className?: string;
}}

export const {entity}Component: React.FC<{entity}ComponentProps> = ({{
  className
}}) => {{
  const {{ client }} = use{domain.capitalize()}();
  
  return (
    <div className={{className}}>
      <h2>{entity} Component</h2>
      <p>Domain: {domain}</p>
      <p>This is a placeholder component for {entity} operations.</p>
      
      <div>
        <button 
          onClick={{() => console.log('TODO: Implement {entity} operations')}}
        >
          Test {entity} Operations
        </button>
      </div>
    </div>
  );
}};

export default {entity}Component;
"""
            
            component_file = components_path / f"{entity}Component.tsx"
            component_file.write_text(component_content)
            
        print(f"📝 Generated components for {domain} domain")
    
    def generate_all_domains(self):
        """Generate all domain files following the architecture"""
        print("🚀 Domain-Driven Frontend Generator Starting...")
        
        # Load backend configuration
        self.load_backend_config()
        
        # Create directory structure
        self.create_directory_structure()
        
        # Group endpoints by domain
        domains = {}
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            domain = self.domain_mapping.get(endpoint_name, 'common')
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(endpoint_name)
        
        print(f"📊 Organized {len(self.backend_config['endpoints'])} endpoints into {len(domains)} domains")
        
        # Generate files for each domain following priority order
        for domain, endpoints in domains.items():
            print(f"🔧 Generating {domain} domain...")
            
            # Priority 1: Foundation Layer
            self.generate_domain_types(domain, endpoints)
            
            # Priority 2: Infrastructure Layer
            self.generate_domain_client(domain, endpoints)
            
            # Priority 3: Data Layer
            self.generate_domain_hooks(domain, endpoints)
            
            # Priority 4: Presentation Layer
            self.generate_domain_components(domain, endpoints)
        
        # Generate global stores (Priority 3)
        self.generate_domain_stores()
        
        # Generate index files for easier imports
        self._generate_domain_indices()
        
        print("✅ Domain-driven frontend generation complete!")
    
    def _generate_domain_indices(self):
        """Generate index files for each domain"""
        src_path = self.frontend_path / "src"
        
        domains = ['auth', 'chess', 'performance', 'learning']
        
        for domain in domains:
            # Types index
            types_index = f"export * from './{domain}';"
            (src_path / "types" / "index.ts").write_text(
                "\n".join([f"export * from './{d}';" for d in domains])
            )
            
            # Clients index  
            (src_path / "clients" / "index.ts").write_text(
                "\n".join([f"export * from './{d}';" for d in domains])
            )
            
            # Hooks index
            (src_path / "hooks" / "index.ts").write_text(
                "\n".join([f"export * from './{d}';" for d in domains])
            )
            
            # Components index
            (src_path / "components" / "index.ts").write_text(
                "\n".join([f"export * from './{d}';" for d in domains])
            )
        
        print("📝 Generated domain index files")

def main():
    """Main function to run the domain-driven generator"""
    generator = DomainDrivenFrontendGenerator()
    generator.generate_all_domains()

if __name__ == "__main__":
    main()