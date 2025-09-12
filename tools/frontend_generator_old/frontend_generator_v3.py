#!/usr/bin/env python3
"""
Domain-Driven Frontend Generator V3
Fixed version that generates proper TypeScript code with correct imports and no duplicates
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class FixedFrontendGenerator:
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
        
    def load_backend_config(self, config_path: str = "backend_config.json"):
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
            "types/common",
            "types/auth",
            "types/chess", 
            "types/performance",
            "types/learning",
            
            "utils/common",
            "utils/auth",
            "utils/chess",
            "utils/performance", 
            "utils/learning",
            
            "constants/auth",
            "constants/chess",
            "constants/performance",
            "constants/learning",
            
            # Priority 2: Infrastructure Layer
            "services/auth",
            "services/chess",
            "services/performance",
            "services/learning",
            
            "clients",
            
            # Priority 3: Data Layer
            "hooks/auth",
            "hooks/chess",
            "hooks/performance",
            "hooks/learning",
            
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
    
    def generate_common_types(self):
        """Generate common types shared across all domains"""
        src_path = self.frontend_path / "src"
        common_types_path = src_path / "types" / "common"
        
        common_content = '''// Common API response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// React hook types
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

// Environment variables
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_API_BASE_URL?: string;
    }
  }
}
'''
        
        # Write common types
        common_file = common_types_path / "index.ts"
        common_file.write_text(common_content)
        
        print(f"📝 Generated {common_file}")
    
    def generate_domain_types(self, domain: str, endpoints: List[str]):
        """Generate TypeScript types for a specific domain"""
        src_path = self.frontend_path / "src"
        types_path = src_path / "types" / domain
        
        # Import common types
        domain_types = [
            "// Import common types",
            "import type { ApiResponse, LoadingState, UseQueryResult, UseMutationResult } from '../common';",
            ""
        ]
        
        # Collect backend model types for this domain
        backend_types = []
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = endpoint_config['entity']
            
            # Read the backend model file
            backend_model_path = Path(f"../backend/src/models/{entity}.ts")
            if backend_model_path.exists():
                content = backend_model_path.read_text()
                backend_types.append(f"// {entity} types from backend")
                backend_types.append(content)
                backend_types.append("")
        
        domain_types.extend(backend_types)
        
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
        
        # Write domain types file
        content = "\n".join(domain_types)
        types_file = types_path / "index.ts"
        types_file.write_text(content)
        
        print(f"📝 Generated {types_file}")
    
    def generate_domain_clients(self):
        """Generate domain-specific API clients following architecture guide"""
        src_path = self.frontend_path / "src"
        clients_path = src_path / "clients"
        
        # Group endpoints by domain
        domains = {}
        for endpoint_name, endpoint_config in self.backend_config['endpoints'].items():
            domain = self.domain_mapping.get(endpoint_name, 'common')
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(endpoint_name)
        
        # Generate base HTTP client first
        base_client_content = """import type { ApiResponse } from '../types/common';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001';

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
        base_client_file.write_text(base_client_content)
        print(f"📝 Generated {base_client_file}")
        
        # Generate domain-specific clients
        for domain, endpoints in domains.items():
            self._generate_domain_client(domain, endpoints)
        
        # Generate main client index that exports all domain clients
        client_index_content = """// Domain-specific API clients
export { BaseAPIClient } from './BaseAPIClient';
export { AuthAPIClient } from './AuthAPIClient';
export { ChessAPIClient } from './ChessAPIClient';
export { PerformanceAPIClient } from './PerformanceAPIClient';
export { LearningAPIClient } from './LearningAPIClient';

// Unified client for convenience (optional)
import { AuthAPIClient } from './AuthAPIClient';
import { ChessAPIClient } from './ChessAPIClient';
import { PerformanceAPIClient } from './PerformanceAPIClient';
import { LearningAPIClient } from './LearningAPIClient';

export class APIClient {
  public readonly auth = new AuthAPIClient();
  public readonly chess = new ChessAPIClient();
  public readonly performance = new PerformanceAPIClient();
  public readonly learning = new LearningAPIClient();
}

// Singleton instance for convenience
export const apiClient = new APIClient();
export default apiClient;
"""
        
        client_index_file = clients_path / "index.ts"
        client_index_file.write_text(client_index_content)
        print(f"📝 Generated domain-organized {client_index_file}")
    
    def _generate_domain_client(self, domain: str, endpoints: List[str]):
        """Generate a domain-specific API client"""
        src_path = self.frontend_path / "src"
        clients_path = src_path / "clients"
        
        # Get relevant endpoints for this domain
        domain_methods = []
        domain_imports = set(['ApiResponse'])
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = endpoint_config['entity']
            api_endpoints = endpoint_config.get('endpoints', [])
            
            # Determine base path
            if endpoint_name == 'auth':
                base_path = '/auth'
            else:
                base_path = f'/api/{endpoint_config.get("entities", endpoint_name)}'
            
            # Fix naming inconsistencies
            if entity == 'Learningpath':
                entity = 'LearningPath'
            
            domain_imports.add(f"{entity}Response")
            domain_imports.add(f"Create{entity}Request") 
            domain_imports.add(f"Update{entity}Request")
            
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
            
        # Generate domain-specific import statement
        type_imports = []
        if domain == 'auth':
            type_imports = ["AuthResponse", "UserResponse", "CreateAuthRequest", "UpdateAuthRequest", "CreateUserRequest", "UpdateUserRequest", "LoginRequest", "RegisterRequest"]
        elif domain == 'chess':
            type_imports = ["PuzzleResponse", "GameResponse", "CreatePuzzleRequest", "UpdatePuzzleRequest", "CreateGameRequest", "UpdateGameRequest"]
        elif domain == 'performance':
            type_imports = ["StatsResponse", "CreateStatsRequest", "UpdateStatsRequest"]
        elif domain == 'learning':
            type_imports = ["TutorialResponse", "LearningPathResponse", "CreateTutorialRequest", "UpdateTutorialRequest", "CreateLearningPathRequest", "UpdateLearningPathRequest"]
        
        imports_str = ", ".join(type_imports) if type_imports else "any"
        
        client_content = f"""import type {{ ApiResponse }} from '../types/common';
import type {{ {imports_str} }} from '../types/{domain}';
import {{ BaseAPIClient }} from './BaseAPIClient';

/**
 * {domain.capitalize()} Domain API Client
 * Handles all {domain}-related API operations
 */
export class {domain.capitalize()}APIClient extends BaseAPIClient {{
{chr(10).join(domain_methods)}
}}

export default {domain.capitalize()}APIClient;
"""
        
        # Write domain client file
        client_file = clients_path / f"{domain.capitalize()}APIClient.ts"
        client_file.write_text(client_content)
        print(f"📝 Generated {client_file}")
    
    def _generate_client_method(self, method: str, path: str, handler: str, entity: str, base_path: str) -> str:
        """Generate individual client method"""
        
        if method == 'get' and '/:id' in path:
            return f"""  async {handler}(id: string): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>(`{base_path}/${{id}}`);
  }}"""
        
        elif method == 'get' and path == '/':
            return f"""  async {handler}(params?: any): Promise<ApiResponse<{entity}Response[]>> {{
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<{entity}Response[]>(`{base_path}${{queryString}}`);
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
                return f"""  async {handler}(id: string, data: Update{entity}Request): Promise<ApiResponse<{entity}Response>> {{
    return this.request<{entity}Response>(`{base_path}/${{id}}`, {{
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
    
    def generate_domain_hooks(self, domain: str, endpoints: List[str]):
        """Generate individual React hook files for a domain"""
        src_path = self.frontend_path / "src"
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
        
        # Create main domain hook file (e.g., useAuth.ts, useChess.ts)
        main_hook_name = f"use{domain.capitalize()}"
        main_hook_content = f"""import {{ useState, useCallback }} from 'react';
import {{ {domain.capitalize()}Service }} from '../../services/{domain}';

/**
 * {domain.capitalize()} domain hook for {domain} operations
 */
export const {main_hook_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Main domain operations would go here
  // This is a placeholder - implement specific operations as needed
  
  return {{
    loading,
    error,
    clearError: () => setError(null)
  }};
}};"""
        
        main_hook_file = hooks_path / f"{main_hook_name}.ts"
        main_hook_file.write_text(main_hook_content)
        generated_hooks.append(main_hook_name)
        print(f"📝 Generated {main_hook_file}")
        
        # Create query hooks file for GET operations
        query_hook_name = f"use{domain.capitalize()}Queries"
        query_hook_content = f"""import {{ useState, useCallback }} from 'react';
import type {{ UseQueryResult }} from '../../types/common';
import {{ {domain.capitalize()}Service }} from '../../services/{domain}';

/**
 * Query hooks for {domain} GET operations
 */
export const {query_hook_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Query operations would go here based on GET endpoints
  // This is a placeholder - implement specific queries as needed
  
  return {{
    loading,
    error,
    refetch: () => {{/* implement refetch logic */}}
  }};
}};"""
        
        query_hook_file = hooks_path / f"{query_hook_name}.ts"
        query_hook_file.write_text(query_hook_content)
        generated_hooks.append(query_hook_name)
        print(f"📝 Generated {query_hook_file}")
        
        # Create mutations hook file for POST/PUT/DELETE operations
        mutations_hook_name = f"use{domain.capitalize()}Mutations"
        mutations_hook_content = f"""import {{ useState, useCallback }} from 'react';
import type {{ UseMutationResult }} from '../../types/common';
import {{ {domain.capitalize()}Service }} from '../../services/{domain}';

/**
 * Mutation hooks for {domain} POST/PUT/DELETE operations
 */
export const {mutations_hook_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Mutation operations would go here based on POST/PUT/DELETE endpoints
  // This is a placeholder - implement specific mutations as needed
  
  return {{
    loading,
    error,
    mutate: async (data: any) => {{
      setLoading(true);
      setError(null);
      try {{
        // Implementation would go here
        return null;
      }} catch (err: any) {{
        setError(err.message || 'An error occurred');
        throw err;
      }} finally {{
        setLoading(false);
      }}
    }}
  }};
}};"""
        
        mutations_hook_file = hooks_path / f"{mutations_hook_name}.ts"
        mutations_hook_file.write_text(mutations_hook_content)
        generated_hooks.append(mutations_hook_name)
        print(f"📝 Generated {mutations_hook_file}")
        
        # Generate index file that exports all hooks
        index_content = f"""// {domain.capitalize()} Domain Hooks
{chr(10).join([f'export {{ {hook} }} from \'./{hook}\';' for hook in generated_hooks])}
"""
        
        index_file = hooks_path / "index.ts"
        index_file.write_text(index_content)
        print(f"📝 Generated hooks index at {index_file}")
    
    def _generate_query_hook(self, handler: str) -> str:
        """Generate useQuery-style hook"""
        hook_name = f"use{handler.capitalize()}Query"
        
        return f"""export const {hook_name} = (params?: any): UseQueryResult<any> => {{
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const fetchData = useCallback(async () => {{
    setLoading(true);
    setError(null);
    
    try {{
      const response = await apiClient.{handler}(params);
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
    
    def _generate_mutation_hook(self, handler: str) -> str:
        """Generate useMutation-style hook"""
        hook_name = f"use{handler.capitalize()}Mutation"
        
        return f"""export const {hook_name} = (): UseMutationResult<any> => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const mutate = useCallback(async (variables: any) => {{
    setLoading(true);
    setError(null);
    
    try {{
      const response = await apiClient.{handler}(variables);
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
import type { AuthState, LoginCredentials, UserInfo } from '../types/auth';
import { AuthAPIClient } from '../clients/AuthAPIClient';

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
          const authClient = new AuthAPIClient();
          const response = await authClient.login(credentials);
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
          
          const authClient = new AuthAPIClient();
          const response = await authClient.verifyToken({ token });
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
import type { GameStatus, PuzzleFilters } from '../types/chess';

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
    
    def generate_domain_services(self, domain: str, endpoints: List[str]):
        """Generate individual service files for a domain"""
        src_path = self.frontend_path / "src"
        services_path = src_path / "services" / domain
        
        # Get relevant endpoints for this domain
        domain_endpoints = []
        for endpoint_name in endpoints:
            if endpoint_name in self.backend_config['endpoints']:
                domain_endpoints.append(endpoint_name)
        
        if not domain_endpoints:
            return
            
        # Create main domain service file
        service_name = f"{domain.capitalize()}Service"
        service_content = f"""import {{ {domain.capitalize()}APIClient }} from '../../clients/{domain.capitalize()}APIClient';
import type {{ ApiResponse }} from '../../types/common';

/**
 * {domain.capitalize()} Domain Service
 * Business logic layer for {domain} operations
 */
export class {service_name} {{
  // Service methods will be implemented based on specific domain requirements
  // This is a placeholder - implement specific methods as needed
  
  static async healthCheck(): Promise<ApiResponse<any>> {{
    try {{
      // Placeholder health check
      return {{ success: true, data: {{ status: 'healthy' }} }} as ApiResponse<any>;
    }} catch (error) {{
      throw new Error(`{domain} service health check failed`);
    }}
  }}
}}

export default {service_name};
"""
        
        # Write main service file
        service_file = services_path / f"{service_name}.ts"
        service_file.write_text(service_content)
        print(f"📝 Generated {service_file}")
        
        # Create additional specialized service files based on domain
        if domain == 'auth':
            # Create AuthService with actual auth methods
            auth_service_content = """import { AuthAPIClient } from '../../clients/AuthAPIClient';
import type { ApiResponse } from '../../types/common';

/**
 * Authentication Service
 * Handles user authentication and authorization
 */
export class AuthService {
  private static client = new AuthAPIClient();

  static async login(credentials: { email: string; password: string }): Promise<ApiResponse<any>> {
    return this.client.login(credentials);
  }

  static async register(userData: { username: string; email: string; password: string }): Promise<ApiResponse<any>> {
    return this.client.register(userData);
  }

  static async logout(): Promise<ApiResponse<void>> {
    return this.client.logout({});
  }

  static async getCurrentUser(): Promise<ApiResponse<any>> {
    return this.client.getCurrentUser();
  }

  static async updateProfile(data: any): Promise<ApiResponse<any>> {
    return this.client.updateProfile(data);
  }

  static async changePassword(data: { currentPassword: string; newPassword: string }): Promise<ApiResponse<void>> {
    return this.client.changePassword(data);
  }

  static async verifyToken(token: string): Promise<ApiResponse<any>> {
    return this.client.verifyToken({ token });
  }

  static async forgotPassword(email: string): Promise<ApiResponse<void>> {
    return this.client.forgotPassword({ email });
  }

  static async resetPassword(data: { token: string; password: string }): Promise<ApiResponse<void>> {
    return this.client.resetPassword(data);
  }

  static async checkEmailAvailability(email: string): Promise<ApiResponse<boolean>> {
    return this.client.checkEmailAvailability({ email });
  }

  static async checkUsernameAvailability(username: string): Promise<ApiResponse<boolean>> {
    return this.client.checkUsernameAvailability({ username });
  }

  static async deleteAccount(id: string): Promise<ApiResponse<void>> {
    return this.client.deleteAccount(id);
  }
}

export default AuthService;
"""
            auth_file = services_path / "AuthService.ts"
            auth_file.write_text(auth_service_content)
            print(f"📝 Generated {auth_file}")
            
        elif domain == 'chess':
            # Create ChessService with chess-specific methods
            chess_service_content = """import { ChessAPIClient } from '../../clients/ChessAPIClient';
import type { ApiResponse } from '../../types/common';

/**
 * Chess Service
 * Handles chess games and puzzles
 */
export class ChessService {
  private static client = new ChessAPIClient();

  static async getNextPuzzle(filters?: any): Promise<ApiResponse<any>> {
    return this.client.getNextPuzzle(filters);
  }

  static async solvePuzzle(id: string, solution: any): Promise<ApiResponse<any>> {
    return this.client.solvePuzzle(id, solution);
  }

  static async getPuzzleHint(id: string): Promise<ApiResponse<any>> {
    return this.client.getPuzzleHint(id);
  }

  static async createGame(gameData: any): Promise<ApiResponse<any>> {
    return this.client.createGame(gameData);
  }

  static async updateGame(id: string, gameData: any): Promise<ApiResponse<any>> {
    return this.client.updateGame(id, gameData);
  }

  static async analyzeGame(id: string, analysisData: any): Promise<ApiResponse<any>> {
    return this.client.analyzeGame(id, analysisData);
  }

  static async getGameById(id: string): Promise<ApiResponse<any>> {
    return this.client.getGameById(id);
  }

  static async getGames(filters?: any): Promise<ApiResponse<any[]>> {
    return this.client.getGames(filters);
  }
}

export default ChessService;
"""
            chess_file = services_path / "ChessService.ts"
            chess_file.write_text(chess_service_content)
            print(f"📝 Generated {chess_file}")
        
        # Generate index file that exports all services
        generated_services = []
        if domain == 'auth':
            generated_services = ['AuthService']
        elif domain == 'chess':
            generated_services = ['ChessService']
        else:
            generated_services = [service_name]
            
        # Remove duplicates and ensure we only export what exists
        unique_services = list(set(generated_services))
            
        index_content = f"""// {domain.capitalize()} Domain Services
{chr(10).join([f'export {{ {service} }} from \'./{service}\';' for service in unique_services])}
"""
        
        index_file = services_path / "index.ts"
        index_file.write_text(index_content)
        print(f"📝 Generated services index at {index_file}")
    
    def generate_domain_components(self, domain: str, endpoints: List[str]):
        """Generate placeholder components for a domain"""
        src_path = self.frontend_path / "src"
        components_path = src_path / "components" / domain
        
        domain_components = []
        
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
  
  const handleTestClick = () => {{
    console.log('TODO: Implement {entity} operations', {{ client }});
  }};
  
  return (
    <div className={{`{entity.lower()}-component ${{className || ''}}`}}>
      <h2>{entity} Component</h2>
      <p>Domain: {domain}</p>
      <p>This is a placeholder component for {entity} operations.</p>
      
      <div>
        <button onClick={{handleTestClick}}>
          Test {entity} Operations
        </button>
      </div>
    </div>
  );
}};
"""
            
            component_file = components_path / f"{entity}Component.tsx"
            component_file.write_text(component_content)
            domain_components.append(entity)
        
        # Generate domain component index
        if domain_components:
            domain_index = "\n".join([
                f"export {{ {comp}Component }} from './{comp}Component';" 
                for comp in domain_components
            ])
            
            domain_index_file = components_path / "index.ts"
            domain_index_file.write_text(domain_index)
        
        print(f"📝 Generated components for {domain} domain")
    
    def generate_main_entry_files(self):
        """Generate main React entry files"""
        src_path = self.frontend_path / "src"
        
        # Generate main.tsx
        main_content = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)"""
        
        main_file = src_path / "main.tsx"
        main_file.write_text(main_content)
        
        # Generate App.tsx  
        app_content = """import './App.css'

// Import our generated components
import { AuthComponent } from './components/auth'
import { PuzzleComponent, GameComponent } from './components/chess'
import { StatsComponent } from './components/performance'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Chess Platform - Domain-Driven Frontend</h1>
        <p>Generated frontend with complete API contract coverage</p>
      </header>
      
      <main className="App-main">
        <div className="domain-section">
          <h2>Authentication Domain</h2>
          <AuthComponent />
        </div>
        
        <div className="domain-section">
          <h2>Chess Domain</h2>
          <PuzzleComponent />
          <GameComponent />
        </div>
        
        <div className="domain-section">
          <h2>Performance Domain</h2>
          <StatsComponent />
        </div>
      </main>
    </div>
  )
}

export default App"""
        
        app_file = src_path / "App.tsx" 
        app_file.write_text(app_content)
        
        # Generate CSS files
        app_css = """.App {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.App-header {
  margin-bottom: 2rem;
}

.App-header h1 {
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.App-header p {
  color: #666;
  font-size: 1.1rem;
}

.App-main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.domain-section {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: #f9f9f9;
}

.domain-section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

button {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

button:hover {
  background: #2980b9;
}"""
        
        app_css_file = src_path / "App.css"
        app_css_file.write_text(app_css)
        
        index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}"""
        
        index_css_file = src_path / "index.css"
        index_css_file.write_text(index_css)
        
        print("📝 Generated main React entry files")
    
    def generate_all_domains(self):
        """Generate all domain files following the architecture"""
        print("🚀 Fixed Domain-Driven Frontend Generator Starting...")
        
        # Load backend configuration
        self.load_backend_config()
        
        # Create directory structure
        self.create_directory_structure()
        
        # Generate common types first
        self.generate_common_types()
        
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
            self.generate_domain_services(domain, endpoints)
            
            # Priority 3: Data Layer
            self.generate_domain_hooks(domain, endpoints)
            
            # Priority 4: Presentation Layer
            self.generate_domain_components(domain, endpoints)
        
        # Generate domain-specific clients (Priority 2)
        self.generate_domain_clients()
        
        # Generate global stores (Priority 3)
        self.generate_domain_stores()
        
        # Generate main React entry files
        self.generate_main_entry_files()
        
        # Generate index files for easier imports
        self._generate_final_indices()
        
        print("✅ Fixed domain-driven frontend generation complete!")
    
    def _generate_final_indices(self):
        """Generate final index files with proper exports"""
        src_path = self.frontend_path / "src"
        
        # Main types index - only re-export common, avoid duplicates
        main_types_index = """// Common types - shared across all domains
export * from './common';

// Domain-specific types - import from specific domains as needed
// Avoid re-exporting everything to prevent conflicts
"""
        (src_path / "types" / "index.ts").write_text(main_types_index)
        
        # Main hooks index
        main_hooks_index = """export * from './auth';
export * from './chess';
export * from './performance';
export * from './learning';
"""
        (src_path / "hooks" / "index.ts").write_text(main_hooks_index)
        
        # Main components index
        main_components_index = """export * from './auth';
export * from './chess';
export * from './performance';
export * from './learning';
"""
        (src_path / "components" / "index.ts").write_text(main_components_index)
        
        print("📝 Generated final index files")

def main():
    """Main function to run the fixed generator"""
    generator = FixedFrontendGenerator()
    generator.generate_all_domains()

if __name__ == "__main__":
    main()