# Frontend Generator V4 - Comprehensive Guide

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Domain-Driven Structure](#domain-driven-structure)
5. [Generation System](#generation-system)
6. [Module Generators](#module-generators)
7. [Usage Guide](#usage-guide)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [Extension Guide](#extension-guide)

---

## Overview

Frontend Generator V4 is a sophisticated domain-driven code generation system that creates complete React/TypeScript frontends from backend configuration. It follows a modular architecture that generates type-safe, production-ready frontend applications with full API integration, state management, and component architecture.

### Key Features

- **Domain-Driven Architecture**: Organizes code by business domains rather than technical layers
- **Configuration-Driven**: Generates complete frontend from `backend_config.json`
- **TypeScript First**: Complete type safety across all generated components
- **Modular Generation**: Specialized generators for types, services, hooks, components, and clients
- **API Contract Synchronization**: Automatically syncs with backend API definitions
- **Production Ready**: Includes authentication, error handling, and state management
- **React Integration**: Modern React patterns with hooks and functional components

### Generated Structure

```
frontend-v2/
├── src/
│   ├── types/           # TypeScript definitions by domain
│   ├── services/        # Business logic layer
│   ├── hooks/           # React hooks for data management
│   ├── components/      # React components by domain
│   ├── clients/         # API client classes
│   ├── stores/          # Zustand state management
│   ├── utils/           # Utility functions
│   └── constants/       # Domain constants
```

---

## Architecture

The Frontend Generator V4 follows a layered, domain-driven architecture designed for scalability and maintainability:

```
Frontend Generator V4
├── Frontend Orchestrator (Main Coordinator)
│   ├── Domain Mapping (Business Domain Organization)
│   ├── Backend Config Loader (API Contract Integration)
│   └── Generation Priority Manager
├── Layer 1: Foundation
│   └── Types Generator (TypeScript Definitions)
├── Layer 2: Infrastructure
│   ├── Services Generator (Business Logic)
│   └── Clients Generator (API Communication)
├── Layer 3: Data Management
│   ├── Hooks Generator (React Hooks)
│   └── Stores Generator (State Management)
├── Layer 4: Presentation
│   └── Components Generator (React Components)
└── Shared Infrastructure
    ├── Base Generator (Common Functionality)
    └── Domain Mapping (Entity-Domain Relations)
```

### Generation Layers

**Layer 1 - Foundation**: Types and interfaces that define the data structures

**Layer 2 - Infrastructure**: Services and API clients that handle business logic and communication

**Layer 3 - Data Management**: Hooks and stores that manage state and data flow

**Layer 4 - Presentation**: React components that render the user interface

---

## Core Components

### Frontend Orchestrator (`frontend_orchestrator.py`)

**Purpose**: Main coordinator that orchestrates the entire generation process and manages dependencies between generators.

#### Class: `FrontendOrchestrator`

**Methods**:

**`__init__(self, frontend_path: str = "../frontend-v2")`**
- Initializes all specialized generators
- Sets up domain mapping system
- Establishes backend configuration loading

**`create_directory_structure(self)`**
- Creates complete domain-driven directory structure
- Generates all necessary directories based on domain mapping
- Uses `DomainMapping.get_directory_structure()` for completeness

**`generate_all_domains(self)`**
- **Main Generation Process**: Orchestrates complete frontend generation
- **Process Flow**:
  1. Load backend configuration
  2. Share config with all generators
  3. Create directory structure
  4. Generate common types
  5. Group endpoints by domains
  6. Generate each domain in priority order:
     - **Priority 1**: Types (Foundation)
     - **Priority 2**: Services (Infrastructure)
     - **Priority 3**: Hooks (Data Layer)
     - **Priority 4**: Components (Presentation)
  7. Generate domain clients
  8. Generate global stores
  9. Generate React entry files
  10. Create index files for exports

**`generate_specific_domain(self, domain: str)`**
- Generates files for a single domain
- Useful for incremental updates
- Validates domain exists before generation

**`list_available_domains(self)`**
- Lists all available domains from backend configuration
- Shows endpoint counts per domain
- Useful for understanding project structure

### Base Generator (`base_generator.py`)

**Purpose**: Provides common functionality shared across all specialized generators.

#### Class: `BaseFrontendGenerator`

**Core Methods**:

**`load_backend_config(self, config_path: str = "backend_config.json")`**
- Loads backend API contract
- Validates configuration structure
- Makes config available to all generators

**`get_src_path(self) -> Path`**
- Returns standardized src path
- Ensures consistent path resolution

**`write_file(self, file_path: Path, content: str)`**
- Writes content to file with logging
- Creates parent directories automatically
- Provides generation feedback

**`get_entity_name(self, endpoint_name: str) -> str`**
- Extracts entity name from endpoint configuration
- Handles naming inconsistencies (e.g., `Learningpath` → `LearningPath`)
- Returns `None` for invalid endpoints

**`get_api_base_path(self, endpoint_name: str, endpoint_config: Dict[str, Any]) -> str`**
- Generates API base paths for endpoints
- Special handling for auth endpoints (`/api/auth`)
- Converts snake_case to camelCase for consistency

**Utility Methods**:
- **`_snake_to_camel_case(self, snake_str: str) -> str`**: Converts naming conventions
- **`capitalize_domain(self, domain: str) -> str`**: PascalCase conversion (e.g., 'ai-opponents' → 'AiOpponents')
- **`camel_case_domain(self, domain: str) -> str`**: camelCase conversion (e.g., 'ai-opponents' → 'aiOpponents')

### Domain Mapping (`domain_mapping.py`)

**Purpose**: Manages the relationship between backend endpoints and frontend domains, ensuring proper organization.

#### Class: `DomainMapping`

**Configuration**:
```python
domain_mapping = {
    'auth': 'auth',
    'users': 'users', 
    'sessions': 'sessions',
    'profiles': 'profiles',
    'puzzles': 'puzzles',
    'games': 'games',
    'stats': 'stats',
    'learning': 'learning',
    # ... 22+ total mappings
}
```

**Methods**:

**`get_domain_for_endpoint(self, endpoint_name: str) -> str`**
- Maps endpoint names to domain classifications
- Returns 'common' for unmapped endpoints
- Ensures consistent domain organization

**`group_endpoints_by_domain(self, endpoints: Dict[str, any]) -> Dict[str, List[str]]`**
- Groups all endpoints by their assigned domains
- Creates domain-based endpoint collections
- Essential for domain-driven generation

**`get_directory_structure(self) -> List[str]`**
- Returns complete directory structure for all domains
- Includes both common and domain-specific directories
- Used by orchestrator for directory creation

**Domain Directory Structure**:
```python
# Per domain:
f"types/{domain}"
f"utils/{domain}"  
f"constants/{domain}"
f"services/{domain}"
f"hooks/{domain}"
f"components/{domain}"

# Common:
"types/common"
"utils/common"
"clients"
"stores"
"providers"
"components/ui"
```

---

## Domain-Driven Structure

The Frontend Generator V4 organizes code by business domains rather than technical layers, promoting better maintainability and feature isolation.

### Domain Organization

**Domain Classification**:
- **Auth Domain**: Authentication, authorization, user management
- **Chess Domains**: Puzzles, games, analysis, openings, endgames
- **Learning Domains**: Tutorials, learning paths, modules, study plans
- **Progress Domains**: Stats, progress tracking, achievements, analytics
- **Content Domains**: Historic games, reviews, help, subscriptions

### Domain Directory Structure

Each domain gets its own directory structure:

```
src/
├── types/
│   ├── common/           # Shared types
│   ├── auth/            # Auth domain types
│   ├── puzzles/         # Puzzle domain types
│   └── games/           # Game domain types
├── services/
│   ├── auth/            # Auth business logic
│   ├── puzzles/         # Puzzle operations
│   └── games/           # Game management
├── hooks/
│   ├── auth/            # Auth React hooks
│   ├── puzzles/         # Puzzle data hooks
│   └── games/           # Game state hooks
├── components/
│   ├── auth/            # Auth UI components
│   ├── puzzles/         # Puzzle components
│   └── games/           # Game components
├── clients/             # API clients (shared)
└── stores/              # Global state (shared)
```

### Benefits of Domain-Driven Structure

1. **Feature Isolation**: Each domain is self-contained
2. **Team Collaboration**: Different teams can work on different domains
3. **Maintainability**: Changes in one domain don't affect others
4. **Scalability**: Easy to add new domains without restructuring
5. **Testing**: Domain-focused testing strategies

---

## Generation System

### Generation Priority

The system generates files in a specific order to ensure dependencies are resolved correctly:

**Priority 1 - Foundation Layer**:
- Common types (shared interfaces)
- Domain-specific types
- TypeScript definitions

**Priority 2 - Infrastructure Layer**:
- Base API client
- Domain-specific API clients
- Service layer classes

**Priority 3 - Data Layer**:
- React hooks for data fetching
- State management stores
- Data transformation utilities

**Priority 4 - Presentation Layer**:
- React components
- UI components
- Main application files

### Configuration Integration

The generation system reads `backend_config.json` to understand:
- Available endpoints and their methods
- Entity properties and data types
- Authentication requirements
- API path structures

**Example Backend Config Usage**:
```python
# Extract entity information
endpoint_config = backend_config['endpoints']['puzzles']
entity = endpoint_config['entity']  # "Puzzle"
properties = endpoint_config['properties']  # {"id": "string", "fen": "string", ...}
api_endpoints = endpoint_config['endpoints']  # [{"method": "GET", "path": "/", ...}]
```

### File Generation Process

For each domain, the system:

1. **Analyzes Endpoints**: Determines what types, services, and components are needed
2. **Generates Types**: Creates TypeScript interfaces from entity properties
3. **Creates Services**: Builds business logic classes with proper methods
4. **Builds Clients**: Generates API client methods from endpoint definitions
5. **Creates Hooks**: Generates React hooks for data management
6. **Builds Components**: Creates React components with proper integration
7. **Exports Everything**: Creates index files for easy imports

---

## Module Generators

### Types Generator (`types_generator.py`)

**Purpose**: Generates TypeScript type definitions for all domains and common interfaces.

#### Key Methods

**`generate_common_types(self)`**
- Creates shared type definitions used across all domains
- **Generated Types**:
  - `ApiResponse<T>`: Standard API response wrapper
  - `PaginatedResponse<T>`: Paginated data response
  - `LoadingState`: Loading state enumeration
  - `DomainState<T>`: Generic domain state interface
  - `UseQueryResult<T>`: React query hook result type
  - `UseMutationResult<T, V>`: React mutation hook result type

**Common Types Example**:
```typescript
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface DomainState<T = any> {
  items: T[];
  selectedItem: T | null;
  loading: LoadingState;
  error: string | null;
}
```

**`generate_domain_types(self, domain: str, endpoints: List[str])`**
- Generates domain-specific TypeScript types
- Creates entity interfaces from backend properties
- **Generated Interfaces**:
  - Base entity interfaces (e.g., `Puzzle`, `Game`)
  - Response types (e.g., `PuzzleResponse`)
  - Request types (e.g., `CreatePuzzleRequest`, `UpdatePuzzleRequest`)
  - Domain-specific frontend types

**Type Generation Logic**:
```python
# Generate base entity interface
base_interface = [f"export interface {entity} {{"]
for prop_name, prop_type in properties.items():
    ts_type = self._convert_to_typescript_type(prop_type)
    base_interface.append(f"  {prop_name}: {ts_type};")
base_interface.append("}")

# Use utility types for efficiency
backend_types.append(f"export type {entity}Response = {entity};")
backend_types.append(f"export type Create{entity}Request = Omit<{entity}, 'id' | 'created_at' | 'updated_at'>;")
backend_types.append(f"export type Update{entity}Request = Partial<Create{entity}Request>;")
```

**Special Domain Types**:

**Auth Domain**:
```typescript
export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated' | 'error';

export interface AuthState {
  status: AuthStatus;
  user: UserInfo | null;
  token: string | null;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}
```

**Chess Domain**:
```typescript
export type GameStatus = 'idle' | 'active' | 'paused' | 'completed' | 'abandoned';

export interface ChessPosition {
  rank: number;
  file: string;
}

export interface PuzzleFilters {
  minRating?: number;
  maxRating?: number;
  themes?: string[];
  limit?: number;
}
```

### Services Generator (`services_generator.py`)

**Purpose**: Creates business logic service classes for domain operations.

#### Key Methods

**`generate_domain_services(self, domain: str, endpoints: List[str])`**
- Creates service classes for domain business logic
- Generates specialized services for auth and chess domains
- Creates generic services for other domains

**Base Service Structure**:
```typescript
export class PuzzlesService {
  static async healthCheck(): Promise<any> {
    try {
      return { success: true, data: { status: 'healthy', domain: 'puzzles' } };
    } catch (error) {
      throw new Error('puzzles service health check failed');
    }
  }
}
```

**Auth Service (Specialized)**:
```typescript
export class AuthService {
  private static client = new AuthAPIClient();

  static async login(credentials: { email: string; password: string }): Promise<ApiResponse<any>> {
    return this.client.login(credentials);
  }

  static async register(userData: { username: string; email: string; password: string }): Promise<ApiResponse<any>> {
    return this.client.register(userData);
  }

  static async getCurrentUser(): Promise<ApiResponse<any>> {
    return this.client.getCurrentUser();
  }
  // ... more auth methods
}
```

**Chess Service (Specialized)**:
```typescript
export class ChessService {
  private static client = new ChessAPIClient();

  static async getNextPuzzle(filters?: any): Promise<ApiResponse<any>> {
    return this.client.getNextPuzzle(filters);
  }

  static async solvePuzzle(id: string, solution: any): Promise<ApiResponse<any>> {
    return this.client.solvePuzzle(id, solution);
  }

  static async createGame(gameData: any): Promise<ApiResponse<any>> {
    return this.client.createGame(gameData);
  }
  // ... more chess methods
}
```

### Hooks Generator (`hooks_generator.py`)

**Purpose**: Generates React hooks for data management and API interaction.

#### Key Methods

**`generate_domain_hooks(self, domain: str, endpoints: List[str])`**
- Creates three types of hooks per domain:
  1. **Main Hook**: General domain operations
  2. **Query Hook**: GET operations and data fetching
  3. **Mutations Hook**: POST/PUT/DELETE operations

**Main Domain Hook Example**:
```typescript
export const usePuzzles = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzlesAPIClient();

  const getNextPuzzle = async (...args: any[]) => {
    setLoading(true);
    setError(null);
    try {
      const result = await (client.getNextPuzzle as any)(...args);
      console.log('getNextPuzzle result:', result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'getNextPuzzle failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    clearError: () => setError(null),
    client,
    getNextPuzzle
  };
};
```

**Query Hook Example**:
```typescript
export const usePuzzlesQueries = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const client = new PuzzlesAPIClient();

  const refetch = async (params?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Fetching puzzles data using getAllPuzzles');
      const result = await (client.getAllPuzzles as any)(params);
      setData(result);
    } catch (err: any) {
      const errorMessage = err.message || 'Query failed';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refetch();
  }, []);
  
  return {
    data,
    loading,
    error,
    refetch
  };
};
```

**Mutations Hook Example**:
```typescript
export const usePuzzlesMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzlesAPIClient();

  const mutate = async (data: any, id?: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log('Mutating puzzles data using solvePuzzle:', data);
      const result = await (client.solvePuzzle as any)(id || data, data);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Mutation failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    error,
    mutate
  };
};
```

### Components Generator (`components_generator.py`)

**Purpose**: Creates React components for each domain with proper integration.

#### Key Methods

**`generate_domain_components(self, domain: str, endpoints: List[str])`**
- Creates React components for each entity in the domain
- Integrates with domain hooks for data management
- Generates responsive, accessible UI components

**Component Structure Example**:
```typescript
import React, { useEffect } from 'react';
import { usePuzzlesQueries } from '../../hooks/puzzles';

interface PuzzleComponentProps {
  className?: string;
}

export const PuzzleComponent: React.FC<PuzzleComponentProps> = ({
  className
}) => {
  const { data, loading, error, refetch } = usePuzzlesQueries();
  
  useEffect(() => {
    refetch();
  }, []);
  
  const renderTable = () => {
    if (!data?.data || !Array.isArray(data.data)) {
      return <p>No data available</p>;
    }
    
    const items = data.data;
    const columns = Object.keys(items[0]);
    
    return (
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {columns.map((col: string) => (
              <th key={col} style={{ 
                border: '1px solid #ddd', 
                padding: '8px',
                backgroundColor: '#f5f5f5'
              }}>
                {col.charAt(0).toUpperCase() + col.slice(1).replace(/_/g, ' ')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((item: any, index: number) => (
            <tr key={item.id || index}>
              {columns.map((col: string) => (
                <td key={col} style={{ 
                  border: '1px solid #ddd', 
                  padding: '8px'
                }}>
                  {typeof item[col] === 'object' ? JSON.stringify(item[col]) : String(item[col] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };
  
  return (
    <div className={`puzzle-component ${className || ''}`}>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <h2>Puzzle Data</h2>
        <button onClick={() => refetch()} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
      
      {error && (
        <div style={{ color: 'red', backgroundColor: '#ffebee', padding: '12px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {loading && !data && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Loading puzzle data...</p>
        </div>
      )}
      
      {!loading && renderTable()}
    </div>
  );
};
```

**`generate_main_entry_files(self)`**
- Creates `main.tsx` (React entry point)
- Generates `App.tsx` with authentication and domain sections
- Creates CSS files for styling

**App.tsx Features**:
- Authentication integration
- Dynamic domain sections
- Auto-login with demo credentials
- Error handling and loading states
- Responsive design

### Clients Generator (`clients_generator.py`)

**Purpose**: Creates API client classes for communicating with backend endpoints.

#### Key Methods

**`generate_domain_clients(self)`**
- Creates base HTTP client for common functionality
- Generates domain-specific API clients
- Creates unified client index for convenience

**Base API Client**:
```typescript
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
```

**Domain Client Generation**:
```python
def _generate_client_method(self, method: str, path: str, handler: str, entity: str, base_path: str) -> str:
    if method == 'get' and '/:id' in path:
        return f"""  async {handler}(id: string): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}/${{id}}`);
  }}"""
    
    elif method == 'post':
        return f"""  async {handler}(data: any): Promise<ApiResponse<any>> {{
    return this.request<any>(`{base_path}{path}`, {{
      method: 'POST',
      body: JSON.stringify(data),
    }});
  }}"""
    # ... more method patterns
```

**Unified Client System**:
```typescript
export class APIClient {
  public readonly auth = new AuthAPIClient();
  public readonly puzzles = new PuzzlesAPIClient();
  public readonly games = new GamesAPIClient();
  // ... all domain clients
}

export const apiClient = new APIClient();
```

### Stores Generator (`stores_generator.py`)

**Purpose**: Creates Zustand stores for global state management.

#### Key Methods

**`generate_domain_stores(self)`**
- Creates authentication store with persistence
- Generates domain-specific stores as needed
- Creates store index for exports

**Auth Store Example**:
```typescript
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
      // ... more methods
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
```

---

## Usage Guide

### Prerequisites

1. **Backend Configuration**: Ensure `backend_config.json` exists and is valid
2. **Python Environment**: Python 3.7+ with required dependencies
3. **Frontend Directory**: Target frontend directory structure

### Basic Usage

**Generate Complete Frontend**:
```bash
cd tools
python frontend_generator_v4.py
```

**Generate Specific Domain**:
```bash
python frontend_generator_v4.py --domain auth
python frontend_generator_v4.py --domain puzzles
```

**List Available Domains**:
```bash
python frontend_generator_v4.py --list
```

**Custom Frontend Path**:
```bash
python frontend_generator_v4.py --frontend-path ./my-frontend
```

### Configuration Integration

The generator reads from `backend_config.json` to understand:
- Entity structures and properties
- API endpoints and methods
- Authentication requirements
- Domain relationships

**Example Backend Config Structure**:
```json
{
  "endpoints": {
    "puzzles": {
      "entity": "Puzzle",
      "entities": "puzzles",
      "table_name": "puzzles",
      "properties": {
        "id": "string",
        "fen": "string",
        "solution_moves": "string",
        "themes": "string",
        "rating": "number",
        "description": "string"
      },
      "methods": ["getNextPuzzle", "solvePuzzle", "getPuzzleHint"],
      "endpoints": [
        {
          "method": "GET",
          "path": "/next",
          "handler": "getNextPuzzle",
          "auth_required": true
        }
      ]
    }
  }
}
```

### Generated File Structure

After generation, you'll have:

```
frontend-v2/
├── src/
│   ├── types/
│   │   ├── common/index.ts       # Shared types
│   │   ├── auth/index.ts         # Auth domain types  
│   │   ├── puzzles/index.ts      # Puzzle domain types
│   │   └── index.ts              # Main types export
│   ├── services/
│   │   ├── auth/AuthService.ts   # Auth business logic
│   │   ├── puzzles/PuzzlesService.ts
│   │   └── index.ts
│   ├── hooks/
│   │   ├── auth/useAuth.ts       # Auth hooks
│   │   ├── puzzles/usePuzzles.ts # Puzzle hooks
│   │   └── index.ts
│   ├── components/
│   │   ├── auth/AuthComponent.tsx
│   │   ├── puzzles/PuzzleComponent.tsx
│   │   └── index.ts
│   ├── clients/
│   │   ├── BaseAPIClient.ts      # Base HTTP client
│   │   ├── AuthAPIClient.ts      # Auth API client
│   │   ├── PuzzlesAPIClient.ts   # Puzzles API client
│   │   └── index.ts
│   ├── stores/
│   │   ├── authStore.ts          # Auth state management
│   │   └── index.ts
│   ├── App.tsx                   # Main app component
│   ├── main.tsx                  # React entry point
│   ├── App.css                   # Styles
│   ├── index.css
│   └── vite-env.d.ts            # Type declarations
```

### Integration with React App

**Using Generated Hooks**:
```typescript
import { usePuzzlesQueries, usePuzzlesMutations } from '../hooks/puzzles';

function PuzzlePage() {
  const { data, loading, error, refetch } = usePuzzlesQueries();
  const { mutate } = usePuzzlesMutations();

  const handleSolvePuzzle = async (puzzleId: string, solution: any) => {
    try {
      await mutate({ puzzleId, solution });
      refetch(); // Refresh data after mutation
    } catch (error) {
      console.error('Failed to solve puzzle:', error);
    }
  };

  return (
    <div>
      {/* Component JSX */}
    </div>
  );
}
```

**Using API Clients Directly**:
```typescript
import { apiClient } from '../clients';

async function customOperation() {
  try {
    const response = await apiClient.puzzles.getNextPuzzle({ difficulty: 'medium' });
    console.log('Next puzzle:', response.data);
  } catch (error) {
    console.error('Failed to get puzzle:', error);
  }
}
```

**Using Stores**:
```typescript
import { useAuthStore } from '../stores';

function LoginComponent() {
  const { status, user, login, logout, error } = useAuthStore();

  const handleLogin = async (credentials: LoginCredentials) => {
    try {
      await login(credentials);
      // User is now logged in, store is updated automatically
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div>
      {status === 'authenticated' ? (
        <div>Welcome, {user?.username}!</div>
      ) : (
        <LoginForm onSubmit={handleLogin} />
      )}
    </div>
  );
}
```

---

## Advanced Features

### Environment Configuration

The generator supports environment-based configuration:

**Environment Variables**:
```bash
# .env file in frontend directory
VITE_API_BASE_URL=http://localhost:3001
VITE_APP_NAME="Chess Platform"
```

**Generated Environment Integration**:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001';
```

### Type Safety Features

**Generic Type System**:
```typescript
// Generated hooks with proper typing
export const usePuzzlesQueries = <T = PuzzleResponse[]>() => {
  const [data, setData] = useState<T | null>(null);
  // ...
};

// API clients with response typing
async getNextPuzzle(filters?: PuzzleFilters): Promise<ApiResponse<PuzzleResponse>> {
  return this.request<PuzzleResponse>(`/api/puzzles/next`);
}
```

**Utility Types**:
```typescript
// Generated from backend properties
export type CreatePuzzleRequest = Omit<Puzzle, 'id' | 'created_at' | 'updated_at'>;
export type UpdatePuzzleRequest = Partial<CreatePuzzleRequest>;

// Domain state management
export type PuzzlesState = DomainState<PuzzleResponse>;
```

### Authentication Integration

**Token Management**:
```typescript
// Automatic token handling in BaseAPIClient
const token = localStorage.getItem('auth_token');
if (token) {
  defaultHeaders.Authorization = `Bearer ${token}`;
}
```

**Protected Routes**:
```typescript
// Generated components check auth status
const { status } = useAuthStore();

if (status !== 'authenticated') {
  return <LoginRequired />;
}
```

**Auth Store Persistence**:
```typescript
// Auth state persists across browser sessions
export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({ /* store logic */ }),
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
```

### Error Handling

**API Error Handling**:
```typescript
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
```

**Component Error Boundaries**:
```typescript
{error && (
  <div style={{
    color: 'red', 
    backgroundColor: '#ffebee', 
    padding: '12px', 
    borderRadius: '4px'
  }}>
    <strong>Error:</strong> {error}
  </div>
)}
```

**Hook Error Management**:
```typescript
const [error, setError] = useState<string | null>(null);

const clearError = () => setError(null);

return {
  error,
  clearError,
  // ... other hook returns
};
```

### Performance Optimizations

**Code Splitting by Domain**:
```typescript
// Each domain can be lazy-loaded
const PuzzlesComponent = lazy(() => import('./components/puzzles'));
const GamesComponent = lazy(() => import('./components/games'));
```

**Efficient Type Generation**:
```python
# Uses TypeScript utility types for efficiency
backend_types.append(f"export type {entity}Response = {entity};")
backend_types.append(f"export type Create{entity}Request = Omit<{entity}, 'id' | 'created_at' | 'updated_at'>;")
```

**Optimized API Clients**:
```typescript
// Single base client, extended by domains
export class PuzzlesAPIClient extends BaseAPIClient {
  // Domain-specific methods
}
```

---

## Best Practices

### Domain Organization

**Keep Domains Focused**: Each domain should have a single responsibility
```python
# Good domain separation
'auth': ['login', 'register', 'logout']
'puzzles': ['getNextPuzzle', 'solvePuzzle', 'getPuzzleHint']
'games': ['createGame', 'updateGame', 'analyzeGame']

# Avoid mixing concerns
# Don't put auth methods in puzzles domain
```

**Consistent Naming**: Use consistent naming patterns across domains
```python
# Good naming patterns
f"use{domain_capitalized}"           # Main hook
f"use{domain_capitalized}Queries"   # Query hook
f"use{domain_capitalized}Mutations" # Mutation hook
f"{domain_capitalized}APIClient"    # API client
f"{domain_capitalized}Service"      # Service class
```

### Type Safety

**Use Specific Types**: Avoid `any` in generated code when possible
```typescript
// Generated types should be specific
export interface PuzzleResponse {
  id: string;
  fen: string;
  solution_moves: string[];
  rating: number;
}

// Not generic any
export interface PuzzleResponse {
  [key: string]: any;
}
```

**Leverage Utility Types**: Use TypeScript utility types for maintainability
```typescript
// Good - uses utility types
export type CreatePuzzleRequest = Omit<Puzzle, 'id' | 'created_at' | 'updated_at'>;
export type UpdatePuzzleRequest = Partial<CreatePuzzleRequest>;

// Avoid - explicit interfaces that duplicate properties
export interface CreatePuzzleRequest {
  fen: string;
  solution_moves: string[];
  themes: string[];
  rating: number;
  description: string;
}
```

### Component Architecture

**Single Responsibility**: Each component should focus on one entity or operation
```typescript
// Good - focused component
export const PuzzleComponent: React.FC<PuzzleComponentProps> = ({ className }) => {
  // Only handles puzzle-related operations
};

// Avoid - mixed responsibilities
export const PuzzleGameComponent = () => {
  // Handles both puzzles AND games - too broad
};
```

**Hook Integration**: Use generated hooks for data management
```typescript
// Good - uses generated hooks
const { data, loading, error, refetch } = usePuzzlesQueries();
const { mutate } = usePuzzlesMutations();

// Avoid - direct API calls in components
const response = await apiClient.puzzles.getNextPuzzle();
```

### API Integration

**Use Base Client**: Extend the base client for consistency
```typescript
// Good - extends base client
export class PuzzlesAPIClient extends BaseAPIClient {
  async getNextPuzzle(filters?: PuzzleFilters): Promise<ApiResponse<PuzzleResponse>> {
    return this.request<PuzzleResponse>('/api/puzzles/next');
  }
}

// Avoid - standalone client
export class PuzzlesAPIClient {
  async getNextPuzzle() {
    // Duplicates auth, error handling, etc.
  }
}
```

**Error Handling**: Implement consistent error handling patterns
```typescript
// Good - consistent error handling
try {
  const result = await client.method(...args);
  return result;
} catch (err: any) {
  const errorMessage = err.message || 'Operation failed';
  setError(errorMessage);
  throw err;
}
```

### State Management

**Use Appropriate State**: Choose between local state, domain stores, and global stores
```typescript
// Local component state
const [loading, setLoading] = useState(false);

// Domain-specific operations
const { data, refetch } = usePuzzlesQueries();

// Global user state
const { user, logout } = useAuthStore();
```

**Persist Important State**: Use persistence for critical state like authentication
```typescript
// Good - auth state persists
export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({ /* store logic */ }),
    { name: 'auth-store' }
  )
);
```

---

## Troubleshooting

### Common Issues

#### 1. Backend Config Not Found

**Error**: `FileNotFoundError: backend_config.json not found`

**Causes**:
- Missing backend configuration file
- Incorrect path to configuration
- Invalid JSON format

**Solutions**:
```bash
# Check if file exists
ls -la backend_config.json

# Validate JSON format
python -m json.tool backend_config.json

# Specify custom config path
python frontend_generator_v4.py --config-path ./custom_config.json
```

#### 2. Domain Not Found

**Error**: `Domain 'custom-domain' not found in available domains`

**Cause**: Specified domain doesn't exist in domain mapping

**Solution**: Check available domains
```bash
python frontend_generator_v4.py --list
```

Add domain to `domain_mapping.py`:
```python
self.domain_mapping = {
    # ... existing mappings
    'custom-domain': 'custom-domain'
}
```

#### 3. Missing Entity Properties

**Error**: Generated types are empty or missing properties

**Cause**: Backend config missing `properties` field

**Solution**: Verify backend config structure
```json
{
  "endpoints": {
    "puzzles": {
      "entity": "Puzzle",
      "properties": {
        "id": "string",
        "fen": "string",
        "rating": "number"
      }
    }
  }
}
```

#### 4. API Client Compilation Errors

**Error**: TypeScript compilation errors in generated clients

**Causes**:
- Missing imports
- Type mismatches
- Incorrect API paths

**Solutions**:
- Check generated imports match available types
- Verify API paths match backend routes
- Ensure entity names are consistent

#### 5. Authentication Issues

**Error**: API calls return 401 Unauthorized

**Causes**:
- Missing auth token
- Expired token
- Incorrect token format

**Solutions**:
```typescript
// Check token exists
const token = localStorage.getItem('auth_token');
console.log('Auth token:', token);

// Verify token format
// Should be: Bearer <jwt-token>

// Test authentication
const authStore = useAuthStore();
console.log('Auth status:', authStore.status);
```

### Debugging Techniques

#### Generator Debugging

**Add Logging**: Add debug prints to generators
```python
# In generator methods
print(f"Generating {domain} with endpoints: {endpoints}")
print(f"Entity config: {endpoint_config}")
```

**Validate Configuration**: Check config parsing
```python
def debug_config(self):
    print("Backend config endpoints:")
    for name, config in self.backend_config['endpoints'].items():
        print(f"  {name}: {config.get('entity', 'No entity')}")
```

**File Generation Tracking**: Monitor file creation
```python
def write_file(self, file_path: Path, content: str):
    self.ensure_directory(file_path.parent)
    file_path.write_text(content)
    print(f"📝 Generated {file_path} ({len(content)} chars)")
```

#### Frontend Debugging

**API Client Testing**: Test API calls directly
```typescript
// In browser console
const client = new PuzzlesAPIClient();
client.getNextPuzzle().then(console.log).catch(console.error);
```

**Hook State Inspection**: Debug hook state
```typescript
export const usePuzzlesQueries = () => {
  const [data, setData] = useState<any>(null);
  
  // Debug logging
  console.log('usePuzzlesQueries state:', { data, loading, error });
  
  return { data, loading, error };
};
```

**Store State Monitoring**: Monitor store changes
```typescript
const authStore = useAuthStore();
console.log('Auth store state:', {
  status: authStore.status,
  user: authStore.user,
  token: !!authStore.token
});
```

### Performance Issues

#### Large Configuration Files

**Problem**: Generation is slow with large backend configs

**Solutions**:
- Generate specific domains instead of all domains
- Optimize type generation with utility types
- Use incremental generation for development

```bash
# Generate only changed domains
python frontend_generator_v4.py --domain puzzles
python frontend_generator_v4.py --domain games
```

#### Memory Usage

**Problem**: Generator uses too much memory

**Solutions**:
- Process domains sequentially instead of loading all at once
- Clear intermediate data structures
- Use generators instead of lists for large datasets

#### Compilation Speed

**Problem**: TypeScript compilation is slow

**Solutions**:
- Use TypeScript project references
- Optimize type imports
- Use incremental compilation

```typescript
// Instead of importing everything
import * from '../types/puzzles';

// Import only what you need
import type { PuzzleResponse, CreatePuzzleRequest } from '../types/puzzles';
```

---

## Extension Guide

### Adding New Domains

**Step 1**: Add to Domain Mapping
```python
# In domain_mapping.py
self.domain_mapping = {
    # ... existing mappings
    'custom-entity': 'custom-domain'
}
```

**Step 2**: Add to Backend Config
```json
{
  "endpoints": {
    "custom-entity": {
      "entity": "CustomEntity",
      "entities": "custom_entities",
      "properties": {
        "id": "string",
        "name": "string",
        "custom_field": "number"
      },
      "endpoints": [
        {
          "method": "GET",
          "path": "/",
          "handler": "getAllCustomEntities"
        }
      ]
    }
  }
}
```

**Step 3**: Generate the Domain
```bash
python frontend_generator_v4.py --domain custom-domain
```

### Custom Generator Methods

**Add Specialized Service Generator**:
```python
# In services_generator.py
def _generate_custom_service_content(self) -> str:
    return """import { CustomAPIClient } from '../../clients/CustomAPIClient';
    
export class CustomService {
  private static client = new CustomAPIClient();
  
  static async customOperation(data: any): Promise<any> {
    return this.client.customOperation(data);
  }
}"""

# In generate_domain_services method
elif domain == 'custom-domain':
    custom_service_content = self._generate_custom_service_content()
    custom_file = services_path / "CustomService.ts"
    self.write_file(custom_file, custom_service_content)
    generated_services.append('CustomService')
```

**Add Custom Hook Patterns**:
```python
# In hooks_generator.py
def _generate_custom_hook_content(self, domain: str) -> str:
    return f"""import {{ useState, useEffect }} from 'react';
import {{ {self.capitalize_domain(domain)}APIClient }} from '../../clients/{self.capitalize_domain(domain)}APIClient';

export const use{self.capitalize_domain(domain)}Custom = () => {{
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  
  const customOperation = async (params: any) => {{
    setLoading(true);
    try {{
      const client = new {self.capitalize_domain(domain)}APIClient();
      const result = await client.customOperation(params);
      setData(result);
      return result;
    }} catch (error) {{
      console.error('Custom operation failed:', error);
      throw error;
    }} finally {{
      setLoading(false);
    }}
  }};
  
  return {{
    data,
    loading,
    customOperation
  }};
}};"""
```

### Custom Component Templates

**Override Component Generation**:
```python
# In components_generator.py
def _generate_custom_component_content(self, domain: str, entity: str) -> str:
    return f"""import React from 'react';
import {{ use{entity}Custom }} from '../../hooks/{domain}';

interface {entity}CustomProps {{
  customProp?: string;
}}

export const {entity}Custom: React.FC<{entity}CustomProps> = ({{ customProp }}) => {{
  const {{ data, loading, customOperation }} = use{entity}Custom();
  
  return (
    <div className="{entity.lower()}-custom">
      <h3>{entity} Custom Component</h3>
      {{/* Custom component logic */}}
    </div>
  );
}};"""

# Use in generate_domain_components
if domain == 'custom-domain':
    component_content = self._generate_custom_component_content(domain, entity)
```

### Adding New Generator Types

**Create New Generator Module**:
```python
# utils_generator.py
from base_generator import BaseFrontendGenerator

class UtilsGenerator(BaseFrontendGenerator):
    """Generates utility functions for domains"""
    
    def generate_domain_utils(self, domain: str, endpoints: List[str]):
        src_path = self.get_src_path()
        utils_path = src_path / "utils" / domain
        
        utils_content = self._generate_utils_content(domain)
        utils_file = utils_path / f"{domain}Utils.ts"
        self.write_file(utils_file, utils_content)
    
    def _generate_utils_content(self, domain: str) -> str:
        return f"""// {domain.capitalize()} domain utilities

export const {domain}Utils = {{
  formatData: (data: any) => {{
    // Format data for {domain}
    return data;
  }},
  
  validateInput: (input: any) => {{
    // Validate {domain} input
    return true;
  }}
}};"""
```

**Integrate with Orchestrator**:
```python
# In frontend_orchestrator.py
from utils_generator import UtilsGenerator

class FrontendOrchestrator(BaseFrontendGenerator):
    def __init__(self, frontend_path: str = "../frontend-v2"):
        super().__init__(frontend_path)
        # ... existing generators
        self.utils_generator = UtilsGenerator(frontend_path)
    
    def generate_all_domains(self):
        # ... existing generation logic
        
        # Add utils generation
        for domain, endpoints in domains.items():
            self.utils_generator.generate_domain_utils(domain, endpoints)
```

### Custom Type Definitions

**Add Domain-Specific Types**:
```python
# In types_generator.py
def _get_custom_domain_types(self, entity: str = None) -> List[str]:
    return [
        "// Custom domain types",
        f"export interface CustomDomainConfig {{",
        f"  apiEndpoint: string;",
        f"  timeout: number;",
        f"  retryCount: number;",
        f"}}",
        "",
        f"export interface CustomDomainState {{",
        f"  config: CustomDomainConfig;",
        f"  isInitialized: boolean;",
        f"}}",
        ""
    ]

# Add to _get_domain_specific_types
special_types = {
    'auth': self._get_auth_types(),
    'chess': self._get_chess_types(),
    'custom-domain': self._get_custom_domain_types()
}
```

---

## Conclusion

The Frontend Generator V4 represents a significant advancement in automated frontend development. Its domain-driven architecture, comprehensive type safety, and modular design make it an powerful tool for creating maintainable, scalable React applications.

**Key Strengths**:
- **Domain-Driven Design**: Promotes better code organization and team collaboration
- **Configuration-Driven**: Eliminates manual coding for standard CRUD operations
- **Type Safety**: Complete TypeScript integration ensures runtime reliability
- **Modular Architecture**: Easy to extend and customize for specific needs
- **Production Ready**: Includes authentication, error handling, and performance optimizations

**Best Use Cases**:
- Rapid prototyping of complex web applications
- Large-scale applications with multiple business domains
- Teams needing consistent frontend architecture patterns
- Projects requiring strong API contract synchronization
- Applications with complex state management requirements

The generator's extensible design ensures it can evolve with project requirements while maintaining its core principles of domain separation, type safety, and developer productivity.