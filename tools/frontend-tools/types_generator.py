#!/usr/bin/env python3
"""
Types Generator Module
Handles generation of TypeScript types for all domains
"""

from pathlib import Path
from typing import List
from base_generator import BaseFrontendGenerator

class TypesGenerator(BaseFrontendGenerator):
    """Generates TypeScript types for all domains"""
    
    def generate_common_types(self):
        """Generate common types shared across all domains"""
        src_path = self.get_src_path()
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

// Common loading and state types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

// Generic domain state interface
export interface DomainState<T = any> {
  items: T[];
  selectedItem: T | null;
  loading: LoadingState;
  error: string | null;
}

// React hook types
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
        
        common_file = common_types_path / "index.ts"
        self.write_file(common_file, common_content)
        
        # Create CSS module type declarations
        vite_env_content = '''/// <reference types="vite/client" />

// CSS Module declarations
declare module '*.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}

declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}
'''
        
        vite_env_file = src_path / "vite-env.d.ts"
        self.write_file(vite_env_file, vite_env_content)
    
    def generate_domain_types(self, domain: str, endpoints: List[str]):
        """Generate TypeScript types for a specific domain"""
        src_path = self.get_src_path()
        
        # Skip generating domain types for 'common' to avoid overwriting shared common types
        if domain == 'common':
            return
            
        types_path = src_path / "types" / domain
        
        # Start with domain header
        domain_types = [
            f"// {domain.capitalize()} Domain Types",
            ""
        ]
        
        has_common_imports = False
        
        # Generate types based on backend config properties
        backend_types = []
        
        for endpoint_name in endpoints:
            if endpoint_name not in self.backend_config['endpoints']:
                continue
                
            endpoint_config = self.backend_config['endpoints'][endpoint_name]
            entity = self.get_entity_name(endpoint_name)
            properties = endpoint_config.get('properties', {})
            
            if entity and properties:
                backend_types.append(f"// {entity} types from backend")
                
                # Generate base entity interface
                base_interface = [f"export interface {entity} {{"]
                create_fields = []
                
                for prop_name, prop_type in properties.items():
                    ts_type = self._convert_to_typescript_type(prop_type)
                    base_interface.append(f"  {prop_name}: {ts_type};")
                    
                    # Collect non-auto-generated fields for create/update
                    if prop_name not in ['id', 'created_at', 'updated_at']:
                        create_fields.append((prop_name, ts_type))
                
                base_interface.append("}")
                backend_types.extend(base_interface)
                backend_types.append("")
                
                # Use utility types for efficiency
                backend_types.append(f"// Response type (same as base entity)")
                backend_types.append(f"export type {entity}Response = {entity};")
                backend_types.append("")
                
                # Generate Create Request using Omit utility type if most fields are used
                if len(create_fields) > 3:
                    excluded_fields = ["'id'"]
                    if 'created_at' in properties:
                        excluded_fields.append("'created_at'")
                    if 'updated_at' in properties:
                        excluded_fields.append("'updated_at'")
                    excluded_fields_str = " | ".join(excluded_fields)
                    backend_types.append(f"// Create request omits auto-generated fields")
                    backend_types.append(f"export type Create{entity}Request = Omit<{entity}, {excluded_fields_str}>;")
                else:
                    # For simple entities, generate explicit interface
                    create_interface = [f"export interface Create{entity}Request {{"]
                    for prop_name, ts_type in create_fields:
                        create_interface.append(f"  {prop_name}: {ts_type};")
                    create_interface.append("}")
                    backend_types.extend(create_interface)
                backend_types.append("")
                
                # Update Request uses Partial
                backend_types.append(f"// Update request makes create fields optional")
                backend_types.append(f"export type Update{entity}Request = Partial<Create{entity}Request>;")
                backend_types.append("")
        
        domain_types.extend(backend_types)
        
        # Get the first entity name for frontend types
        first_entity = None
        for endpoint_name in endpoints:
            if endpoint_name in self.backend_config['endpoints']:
                entity = self.get_entity_name(endpoint_name) 
                if entity:
                    first_entity = entity
                    break
        
        # Add domain-specific frontend types
        domain_specific_types = self._get_domain_specific_types(domain, first_entity)
        
        # Check if we need common imports
        if any('from ../common' in line for line in domain_specific_types):
            has_common_imports = True
        
        domain_types.extend(domain_specific_types)
        
        # Add import at the top if needed (only DomainState, not LoadingState)
        if has_common_imports:
            import_line = "import type { DomainState } from '../common';"
            # Insert import after the header
            domain_types.insert(2, import_line)
            domain_types.insert(3, "")
        
        # Write domain types file
        content = "\n".join(domain_types)
        types_file = types_path / "index.ts"
        self.write_file(types_file, content)
    
    def _convert_to_typescript_type(self, backend_type: str) -> str:
        """Convert backend type to TypeScript type"""
        type_mapping = {
            'string': 'string',
            'number': 'number', 
            'boolean': 'boolean',
            'date': 'string',  # Dates are typically handled as strings in JSON
            'datetime': 'string',
            'text': 'string',
            'int': 'number',
            'float': 'number',
            'decimal': 'number'
        }
        
        return type_mapping.get(backend_type.lower(), 'any')
    
    def _get_domain_specific_types(self, domain: str, entity: str = None) -> List[str]:
        """Get domain-specific frontend types - keep special ones, generate basic ones for others"""
        # Keep the special domain types for domains that need custom frontend types
        special_types = {
            'auth': self._get_auth_types(),
            'chess': self._get_chess_types(), 
            'performance': self._get_performance_types(),
            'learning': self._get_learning_types()
        }
        
        # Return special types if they exist, otherwise generate basic frontend types
        if domain in special_types:
            return special_types[domain]
        else:
            return self._generate_basic_frontend_types(domain, entity)
    
    def _generate_basic_frontend_types(self, domain: str, entity: str = None) -> List[str]:
        """Generate basic frontend-specific types for any domain using common types"""
        domain_capitalized = self.capitalize_domain(domain)
        
        # Use the actual entity response type if we have it
        response_type = f"{entity}Response" if entity else f"{domain_capitalized}Response"
        
        return [
            f"// Frontend-specific {domain} types",
            f"// Uses common DomainState interface from ../common",
            f"export type {domain_capitalized}State = DomainState<{response_type}>;",
            ""
        ]
    
    def _get_auth_types(self) -> List[str]:
        """Get auth domain specific types"""
        return [
            "// Frontend-specific auth types",
            "export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated' | 'error';",
            "",
            "export interface UserInfo {",
            "  id: string;",
            "  username: string;",
            "  email: string;",
            "  chess_elo: number;",
            "  puzzle_rating: number;",
            "  preferences: string;",
            "  created_at: string;",
            "  updated_at: string;",
            "}",
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
        ]
    
    def _get_chess_types(self) -> List[str]:
        """Get chess domain specific types"""
        return [
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
        ]
    
    def _get_performance_types(self) -> List[str]:
        """Get performance domain specific types"""
        return [
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
        ]
    
    def _get_learning_types(self) -> List[str]:
        """Get learning domain specific types"""
        return [
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
        ]
    
    def generate_main_types_index(self):
        """Generate main types index file"""
        src_path = self.get_src_path()
        
        main_types_index = """// Common types - shared across all domains
export * from './common';

// Domain-specific types - import from specific domains as needed
// Avoid re-exporting everything to prevent conflicts
"""
        
        types_index_file = src_path / "types" / "index.ts"
        self.write_file(types_index_file, main_types_index)