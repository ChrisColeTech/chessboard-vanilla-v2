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
    └── stores_generator.py                # State management
```

## Quick Start

```bash
# Generate complete frontend
cd tools
python frontend_generator_v4.py

# Generate specific domain
python frontend_generator_v4.py --domain auth

# List available domains
python frontend_generator_v4.py --list

# Custom frontend path
python frontend_generator_v4.py --frontend-path ./my-frontend
```

## Generation Layers (Priority Order)

1. **Foundation**: Common types, domain types
2. **Infrastructure**: Services, API clients  
3. **Data Management**: React hooks, stores
4. **Presentation**: React components, main app

## Key Features

- **Domain-Driven**: Organizes by business domains (auth, puzzles, games, etc.)
- **Configuration-Driven**: Reads from `backend_config.json`
- **TypeScript First**: Complete type safety
- **Modular**: Specialized generators for each layer
- **Production Ready**: Authentication, error handling, state management

## Generated Structure

```
frontend-v2/src/
├── types/           # TypeScript definitions by domain
├── services/        # Business logic layer
├── hooks/           # React hooks for data management
├── components/      # React components by domain
├── clients/         # API client classes
├── stores/          # Zustand state management
├── App.tsx          # Main app with auth integration
└── main.tsx         # React entry point
```

## Domain Mapping

25+ domains including:
- `auth` - Authentication and user management
- `puzzles` - Chess puzzles and solving
- `games` - Game creation and management
- `learning` - Learning modules and tutorials
- `analytics` - Progress tracking and stats
- `ai-opponents` - AI game opponents
- `historic-games` - Historical game analysis

## Core Classes

### FrontendOrchestrator
Main coordinator that manages all generators and orchestrates the complete generation process.

### BaseFrontendGenerator  
Shared functionality including config loading, file writing, and domain utilities.

### Domain-Specific Generators
- **TypesGenerator**: Creates TypeScript interfaces and utility types
- **ServicesGenerator**: Business logic classes with specialized auth/chess services
- **HooksGenerator**: Three hooks per domain (main, queries, mutations)
- **ComponentsGenerator**: React components with data integration
- **ClientsGenerator**: API clients extending BaseAPIClient
- **StoresGenerator**: Zustand stores with persistence

## Generated Code Examples

### Types
```typescript
export interface Puzzle {
  id: string;
  fen: string;
  solution_moves: string;
  rating: number;
}

export type CreatePuzzleRequest = Omit<Puzzle, 'id'>;
export type UpdatePuzzleRequest = Partial<CreatePuzzleRequest>;
```

### Hooks
```typescript
export const usePuzzles = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const client = new PuzzlesAPIClient();
  
  const getNextPuzzle = async (...args: any[]) => {
    // Implementation with error handling
  };
  
  return { loading, error, getNextPuzzle, client };
};
```

### API Clients
```typescript
export class PuzzlesAPIClient extends BaseAPIClient {
  async getNextPuzzle(filters?: any): Promise<ApiResponse<any>> {
    return this.request<any>('/api/puzzles/next');
  }
}
```

## Best Practices

- **Domain Focus**: Keep domains single-responsibility
- **Type Safety**: Use specific types, avoid `any`
- **Hook Integration**: Use generated hooks for data management
- **Error Handling**: Implement consistent error patterns
- **State Management**: Local state for UI, stores for global data

## Common Usage Patterns

### Using Generated Hooks
```typescript
const { data, loading, error, refetch } = usePuzzlesQueries();
const { mutate } = usePuzzlesMutations();
```

### API Integration
```typescript
import { apiClient } from '../clients';
const response = await apiClient.puzzles.getNextPuzzle();
```

### Authentication
```typescript
const { status, user, login, logout } = useAuthStore();
```

## Requirements

- Python 3.7+
- Valid `backend_config.json`
- Target frontend directory structure

## Extension Points

- Add new domains to `domain_mapping.py`
- Create specialized service generators
- Custom hook patterns for specific domains
- Override component templates
- Add new generator types

## Related Documentation

- [Frontend Generator V4 Comprehensive Guide](66-frontend-generator-v4-comprehensive-guide.md) - Complete documentation
- [Backend Generator V2 Guide](63-backend-generator-v2-comprehensive-guide.md) - Backend counterpart
- [API Integration Plan](60-frontend-api-integration-plan.md) - Integration strategy