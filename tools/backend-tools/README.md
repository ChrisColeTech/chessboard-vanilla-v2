# Backend Tools - Modular Architecture

This directory contains the refactored, modular version of the backend generator.

## Architecture

The original monolithic `backend_generator.py` has been refactored into these components:

### Core Modules

- **`pattern_analyzer.py`** - Analyzes existing backend files to extract patterns
- **`template_generator.py`** - Generates TypeScript files (models, routes) based on patterns
- **`service_generator.py`** - Generates TypeScript service files with entity-specific methods
- **`backend_generator_refactored.py`** - Main orchestrator that uses all modules

### Method Generators

Located in `method_generators/`:

- **`base_generator.py`** - Abstract base class for all method generators
- **`puzzle_methods.py`** - Generates puzzle-specific service methods
- **`game_methods.py`** - Generates game-specific service methods  
- **`auth_methods.py`** - Generates authentication-specific service methods
- **`user_methods.py`** - Generates user-specific service methods
- **`generic_methods.py`** - Generates generic CRUD service methods

## Benefits

1. **Modularity** - Each component has a single responsibility
2. **Extensibility** - Easy to add new method generators for different entities
3. **Maintainability** - Smaller, focused modules are easier to understand and modify
4. **Testability** - Individual components can be unit tested in isolation
5. **Backward Compatibility** - Original generator still works and falls back to modular components

## Usage

### Direct Usage
```python
from backend_tools import BackendGeneratorRefactored

generator = BackendGeneratorRefactored("../backend")
generator.generate_endpoint(config)
```

### Legacy Compatibility
The original `backend_generator.py` automatically detects and uses these modules when available.

## Adding New Method Generators

1. Create a new file in `method_generators/` (e.g., `tournament_methods.py`)
2. Extend `BaseMethodGenerator`
3. Implement entity-specific logic in `generate_method()`
4. Update `service_generator.py` to use the new generator