# Backend Generator v2 - Quick Reference

## Overview

The Backend Generator v2 is a modular Python system that automatically generates complete TypeScript backends from JSON configuration. Located in `tools/backend-tools/`, it transforms configuration into production-ready Express.js applications with PostgreSQL, JWT auth, and comprehensive APIs.

## Project Structure

```
tools/backend-tools/                     # Generator root directory
├── backend_generator_v2.py             # Main orchestrator
├── backend_config.json                 # Configuration file
├── config.py                          # Path management
├── pattern_analyzer.py                # Code pattern analysis
├── template_generator.py              # Model & route generation
├── service_generator.py               # Service class generation
├── infrastructure_generator.py        # Middleware & utilities
├── parameter_mapper.py                # Route parameter mapping
├── method_generators/                 # Specialized method generators
│   ├── base_generator.py             # Abstract base class
│   ├── auth_methods.py               # Authentication system
│   ├── puzzle_methods.py             # Chess puzzle methods
│   ├── game_methods.py               # Chess game methods
│   ├── user_methods.py               # User management
│   ├── learning_path_methods.py      # Learning paths
│   └── generic_methods.py            # Standard CRUD
├── payload-generator/                 # Test data generation
└── missing-columns/                   # Database utilities
```

## Quick Start

```bash
# Navigate to generator
cd tools/backend-tools

# Generate all endpoints
python backend_generator_v2.py --all

# Generate specific endpoint
python backend_generator_v2.py puzzles

# Preview without creating files
python backend_generator_v2.py --all --dry-run

# Verbose output
python backend_generator_v2.py auth --verbose --force
```

## Core Components

### 1. Main Orchestrator (`backend_generator_v2.py`)
- **BackendGeneratorV2**: Main class coordinating all modules
- **GenerationOptions**: Configuration for dry-run, verbose, force overwrite
- **CLI Interface**: Command-line arguments and validation

### 2. Configuration System (`config.py`)
- Intelligent backend path detection
- Environment variable support (`BACKEND_PATH`)
- Project root detection (`.git`, `package.json`)

### 3. Method Generators (`method_generators/`)
- **Auth Methods**: Registration, login, JWT tokens, password management
- **Puzzle Methods**: Next puzzle, solve validation, hints, categories
- **Game Methods**: Game creation, updates, analysis integration
- **User Methods**: Profile management, preferences, settings
- **Learning Path Methods**: Enrollment, progress tracking, CRUD operations
- **Generic Methods**: Standard CRUD for all entities

### 4. Infrastructure Generator
- Database utilities with Supabase optimization
- JWT authentication middleware
- Validation middleware
- Main app.ts with dynamic route loading

## Configuration Format

Edit `tools/backend-tools/backend_config.json`:

```json
{
  "endpoints": {
    "entity-name": {
      "entity": "EntityName",
      "entities": "entity_names",
      "table_name": "database_table",
      "properties": {
        "field_name": "typescript_type"
      },
      "methods": ["method1", "method2"],
      "endpoints": [
        {
          "method": "GET|POST|PUT|DELETE",
          "path": "/api/path",
          "handler": "methodName",
          "auth_required": true
        }
      ]
    }
  }
}
```

## Generated Output

```
backend-v2/
├── src/
│   ├── models/           # TypeScript interfaces
│   ├── services/         # Business logic classes
│   ├── routes/           # Express.js route handlers
│   ├── middleware/       # Auth & validation
│   ├── utils/           # Database utilities
│   └── app.ts           # Main application
```

## Key Features

- **22+ Entity Support**: Users, Auth, Puzzles, Games, Learning, Analytics
- **Production Ready**: PostgreSQL pooling, JWT auth, error handling
- **TypeScript First**: Complete type safety
- **Extensible**: Plugin-based method generators
- **Intelligent**: Auto-detects backend paths, validates config

## CLI Options

- `--all` - Generate all endpoints
- `--dry-run` - Preview without creating files
- `--verbose` - Detailed output
- `--force` - Overwrite existing files
- `--backend-path` - Custom backend directory
- `--config` - Custom config file path

## Supported Entities

**Core**: users, auth, sessions  
**Chess**: puzzles, games, openings, endgames, analysis, ai-opponents  
**Learning**: tutorials, learning-paths, learning-modules, tutorial-steps  
**Progress**: progress, achievements, stats, analytics  
**Content**: historic-games, game-reviews, puzzle-attempts, puzzle-sources  
**User Features**: profiles, study-plans, subscriptions, help

## Common Commands

```bash
# Validate configuration
python -m json.tool backend_config.json

# Generate with custom backend path
python backend_generator_v2.py --backend-path /custom/path --all

# Generate single entity with force overwrite
python backend_generator_v2.py users --force --verbose
```

## Environment Variables

- `BACKEND_PATH` - Override backend directory
- `DATABASE_URL` - PostgreSQL connection string  
- `JWT_SECRET` - JWT signing secret

## Extension Points

1. **Custom Method Generators**: Extend `BaseMethodGenerator` in `method_generators/`
2. **Custom Entities**: Add to `backend_config.json`
3. **Custom Middleware**: Create in generated `src/middleware/`
4. **Database Utilities**: Extend `src/utils/database.ts`

## Troubleshooting

- **Path Issues**: Set `BACKEND_PATH` environment variable
- **Config Errors**: Use `--dry-run` to validate before generation
- **Method Missing**: Check entity type matches available generators
- **DB Connection**: Verify `DATABASE_URL` and PostgreSQL accessibility

For detailed information, see the comprehensive guide in `docs/63-backend-generator-v2-comprehensive-guide.md`.