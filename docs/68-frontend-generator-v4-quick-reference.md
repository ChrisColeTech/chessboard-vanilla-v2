# Frontend Generator V4 - Quick Reference

## Overview

Frontend Generator V4 is a domain-driven code generation system that creates complete React/TypeScript frontends from backend configuration. It uses a modular architecture with specialized generators for different layers.

## Location and Structure

```
tools/
├── frontend_generator_v4.py               # Main CLI entry point
└── frontend-tools/                        # Modular components
    ├── frontend_orchestrator.py           # Main coordinator
    ├── base_generator.py                  # Common functionality
    ├── domain_mapping.py                  # Entity-domain relationships
    ├── types_generator.py                 # TypeScript definitions
    ├── services_generator.py              # Business logic
    ├── hooks_generator.py                 # React data hooks
    ├── components_generator.py            # React components
    ├── clients_generator.py               # API clients
    ├── stores_generator.py                # State management
    ├── pages_generator.py                 # Page components
    ├── layout_generator.py                # Layout system
    └── dynamic_system_generator.py        # Dynamic page system
```

## Quick Start Commands

```bash
# Generate complete frontend
cd tools && python frontend_generator_v4.py

# Generate specific domain
python frontend_generator_v4.py --domain auth
python frontend_generator_v4.py --domain puzzles

# List available domains
python frontend_generator_v4.py --list

# Custom frontend path
python frontend_generator_v4.py --frontend-path ./my-frontend
```

## Generation Layers (Priority Order)

1. **Foundation**: Common types (`ApiResponse<T>`, `DomainState<T>`, utility types), domain-specific types (entity interfaces, request/response types)
2. **Infrastructure**: Domain services (business logic classes), API clients (HTTP communication with auth)
3. **Data Management**: React hooks (main, queries, mutations per domain), global stores (Zustand with persistence)
4. **Presentation**: React components (domain-specific with error handling), UI components (DataTable, forms)
5. **Pages**: Full page components (combining multiple domains), navigation integration
6. **Layout**: Application layout system, responsive navigation, routing infrastructure

## Key Features & Critical Details

### Domain-Driven Architecture
- **25+ Domains**: auth, users, puzzles, games, learning, analytics, ai-opponents, historic-games, etc.
- **Organization**: Each domain gets own folders in types/, services/, hooks/, components/, pages/
- **Mapping**: Configurable in `domain_mapping.py`, maps endpoints to logical domains
- **Independence**: Domains are self-contained with clear boundaries

### Configuration-Driven Generation
- **Source**: `backend_config.json` defines entities, properties, endpoints, HTTP methods
- **Type Mapping**: Python types → TypeScript (string→string, number→number, etc.)
- **API Paths**: Auto-generates from entity names with camelCase conversion
- **Auth Handling**: Special handling for auth endpoints and token management

### TypeScript Integration
- **Type Safety**: Complete type coverage across all layers
- **Utility Types**: Uses `Omit<>`, `Partial<>` for efficient type definitions
- **Smart Generation**: 
  - Simple entities: Explicit interfaces
  - Complex entities: Utility type composition
  - Request types: `Omit<Entity, 'id' | 'created_at' | 'updated_at'>`
  - Update types: `Partial<CreateRequest>`

### React Architecture
- **Hook Pattern**: Three hooks per domain
  - `use{Domain}`: Main operations with error handling
  - `use{Domain}Queries`: GET operations with automatic refresh
  - `use{Domain}Mutations`: POST/PUT/DELETE operations
- **Component Integration**: Components use hooks, not direct API calls
- **Error Handling**: Consistent error boundaries and user feedback
- **Loading States**: Built-in loading indicators and state management

## Generated Structure & File Details

```
frontend-v2/src/
├── types/
│   ├── common/index.ts        # ApiResponse<T>, PaginatedResponse<T>, LoadingState, DomainState<T>
│   ├── auth/index.ts          # User, AuthState, LoginCredentials, AuthStatus types
│   ├── puzzles/index.ts       # Puzzle, CreatePuzzleRequest, UpdatePuzzleRequest, PuzzleFilters
│   └── index.ts               # Main exports from all domains
├── services/
│   ├── auth/AuthService.ts    # login(), register(), logout(), getCurrentUser(), refreshToken()
│   ├── puzzles/PuzzlesService.ts # healthCheck() and domain-specific methods
│   └── index.ts               # Service exports
├── hooks/
│   ├── auth/
│   │   ├── useAuth.ts         # Main auth operations (login, logout, token management)
│   │   ├── useAuthQueries.ts  # GET operations (getCurrentUser, profile data)
│   │   └── useAuthMutations.ts # POST operations (register, password change)
│   ├── puzzles/
│   │   ├── usePuzzles.ts      # Main puzzle operations (getNextPuzzle, solvePuzzle)
│   │   ├── usePuzzlesQueries.ts # Data fetching with auto-refresh
│   │   └── usePuzzlesMutations.ts # Puzzle solving, rating updates
│   ├── core/                  # Navigation, routing, infrastructure hooks
│   ├── standalone/            # Utility hooks used across domains
│   └── index.ts               # All hook exports
├── components/
│   ├── auth/AuthComponent.tsx # Login/register UI with form handling
│   ├── puzzles/PuzzleComponent.tsx # Puzzle display with data tables
│   ├── ui/
│   │   ├── DataTable.tsx      # Reusable data table component
│   │   └── Forms.tsx          # Form components and validation
│   ├── chess/                 # Chess-specific UI (board, pieces, notation)
│   └── index.ts               # Component exports
├── pages/
│   ├── auth/AuthPage.tsx      # Complete auth page with navigation
│   ├── chess/ChessPage.tsx    # Combined chess functionality (puzzles + games)
│   ├── learning/LearningPage.tsx # Learning modules and tutorials
│   └── analytics/AnalyticsPage.tsx # Progress tracking and statistics
├── clients/
│   ├── BaseAPIClient.ts       # HTTP client with auth headers, error handling, request method
│   ├── AuthAPIClient.ts       # Extends base, auth-specific endpoints
│   ├── PuzzlesAPIClient.ts    # Puzzle operations (getNextPuzzle, solvePuzzle, etc.)
│   └── index.ts               # Unified APIClient with all domain clients
├── stores/
│   ├── authStore.ts           # Zustand store with persistence (login state, user data)
│   └── index.ts               # Store exports
├── layout/
│   ├── AppLayout.tsx          # Main app wrapper with navigation
│   ├── Navigation.tsx         # Responsive nav menu with domain sections
│   └── MobileLayout.tsx       # Mobile-optimized layout
├── utils/common/              # Shared utilities and constants
├── providers/                 # React context providers
├── App.tsx                    # Main app with auth integration and routing
├── main.tsx                   # React entry point with providers
└── vite-env.d.ts             # TypeScript environment declarations
```

## Core Classes & Methods

### FrontendOrchestrator
- **`generate_all_domains()`**: Complete generation following priority order, handles 50+ endpoints
- **`generate_specific_domain(domain: str)`**: Incremental generation for development
- **`list_available_domains()`**: Shows all domains with endpoint counts
- **`_share_backend_config()`**: Distributes config to all generators
- **`_cleanup_empty_directories()`**: Post-generation cleanup

### BaseFrontendGenerator (Shared Functionality)
- **`load_backend_config(path: str)`**: JSON parsing with validation
- **`get_entity_name(endpoint: str)`**: Entity extraction with name fixes
- **`get_api_base_path(endpoint, config)`**: API path generation with auth handling
- **`capitalize_domain(domain: str)`**: PascalCase conversion (ai-opponents → AiOpponents)
- **`camel_case_domain(domain: str)`**: camelCase conversion (ai-opponents → aiOpponents)

### Domain-Specific Generators
- **TypesGenerator**: 
  - `generate_common_types()`: Shared interfaces across all domains
  - `generate_domain_types(domain, endpoints)`: Entity-specific types with utility type usage
- **ServicesGenerator**: 
  - `generate_domain_services()`: Business logic classes
  - Auth/Chess specialized services with full method implementations
- **HooksGenerator**: 
  - Three hooks per domain pattern
  - Core infrastructure hooks (navigation, error handling)
  - Standalone utility hooks
- **ComponentsGenerator**: 
  - Domain components with hook integration
  - Chess-specific UI components (board, pieces)
  - Reusable UI components (tables, forms)
- **ClientsGenerator**: 
  - BaseAPIClient with auth and error handling
  - Domain-specific clients extending base
  - Unified client with all domain clients
- **PagesGenerator**: 
  - Full page components combining multiple domains
  - Page routing and navigation integration
- **LayoutGenerator**: 
  - Application layout with responsive navigation
  - Mobile/desktop layout variants

## Generated Code Patterns

### TypeScript Types
```typescript
// Base entity interface
export interface Puzzle {
  id: string;
  fen: string;
  solution_moves: string;
  rating: number;
  themes: string[];
}

// Utility type usage for efficiency
export type PuzzleResponse = Puzzle;
export type CreatePuzzleRequest = Omit<Puzzle, 'id' | 'created_at' | 'updated_at'>;
export type UpdatePuzzleRequest = Partial<CreatePuzzleRequest>;

// Domain-specific types
export interface PuzzleFilters {
  minRating?: number;
  maxRating?: number;
  themes?: string[];
}
```

### React Hooks
```typescript
// Main domain hook with error handling
export const usePuzzles = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzlesAPIClient();
  
  const getNextPuzzle = async (filters?: PuzzleFilters) => {
    setLoading(true);
    try {
      return await client.getNextPuzzle(filters);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  
  return { loading, error, getNextPuzzle, clearError: () => setError(null) };
};

// Query hook with auto-refresh
export const usePuzzlesQueries = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const refetch = async () => {
    // Auto-refresh implementation
  };
  
  useEffect(() => { refetch(); }, []);
  return { data, loading, refetch };
};
```

### API Clients
```typescript
// Base client with auth and error handling
export class BaseAPIClient {
  protected async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const token = localStorage.getItem('auth_token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers.Authorization = `Bearer ${token}`;
    
    const response = await fetch(API_BASE_URL + endpoint, { ...options, headers });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }
}

// Domain-specific client
export class PuzzlesAPIClient extends BaseAPIClient {
  async getNextPuzzle(filters?: PuzzleFilters): Promise<ApiResponse<PuzzleResponse>> {
    return this.request<PuzzleResponse>('/api/puzzles/next', {
      method: 'POST',
      body: JSON.stringify(filters || {})
    });
  }
}
```

### Component Integration
```typescript
// Component with hook integration and error handling
export const PuzzleComponent: React.FC = ({ className }) => {
  const { data, loading, error, refetch } = usePuzzlesQueries();
  const { mutate } = usePuzzlesMutations();
  
  if (loading) return <div>Loading puzzles...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  
  return (
    <div className={`puzzle-component ${className}`}>
      <button onClick={refetch}>Refresh</button>
      {/* Data table with dynamic columns */}
    </div>
  );
};
```

## Domain Organization & Mapping

### Major Domain Categories
- **Authentication**: auth (login, register, tokens, user management)
- **Chess Gameplay**: puzzles, games, analysis, openings, endgames
- **Learning System**: learning, tutorials, learning-modules, tutorial-steps, study-plans
- **Progress Tracking**: stats, progress, achievements, analytics
- **Content Management**: historic-games, game-reviews, help, subscriptions
- **AI Features**: ai-opponents (chess AI integration)
- **User Management**: users, profiles, sessions

### Domain Mapping Configuration
Located in `domain_mapping.py` with 25+ endpoint → domain mappings. Each domain gets:
- Own directory structure in each layer
- Specialized generators when needed (auth, chess)
- Independent component and hook ecosystem
- Dedicated API client extending base client

## Authentication & Security

### Auth Flow
- JWT token storage in localStorage
- Automatic token inclusion in API requests
- Token persistence across browser sessions
- Login/logout state management with Zustand
- Protected route handling in components

### API Security
- BaseAPIClient handles auth headers automatically
- Token expiration and refresh logic
- Secure error handling without exposing sensitive data
- HTTPS enforcement and CORS handling

## Error Handling Patterns

### Consistent Error Management
- All hooks return error state and clearError function
- Components display user-friendly error messages
- API errors are logged and transformed for display
- Network errors handled gracefully with retry options
- Form validation errors integrated with UI feedback

### Loading States
- Loading indicators at hook level
- Skeleton loading for data tables
- Button loading states during mutations
- Page-level loading for navigation transitions

## Best Practices & Usage Patterns

### Development Workflow
1. **Add Domain**: Update `domain_mapping.py` and `backend_config.json`
2. **Generate Code**: Run generator for specific domain or full generation
3. **Integration**: Use generated hooks in components, never direct API calls
4. **Customization**: Override generators for specialized functionality
5. **Testing**: Generated code includes error scenarios for testing

### Performance Considerations
- Lazy loading of domain components
- Efficient TypeScript utility type usage
- Single base client shared across domains
- Selective hook usage (don't load all hooks if not needed)
- Component-level error boundaries

### State Management Strategy
- **Local State**: UI-only data (form inputs, modal visibility)
- **Hook State**: Domain-specific operations (API data, loading states)  
- **Global Store**: Cross-domain state (auth, navigation, user preferences)

## Extension Points & Customization

### Adding Custom Domains
1. Add to `domain_mapping.py` configuration
2. Define endpoints in `backend_config.json`
3. Run domain-specific generation
4. Customize generators for specialized needs

### Generator Customization
- Override `_generate_*_content()` methods for custom templates
- Add specialized service methods for complex business logic
- Create custom hook patterns for unique domain requirements
- Implement custom component templates for specific UI needs

### Advanced Features
- Dynamic page generation system for mobile/desktop variants
- Layout customization with responsive navigation
- Custom type definitions for complex domain requirements
- Integration with external APIs and services

## Prerequisites & Requirements

### Environment Setup
- **Python 3.7+**: For running the generator
- **Valid backend_config.json**: Must contain valid endpoint definitions
- **Frontend directory**: Target directory structure for generated code
- **Node.js/npm**: For running the generated React application

### Backend Configuration Format
```json
{
  "endpoints": {
    "puzzles": {
      "entity": "Puzzle",
      "entities": "puzzles",
      "properties": {
        "id": "string",
        "fen": "string",
        "rating": "number"
      },
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

## Related Documentation

- **Comprehensive Guide**: [Frontend Generator V4 Comprehensive Guide](66-frontend-generator-v4-comprehensive-guide.md) - Complete documentation with detailed examples
- **Backend Integration**: [Backend Generator V2 Guide](63-backend-generator-v2-comprehensive-guide.md) - Backend counterpart documentation
- **API Strategy**: [API Integration Plan](60-frontend-api-integration-plan.md) - Integration patterns and best practices