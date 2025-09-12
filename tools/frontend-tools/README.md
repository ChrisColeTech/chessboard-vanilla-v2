# Frontend Tools - Refactored Generator Components

This directory contains the refactored frontend generator components that provide a modular, maintainable approach to generating domain-driven frontend code.

## Architecture

The refactored generator follows a modular architecture with the following components:

### Core Components

1. **base_generator.py** - Base class with common functionality shared across all generators
2. **domain_mapping.py** - Manages domain mapping and directory structure definitions  
3. **frontend_orchestrator.py** - Main orchestrator that coordinates all generators

### Specialized Generators

4. **types_generator.py** - Generates TypeScript types for all domains
5. **services_generator.py** - Generates service layer files for business logic
6. **hooks_generator.py** - Generates React hooks for data fetching and state management
7. **components_generator.py** - Generates React components and UI elements
8. **clients_generator.py** - Generates API clients for HTTP requests
9. **stores_generator.py** - Generates Zustand stores for state management

## Usage

### Using the Orchestrator Directly

```python
from frontend_tools import FrontendOrchestrator

# Create orchestrator
orchestrator = FrontendOrchestrator("/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2")

# Generate all domains
orchestrator.generate_all_domains()

# Generate specific domain
orchestrator.generate_specific_domain("auth")

# List available domains
orchestrator.list_available_domains()
```

### Using Individual Generators

```python
from frontend_tools import TypesGenerator, ServicesGenerator

# Use individual generators
types_gen = TypesGenerator("/mnt/c/Projects/chessboard-vanilla-v2/frontend-v2")
types_gen.load_backend_config("backend_config.json")
types_gen.generate_common_types()
types_gen.generate_domain_types("auth", ["auth", "users"])
```

### Command Line Interface

```bash
# Generate all domains
python frontend_generator_v4.py

# Generate specific domain
python frontend_generator_v4.py --domain auth

# List available domains
python frontend_generator_v4.py --list

# Custom frontend path
python frontend_generator_v4.py --frontend-path ../my-frontend
```

## Benefits of Refactoring

1. **Modularity** - Each generator has a single responsibility
2. **Maintainability** - Easier to update and modify individual components
3. **Testability** - Individual components can be unit tested
4. **Reusability** - Generators can be used independently
5. **Extensibility** - Easy to add new generators or modify existing ones

## Directory Structure Generated

```
frontend-v2/src/
├── types/
│   ├── common/
│   ├── auth/
│   ├── chess/
│   ├── performance/
│   └── learning/
├── services/
│   ├── auth/
│   ├── chess/
│   ├── performance/
│   └── learning/
├── hooks/
│   ├── auth/
│   ├── chess/
│   ├── performance/
│   └── learning/
├── components/
│   ├── auth/
│   ├── chess/
│   ├── performance/
│   ├── learning/
│   └── ui/
├── clients/
├── stores/
└── providers/
```

## Domain Mapping

The generator automatically maps backend endpoints to frontend domains:

- `auth`, `users` → **auth** domain
- `puzzles`, `games` → **chess** domain  
- `stats` → **performance** domain
- `learning`, `tutorials` → **learning** domain

## Extension Points

To add a new generator:

1. Create a new generator class inheriting from `BaseFrontendGenerator`
2. Implement the specific generation logic
3. Add it to the `FrontendOrchestrator`
4. Export it in `__init__.py`

Example:

```python
from .base_generator import BaseFrontendGenerator

class NewGenerator(BaseFrontendGenerator):
    def generate_something(self, domain: str):
        # Implementation here
        pass
```