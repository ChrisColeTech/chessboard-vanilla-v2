# Frontend Generator V4 - Comprehensive Guide

## Generator Location and Structure

```
chessboard-vanilla-v2/
├── tools/
│   ├── frontend_generator_v4.py               # Main entry point (lightweight wrapper)
│   └── frontend-tools/                        # Modular generator components
│       ├── __init__.py                        # Package initialization
│       ├── frontend_orchestrator.py           # Main coordinator
│       ├── base_generator.py                  # Common functionality
│       ├── domain_mapping.py                  # Entity-domain relationships
│       ├── types_generator.py                 # TypeScript type definitions
│       ├── services_generator.py              # Business logic services
│       ├── hooks_generator.py                 # React hooks for data management
│       ├── components_generator.py            # React components
│       ├── clients_generator.py               # API client classes
│       ├── stores_generator.py                # Zustand state management
│       ├── pages_generator.py                 # Page components
│       ├── layout_generator.py                # Layout system
│       └── dynamic_system_generator.py        # Dynamic page system
```

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Domain-Driven Structure](#domain-driven-structure)
5. [Generation System](#generation-system)
6. [Module Generators](#module-generators)
7. [Usage Guide](#usage-guide)
8. [Best Practices](#best-practices)
9. [Extension Guide](#extension-guide)

---

## Overview

Frontend Generator V4 is a sophisticated domain-driven code generation system that creates complete React/TypeScript frontends from backend configuration. It follows a modular architecture that generates type-safe, production-ready frontend applications with full API integration, state management, and component architecture.

### Key Features

- **Domain-Driven Architecture**: Organizes code by business domains rather than technical layers
- **Configuration-Driven**: Generates complete frontend from `backend_config.json`
- **TypeScript First**: Complete type safety across all generated components
- **Modular Generation**: Specialized generators for types, services, hooks, components, clients, pages, and layouts
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
│   ├── pages/           # Page components by domain
│   ├── clients/         # API client classes
│   ├── stores/          # Zustand state management
│   ├── utils/           # Utility functions
│   ├── constants/       # Domain constants
│   └── providers/       # React context providers
```

---

## Architecture

The Frontend Generator V4 follows a layered, domain-driven architecture designed for scalability and maintainability:

### Generation Layers

**Priority 1 - Foundation Layer**: Types and interfaces that define data structures
**Priority 2 - Infrastructure Layer**: Services and API clients that handle business logic and communication
**Priority 3 - Data Management Layer**: Hooks and stores that manage state and data flow
**Priority 4 - Presentation Layer**: React components that render the user interface
**Priority 5 - Pages Layer**: Full page components that combine multiple components
**Priority 6 - Layout Layer**: Application layout and navigation structure

---

## Core Components

### Frontend Orchestrator (`frontend_orchestrator.py`)

**Purpose**: Main coordinator that orchestrates the entire generation process and manages dependencies between generators.

#### Class: `FrontendOrchestrator`

**`__init__(frontend_path: str)`**
- Inherits from `BaseFrontendGenerator`
- Initializes `DomainMapping` instance
- Creates all specialized generator instances

**`create_directory_structure()`**
- Creates complete domain-driven directory structure
- Generates all necessary directories based on domain mapping
- Uses `DomainMapping.get_directory_structure()` for completeness

**`generate_all_domains()`**
- Main generation orchestrator that follows priority order
- Loads backend configuration and shares with all generators
- Creates directory structure
- Generates common types first
- Groups endpoints by domains
- Generates each layer in sequence for all domains
- Generates final infrastructure (pages, layouts, dynamic system)

**`generate_specific_domain(domain: str)`**
- Generates files for a single domain only
- Useful for incremental updates and development
- Validates domain exists before generation

**`list_available_domains()`**
- Lists all available domains from backend configuration
- Shows endpoint counts per domain
- Returns list of domain names

**`_share_backend_config()`**
- Distributes backend configuration to all generators

**`_generate_final_indices()`**
- Creates index files for easy imports across all layers

**`_cleanup_empty_directories()`**
- Removes empty directories after generation

### Base Generator (`base_generator.py`)

**Purpose**: Provides common functionality shared across all specialized generators.

#### Class: `BaseFrontendGenerator`

**`load_backend_config(config_path: str)`**
- Loads backend API contract from JSON file
- Validates configuration structure
- Makes config available to all generators

**`get_src_path() -> Path`**
- Returns standardized src path for consistent file placement

**`write_file(file_path: Path, content: str)`**
- Writes content to file with automatic directory creation
- Provides generation feedback and logging

**`get_entity_name(endpoint_name: str) -> str`**
- Extracts entity name from endpoint configuration
- Handles naming inconsistencies (e.g., `Learningpath` → `LearningPath`)

**`get_api_base_path(endpoint_name: str, endpoint_config: Dict) -> str`**
- Generates API base paths for endpoints
- Special handling for auth endpoints
- Converts snake_case to camelCase

**Utility Methods**:
- **`capitalize_domain(domain: str) -> str`**: Converts to PascalCase (e.g., 'ai-opponents' → 'AiOpponents')
- **`camel_case_domain(domain: str) -> str`**: Converts to camelCase (e.g., 'ai-opponents' → 'aiOpponents')
- **`_snake_to_camel_case(snake_str: str) -> str`**: Snake case to camel case conversion

### Domain Mapping (`domain_mapping.py`)

**Purpose**: Manages the relationship between backend endpoints and frontend domains.

#### Class: `DomainMapping`

**Domain Configuration**:
Maintains mapping of 25+ domains including auth, users, puzzles, games, learning modules, analytics, etc.

**`get_domain_for_endpoint(endpoint_name: str) -> str`**
- Maps endpoint names to domain classifications
- Returns 'common' for unmapped endpoints

**`group_endpoints_by_domain(endpoints: Dict) -> Dict[str, List[str]]`**
- Groups all endpoints by their assigned domains
- Creates domain-based endpoint collections for generation

**`get_directory_structure() -> List[str]`**
- Returns complete directory structure for all domains
- Includes both common and domain-specific directories

**`get_all_domains() -> List[str]`**
- Returns list of all unique domain names

---

## Module Generators

### Types Generator (`types_generator.py`)

**Purpose**: Generates TypeScript type definitions for all domains and common interfaces.

#### Key Methods

**`generate_common_types()`**
- Creates shared type definitions used across all domains
- Generates `ApiResponse<T>`, `PaginatedResponse<T>`, `LoadingState`, `DomainState<T>`, etc.

**`generate_domain_types(domain: str, endpoints: List[str])`**
- Generates domain-specific TypeScript types from backend properties
- Creates base entity interfaces, response types, request types
- Uses utility types for efficiency (Omit, Partial, etc.)

**`generate_main_types_index()`**
- Creates main types index file with all exports

**`_convert_to_typescript_type(python_type: str) -> str`**
- Converts Python/backend types to TypeScript equivalents

### Services Generator (`services_generator.py`)

**Purpose**: Creates business logic service classes for domain operations.

#### Key Methods

**`generate_domain_services(domain: str, endpoints: List[str])`**
- Creates service classes for domain business logic
- Generates specialized services for auth and chess domains
- Creates generic services for other domains

**`_generate_auth_service_content() -> str`**
- Specialized auth service with login, register, logout, token management

**`_generate_chess_service_content() -> str`**
- Specialized chess service with puzzle solving, game management

### Hooks Generator (`hooks_generator.py`)

**Purpose**: Generates React hooks for data management and API interaction.

#### Key Methods

**`generate_domain_hooks(domain: str, endpoints: List[str])`**
- Creates three types of hooks per domain:
  - Main Hook: General domain operations with error handling
  - Query Hook: GET operations and data fetching with automatic refresh
  - Mutations Hook: POST/PUT/DELETE operations

**`generate_core_hooks()`**
- Generates core infrastructure hooks (navigation, authentication, etc.)

**`generate_standalone_hooks()`**
- Creates utility hooks used across multiple domains

**`generate_main_hooks_index()`**
- Creates main hooks index file with all exports

### Components Generator (`components_generator.py`)

**Purpose**: Creates React components for each domain with proper integration.

#### Key Methods

**`generate_domain_components(domain: str, endpoints: List[str])`**
- Creates React components for each entity in the domain
- Integrates with domain hooks for data management
- Generates responsive, accessible UI components with error handling

**`generate_main_entry_files()`**
- Creates `main.tsx` (React entry point) and `App.tsx` with authentication

**`generate_chess_components()`**
- Creates specialized chess UI components (chessboard, puzzle solver, etc.)

**`generate_ui_components()`**
- Generates reusable UI components (DataTable, forms, etc.)

**`generate_main_components_index()`**
- Creates main components index file with all exports

### Clients Generator (`clients_generator.py`)

**Purpose**: Creates API client classes for communicating with backend endpoints.

#### Key Methods

**`generate_domain_clients()`**
- Creates base HTTP client with authentication and error handling
- Generates domain-specific API clients extending base client
- Creates unified client index for easy access

**`_generate_base_client_content() -> str`**
- Base API client with request method, auth headers, error handling

**`_generate_client_method(method: str, path: str, handler: str) -> str`**
- Generates individual API client methods based on endpoint configuration

### Stores Generator (`stores_generator.py`)

**Purpose**: Creates Zustand stores for global state management.

#### Key Methods

**`generate_domain_stores()`**
- Creates authentication store with persistence
- Generates domain-specific stores as needed
- Creates store index for exports

### Pages Generator (`pages_generator.py`)

**Purpose**: Creates full page components that combine multiple domain components.

#### Key Methods

**`generate_all_domain_pages(endpoints: List[str])`**
- Groups endpoints into logical page domains
- Creates comprehensive page components with navigation

**`generate_core_infrastructure()`**
- Creates core page infrastructure (error boundaries, loading components)

**`group_endpoints_by_page_domain(endpoints: List[str]) -> Dict`**
- Groups endpoints into logical page categories

### Layout Generator (`layout_generator.py`)

**Purpose**: Creates the application layout and navigation structure.

#### Key Methods

**`generate_complete_app_infrastructure(domain_list: List[str])`**
- Creates main app layout with navigation
- Generates responsive navigation menu
- Creates layout wrapper components

### Dynamic System Generator (`dynamic_system_generator.py`)

**Purpose**: Creates dynamic page generation system for mobile/desktop variants.

#### Key Methods

**`generate_dynamic_system()`**
- Creates dynamic page routing system
- Generates mobile page variants

**`generate_mobile_page_variant(page_name: str, parent: str, icon: str, description: str)`**
- Creates mobile-optimized page variants

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
- Entity structures and properties with TypeScript type mapping
- API endpoints and HTTP methods
- Authentication requirements
- Domain relationships and organization

### Generated File Structure

After generation, you'll have a complete domain-driven frontend with:
- Type-safe TypeScript interfaces for all entities
- React hooks for data management with error handling
- API clients with authentication and error handling
- React components with proper integration
- Full page components with navigation
- Application layout and routing
- State management with persistence

---

## Best Practices

### Domain Organization

**Keep Domains Focused**: Each domain should have a single responsibility and clear boundaries.

**Consistent Naming**: Use consistent naming patterns across domains:
- `use{Domain}` for main hooks
- `use{Domain}Queries` for query hooks
- `use{Domain}Mutations` for mutation hooks
- `{Domain}APIClient` for API clients
- `{Domain}Service` for service classes

### Type Safety

**Use Specific Types**: Leverage TypeScript utility types for maintainability:
- `Omit<Entity, 'id' | 'created_at' | 'updated_at'>` for create requests
- `Partial<CreateRequest>` for update requests
- `ApiResponse<T>` for API responses

**Avoid Any Types**: Generated code minimizes `any` usage in favor of specific types.

### Component Architecture

**Single Responsibility**: Each component focuses on one entity or specific operation.

**Hook Integration**: Use generated hooks for all data management instead of direct API calls.

### API Integration

**Use Base Client**: All domain clients extend BaseAPIClient for consistent authentication and error handling.

**Error Handling**: Implement consistent error handling patterns across all API operations.

### State Management

**Appropriate State Scope**:
- Local component state for UI-only data
- Domain hooks for domain-specific operations
- Global stores for cross-domain state (auth, navigation)

---

## Extension Guide

### Adding New Domains

1. **Add to Domain Mapping**: Update `domain_mapping.py` with new domain
2. **Add to Backend Config**: Include domain endpoints in `backend_config.json`
3. **Generate Domain**: Run generator for new domain

### Custom Generator Methods

**Specialized Services**: Add domain-specific service methods for complex business logic.

**Custom Hook Patterns**: Create specialized hooks for unique domain requirements.

**Component Templates**: Override component generation for specific UI patterns.

### Adding New Generator Types

1. **Create Generator Module**: Extend `BaseFrontendGenerator`
2. **Implement Generation Methods**: Add domain-specific generation logic
3. **Integrate with Orchestrator**: Add to generation pipeline

### Custom Type Definitions

**Domain-Specific Types**: Add specialized TypeScript interfaces for complex domains.

**Utility Types**: Create reusable type utilities for common patterns.

---

## Conclusion

The Frontend Generator V4 provides a comprehensive, domain-driven approach to frontend development. Its modular architecture, complete type safety, and configuration-driven generation make it ideal for rapid development of maintainable, scalable React applications.

**Key Strengths**:
- Domain-driven organization promotes better code structure
- Complete TypeScript integration ensures type safety
- Modular generators allow for easy customization
- Production-ready features include authentication and error handling
- Extensible architecture supports growing application needs